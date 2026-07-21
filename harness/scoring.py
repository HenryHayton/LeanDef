"""Generic candidate scoring: splice a candidate under a pinned signature, run it through the
admissibility gate, and -- only if admitted -- score it against a fact suite.

Extracted and parameterized from `archive/n1_tau/score.py` per `docs/repo_audit.md` §2
(generic vs tau-specific classification): the REPL bootstrap, splice mechanism, fact-checking
loop, and result collection identified there as generic are here; the specific facts,
candidate bodies, and pinned signature are left as caller-supplied data.
`archive/n1_tau/` itself is left untouched -- nothing in this module reads from it.

Per `docs/design/reward_structure_2026-07-21.md` §2, a fact suite has three types: decidable
casework, membership facts (decidable where possible, proof-based otherwise), and global
theorem facts (always proof-based, adjudicated by a prover agent with tri-state TRUE/FALSE/
UNKNOWN semantics). This module implements exactly one of those three mechanisms: `run_facts`
sends each fact as a raw REPL command and reads PASSED/FAILED off `has_errors()` -- correct
for decidable casework and decidable membership checks, and *only* those. It has no path for
a fact that needs a prover agent, and no representation for UNKNOWN. A τ-shaped object (this
repo's only worked example so far, `archive/n1_tau/` -- computable, cheap, decidable-fact-rich)
is fully covered by what's here; a proof-heavy object (e.g. a compactness-style property on an
infinite carrier, with almost no decidable facts at all) is not, and would need a genuinely
different adjudication path, not an extension of `run_facts`. See
`docs/decidability_bias_survey.md` for exactly where this module's result types and defaults
assume decidable-scale cost.

Deliberately out of scope (see `docs/design/`): fact mining, mutant generation, the prover
layer, tri-state adjudication.
"""

from lean_interact import AutoLeanServer, Command

from harness import config as cfg
from harness.admissibility import check_admissibility
from harness.repl import run_checked
from harness.results import CandidateScore, CheckResult, CheckStatus
from harness.signature import PinnedSignature

__all__ = [
    "PinnedSignature",
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
    timeout = timeout if timeout is not None else cfg.DEFAULT_CHECK_TIMEOUT
    return run_checked(server, Command(cmd=cmd_text, env=base_env, declarations=True), timeout=timeout)


def run_facts(
    server: AutoLeanServer,
    candidate_env: int,
    facts: list[str],
    *,
    timeout: float | None = None,
) -> list[CheckResult]:
    """Run each fact (a full `example ... := by decide` source string) against the spliced
    candidate's environment. One `CheckResult` per fact, in order.

    This is the decidable-casework adjudication mechanism only (reward-structure design
    §2.1) -- every fact here is assumed to resolve via kernel computation within `timeout`.
    Membership facts that need a proof and global theorem facts (§2.2-§2.3) are not
    representable as a plain fact string and are not handled by this function; see the
    module docstring and `docs/decidability_bias_survey.md`.
    """
    timeout = timeout if timeout is not None else cfg.DEFAULT_CHECK_TIMEOUT
    return [run_checked(server, Command(cmd=fact, env=candidate_env), timeout=timeout) for fact in facts]


def score_candidate(
    server: AutoLeanServer,
    base_env: int,
    signature: PinnedSignature,
    body: str,
    facts: list[str],
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
    facts: list[str],
    *,
    label: str = "candidate",
    baseline_axioms: frozenset[str] | None = None,
    check_timeout: float | None = None,
) -> CandidateScore:
    """Splice arbitrary candidate command text, gate it, and -- only if admitted -- score it.

    Refuses to run any fact against a candidate that fails the admissibility gate (Layer 0):
    `fact_results` stays empty and `CandidateScore.fidelity` is `None` in that case.
    """
    check_timeout = check_timeout if check_timeout is not None else cfg.DEFAULT_CHECK_TIMEOUT

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

    fact_results = run_facts(server, splice_result.env, facts, timeout=check_timeout)
    return CandidateScore(
        label=label,
        splice=splice_result,
        admissible=True,
        admissibility_detail="",
        fact_results=fact_results,
    )
