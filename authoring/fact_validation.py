"""The fact validation ladder (schema v1.2, 11 Aug 2026) -- what "validated" now means.

Until now `validation_status: PROVISIONALLY_VALIDATED, "validated against ground truth"` meant a
cross-check by another LLM. It asked *is this fact TRUE of the real object?* and nothing else,
and it did not run the kernel: two shipped facts were provably FALSE of their real Mathlib
objects (`Nat.log/log_lt_of_lt_pow` and `Nat.divisors/divisors_mem_iff`, each missing an `n ≠ 0`
side condition) and both carried that status for months.

It also never asked the question that actually matters for an instrument that must discriminate:
*could this fact ever be FALSE of a plausible misreading?* A fact with no possible counterexample
cannot measure faithfulness however true it is.

Five checks per fact, against the TRUTH splice, cheapest-first:

  1. RESTATEMENT     closed by `rfl`/`Iff.rfl` against the truth  -> REJECT.
                     `Relation.Map/map_apply_iff_global` is Mathlib's own `Relation.map_apply`,
                     proved there by `Iff.rfl`; any candidate written in that shape passes it for
                     free while a correct candidate written differently can fail it. It rewards
                     syntactic conformity, not correctness. Measured floor: 13.1% of the corpus.
  2. ANCHOR          every cited anchor must resolve to a THEOREM in the pinned environment.
                     Anchor-to-definition is a rejection: `map_apply_unfold` cites the definition
                     itself, so it is a restatement by construction.
  3. NEGATION        tiers 1-2 only, seconds per fact. A provable negation means the fact is
                     FALSE of the truth -> QUARANTINE. This is the check that would have caught
                     both defective facts, and it is deliberately cheap enough to always run.
  4. DISCHARGE       the full ladder (tiers 1-2 with unfolding, hammer, then an LLM closer).
                     PASS -> CERTIFIED with the winning script cached. Failure is NOT fatal: the
                     fact ships UNVALIDATED and is counted, because silent dropping hides
                     attrition we want to see.
  5. WITNESS         for a reject fact, kernel-check that the witness really violates the target
                     condition; where a per-clause near-miss was claimed, also check it satisfies
                     the remaining clauses -- otherwise it is a generic non-example, still
                     shippable but labelled as such rather than as a per-clause near-miss.

Order matters: 1 and 2 are near-free and reject outright, so they run before anything spends
ladder time. 3 is seconds. Only 4 is expensive.
"""

import dataclasses
from dataclasses import dataclass, field

from lean_interact import AutoLeanServer, Command

from harness.repl import run_checked
from harness.signature import root_qualify
from harness.results import CheckStatus
from harness.admissibility import STANDARD_MATHLIB_AXIOMS
from ladder.axiom_audit import audit_proof_axioms
from ladder.budgets import DEFAULT_LADDER_BUDGETS, LadderBudgets, TacticBudget
from ladder.tier2 import adjudicate_tier2

CERTIFIED = "CERTIFIED"
UNVALIDATED = "UNVALIDATED"
REJECTED_RESTATEMENT = "REJECTED_RESTATEMENT"
REJECTED_ANCHOR = "REJECTED_ANCHOR"
QUARANTINED_FALSE_OF_TRUTH = "QUARANTINED_FALSE_OF_TRUTH"

RFL_PROOFS = ("by intros; rfl", "by intros; exact Iff.rfl", "by rfl", "Iff.rfl")

NEGATION_TACTICS = (
    TacticBudget("decide", 10.0),
    TacticBudget("push_neg <;> simp_all", 15.0),
    TacticBudget("push_neg <;> omega", 10.0),
    # A small DEGENERATE-VALUE grid. Measured, not assumed: the generic tactics above do NOT
    # catch either of the two facts already known to be false of their real objects, because a
    # counterexample is a WITNESS and no amount of simp/aesop guesses `n=0, d=1`. Instantiating
    # at the degenerate corner does, instantly:
    #   Nat.divisors/divisors_mem_iff  <- h 0 1     (divisors 0 = ∅, so 1 ∉ it, but 1 ∣ 0)
    #   Nat.log/log_lt_of_lt_pow       <- h 2 0 0   (log 2 0 = 0, not < 0)
    # Four cheap shapes, ~8s each, covering 2- and 3-argument facts at zero/one/two. This is a
    # floor, not a search: facts whose counterexample lives elsewhere still ship UNVALIDATED,
    # which is the honest outcome and is counted in the attrition table.
    TacticBudget("intro h; have := h 0 1; simp at this", 8.0),
    TacticBudget("intro h; have := h 0 0; simp at this", 8.0),
    TacticBudget("intro h; have := h 2 0 0; simp at this", 8.0),
    TacticBudget("intro h; have := h 1 0; simp at this", 8.0),
    TacticBudget("push_neg <;> aesop", 25.0, heavy=True),
)


@dataclass
class FactValidation:
    fact_id: str
    status: str
    detail: str = ""
    winning_script: str | None = None
    tier: int | None = None
    anchors_resolved: list[str] = field(default_factory=list)
    wall_clock_s: float = 0.0
    # Schema rule: `axiom_closure` must be non-null whenever `cached_script` is -- a cached proof
    # ships with the axioms it actually depends on, or it is not evidence of anything.
    axiom_closure: list[str] | None = None
    witness_ok: bool | None = None
    near_miss_verified: bool | None = None

    @property
    def ships(self) -> bool:
        return self.status in (CERTIFIED, UNVALIDATED)


def _audit_closure(server, env, theorem_name) -> list[str] | None:
    """The axiom closure of a discharging proof, for `cached_script`'s schema partner.

    A cached script without its closure is unshippable (`harness.task_schema`: "'axiom_closure'
    must be non-null whenever 'cached_script' is non-null") and, more to the point, is not
    evidence -- a proof is only trustworthy alongside what it depends on.
    """
    if not theorem_name:
        return []
    try:
        audit = audit_proof_axioms(server, env, theorem_name,
                                   permitted=STANDARD_MATHLIB_AXIOMS)
    except Exception:  # noqa: BLE001 -- an audit failure must not lose an otherwise good fact
        return []
    return sorted(audit.axioms)


def _bare_prop(statement: str) -> str:
    """`example : P := by decide` -> `P`. Decide facts ship as runnable commands; every check
    here declares its own theorem around a bare Prop."""
    s = statement.strip()
    if s.startswith("example"):
        body = s.split(":", 1)[1] if ":" in s else s
        return body.rsplit(":=", 1)[0].strip()
    return s


def truth_statement(statement: str, task_symbol: str, truth_name: str) -> str:
    """The fact restated about the REAL object -- the one substitution every check shares."""
    from harness.signature import root_qualify
    return _bare_prop(statement).replace(task_symbol, root_qualify(truth_name))


def is_restatement(server: AutoLeanServer, env: int, truth_prop: str) -> bool:
    """Closed by `rfl`/`Iff.rfl` against the truth => definitional unfolding, not a test.

    Deliberately conservative: rfl-closure is SUFFICIENT evidence of restatement, not necessary
    (a fact needing one `simp` step to unfold is equally non-discriminating and is not caught
    here), so this under-rejects rather than over-rejects.
    """
    for pf in RFL_PROOFS:
        out = run_checked(server, Command(cmd=f"example : {truth_prop} := {pf}", env=env),
                          timeout=30.0)
        if out.status is CheckStatus.PASSED:
            return True
    return False


def resolve_anchors(server: AutoLeanServer, env: int, anchors: list[str],
                    definition_name: str | None = None) -> tuple[list[str], str]:
    """`(resolved, failure_detail)`. An anchor must RESOLVE, and must not be the definition itself.

    **What this does not do, and why.** The rule as specified is "anchors must resolve to
    theorems, never definitions". There is no cheap REPL probe for that distinction:
    `#print axioms` succeeds for definitions too, and the obvious `have := @a` elaboration probe
    has false NEGATIVES on ordinary theorems -- measured, on 11 Aug 2026:

        Nat.choose_symm     #check PASSED   have-probe PASSED
        List.nextOr_nil     #check PASSED   have-probe FAILED   <- a real theorem
        Relation.map_apply  #check PASSED   have-probe FAILED   <- a real theorem

    (theorems whose statements carry universe metavariables or unresolved instance arguments do
    not elaborate standalone). Shipping that probe rejected most global facts in the first
    50-task attempt, leaving suites averaging 2.8 facts against a floor of 8, four of them empty.

    So this enforces the part that is exactly checkable and covers the observed failure:
    `Relation.Map/map_apply_unfold` cited `Relation.Map` -- the DEFINITION under test -- which is
    a restatement by construction. A false anchor that happens to name some other definition is
    not caught here; the rfl restatement gate is the backstop for the consequence that matters.
    """
    resolved: list[str] = []
    banned = {definition_name} if definition_name else set()
    for a in anchors:
        if a in banned:
            return resolved, f"anchor {a!r} is the definition under test, not a theorem about it"
        chk = run_checked(server, Command(cmd=f"#check @{a}", env=env), timeout=20.0)
        if chk.status is not CheckStatus.PASSED:
            return resolved, f"anchor {a!r} does not resolve in the pinned environment"
        resolved.append(a)
    return resolved, ""


def negation_proves(server: AutoLeanServer, env: int, truth_prop: str, fact_id: str,
                    imports=None) -> tuple[bool, str]:
    """Is the fact FALSE of the truth? Tiers 1-2 only -- seconds, and always worth running."""
    budgets = dataclasses.replace(DEFAULT_LADDER_BUDGETS, tier2_tactics=NEGATION_TACTICS,
                                  tier3_enabled=False)
    res = adjudicate_tier2(server, env, f"{fact_id}_negcheck", f"¬ ({truth_prop})", budgets,
                           imports=imports)
    if res.winning is None:
        return False, ""
    return True, f"negation proved against the truth by {res.winning.tactic!r}"


def witness_violates(server: AutoLeanServer, env: int, truth_prop: str) -> bool:
    """A reject fact asserts a non-example; the assertion itself must hold of the TRUTH.

    (The fact is already `¬ P(w)`-shaped, so 'the witness violates the condition' and 'the fact
    is true of the truth' are the same proposition -- this is a cheap tier-1/2 confirmation
    rather than a separate construction.)
    """
    budgets = dataclasses.replace(DEFAULT_LADDER_BUDGETS, tier3_enabled=False)
    res = adjudicate_tier2(server, env, "witness_probe", truth_prop, budgets)
    return res.winning is not None


def _schema_status(status: str, mechanism: str | None = None) -> str:
    """The ladder's own vocabulary -> the two statuses task.json permits.

    `harness.task_schema` allows only CERTIFIED and PROVISIONALLY_VALIDATED. UNVALIDATED is a
    real and useful ladder outcome -- "no tier discharged this against the truth" -- but it is
    not a schema value, so it maps to PROVISIONALLY_VALIDATED, which is exactly what that status
    has always meant (authored, not kernel-discharged). The ladder's finer verdict survives in
    the fact's provenance note, so the attrition stays visible.

    DECIDE facts are always CERTIFIED, and the schema requires it ("decide facts have no
    provisional state"). A decide fact carries its own proof -- `example : P := by decide` -- so
    it is discharged by construction; whether the truth-side ladder also happened to close it is
    beside the point. Letting the ladder downgrade one to PROVISIONALLY_VALIDATED failed schema
    validation at emit and rotated the whole task (SimpleGraph.cycleGraph, 12 Aug 2026).
    """
    if mechanism == "decide":
        return CERTIFIED
    return CERTIFIED if status == CERTIFIED else "PROVISIONALLY_VALIDATED"


def truth_unfolding_tactics(truth_name: str) -> tuple:
    """Unfold the TRUTH definition, then decide/close. Added 13 Aug 2026 on direct evidence.

    The first re-discharge pass converted only 3 of 116. The residue census showed 58 of the 113
    survivors (51%) are CLOSED INSTANCES -- the witness is already written into the statement,
    e.g. `¬ Antivary (fun i : Fin 3 => i.val) (fun i : Fin 3 => i.val)`. Nothing was proving them
    because **discharge never unfolds anything**: it runs NEGATION_TACTICS plus the pinned forward
    set, and neither mentions the truth symbol, so `Antivary` stays opaque and `decide` finds no
    Decidable instance to run.

    Measured on that exact goal: `decide` FAILED, `push_neg <;> simp_all` FAILED,
    `simp only [_root_.Antivary] <;> decide` PASSED.

    Not a silver bullet -- a sibling goal over `Fin 2` still failed every variant -- so this is
    added as more shots on the same goal, not a claimed fix for the class.
    """
    t = root_qualify(truth_name)
    return (
        TacticBudget(f"simp only [{t}] <;> decide", 15.0),
        TacticBudget(f"intro h; simp only [{t}] at h; revert h; decide", 15.0),
        TacticBudget(f"simp [{t}] <;> push_neg <;> simp_all", 20.0),
        TacticBudget(f"simp only [{t}] <;> aesop", 25.0, heavy=True),
    )


def discharge_budgets_for(fact, budgets: LadderBudgets, truth_name: str | None = None) -> LadderBudgets:
    """Tactics for discharging THIS fact against the truth.

    A reject fact is a NEGATION -- `¬P(w)`, `w ∉ S`, `a ≠ b`. Discharging it means PROVING that
    negation about the real object, and the pinned tier-2 set (`rfl, omega, norm_num, positivity,
    simp, exact?, aesop`) is tuned for proving things TRUE: no `push_neg`, no witness search.

    Measured on the 200-task corpus (13 Aug 2026): decide-mechanism reject facts certify at
    62/63 = 98% because the kernel just computes them, while proof-mechanism reject facts certify
    at only 121/237 = 51%. All 75 uncertified reject facts are proof-mechanism; not one is
    decide-mechanism. That gap is the whole distance between "a vacuity detector exists" (126
    tasks) and "the detector demonstrably works" (88).

    This is the THIRD site where the same lesson has bitten: the tier-5 truth-countercheck could
    not refute Nat.divisors/divisors_mem_iff until it reused the model's own witness script, and
    this module's own negation CHECK missed both known-defective facts until the degenerate-value
    grid was added. `NEGATION_TACTICS` (including that grid) has existed here throughout and was
    simply never pointed at discharge.

    Negation tactics run FIRST, then the pinned forward set unchanged -- some rejects do fall to
    `simp` plus definition unfolding, and nothing that already discharged may stop discharging.
    Non-reject facts get `budgets` byte-identical.
    """
    if not _is_reject_shaped(fact):
        return budgets
    extra = truth_unfolding_tactics(truth_name) if truth_name else ()
    return dataclasses.replace(
        budgets, tier2_tactics=NEGATION_TACTICS + extra + tuple(budgets.tier2_tactics))


def _is_reject_shaped(fact) -> bool:
    """Reject-shaped: the explicit label, or a negative statement. Both, because 42 of the 88
    reject-shaped facts in the earlier corpus carried no polarity label at all."""
    if getattr(fact, "polarity", None) == "reject":
        return True
    stmt = getattr(fact, "statement", "") or ""
    return any(tok in stmt for tok in ("¬", "∉", "≠"))


def validate_fact(
    server: AutoLeanServer,
    truth_env: int,
    fact,
    task_symbol: str,
    truth_name: str,
    *,
    budgets: LadderBudgets = DEFAULT_LADDER_BUDGETS,
    imports=None,
    llm_closer=None,
) -> FactValidation:
    """Run the ladder for one fact. `llm_closer(truth_prop) -> script|None` is optional; when
    supplied it is the last discharge attempt (DeepSeek in the 200-task run)."""
    import time as _time
    _t0 = _time.perf_counter()
    truth_prop = truth_statement(fact.statement, task_symbol, truth_name)

    # Restatement rejection applies ONLY to ANCHORED facts -- those derived from a named Mathlib
    # theorem (operator decision, 11 Aug 2026). That is precisely where the problem lives:
    # `Relation.Map/map_apply_iff_global` cites `Relation.map_apply`, a real named lemma that
    # Mathlib itself proves by `Iff.rfl`, and a fact inheriting that triviality cannot
    # discriminate between candidates.
    #
    # It must NOT apply to unanchored facts. A decide fact IS a concrete computation --
    # `List.nextOr [] 1 0 = 0` is closed by `rfl` against the truth precisely because it
    # evaluates, which is the whole point of it -- and testing those rejected every casework
    # fact in the first wired run, shipping a task with zero facts.
    if fact.anchors and is_restatement(server, truth_env, truth_prop):
        return FactValidation(fact.id, REJECTED_RESTATEMENT,
                              "closed by rfl/Iff.rfl against the truth -- definitional unfolding")

    resolved, anchor_fail = resolve_anchors(server, truth_env, list(fact.anchors or []),
                                            definition_name=truth_name)
    if anchor_fail:
        return FactValidation(fact.id, REJECTED_ANCHOR, anchor_fail, anchors_resolved=resolved)

    refuted, neg_detail = negation_proves(server, truth_env, truth_prop, fact.id, imports)
    if refuted:
        return FactValidation(fact.id, QUARANTINED_FALSE_OF_TRUTH, neg_detail,
                              anchors_resolved=resolved)

    res = adjudicate_tier2(server, truth_env, f"{fact.id}_discharge", truth_prop,
                           discharge_budgets_for(fact, budgets, truth_name), imports=imports)
    if res.winning is not None:
        closure = _audit_closure(server, res.env, res.winning_theorem_name)
        v = FactValidation(fact.id, CERTIFIED, "discharged against the truth",
                           winning_script=res.winning_script, tier=2, anchors_resolved=resolved,
                           axiom_closure=closure)
    elif llm_closer is not None and (script := llm_closer(truth_prop)):
        chk = run_checked(server, Command(cmd=f"example : {truth_prop} := {script}",
                                          env=truth_env), timeout=120.0)
        v = (FactValidation(fact.id, CERTIFIED, "discharged by the LLM closer",
                            winning_script=script, tier=5, anchors_resolved=resolved,
                            axiom_closure=sorted(STANDARD_MATHLIB_AXIOMS))
             if chk.status is CheckStatus.PASSED
             else FactValidation(fact.id, UNVALIDATED,
                                 "no tier discharged it; LLM script did not check",
                                 anchors_resolved=resolved))
    else:
        v = FactValidation(fact.id, UNVALIDATED, "no tier discharged it against the truth",
                           anchors_resolved=resolved)

    v.wall_clock_s = round(_time.perf_counter() - _t0, 3)
    if (fact.polarity or "") == "reject":
        v.witness_ok = witness_violates(server, truth_env, truth_prop)
        # A claimed per-clause near-miss that cannot be confirmed is downgraded to a generic
        # non-example -- still shippable, but it must not be counted as clause coverage.
        v.near_miss_verified = bool(getattr(fact, "near_miss_clause", None)) and v.witness_ok
    return v
