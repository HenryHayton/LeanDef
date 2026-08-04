"""Generic candidate scoring: splice a candidate under a pinned signature, run it through the
admissibility gate, and -- only if admitted -- score it against a fact suite.

Extracted and parameterized from `archive/n1_tau/score.py` per `docs/repo_audit.md` §2
(generic vs tau-specific classification): the REPL bootstrap, splice mechanism, fact-checking
loop, and result collection identified there as generic are here; the specific facts,
candidate bodies, and pinned signature are left as caller-supplied data.
`archive/n1_tau/` itself is left untouched -- nothing in this module reads from it.

Per `docs/design/reward_structure_2026-07-21.md` §2 and `docs/design/task_schema_v1_1.md`, a
fact declares its own `mechanism` (`decide` or `proof`) -- see `harness.facts.Fact`.
`run_facts` dispatches on it: `decide` runs as a REPL command and reads PASSED/FAILED off
`has_errors()`, exactly as before; `proof` has no adjudication path yet and raises
`NotImplementedError` rather than silently mis-scoring (the prover scaffold -- tri-state
TRUE/FALSE/UNKNOWN per `docs/design/verifier_architecture_2026-07-20.md` §4 -- is not built).
See `docs/decidability_bias_survey.md` for the gap this closes and what's still open.

Deliberately out of scope (see `docs/design/`): fact mining, mutant generation, the prover
layer itself, task-schema validation (see `harness.task_schema`).
"""

from lean_interact import AutoLeanServer, Command

from harness import config as cfg
from harness.admissibility import check_admissibility
from harness.facts import Fact
from harness.repl import run_checked
from harness.results import (
    CandidateScore,
    CheckResult,
    CheckStatus,
    FactResult,
    SpliceAttempt,
    SpliceOutcome,
    SplicePath,
)
from harness.signature import PinnedSignature, reducible_declaration

__all__ = [
    "PinnedSignature",
    "Fact",
    "splice_candidate",
    "splice_candidate_body",
    "splice_candidate_declaration",
    "splice_real_name",
    "SpliceOutcome",
    "SplicePath",
    "run_facts",
    "score_candidate",
    "score_spliced_candidate",
]

# Lean's own compiler error text for the noncomputability case `PinnedSignature.splice_real_name`'s
# own docstring describes -- confirmed verbatim (2026-07-31) against a real failing case
# (`Function.extend`): "failed to compile definition, consider marking it as 'noncomputable'
# because it depends on '<name>', which is 'noncomputable'". Matched as a substring, not an
# exact string, since `<name>` varies per declaration.
_NONCOMPUTABLE_ERROR_MARKER = "consider marking it as 'noncomputable'"

# Error shapes that mean "a bare reference in the body resolved to the declaration currently
# being elaborated" -- the self-reference collision `PinnedSignature.splice_real_name`'s
# docstring documents on the truth side. Lean never says "self-reference": the collision
# manufactures a bogus recursive definition, so what surfaces is a TERMINATION complaint.
#
# `well-founded recursion` is the shape confirmed verbatim against real Mathlib (2026-07-31,
# the 4-name x 3-attribute repro matrix; asserted in `tests/test_signature_reducible_splice.py`).
# `failed to show termination` is Lean 4's other standard phrasing for the same class. Both are
# matched case-insensitively as substrings.
#
# Kept DELIBERATELY narrow, per this stage's brief: prefer failing to rescue an exotic case
# over rescuing one that should not be rescued. A genuinely recursive candidate that fails its
# own termination proof produces these same strings, which is exactly why matching the error is
# necessary but NOT sufficient -- `_can_root_qualify` adds two further guards before any rewrite.
_SELF_REFERENCE_ERROR_MARKERS = ("well-founded recursion", "failed to show termination")


def _needs_noncomputable(detail: str) -> bool:
    return _NONCOMPUTABLE_ERROR_MARKER in (detail or "")


def _looks_like_self_reference(detail: str) -> bool:
    lowered = (detail or "").lower()
    return any(marker in lowered for marker in _SELF_REFERENCE_ERROR_MARKERS)


def _can_root_qualify(signature: PinnedSignature, body: str) -> bool:
    """Whether rewriting `body`'s bare self-references is permissible AT ALL.

    Two guards, both required, both conservative:

    1. The body must not name the task symbol in full (`VTask.Monotone`). That spelling is an
       unambiguous declaration of intent to recurse, and a candidate that means to recurse and
       fails its termination proof must be allowed to fail on its own terms.
    2. There must be something to rewrite -- at least one bare `base_name` occurrence. Without
       one, a termination error is a real termination error, and the retry would re-send byte-
       identical text for a guaranteed-identical failure.
    """
    if signature.references_self_explicitly(body):
        return False
    _, n = signature.root_qualified_body(body)
    return n > 0


def splice_real_name(
    server: AutoLeanServer,
    base_env: int,
    signature: PinnedSignature,
    real_name: str,
    *,
    timeout: float | None = None,
) -> CheckResult:
    """Splice an EXISTING Mathlib declaration under `signature` (`PinnedSignature.splice_real_name`),
    with the noncomputable retry that method's own docstring describes: try a plain (reducible)
    alias first, and retry ONCE with `noncomputable` only on that specific compiler error --
    never on any other failure (a genuine type/termination error retried with `noncomputable`
    would just fail again, having burned a REPL round-trip for nothing). Lives here (not in
    `authoring.pipeline`, where the truth-splice call site originally built this inline) so
    `authoring.preflight`'s selection-time full-splice check can share it without pulling in
    `authoring.pipeline`'s much heavier dependency graph (Bedrock, orchestrate, emit, ...) --
    both callers need exactly this, nothing authoring-specific."""
    cmd = signature.splice_real_name(real_name)
    result = splice_candidate(server, base_env, cmd, timeout=timeout)
    if result.status is CheckStatus.PASSED:
        return result
    if _NONCOMPUTABLE_ERROR_MARKER in (result.detail or ""):
        retry_cmd = signature.splice_real_name(real_name, noncomputable=True)
        return splice_candidate(server, base_env, retry_cmd, timeout=timeout)
    return result


def splice_candidate(
    server: AutoLeanServer,
    base_env: int,
    cmd_text: str,
    *,
    timeout: float | None = None,
) -> CheckResult:
    """Splice a candidate's full command text against the warm base environment.

    `cmd_text` is sent as-is -- build it via `PinnedSignature.splice(body)` for the common,
    well-formed, single-declaration case, or construct raw multi-declaration text directly
    (helper lemmas, or an adversarial extra declaration for admissibility-gate testing).
    Always requests `declarations=True` so the admissibility gate can inspect exactly what
    got declared.
    """
    timeout = timeout if timeout is not None else cfg.DECIDE_TIMEOUT
    return run_checked(server, Command(cmd=cmd_text, env=base_env, declarations=True), timeout=timeout)


def splice_candidate_body(
    server: AutoLeanServer,
    base_env: int,
    signature: PinnedSignature,
    body: str,
    *,
    timeout: float | None = None,
) -> SpliceOutcome:
    """Splice a candidate BODY, retrying the two rescues the truth side already had.

    This is the candidate-side counterpart to `splice_real_name` (2026-08-04). Both
    protections previously existed only on the truth path, and both silently convert a correct
    candidate into a `COMPILE_ERROR` admissibility failure -- differentially, since they punish
    exactly the Lean-fluent output styles that reference real declarations by their bare names
    or reach for classical constructions.

    The ladder, bounded at four attempts and never looping:

        plain -> noncomputable -> root_qualified -> root_qualified+noncomputable

    Each step is taken ONLY when the previous attempt's error specifically calls for it
    (`_needs_noncomputable` / `_looks_like_self_reference` plus `_can_root_qualify`), so a
    candidate needing nothing costs exactly one round-trip. The two triggers are independent
    and can fire in either order -- a body that needs both converges on the fourth state from
    either direction -- and a `seen` set makes re-entering a state impossible.

    An ERRORED attempt (timeout, dead REPL) stops the ladder immediately: that is an
    infrastructure event, not evidence about the candidate, and retrying a variant against a
    server that may have just died would only confuse the diagnosis.
    """
    timeout = timeout if timeout is not None else cfg.DECIDE_TIMEOUT
    qualified_body, _ = signature.root_qualified_body(body)
    may_qualify = _can_root_qualify(signature, body)

    paths = {
        (False, False): SplicePath.PLAIN,
        (False, True): SplicePath.NONCOMPUTABLE,
        (True, False): SplicePath.ROOT_QUALIFIED,
        (True, True): SplicePath.ROOT_QUALIFIED_NONCOMPUTABLE,
    }

    attempts: list[SpliceAttempt] = []
    plain_result: CheckResult | None = None
    plain_cmd = ""
    state: tuple[bool, bool] | None = (False, False)
    seen: set[tuple[bool, bool]] = set()

    while state is not None and state not in seen:
        seen.add(state)
        root_q, noncomp = state
        cmd = signature.splice(qualified_body if root_q else body, noncomputable=noncomp)
        result = splice_candidate(server, base_env, cmd, timeout=timeout)
        attempts.append(SpliceAttempt(paths[state], cmd, result.status, result.detail or ""))
        if plain_result is None:
            plain_result, plain_cmd = result, cmd

        if result.status is CheckStatus.PASSED:
            return SpliceOutcome(result=result, path=paths[state], cmd_text=cmd, attempts=attempts)
        if result.status is CheckStatus.ERRORED:
            break

        if not noncomp and _needs_noncomputable(result.detail):
            state = (root_q, True)
        elif not root_q and may_qualify and _looks_like_self_reference(result.detail):
            state = (True, noncomp)
        else:
            state = None

    return SpliceOutcome(
        result=plain_result, path=SplicePath.PLAIN, cmd_text=plain_cmd, attempts=attempts
    )


def splice_candidate_declaration(
    server: AutoLeanServer,
    base_env: int,
    signature: PinnedSignature,
    decl_text: str,
    *,
    timeout: float | None = None,
) -> SpliceOutcome:
    """Splice a candidate's own DECLARATION verbatim, with `@[reducible]` applied.

    The real-candidate path since 2026-08-05. `splice_candidate_body` builds the declaration
    from a body expression, which is what `authoring.roundtrip` supplies; the prelim prompt
    instead asks models for a complete declaration, and 1040 of 1040 extractable candidates are
    one. Parsing them back into bodies would be fragile against implicit/instance binders,
    equation-style definitions and `where` clauses, and every parse failure would be another
    differential-by-output-style false negative -- the bug class Stage A and the tier-1 fix
    exist to remove. The pinned type is instead enforced by kernel check in
    `harness.admissibility` (`WRONG_TYPE`), which is strictly stronger than construction.

    Runs the SAME bounded four-state ladder as `splice_candidate_body`
    (plain -> noncomputable -> root-qualified -> both), on declaration text: `@[reducible]` is
    merged into the model's own attribute group rather than stacked (stacking is a Lean syntax
    error), and root-qualification rewrites only the body region, since a declaration always
    spells its own task symbol in its header.
    """
    timeout = timeout if timeout is not None else cfg.DECIDE_TIMEOUT
    qualified, n_rewrites = signature.root_qualified_declaration(decl_text)
    may_qualify = n_rewrites > 0 and not signature.declaration_references_self_explicitly(decl_text)

    paths = {
        (False, False): SplicePath.PLAIN,
        (False, True): SplicePath.NONCOMPUTABLE,
        (True, False): SplicePath.ROOT_QUALIFIED,
        (True, True): SplicePath.ROOT_QUALIFIED_NONCOMPUTABLE,
    }
    attempts: list[SpliceAttempt] = []
    plain_result: CheckResult | None = None
    plain_cmd = ""
    state: tuple[bool, bool] | None = (False, False)
    seen: set[tuple[bool, bool]] = set()

    while state is not None and state not in seen:
        seen.add(state)
        root_q, noncomp = state
        cmd = reducible_declaration(qualified if root_q else decl_text, noncomputable=noncomp)
        result = splice_candidate(server, base_env, cmd, timeout=timeout)
        attempts.append(SpliceAttempt(paths[state], cmd, result.status, result.detail or ""))
        if plain_result is None:
            plain_result, plain_cmd = result, cmd

        if result.status is CheckStatus.PASSED:
            return SpliceOutcome(result=result, path=paths[state], cmd_text=cmd, attempts=attempts)
        if result.status is CheckStatus.ERRORED:
            break

        if not noncomp and _needs_noncomputable(result.detail):
            state = (root_q, True)
        elif not root_q and may_qualify and _looks_like_self_reference(result.detail):
            state = (True, noncomp)
        else:
            state = None

    return SpliceOutcome(
        result=plain_result, path=SplicePath.PLAIN, cmd_text=plain_cmd, attempts=attempts
    )


def run_facts(
    server: AutoLeanServer,
    candidate_env: int,
    facts: list[Fact],
    *,
    decide_timeout: float | None = None,
) -> list[FactResult]:
    """Adjudicate each fact against the spliced candidate's environment, dispatching on
    `fact.mechanism`. One `FactResult` per fact, in order.

    `mechanism == "decide"`: sent as a REPL command, status read off `has_errors()` -- the
    decidable-casework/decidable-membership path (reward-structure design §2.1-2.2).
    `mechanism == "proof"`: raises `NotImplementedError` immediately. There is no prover
    scaffold yet (§2.3, §4 of the architecture doc) to attempt the fact and its negation
    under budget, so pretending to score a proof-mechanism fact here would silently produce
    a meaningless result rather than an honest gap.
    """
    decide_timeout = decide_timeout if decide_timeout is not None else cfg.DECIDE_TIMEOUT
    results: list[FactResult] = []
    for fact in facts:
        if fact.mechanism == "decide":
            check = run_checked(
                server, Command(cmd=fact.statement, env=candidate_env), timeout=decide_timeout
            )
            results.append(
                FactResult(
                    fact_id=fact.id,
                    status=check.status,
                    elapsed_s=check.elapsed_s,
                    detail=check.detail,
                    raw_response=check.raw_response,
                )
            )
        elif fact.mechanism == "proof":
            raise NotImplementedError(
                f"fact {fact.id!r}: mechanism 'proof' has no adjudication path yet -- the "
                "prover scaffold (docs/design/verifier_architecture_2026-07-20.md §4) is not "
                "built. Not falling back to `decide` or any other guess: an unscored fact "
                "must fail loudly, not silently."
            )
        else:
            # harness.task_schema.validate_task_data rejects any other value before a task
            # ships; a Fact built by hand (as in this codebase's own tests) could still reach
            # here with something else, so this stays a real check, not a comment.
            raise ValueError(f"fact {fact.id!r}: unknown mechanism {fact.mechanism!r}")
    return results


def score_candidate(
    server: AutoLeanServer,
    base_env: int,
    signature: PinnedSignature,
    body: str,
    facts: list[Fact],
    *,
    label: str = "candidate",
    baseline_axioms: frozenset[str] | None = None,
    check_timeout: float | None = None,
) -> CandidateScore:
    """Splice a well-formed (single-declaration) candidate body, then score it.

    Routes through `splice_candidate_body`, so a candidate needing `noncomputable` or
    root-qualification is rescued rather than failed at the admissibility gate, and the
    winning path is recorded on `CandidateScore.splice_outcome`. Use `score_spliced_candidate`
    directly for a candidate whose command text is NOT a simple `PinnedSignature.splice(body)`
    -- that path has no body to rewrite and so runs no ladder.
    """
    check_timeout = check_timeout if check_timeout is not None else cfg.DECIDE_TIMEOUT
    outcome = splice_candidate_body(server, base_env, signature, body, timeout=check_timeout)
    return _score_from_splice(
        server,
        outcome.result,
        signature,
        facts,
        label=label,
        baseline_axioms=baseline_axioms,
        check_timeout=check_timeout,
        splice_outcome=outcome,
    )


def score_spliced_candidate(
    server: AutoLeanServer,
    base_env: int,
    cmd_text: str,
    signature: PinnedSignature,
    facts: list[Fact],
    *,
    label: str = "candidate",
    baseline_axioms: frozenset[str] | None = None,
    check_timeout: float | None = None,
) -> CandidateScore:
    """Splice arbitrary candidate command text, gate it, and -- only if admitted -- score it.

    Refuses to run any fact against a candidate that fails the admissibility gate (Layer 0):
    `fact_results` stays empty and `CandidateScore.fidelity` is `None` in that case. Raises
    `NotImplementedError` (propagated from `run_facts`) if `facts` contains any
    mechanism-`proof` fact -- there is nothing to catch that with yet.
    """
    check_timeout = check_timeout if check_timeout is not None else cfg.DECIDE_TIMEOUT
    splice_result = splice_candidate(server, base_env, cmd_text, timeout=check_timeout)
    return _score_from_splice(
        server,
        splice_result,
        signature,
        facts,
        label=label,
        baseline_axioms=baseline_axioms,
        check_timeout=check_timeout,
        splice_outcome=None,
    )


def _score_from_splice(
    server: AutoLeanServer,
    splice_result: CheckResult,
    signature: PinnedSignature,
    facts: list[Fact],
    *,
    label: str,
    baseline_axioms: frozenset[str] | None,
    check_timeout: float,
    splice_outcome: SpliceOutcome | None,
) -> CandidateScore:
    """Gate-then-score an already-spliced candidate. Shared by both public entry points so the
    admissibility/fact sequence exists once; they differ only in how the splice was produced
    (raw command text vs the retry ladder)."""
    if splice_result.status is CheckStatus.ERRORED:
        return CandidateScore(
            label=label,
            splice=splice_result,
            admissible=False,
            admissibility_detail=splice_result.detail or "splice errored",
            splice_outcome=splice_outcome,
        )

    verdict = check_admissibility(
        server,
        splice_result.env,
        signature,
        baseline_axioms=baseline_axioms,
        splice_response=splice_result.raw_response,
        timeout=check_timeout,
    )
    if not verdict.passed:
        detail = f"{verdict.failure.value}: {verdict.detail}"
        # Retry errors are SECONDARY: `splice_result` is already the plain attempt's on total
        # failure, so `admissibility_detail` leads with the honest primary diagnostic and the
        # rescue attempts are appended behind it rather than displacing it.
        if splice_outcome is not None and splice_outcome.retries_consumed:
            detail = f"{detail} [rescues attempted: {'; '.join(splice_outcome.secondary_details[1:])}]"
        return CandidateScore(
            label=label,
            splice=splice_result,
            admissible=False,
            admissibility_detail=detail,
            splice_outcome=splice_outcome,
        )

    fact_results = run_facts(server, splice_result.env, facts, decide_timeout=check_timeout)
    return CandidateScore(
        label=label,
        splice=splice_result,
        admissible=True,
        admissibility_detail="",
        fact_results=fact_results,
        splice_outcome=splice_outcome,
    )
