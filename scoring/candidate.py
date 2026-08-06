"""Score one candidate definition end-to-end.

This is the callable that closes the gap `harness.scoring.run_facts` leaves open: it raises
`NotImplementedError` on proof-mechanism facts, which are 58% of the 41-task corpus (275 of 471).

The pipeline, in order, and why the order is what it is:

1. **Truth splice** (only when a real name is supplied) under `VTruth.<base>`, a symbol
   deliberately distinct from the task symbol `VTask.<base>` that every fact statement names.
2. **Candidate splice** with the TRUTH environment as its base, via the Stage A retry ladder
   (plain -> noncomputable -> root-qualified -> both). Because a spliced environment is a
   descendant of its base, the resulting environment holds both definitions -- which is exactly
   what `ladder.tier4` requires and the only reason the equivalence probe is possible at all.
3. **Admissibility**, strictly. An inadmissible candidate still gets a written record: it is
   data for the funnel, not something to skip.
4. **Equivalence fast path** -- attempt `candidate = truth` (`↔` for Props). One success
   certifies the ENTIRE fact suite at the cost of a single cheap `rfl`, and the 12
   `RECALLED_TARGET` tasks guarantee a large near-verbatim population where it fires constantly.
5. **Per-fact walk** otherwise: decide -> tier 1, proof -> the ladder, carrying `current_env`
   forward because tier 2's recovery loop may have replaced it.

**The inertness argument for step 4**, which is the risky part. Facts name `VTask.*`. The truth
lives at `VTruth.*` and is referenced by nothing except the equivalence goal. Lean name
resolution cannot reach `VTruth.clog` from a fact that says `VTask.clog`, so a co-resident truth
cannot rescue a wrong candidate's facts. `@[reducible]` does not change this -- it affects
whether a definition unfolds once named, not whether a different name finds it -- and the truth
splice registers no instances (it is a plain `def`, not an `instance`). This is asserted, not
assumed: `test_wrong_candidate_still_fails_its_facts_with_truth_co_resident` scores a
deliberately wrong candidate with the truth present and requires the facts to still fail.
"""

import time
from dataclasses import dataclass, field

from lean_interact import AutoLeanServer

from harness.admissibility import check_admissibility
from harness.facts import Fact
from harness.results import CheckStatus, SpliceOutcome, SplicePath
from harness.scoring import splice_candidate_declaration, splice_real_name
from harness.signature import PinnedSignature
from ladder.adjudicate import adjudicate_fact
from ladder.budgets import DEFAULT_LADDER_BUDGETS, LadderBudgets
from ladder.tier1 import adjudicate_tier1
from ladder.tier4 import adjudicate_tier4_equivalence
from scoring import config as cfg
from scoring.verdicts import RETRYABLE, Verdict, check_mechanism_invariant, fidelity, verdict_for

CERTIFIED_VIA_FACT = "fact"
CERTIFIED_VIA_EQUIVALENCE = "equivalence"


@dataclass
class FactVerdict:
    fact_id: str
    mechanism: str
    verdict: Verdict
    tier: int | None
    certified_via: str
    elapsed_s: float
    detail: str = ""
    attempts: list[dict] = field(default_factory=list)
    retried: bool = False

    def to_dict(self) -> dict:
        return {
            "fact_id": self.fact_id,
            "mechanism": self.mechanism,
            "verdict": self.verdict.value,
            "tier": self.tier,
            "certified_via": self.certified_via,
            "elapsed_s": round(self.elapsed_s, 4),
            "detail": self.detail[:2000],
            "retried": self.retried,
            # TierAttempt records are persisted in full: the pilot's per-tactic timing data then
            # collects itself, and calibrating budgets later needs the losers, not just winners.
            "attempts": self.attempts,
        }


def _attempt_dicts(attempts) -> list[dict]:
    return [
        {
            "tier": a.tier,
            "tactic": a.tactic,
            "status": a.status.value,
            "elapsed_s": round(a.elapsed_s, 4),
            "detail": (a.detail or "")[:500],
        }
        for a in (attempts or [])
    ]


def truth_signature_for(signature: PinnedSignature) -> PinnedSignature:
    """The same pinned type under `VTruth.<base>` -- see the module docstring's inertness
    argument for why the name must differ from the task symbol."""
    return PinnedSignature(name=f"{cfg.TRUTH_SYMBOL_PREFIX}{signature.base_name}", type_sig=signature.type_sig)


def is_prop_valued(signature: PinnedSignature) -> bool:
    """Whether the pinned type's result is `Prop`, which decides `↔` vs `=` in the equivalence
    probe. Textual on the pinned type -- the signature is ours and canonical, not model output,
    so its final token is trustworthy in a way a candidate body never is."""
    return signature.type_sig.rstrip().rstrip("()").strip().endswith("Prop")


def _adjudicate_one_fact(
    server: AutoLeanServer,
    env: int,
    fact: Fact,
    budgets: LadderBudgets,
    cache,
    imports: list[str] | None,
) -> tuple[FactVerdict, int]:
    """One fact, with a single retry for infrastructure failures. Returns `(verdict, env)` --
    the env may have been replaced by tier 2's recovery loop and MUST be carried forward."""
    started = time.perf_counter()
    retried = False

    for attempt_n in range(1 + cfg.INFRA_RETRY_ATTEMPTS):
        if fact.mechanism == "decide":
            attempt = adjudicate_tier1(server, env, fact.statement, budgets)
            status, tier, attempts, detail = attempt.status, 1, [attempt], attempt.detail
        else:
            adjudication, env = adjudicate_fact(fact, env, server, budgets, cache, imports=imports)
            status, tier = adjudication.status, adjudication.tier
            attempts, detail = adjudication.attempts, adjudication.detail

        if status not in RETRYABLE or attempt_n == cfg.INFRA_RETRY_ATTEMPTS:
            break
        # Infrastructure said nothing about the candidate; one cheap repeat guards a transient.
        retried = True

    verdict = verdict_for(status)
    check_mechanism_invariant(fact.mechanism, verdict)
    return (
        FactVerdict(
            fact_id=fact.id,
            mechanism=fact.mechanism,
            verdict=verdict,
            tier=tier,
            certified_via=CERTIFIED_VIA_FACT,
            elapsed_s=time.perf_counter() - started,
            detail=detail or "",
            attempts=_attempt_dicts(attempts),
            retried=retried,
        ),
        env,
    )


def score_candidate_body(
    server: AutoLeanServer,
    base_env: int,
    signature: PinnedSignature,
    declaration: str,
    facts: list[Fact],
    *,
    truth_real_name: str | None = None,
    budgets: LadderBudgets = DEFAULT_LADDER_BUDGETS,
    cache=None,
    imports: list[str] | None = None,
    try_equivalence: bool = True,
    mechanisms: tuple[str, ...] = ("decide", "proof"),
) -> dict:
    """Score one candidate. `declaration` is the model's full Lean declaration, as extracted.

    Returns the verdict payload (the caller adds sample identity).

    `truth_real_name` enables the equivalence fast path; omit it to force the per-fact walk
    (which is what the adversarial and per-fact tests do). Never raises on a candidate's
    account: a candidate that fails to splice or fails admissibility returns a record saying so.
    """
    result: dict = {
        "schema_version": cfg.SCHEMA_VERSION,
        "splice_path": None,
        "splice_retries": 0,
        "admissible": False,
        "admissibility_failure": None,
        "admissibility_detail": "",
        "equivalence_attempted": False,
        "equivalence_certified": False,
        "fact_verdicts": [],
        "fidelity": None,
        "mechanisms_attempted": list(mechanisms),
        # Whether this candidate is noncomputable -- either because the model wrote the modifier
        # or because the splice ladder had to add it. Recorded per candidate so the per-model
        # emission rate can be reported beside coverage: a noncomputable definition cannot
        # evaluate its decide facts (correctly UNKNOWN), so a model that emits them more often
        # is judged on a different, smaller fact population than one that does not. That is a
        # differential-coverage mechanism, and it must be visible rather than silent.
        "noncomputable": False,
    }
    started = time.perf_counter()

    # 1. Truth splice, so the equivalence probe has something to compare against. A failure here
    #    is OUR problem, not the candidate's: fall back to per-fact rather than failing the
    #    candidate for it.
    env_for_candidate, truth_env, truth_name = base_env, None, None
    if truth_real_name and try_equivalence:
        truth_sig = truth_signature_for(signature)
        truth_splice = splice_real_name(server, base_env, truth_sig, truth_real_name)
        if truth_splice.status is CheckStatus.PASSED and truth_splice.env is not None:
            env_for_candidate, truth_env, truth_name = truth_splice.env, truth_splice.env, truth_sig.name
        else:
            result["truth_splice_failed"] = (truth_splice.detail or "")[:500]

    # 2. Candidate splice, on top of the truth env so both are co-resident. The candidate's own
    #    DECLARATION is spliced verbatim (with `@[reducible]` merged in) rather than rebuilt from
    #    a body expression -- see `harness.scoring.splice_candidate_declaration`. The pinned type
    #    is therefore enforced by the kernel in step 3 (`WRONG_TYPE`), not by construction.
    outcome: SpliceOutcome = splice_candidate_declaration(server, env_for_candidate, signature, declaration)
    result["splice_path"] = outcome.path.value
    result["splice_retries"] = outcome.retries_consumed
    if not outcome.succeeded:
        result["admissibility_failure"] = "compile_error"
        result["mechanisms_attempted"] = ["decide", "proof"]  # terminal: nothing left to attempt
        result["admissibility_detail"] = (outcome.result.detail or "")[:2000]
        result["splice_secondary_errors"] = outcome.secondary_details[1:]
        result["wall_time_s"] = round(time.perf_counter() - started, 3)
        return result

    candidate_env = outcome.result.env
    result["noncomputable"] = (
        "noncomputable" in (outcome.cmd_text or "")
        or outcome.path in (SplicePath.NONCOMPUTABLE, SplicePath.ROOT_QUALIFIED_NONCOMPUTABLE)
    )

    # 3. Admissibility.
    # `truth_real_name` is the mined provenance: it drives the equivalence fast path AND the
    # self-delegation gate. The two are independent -- `try_equivalence=False` must still reject a
    # candidate that defines the target by calling the target -- so it is passed here regardless.
    verdict = check_admissibility(
        server, candidate_env, signature, splice_response=outcome.result.raw_response,
        target_real_name=truth_real_name,
    )
    if not verdict.passed:
        result["admissibility_failure"] = verdict.failure.value
        result["mechanisms_attempted"] = ["decide", "proof"]  # terminal
        result["admissibility_detail"] = verdict.detail[:2000]
        result["wall_time_s"] = round(time.perf_counter() - started, 3)
        return result
    result["admissible"] = True
    result["axioms"] = sorted(verdict.axioms)

    # 4. Equivalence fast path -- one success certifies the whole suite.
    if truth_env is not None and truth_name is not None:
        result["equivalence_attempted"] = True
        tier4 = adjudicate_tier4_equivalence(
            server, candidate_env, truth_env, signature.name, truth_name, budgets,
            prop_valued=is_prop_valued(signature), fact_id="equivalence", imports=imports,
        )
        result["equivalence_attempts"] = _attempt_dicts(tier4.attempts)
        if tier4.winning is not None:
            result["equivalence_certified"] = True
            result["fact_verdicts"] = [
                FactVerdict(
                    fact_id=f.id, mechanism=f.mechanism, verdict=Verdict.PASS, tier=4,
                    certified_via=CERTIFIED_VIA_EQUIVALENCE, elapsed_s=0.0,
                    detail="certified by candidate=truth equivalence",
                ).to_dict()
                for f in facts
            ]
            result["fidelity"] = 1.0
            # Equivalence certifies the WHOLE suite, both mechanisms, so Stage E has nothing to
            # add for this candidate and must skip it.
            result["mechanisms_attempted"] = ["decide", "proof"]
            result["wall_time_s"] = round(time.perf_counter() - started, 3)
            return result

    # 5. Per-fact walk.
    current_env = candidate_env
    verdicts: list[FactVerdict] = []
    for fact in facts:
        if fact.mechanism not in mechanisms:
            # Deliberately deferred to a later pass -- NOT the same as UNKNOWN, and recorded
            # distinctly so a partial pass can never be mistaken for an exhausted one.
            verdicts.append(
                FactVerdict(
                    fact_id=fact.id, mechanism=fact.mechanism, verdict=Verdict.NOT_ATTEMPTED,
                    tier=None, certified_via=CERTIFIED_VIA_FACT, elapsed_s=0.0,
                    detail=f"mechanism {fact.mechanism!r} not attempted in this pass",
                )
            )
            continue
        fact_verdict, current_env = _adjudicate_one_fact(
            server, current_env, fact, budgets, cache, imports
        )
        verdicts.append(fact_verdict)

    result["fact_verdicts"] = [v.to_dict() for v in verdicts]
    result["fidelity"] = fidelity([v.verdict for v in verdicts])
    result["wall_time_s"] = round(time.perf_counter() - started, 3)
    return result


def summarize(record: dict) -> dict:
    """Counts by verdict, for logging. Analysis reads the per-fact tree, not this."""
    counts: dict[str, int] = {}
    for fv in record.get("fact_verdicts", []):
        counts[fv["verdict"]] = counts.get(fv["verdict"], 0) + 1
    return counts


__all__ = [
    "FactVerdict",
    "score_candidate_body",
    "summarize",
    "truth_signature_for",
    "is_prop_valued",
    "CERTIFIED_VIA_EQUIVALENCE",
    "CERTIFIED_VIA_FACT",
]
