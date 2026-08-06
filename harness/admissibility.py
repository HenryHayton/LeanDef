"""Layer 0 -- the admissibility gate.

See `docs/design/reward_structure_2026-07-21.md` §1 and
`docs/design/verifier_architecture_2026-07-20.md` §2: a candidate must clear this gate before
any fact is scored against it. Admissibility is pass/fail eligibility; it contributes nothing
to the score. `harness.scoring.score_spliced_candidate` refuses to run facts against a
candidate that fails here.

PROVISIONAL: the axiom check (`#print axioms`) is the newest and least battle-tested part of
this module. `#print axioms` is the best mechanism found for this -- environment diffing was
considered but `lean_interact`'s `CommandResponse` doesn't expose enough of the environment to
diff declaration-by-declaration axiom footprints without essentially reimplementing what
`#print axioms` already does inside the kernel. Marked provisional per this task's explicit
instruction to say so plainly rather than silently ship something weak; if `#print axioms`'
message format ever changes, this check fails closed (ERRORED) rather than silently passing
an unparseable result.
"""

import re
from dataclasses import dataclass
from enum import Enum

from lean_interact import AutoLeanServer, Command

from harness import config as cfg
from harness.repl import run_checked
from harness.results import CheckStatus
from harness.signature import PinnedSignature

# The three axioms almost every nontrivial Mathlib definition ends up depending on --
# Finset/Multiset are built on Quotient, which pulls in Quot.sound, and generic
# Decidable/Fintype instance resolution commonly goes through Classical.choice/propext even
# when a computable path also exists. This pattern is general to Mathlib-based definitions,
# not particular to simple/computable ones -- abstract and infinite-carrier objects route
# through the same Quotient/Classical machinery at least as often. Empirically confirmed only
# for this project's own pinned `tau` so far (an easy, decidable-fact-rich object -- see
# docs/repo_audit.md and this task's own verification run): `#print axioms tau` on the true,
# fully computable definition reports exactly this set, NOT the empty set, so "no new axioms"
# has to mean "no axioms beyond what any ordinary Mathlib definition already carries," not
# "zero axioms," or almost every real candidate would be rejected. Not yet confirmed against a
# proof-heavy true definition, where the *facts* also being proof-based (not just the
# definition, per reward-structure design §2.3) could plausibly widen the baseline further.
# Callers whose task's true definition has a different (or empty) axiom footprint should pass
# their own `baseline_axioms`.
STANDARD_MATHLIB_AXIOMS: frozenset[str] = frozenset({"propext", "Classical.choice", "Quot.sound"})

_AXIOM_LIST_RE = re.compile(r"depends on axioms:\s*\[(.*?)\]", re.DOTALL)  # Lean's pretty-printer
# wraps the axiom list onto multiple lines once it's long enough; `.` doesn't match `\n` by
# default, so a wrapped list silently failed to parse (confirmed empirically, Ladder worker
# Session B tier-cascade measurement, 2026-07-27, via `ladder.axiom_audit`'s identical regex --
# fixed there and here together).
_NO_AXIOMS_RE = re.compile(r"does not depend on any axioms")

# Universe variables named in a pinned type (`Type u_1`, `Sort u`, ...). A `def` auto-binds
# these; a bare `#check (name : <type>)` does NOT, and fails with "unknown universe level `u`".
# Found the hard way (2026-08-06): the type probe rejected perfectly correct candidates for
# `Monotone` -- 7 of 7 -- and 32 of the 41 tasks carry universe variables, so unfixed this would
# have manufactured false WRONG_TYPE across 78% of the corpus and read as a model failure.
# `Type*` is deliberately not matched: it is a wildcard, not a named universe.
_UNIVERSE_RE = re.compile(r"(?:Type|Sort)\s+([A-Za-z_][A-Za-z0-9_]*)")


def universe_names(type_sig: str) -> list[str]:
    """Universe variables named in `type_sig`, in first-appearance order."""
    seen: list[str] = []
    for m in _UNIVERSE_RE.finditer(type_sig or ""):
        name = m.group(1)
        if name not in seen:
            seen.append(name)
    return seen


def type_probe_command(signature: PinnedSignature) -> str:
    """The command that checks a candidate has the pinned type.

    `#check (name : type)` rather than `example : type := name`: the `example` form additionally
    COMPILES the definition and so fails every noncomputable candidate with "consider marking it
    as 'noncomputable'", which would have produced systematic false WRONG_TYPE against exactly
    the classical-construction population. `#check` only elaborates, and still catches wrong
    arity and wrong result type (both verified against live Lean).

    Prefixed with a `universe` declaration when the pinned type names universe variables -- see
    `_UNIVERSE_RE`.
    """
    universes = universe_names(signature.type_sig)
    prefix = f"universe {' '.join(universes)}\n" if universes else ""
    return f"{prefix}#check ({signature.name} : {signature.type_sig})"


class AdmissibilityFailure(Enum):
    COMPILE_ERROR = "compile_error"
    SORRY = "sorry"
    NEW_AXIOM = "new_axiom"
    NAME_SHADOWED = "name_shadowed"
    WRONG_TYPE = "wrong_type"  # compiled fine, but does not have the pinned type
    SELF_DELEGATION = "self_delegation"  # defines the target by invoking the target
    ERRORED = "errored"


@dataclass(frozen=True)
class AdmissibilityVerdict:
    passed: bool
    failure: AdmissibilityFailure | None
    detail: str
    axioms: frozenset[str] = frozenset()


_USED_CONSTS_MARKER = "USEDCONSTS"

# Walks the spliced declaration's ELABORATED constant closure, not its source text. Source-text
# matching is defeated by notation, `open`, and abbreviations; the elaborator has already
# resolved all of those by the time a constant lands in the expression.
#
# The walk expands transitively ONLY into constants whose name is prefixed by the task symbol --
# i.e. auxiliaries the candidate itself introduced (`VTask.clog.go` from a `where` clause,
# equation lemmas). That bound matters in both directions:
#
#   - Without it, a full transitive walk into Mathlib would explode and would eventually reach
#     almost anything, manufacturing false positives.
#   - With it, the one real smuggling route stays closed. Verified live (2026-08-07): a candidate
#     whose body is `fun b n => go b n where go b n := Nat.clog b n` reports declarations
#     `[VTask.clog]` ONLY -- the `where` helper is invisible to the NAME_SHADOWED gate -- while
#     the closure walk sees both `VTask.clog.go` and `Nat.clog`.
_USED_CONSTS_PROBE = r"""
open Lean in
#eval show CoreM Unit from do
  let env ← getEnv
  let root : Name := `{root}
  let mut seen : NameSet := {{}}
  let mut out : NameSet := {{}}
  let mut todo : List Name := [root]
  for _ in [0:{fuel}] do
    match todo with
    | [] => pure ()
    | n :: rest =>
      todo := rest
      if !seen.contains n then
        seen := seen.insert n
        match env.find? n with
        | none => pure ()
        | some ci =>
          let e := ci.value?.getD ci.type
          for c in e.getUsedConstants do
            out := out.insert c
            if root.isPrefixOf c && !seen.contains c then
              todo := c :: todo
  IO.println ("{marker} " ++ String.intercalate " " (out.toList.map toString))
"""


def used_constants_command(signature: PinnedSignature, *, fuel: int = 64) -> str:
    """The REPL command that prints the spliced declaration's used-constant closure."""
    return _USED_CONSTS_PROBE.format(
        root=signature.name, fuel=fuel, marker=_USED_CONSTS_MARKER
    )


def parse_used_constants(raw: object) -> frozenset[str] | None:
    """Constants from the probe's info message, or `None` if the marker never appeared.

    `None` is a distinct outcome from "no constants": a probe that did not run tells us nothing
    about the candidate, and the caller reports ERRORED rather than admitting on silence.
    """
    messages = getattr(raw, "messages", None) or []
    for message in messages:
        data = getattr(message, "data", "") or ""
        if _USED_CONSTS_MARKER in data:
            return frozenset(data.split(_USED_CONSTS_MARKER, 1)[1].split())
    return None


def self_delegating_constants(constants: frozenset[str], target_real_name: str) -> list[str]:
    """Which of `constants` are the mined target itself, or one of its tight companions.

    Matching is delegated to `authoring.namematch` -- the single matcher this repo keeps for
    "does this text name this declaration", written after three private copies had independently
    drifted and each carried the same bug. Reusing it here rather than writing a fourth copy is
    a deliberate constraint of this check's brief.

    It gives exactly the semantics needed, for free:

    - `Nat.clog.eq_1`, `Nat.clog.induct` and other auto-generated companions TRIP (the `.` after
      the name is not an identifier character, so the boundary allows it).
    - `Nat.clog2` does NOT trip -- a genuinely different declaration (`2` is an identifier
      character). That is the exact false-positive class the module was built to kill.
    - `Nat.log` inside a `clog` candidate does NOT trip. Using the library is legal; only using
      the object under definition is not.
    - The task symbol itself does NOT trip when the real name is unnamespaced: `VTask.Monotone`
      is excluded by `exclude_task_symbol`, so legitimate recursion through the task symbol stays
      admissible.
    """
    from authoring.namematch import name_occurs  # imported here to keep `harness` importable
    # standalone -- `authoring` depends on `harness`, and a module-level import would invert that.

    return sorted(c for c in constants if name_occurs(c, target_real_name))


def _parse_axioms(message_data: str) -> frozenset[str] | None:
    """Parse one `#print axioms` info message. Returns `None` if it matches neither known
    shape -- the caller treats that as ERRORED rather than guessing."""
    if _NO_AXIOMS_RE.search(message_data):
        return frozenset()
    m = _AXIOM_LIST_RE.search(message_data)
    if m is None:
        return None
    return frozenset(n.strip() for n in m.group(1).split(",") if n.strip())


def check_admissibility(
    server: AutoLeanServer,
    candidate_env: int,
    signature: PinnedSignature,
    *,
    baseline_axioms: frozenset[str] | None = None,
    splice_response: object | None = None,
    target_real_name: str | None = None,
    timeout: float | None = None,
) -> AdmissibilityVerdict:
    """Verdict a spliced candidate before any scoring.

    Checks, in order: compile errors -> `sorry` -> exactly one declaration, named the pinned
    name (nothing shadowed or smuggled in alongside it) -> no axioms beyond baseline.

    `splice_response` -- the raw `CommandResponse` from the splice command that produced
    `candidate_env` -- drives the first three checks with no extra REPL round-trip.
    `harness.scoring.score_spliced_candidate` always provides it (its splice always requests
    `declarations=True`, which the shadowing check requires); without it, only the axiom
    check runs, since compile errors/sorries/declarations can't be reconstructed from an
    environment id alone after the fact.

    Deliberately strict on shadowing: a candidate may declare exactly the pinned name and
    nothing else. This also rejects a well-formed candidate that legitimately wants an
    auxiliary helper lemma alongside its main definition -- a real pipeline supporting that
    would need a smarter check (e.g. an explicit allowlist, or diffing against Mathlib's
    global namespace to distinguish "new helper" from "shadows a real dependency"). Out of
    scope here; this task asked for a gate that fails closed, not a permissive one.
    """
    baseline_axioms = baseline_axioms if baseline_axioms is not None else STANDARD_MATHLIB_AXIOMS
    timeout = timeout if timeout is not None else cfg.DECIDE_TIMEOUT

    if splice_response is not None:
        if splice_response.has_errors():
            return AdmissibilityVerdict(
                passed=False,
                failure=AdmissibilityFailure.COMPILE_ERROR,
                detail="; ".join(m.data for m in splice_response.get_errors()),
            )

        sorry_hit = bool(splice_response.sorries) or any(
            "sorry" in m.data for m in splice_response.get_warnings()
        )
        if sorry_hit:
            return AdmissibilityVerdict(
                passed=False,
                failure=AdmissibilityFailure.SORRY,
                detail="candidate body contains `sorry`",
            )

        # Exactly one declaration, and it must BE the pinned name. Unchanged in intent; the
        # alias carve-out below is the one deliberate relaxation (2026-08-05).
        #
        # `full_name` resolves to the alias TARGET for a body that is a bare reference to an
        # existing constant (`def VTask.choose := Nat.choose` reports
        # `name='VTask.choose', full_name='Nat.choose'`). Unioning both fields therefore invented
        # a phantom second declaration and rejected verbatim recall as tampering. That was the
        # open question at `docs/deferred.md`'s "bare-alias candidate bodies ... rather than being
        # scored as memorization"; its trigger fired at Stage B and the decision is to SCORE
        # them -- they are the memorization population the run measures, not tampering. Measured
        # incidence: 5 of 1040 extractable prelim candidates, four of them verbatim-correct
        # `Nat.choose`, i.e. concentrated exactly on the RECALLED_TARGET slice we report on.
        #
        # A declaration counts as the pinned one when EITHER field names it. Everything else --
        # a second declaration, or a single declaration of some other name -- still fails.
        declarations = list(splice_response.declarations)
        unexpected = [d for d in declarations if signature.name not in (d.name, d.full_name)]
        if unexpected or len(declarations) > 1:
            names = sorted({d.full_name or d.name for d in (unexpected or declarations)})
            return AdmissibilityVerdict(
                passed=False,
                failure=AdmissibilityFailure.NAME_SHADOWED,
                detail=(
                    f"candidate declared name(s) beyond the pinned '{signature.name}': {names}"
                ),
            )

        # Type conformance. Under declaration-verbatim splicing the candidate writes its OWN
        # signature, so the pinned type is no longer guaranteed by construction and has to be
        # checked. `#check (name : type)` rather than `example : type := name`, confirmed
        # against live Lean: the `example` form additionally COMPILES the definition and so
        # fails on any noncomputable candidate with "consider marking it as 'noncomputable'" --
        # which would have produced a systematic false WRONG_TYPE against exactly the
        # classical-construction population. `#check` only elaborates, and still catches wrong
        # arity and wrong result type (both verified).
        type_probe = run_checked(
            server, Command(cmd=type_probe_command(signature), env=candidate_env), timeout=timeout
        )
        if type_probe.status is not CheckStatus.PASSED:
            return AdmissibilityVerdict(
                passed=False,
                failure=AdmissibilityFailure.WRONG_TYPE,
                detail=(
                    f"does not have the pinned type '{signature.type_sig}': "
                    f"{(type_probe.detail or '').strip()[:600]}"
                ),
            )

    # Self-delegation. A candidate that defines the target by invoking the target is a tautology:
    # it type-checks, it passes every fact the real object passes, and it says nothing whatever
    # about whether the model can construct the object. Placed here deliberately -- after
    # compile/`sorry`/shadowing/WRONG_TYPE, before `admitted` -- because it is a SEMANTIC gate:
    # the candidate is well-formed Lean, and what disqualifies it is what it means.
    #
    # Skipped when no target name is supplied, rather than failing closed. The mined real name is
    # provenance the harness cannot derive on its own, and callers that legitimately have none
    # (authoring round-trips, synthetic tests) must not all become inadmissible.
    if target_real_name:
        closure = run_checked(
            server, Command(cmd=used_constants_command(signature), env=candidate_env),
            timeout=timeout,
        )
        if closure.status is not CheckStatus.PASSED:
            return AdmissibilityVerdict(
                passed=False,
                failure=AdmissibilityFailure.ERRORED,
                detail=f"could not read the constant closure: {closure.detail}",
            )
        constants = parse_used_constants(closure.raw_response)
        if constants is None:
            return AdmissibilityVerdict(
                passed=False,
                failure=AdmissibilityFailure.ERRORED,
                detail="constant-closure probe produced no result marker",
            )
        offenders = self_delegating_constants(constants, target_real_name)
        if offenders:
            return AdmissibilityVerdict(
                passed=False,
                failure=AdmissibilityFailure.SELF_DELEGATION,
                detail=(
                    f"body reaches the definition target '{target_real_name}' via {offenders}"
                ),
            )

    axiom_result = run_checked(
        server, Command(cmd=f"#print axioms {signature.name}", env=candidate_env), timeout=timeout
    )
    if axiom_result.status is not CheckStatus.PASSED:
        return AdmissibilityVerdict(
            passed=False,
            failure=AdmissibilityFailure.ERRORED,
            detail=f"could not check axioms: {axiom_result.detail}",
        )

    raw = axiom_result.raw_response
    info_messages = [m.data for m in raw.messages if m.severity == "info"] if raw is not None else []
    axioms: frozenset[str] | None = None
    for data in info_messages:
        parsed = _parse_axioms(data)
        if parsed is not None:
            axioms = parsed
            break

    if axioms is None:
        return AdmissibilityVerdict(
            passed=False,
            failure=AdmissibilityFailure.ERRORED,
            detail=f"could not parse `#print axioms` output: {info_messages!r}",
        )

    new_axioms = axioms - baseline_axioms
    if new_axioms:
        return AdmissibilityVerdict(
            passed=False,
            failure=AdmissibilityFailure.NEW_AXIOM,
            detail=f"candidate depends on axiom(s) beyond baseline: {sorted(new_axioms)}",
            axioms=axioms,
        )

    return AdmissibilityVerdict(passed=True, failure=None, detail="", axioms=axioms)
