"""Generic candidate scoring: splice a candidate under a pinned signature, run it through the
admissibility gate, and -- only if admitted -- score it against a fact suite.

Extracted and parameterized from `archive/n1_tau/score.py` per `docs/repo_audit.md` §2
(generic vs tau-specific classification): the REPL bootstrap, splice mechanism, fact-checking
loop, and result collection identified there as generic are here; the specific facts,
candidate bodies, and pinned signature are left as caller-supplied data.
`archive/n1_tau/` itself is left untouched -- nothing in this module reads from it.

Per `docs/design/reward_structure_2026-07-21.md` §2 and `docs/design/task_schema_v1.md`, a
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
from harness.results import CandidateScore, CheckResult, CheckStatus, FactResult
from harness.signature import PinnedSignature

__all__ = [
    "PinnedSignature",
    "Fact",
    "splice_candidate",
    "run_facts",
    "score_candidate",
    "score_spliced_candidate",
]


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
    """Splice a well-formed (single-declaration) candidate body, then score it. Convenience
    wrapper around `score_spliced_candidate` for the common case; use that function directly
    to score a candidate whose command text isn't a simple `PinnedSignature.splice(body)`."""
    return score_spliced_candidate(
        server,
        base_env,
        signature.splice(body),
        signature,
        facts,
        label=label,
        baseline_axioms=baseline_axioms,
        check_timeout=check_timeout,
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

    if splice_result.status is CheckStatus.ERRORED:
        return CandidateScore(
            label=label,
            splice=splice_result,
            admissible=False,
            admissibility_detail=splice_result.detail or "splice errored",
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
        return CandidateScore(
            label=label,
            splice=splice_result,
            admissible=False,
            admissibility_detail=f"{verdict.failure.value}: {verdict.detail}",
        )

    fact_results = run_facts(server, splice_result.env, facts, decide_timeout=check_timeout)
    return CandidateScore(
        label=label,
        splice=splice_result,
        admissible=True,
        admissibility_detail="",
        fact_results=fact_results,
    )
