"""Tier 3 -- hammer (reward doc §3: LeanHammer, the fact's anchor theorems as explicit
premises). Runs only on the EC2 box (`docs/ec2_runbook.md`): x86 (bundled Zipperposition ATP
binary), large memory (premise-selection spikes >30GB), and a Hammer-enabled Lean project
(`~/verifier-lean` on the box, distinct from the Mac's plain `lean/` project -- see the
runbook's Phase G).

**The --load-dynlib resolution** (`docs/deferred.md`, fired this session): `hammer`'s cvc5/SMT
route needs `libcvc5_cvc5.so`'s symbols loaded into the interpreter or the whole process
SIGABRTs (`docs/ec2_runbook.md` Phase C.7). `lean --load-dynlib=path` does this for a plain
`lake env lean` invocation, but `lean_interact.server.LeanServer.start()` launches the REPL
binary directly with a hardcoded argv (`[lake_path, "env", repl_binary_path]`, no room for
extra flags) -- and even if it could pass extra argv, the REPL project's own `main` discards
its `args` parameter entirely (confirmed by reading `REPL/Main.lean` itself, not assumed). No
CLI-flag injection path exists through LeanInteract.

The actual fix, empirically verified this session (`Monotone (fun n => n + 1) := by hammer` --
the exact goal that historically SIGABRTed per the runbook -- completed cleanly, no crash,
driven from Python): a patched local REPL checkout (`lean/repl_main.ec2.lean`, deployed to
`~/patched-repl` on the box per the runbook's Phase G) whose `main` calls `Lean.loadDynlib`
directly -- the same primitive `lean --load-dynlib` itself calls internally
(`Lean/Shell.lean`'s `'l'` case) -- reading the path from the `LEAN_INTERACT_LOAD_DYNLIB`
environment variable. The caller sets that variable (`os.environ`, inherited by the REPL
subprocess automatically) and constructs `LeanREPLConfig(local_repl_path=".../patched-repl",
build_repl=False, ...)` before this module's functions are ever called -- this module does not
construct servers itself, matching every other tier (`ladder.tier1`/`ladder.tier2` also just
take an already-constructed `server`/`env`).

**Reliability**: reuses `ladder.tier2`'s env-death marker detection and budgeted recovery loop
directly (`_looks_like_env_death`, `_recover_environment` -- both already tactic-agnostic, nothing
tier-2-specific about them) rather than duplicating that logic a second time; only the
run-once/retry-once-after-recovery glue is re-adapted locally, mirroring
`ladder.tier2._run_tactic_with_recovery`'s own shape, per this codebase's established
convention of small, local copy-adapts over cross-module reaching for private helpers.

**Cached script must not itself be `by hammer`.** Caching the literal tactic invocation would
mean replay re-runs hammer's whole ATP search again -- on the Mac, `hammer` isn't even
importable, so replay would just fail outright -- defeating "search happens once, every
re-encounter is replay" (reward doc §3.2) for the one tier that most needs it. `hammer`
itself emits a concrete, directly-substitutable suggestion as an info message on success
(confirmed empirically, box session: `'Try this:\n\n  [apply]     intro a b\n    apply
Nat.add_comm'` -- the same "Try this: <replacement>" convention `exact?`/`apply?` use,
`[apply]`/`[cvc5]`/etc. tagging which solver found it). `_parse_hammer_suggestion` extracts
the replacement tactic block; the caller then VERIFIES it independently (a fresh `example :
... := by\n  <parsed>` check) before trusting it as `winning_script` -- a parse that looks
plausible but reconstructs wrong (a formatting edge case, a solver-specific syntax quirk) must
not silently poison the cache. Falls back to caching `by hammer` itself (still functionally
correct for the CURRENT run's CERTIFIED status, which only needs the already-declared
theorem in the current environment, not a portable script) if parsing or verification fails,
logged in the attempt's `detail` -- degraded portability, not a wrong answer.
"""

import re

from lean_interact import AutoLeanServer, Command

from harness.repl import run_checked
from harness.results import CheckStatus
from ladder.budgets import LadderBudgets
from ladder.statuses import AdjudicationStatus, TierAttempt
from ladder.tier2 import _looks_like_env_death, _recover_environment, _safe_theorem_name

_TRY_THIS_RE = re.compile(r"Try this:\s*\n\n(.*)", re.DOTALL)
_CATEGORY_TAG_RE = re.compile(r"^\s*\[\w+\]\s*")


def _parse_hammer_suggestion(message_data: str) -> str | None:
    """Extracts hammer's suggested replacement tactic block from a `Try this:` info message.
    Returns `None` if the message doesn't match the expected shape -- the caller treats that as
    "could not reconstruct a portable script," never guesses."""
    m = _TRY_THIS_RE.search(message_data)
    if m is None:
        return None
    lines = [ln for ln in m.group(1).splitlines() if ln.strip()]
    if not lines:
        return None
    lines[0] = _CATEGORY_TAG_RE.sub("", lines[0])
    cleaned = [ln.strip() for ln in lines]
    return "by\n  " + "\n  ".join(cleaned)


def _reconstruct_portable_script(server: AutoLeanServer, env: int, canonical_statement: str, check, budgets: LadderBudgets) -> str | None:
    """`check` is the PASSED result of the winning hammer command. Returns a verified,
    hammer-free replacement script, or `None` if no suggestion could be parsed or the
    reconstruction doesn't independently verify."""
    raw = check.raw_response
    if raw is None:
        return None
    for message in raw.messages:
        if message.severity != "info":
            continue
        parsed = _parse_hammer_suggestion(message.data)
        if parsed is None:
            continue
        verify_cmd = f"example : {canonical_statement} := {parsed}"
        verify_check = run_checked(server, Command(cmd=verify_cmd, env=env), timeout=budgets.tier1_timeout_s)
        if verify_check.status is CheckStatus.PASSED:
            return parsed
    return None


def _hammer_command(theorem_name: str, canonical_statement: str, anchors: list[str]) -> str:
    premises = f" [{', '.join(anchors)}]" if anchors else ""
    return f"theorem {theorem_name} : {canonical_statement} := by hammer{premises}"


class Tier3Result:
    """Mirrors `ladder.tier2.Tier2Result`'s shape (same attribute names) so
    `ladder.adjudicate`'s loop can treat a winning tier-2 or tier-3 result identically --
    `winning_theorem_name` is the already-declared theorem the axiom audit inspects directly,
    no second search."""

    def __init__(self, attempts: list[TierAttempt], winning: TierAttempt | None, winning_theorem_name: str | None, winning_script: str | None, env: int):
        self.attempts = attempts
        self.winning = winning
        self.winning_theorem_name = winning_theorem_name
        self.winning_script = winning_script
        self.env = env


def adjudicate_tier3_hammer(
    server: AutoLeanServer,
    env: int,
    fact_id: str,
    canonical_statement: str,
    anchors: list[str],
    budgets: LadderBudgets,
    *,
    imports: list[str] | None = None,
) -> Tier3Result:
    """Attempts `canonical_statement` via `hammer`, citing `anchors` as explicit premises when
    given. One attempt (hammer is not a ladder of alternatives the way tier 2 is), budgeted at
    `budgets.tier3_wall_clock_s` with `budgets.retry_on_timeout_attempts` retries on the
    underlying `run_checked` call (the same variance-driven retry policy every tier uses --
    `docs/ec2_runbook.md`'s own 60s-timeout-then-6.5s-repeat finding). Env-death gets the same
    budgeted recovery loop as tier 2, then one retry against the recovered environment; if
    recovery is exhausted, reports ENV_DEATH and returns the caller's original (possibly still
    dead) `env` unchanged -- never silently stranding the caller on unrecoverable state."""
    theorem_name = _safe_theorem_name(fact_id, "hammer")
    cmd = _hammer_command(theorem_name, canonical_statement, anchors)

    check = run_checked(server, Command(cmd=cmd, env=env), timeout=budgets.tier3_wall_clock_s, retries=budgets.retry_on_timeout_attempts)

    if _looks_like_env_death(check.detail):
        recovered_env = _recover_environment(server, imports, budgets)
        if recovered_env is None:
            attempt = TierAttempt(tier=3, tactic="hammer", status=AdjudicationStatus.ENV_DEATH, elapsed_s=check.elapsed_s, detail=check.detail)
            return Tier3Result([attempt], None, None, None, env)
        env = recovered_env
        check = run_checked(server, Command(cmd=cmd, env=env), timeout=budgets.tier3_wall_clock_s, retries=budgets.retry_on_timeout_attempts)
        if _looks_like_env_death(check.detail):
            attempt = TierAttempt(tier=3, tactic="hammer", status=AdjudicationStatus.ENV_DEATH, elapsed_s=check.elapsed_s, detail=check.detail)
            return Tier3Result([attempt], None, None, None, env)

    if check.status is CheckStatus.PASSED:
        status = AdjudicationStatus.CERTIFIED
        if check.env is not None:  # the declare command opened a NEW env -- see ladder.tier2's
            env = check.env         # own fix for this exact class of bug (Session A).
    elif check.status is CheckStatus.FAILED:
        # hammer failing to close the goal is not evidence the goal is false (reward doc §2.3,
        # same rule as every tier-2 tactic) -- UNKNOWN for this attempt, never FAILED.
        status = AdjudicationStatus.UNKNOWN
    else:
        status = AdjudicationStatus.ERRORED

    detail = check.detail
    if status is AdjudicationStatus.CERTIFIED:
        portable_script = _reconstruct_portable_script(server, env, canonical_statement, check, budgets)
        if portable_script is None:
            portable_script = "by hammer" + (f" [{', '.join(anchors)}]" if anchors else "")
            detail = "could not reconstruct a hammer-free replay script; cached script re-invokes hammer (not Mac-replayable)"
        attempt = TierAttempt(tier=3, tactic="hammer", status=status, elapsed_s=check.elapsed_s, detail=detail)
        return Tier3Result([attempt], attempt, theorem_name, portable_script, env)

    attempt = TierAttempt(tier=3, tactic="hammer", status=status, elapsed_s=check.elapsed_s, detail=detail)
    return Tier3Result([attempt], None, None, None, env)
