"""Tier 1 (decide) -- reward doc §3: "unchanged; reuses `harness/` as built."

A projection of `harness.repl.run_checked`'s three-way `CheckStatus` onto the ladder's own
`ladder.statuses.AdjudicationStatus`, so `ladder.adjudicate`'s loop has one uniform attempt
shape across every tier -- plus, since 2026-08-05, a CONTENT-BASED reading of what a decide
failure actually means.

**Why the content check exists.** `run_checked` reports `CheckStatus.FAILED` whenever the
command produced errors. A decide command errors for at least five distinct reasons, and this
module used to map all of them to `FAILED`, documented as "computed to false -- a genuine,
kernel-certified negative result". Only one of them is. Probed against live Mathlib
(Lean v4.32.0), all five come back as `CheckStatus.FAILED`:

| Lean's message                                  | means                          | maps to  |
|-------------------------------------------------|--------------------------------|----------|
| ``Tactic `decide` proved ... is false``          | the proposition IS false       | FAILED   |
| ``failed to synthesize`` + ``Decidable (...)``   | untestable through this splice | UNKNOWN  |
| ``Unknown identifier`` / ``Unknown constant``    | broken splice                  | ERRORED  |
| ``maximum recursion depth`` / ``timeout``        | computation blew up            | ERRORED  |
| ``failed to synthesize instance of type class``  | malformed statement            | ERRORED  |
| anything unrecognised                            | unknown machinery failure      | ERRORED  |

The UNKNOWN/ERRORED asymmetry is deliberate and load-bearing: UNKNOWN means *unadjudicable for
this candidate* (excluded from denominators, and not worth retrying -- a retry cannot conjure a
`Decidable` instance), while ERRORED means *broken machinery* (retryable, reported). Collapsing
them would either retry a hopeless case or silently penalise a candidate for our own inability
to test it.

This extends the ladder's existing doctrine -- "it only ever finds proofs, it never adjudicates
by opinion" (reward doc §2.3) -- down to tier 1. `FAILED` is the strong claim, so it requires
POSITIVE evidence; anything unrecognised defaults to `ERRORED`, never `FAILED`.

**Why it matters beyond scoring.** The same call adjudicates facts during authoring validation,
where a `Decidable`-synthesis failure read as "the truth definition refutes this fact" would
silently drop a good fact from a suite -- a corpus-quality bug, not merely a scoring one. Truth
splices mostly resolve their instances, which is why this went unnoticed; candidate splices,
which may phrase a definition unusually, hit it far more often. That is the same
differential-by-output-style hazard the Stage A splice fixes addressed elsewhere.
"""

from lean_interact import AutoLeanServer, Command

from harness.repl import run_checked
from harness.results import CheckStatus
from ladder.budgets import LadderBudgets
from ladder.statuses import AdjudicationStatus, TierAttempt

# The ONE route to FAILED. Matched on the stable middle of the sentence rather than its prefix:
# Lean has already reworded the opening of this message once (`decide proved that...` became
# ``Tactic `decide` proved that...``), and a version bump that silently closed this branch would
# turn every genuine refutation into an ERROR and quietly destroy separation scoring.
_KERNEL_FALSE_MARKERS = ("proved that the proposition", "is false")

# Untestable through this splice. Must match BOTH -- `failed to synthesize` alone also prefixes
# ordinary type-class failures (`failed to synthesize instance of type class / HAdd ℕ ℕ Prop`),
# which are malformed statements rather than undecidable ones.
_NO_DECIDABLE_MARKERS = ("failed to synthesize", "Decidable")


def classify_decide_failure(detail: str) -> AdjudicationStatus:
    """Read a decide command's error text and say what it is evidence of.

    Split out from `adjudicate_tier1` so the mapping is testable without a REPL: these are
    decisions about strings, and pinning them against captured real Lean output is both cheaper
    and stricter than round-tripping every case through a live server.
    """
    text = detail or ""
    if all(marker in text for marker in _KERNEL_FALSE_MARKERS):
        return AdjudicationStatus.FAILED
    if all(marker in text for marker in _NO_DECIDABLE_MARKERS):
        return AdjudicationStatus.UNKNOWN
    # Everything else -- unknown identifier, recursion depth, deterministic timeout, type-class
    # failure, and anything Lean invents later -- is broken machinery, not a refutation.
    return AdjudicationStatus.ERRORED


def adjudicate_tier1(server: AutoLeanServer, env: int, statement: str, budgets: LadderBudgets) -> TierAttempt:
    """`statement` is the full runnable decide-mechanism command (schema v1.1 §3.1's decide
    canonical form), run exactly as `harness.scoring.run_facts` already does for mechanism
    `decide`.

    PASSED -> CERTIFIED. FAILED -> whatever `classify_decide_failure` reads the error as (see
    the module docstring's table). Any other `CheckStatus` -- a timeout or dead REPL, where
    there is no Lean message to read at all -> ERRORED.
    """
    check = run_checked(server, Command(cmd=statement, env=env), timeout=budgets.tier1_timeout_s)
    if check.status is CheckStatus.PASSED:
        status = AdjudicationStatus.CERTIFIED
    elif check.status is CheckStatus.FAILED:
        status = classify_decide_failure(check.detail)
    else:
        status = AdjudicationStatus.ERRORED
    return TierAttempt(tier=1, tactic=None, status=status, elapsed_s=check.elapsed_s, detail=check.detail)
