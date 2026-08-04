"""Tests for ladder.tier2 -- the pinned tactic set, its env-chaining, and the budgeted
env-death recovery loop.

Real-discharge tests need a live warm Mathlib environment (there's no ground truth to fake for
"does this tactic actually close this goal"), matching the `mathlib_env` pattern
`tests/test_miner_discharge.py` established. The env-death recovery path is exercised with a
scripted fake server instead (same pattern `tests/test_miner_verify_recovery.py` uses) -- a real
death isn't practical to provoke on demand.
"""

from lean_interact import Command
from lean_interact.interface import CommandResponse, LeanError, Message, Pos

from harness.repl import run_checked
from harness.results import CheckStatus
from ladder.budgets import DEFAULT_LADDER_BUDGETS, LadderBudgets
from ladder.statuses import AdjudicationStatus
from ladder.tier2 import adjudicate_tier2



def _error_message(data: str) -> Message:
    return Message(start_pos=Pos(line=1, column=1), end_pos=None, severity="error", data=data)


class _FakeServer:
    """Same scripted-fake-server pattern `tests/test_miner_verify_recovery.py`'s `_FakeServer`
    uses: one scripted response per `.run()` call, in order."""

    def __init__(self, script: list):
        self.script = list(script)
        self.calls: list[tuple[str, object]] = []

    def run(self, request, timeout=None):
        self.calls.append((request.cmd, request.env))
        if not self.script:
            raise AssertionError(f"fake server ran out of scripted responses at call: {request.cmd!r}")
        return self.script.pop(0)


# --- real discharge: rfl wins immediately -------------------------------------------------


def test_rfl_discharges_a_trivial_statement(mathlib_env):
    server, env = mathlib_env
    # a bare (non-quantified) equality -- `rfl` doesn't auto-`intro` a leading forall binder,
    # so this is the shape that lets rfl win on its first attempt (confirmed empirically:
    # the quantified form `∀ n, n + 0 = n` makes rfl fail with "Expected the goal to be a
    # binary relation" and falls through to `omega`, which does handle the forall).
    result = adjudicate_tier2(server, env, "trivial_add4", "(2:ℕ) + 2 = 4", DEFAULT_LADDER_BUDGETS)
    assert result.winning is not None
    assert result.winning.tactic == "rfl"
    assert len(result.attempts) == 1  # ladder stopped -- no later tactic attempted


# --- real discharge: a genuinely provable Nat.clog fact, drawn from real mention data ------


def test_discharges_a_real_clog_mention_statement(mathlib_env):
    server, env = mathlib_env
    # Nat.clog_one_right (miner/output/mention_names.jsonl, name="Nat.clog"): a real Mathlib
    # lemma with this exact type -- a genuinely provable global-style fact, not a decidable
    # casework instance.
    result = adjudicate_tier2(server, env, "clog_one_right", "∀ (b : ℕ), Nat.clog b 1 = 0", DEFAULT_LADDER_BUDGETS)
    assert result.winning is not None
    assert result.winning_theorem_name is not None
    # the declared theorem must actually exist in the RETURNED env (the env-chaining fix) --
    # #print axioms on it must find the declaration, not "Unknown constant".
    check = run_checked(server, Command(cmd=f"#print axioms {result.winning_theorem_name}", env=result.env), timeout=30.0)
    assert check.status is CheckStatus.PASSED, check.detail
    assert "Unknown constant" not in (check.detail or "")


# --- real discharge: a genuinely hard statement returns UNKNOWN, not FAILED ----------------


def test_genuinely_hard_statement_returns_unknown_not_failed(mathlib_env):
    server, env = mathlib_env
    # Not a restatement of any real Mathlib lemma, and requires induction no pinned tactic
    # performs -- expected to exhaust every tier-2 tactic without a verdict either way.
    result = adjudicate_tier2(
        server, env, "hard_clog_doubling", "∀ (n : ℕ), 1 < n → Nat.clog 2 (2 * n) = Nat.clog 2 n + 1",
        DEFAULT_LADDER_BUDGETS,
    )
    assert result.winning is None
    assert len(result.attempts) == len(DEFAULT_LADDER_BUDGETS.tier2_tactics)  # every tactic tried
    assert all(a.status is AdjudicationStatus.UNKNOWN for a in result.attempts)  # never FAILED


# --- env-death recovery: scripted, deterministic --------------------------------------------


def test_env_death_recovers_and_env_id_is_carried_forward():
    budgets = LadderBudgets(
        tier2_tactics=(DEFAULT_LADDER_BUDGETS.tier2_tactics[0],),  # just `rfl`, for a short script
        retry_on_timeout_attempts=0,  # no extra run_checked-level retry -- isolate the recovery loop
        env_death_max_recovery_attempts=3,
    )
    script = [
        # rfl attempt against the dead env: run_checked with retries=0 sends exactly one call.
        LeanError(message="Unknown environment."),
        # recovery: warm_import succeeds on the first attempt, fresh env 42.
        CommandResponse(env=42, messages=[]),
        # retried rfl attempt against the recovered env -- succeeds this time.
        CommandResponse(env=43, messages=[]),
    ]
    server = _FakeServer(script)

    result = adjudicate_tier2(server, 1, "f1", "True", budgets)

    assert result.winning is not None
    assert result.env == 43  # the POST-declare env, not the recovered-but-pre-declare env 42


def test_env_death_recovery_exhausted_reports_env_death_status():
    budgets = LadderBudgets(
        tier2_tactics=(DEFAULT_LADDER_BUDGETS.tier2_tactics[0],),
        retry_on_timeout_attempts=0,
        env_death_max_recovery_attempts=2,
    )
    # `harness.repl.warm_import` hardcodes `retries=1` internally (unrelated to
    # `budgets.retry_on_timeout_attempts`), so each failed recovery attempt itself consumes
    # TWO scripted responses, not one.
    script = [
        LeanError(message="Unknown environment."),  # initial attempt dies
        LeanError(message="Unknown environment."),  # recovery attempt 1, warm_import's 1st try
        LeanError(message="Unknown environment."),  # recovery attempt 1, warm_import's retry
        LeanError(message="Unknown environment."),  # recovery attempt 2, warm_import's 1st try
        LeanError(message="Unknown environment."),  # recovery attempt 2, warm_import's retry
    ]
    server = _FakeServer(script)

    result = adjudicate_tier2(server, 1, "f1", "True", budgets)

    assert result.winning is None
    assert len(result.attempts) == 1
    assert result.attempts[0].status is AdjudicationStatus.ENV_DEATH
    assert result.env == 1  # unchanged -- caller gets the real (still-dead) state back, never poisoned silently
