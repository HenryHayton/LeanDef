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


class AdmissibilityFailure(Enum):
    COMPILE_ERROR = "compile_error"
    SORRY = "sorry"
    NEW_AXIOM = "new_axiom"
    NAME_SHADOWED = "name_shadowed"
    WRONG_TYPE = "wrong_type"  # compiled fine, but does not have the pinned type
    ERRORED = "errored"


@dataclass(frozen=True)
class AdmissibilityVerdict:
    passed: bool
    failure: AdmissibilityFailure | None
    detail: str
    axioms: frozenset[str] = frozenset()


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
            server,
            Command(cmd=f"#check ({signature.name} : {signature.type_sig})", env=candidate_env),
            timeout=timeout,
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
