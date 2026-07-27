"""Round-trip first-cut scoring path (contract §5, §8 item 5).

`harness.scoring.run_facts` deliberately raises `NotImplementedError` on any mechanism-`proof`
fact -- there is no prover scaffold yet, and that module's own docstring says pretending to
score one "would silently produce a meaningless result rather than an honest gap." The
contract's round-trip check needs a criterion that can run *today*, before the ladder exists:
score every `decide`-mechanism fact for real, and check every `proof`-mechanism (global) fact
only structurally -- does its statement still elaborate as a `Prop` against the round-trip
candidate's own spliced environment? -- without attempting to prove it.

This module is the "suite partitioning" the contract's §5 implementation note calls for:
`score_round_trip_first_cut` never hands a proof-mechanism fact to `run_facts`, so the
`NotImplementedError` path is never reached. The spliced-candidate elaboration check has no
existing precedent -- `authoring.validate.validate_global_fact`'s `#check (STATEMENT : Prop)`
runs against the *true* environment (checking the ground-truth definition names correctly);
here the identical command runs against the *candidate's* spliced environment instead, since
what's being checked is "does this statement even make sense against what the round-trip model
wrote," not "is it well-formed Lean in general."
"""

from dataclasses import dataclass, field

from lean_interact import AutoLeanServer, Command

from harness import config as cfg
from harness.admissibility import check_admissibility
from harness.facts import Fact
from harness.repl import run_checked
from harness.results import CheckResult, CheckStatus, FactResult
from harness.scoring import run_facts, splice_candidate
from harness.signature import PinnedSignature


@dataclass(frozen=True)
class RoundTripScore:
    """The outcome of one first-cut round-trip attempt. `criterion` is always `"first_cut"`
    today -- the `"full"` criterion (contract §5) activates only once ladder execution exists
    to actually adjudicate the withheld global facts, which this module does not attempt."""

    admissible: bool
    admissibility_detail: str
    splice: CheckResult | None = None
    decide_fact_results: list[FactResult] = field(default_factory=list)
    global_elaboration_results: list[tuple[str, CheckResult]] = field(default_factory=list)
    passed: bool = False
    criterion: str = "first_cut"

    @property
    def failing_decide_fact_ids(self) -> list[str]:
        return [r.fact_id for r in self.decide_fact_results if r.status is not CheckStatus.PASSED]

    @property
    def failing_global_fact_ids(self) -> list[str]:
        return [fid for fid, check in self.global_elaboration_results if check.status is not CheckStatus.PASSED]


def score_round_trip_first_cut(
    server: AutoLeanServer,
    base_env: int,
    signature: PinnedSignature,
    body: str,
    facts: list[Fact],
    *,
    baseline_axioms: frozenset[str] | None = None,
    check_timeout: float | None = None,
) -> RoundTripScore:
    """Splice `body` under `signature`, gate it (Layer 0, unchanged from `harness.scoring`),
    then -- only if admitted -- score every `decide`-mechanism fact for real via
    `harness.scoring.run_facts` and check every `proof`-mechanism (global) fact structurally
    against the candidate's own spliced environment. Passes iff admissible, every decide fact
    PASSED, and every global fact's statement still elaborates as a `Prop`."""
    check_timeout = check_timeout if check_timeout is not None else cfg.DECIDE_TIMEOUT

    cmd_text = signature.splice(body)
    splice_result = splice_candidate(server, base_env, cmd_text, timeout=check_timeout)
    if splice_result.status is CheckStatus.ERRORED:
        return RoundTripScore(
            admissible=False,
            admissibility_detail=splice_result.detail or "splice errored",
            splice=splice_result,
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
        return RoundTripScore(
            admissible=False,
            admissibility_detail=f"{verdict.failure.value}: {verdict.detail}",
            splice=splice_result,
        )

    decide_facts = [f for f in facts if f.mechanism == "decide"]
    global_facts = [f for f in facts if f.mechanism == "proof"]

    decide_results = run_facts(server, splice_result.env, decide_facts, decide_timeout=check_timeout)

    global_results: list[tuple[str, CheckResult]] = []
    for fact in global_facts:
        prop_cmd = f"#check ({fact.statement} : Prop)"
        check = run_checked(server, Command(cmd=prop_cmd, env=splice_result.env), timeout=check_timeout)
        global_results.append((fact.id, check))

    decide_passed = all(r.status is CheckStatus.PASSED for r in decide_results)
    global_passed = all(check.status is CheckStatus.PASSED for _, check in global_results)

    return RoundTripScore(
        admissible=True,
        admissibility_detail="",
        splice=splice_result,
        decide_fact_results=decide_results,
        global_elaboration_results=global_results,
        passed=decide_passed and global_passed,
    )
