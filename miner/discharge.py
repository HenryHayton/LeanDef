"""Tier-2 discharge measurement: for each eligible definition with `theorem_mention_count >=
1`, sample up to `DISCHARGE_SAMPLE_SIZE` of its mentioning theorem statements and attempt to
prove each against the *true* definition with a deterministic tactic ladder
(`miner.config.TACTIC_LADDER`), under a pinned per-attempt budget
(`miner.config.DISCHARGE_TACTIC_TIMEOUT`).

**This is a measurement, not a gate** (per the task that introduced this module): nothing here
excludes a candidate or changes its score. Results are written to their own output file
(`miner/output/discharge_manifest.jsonl`) and summarized in a dedicated report section --
deliberately kept out of `miner.rank.ManifestRecord`/`build_manifest` so this module is purely
additive: it reads an already-built eligible set and a warm REPL environment, and touches
nothing about how either was produced.

Reuses `miner.scan.scan_theorem_statements_with_namespace` and the exact same qualified-name-
or-matching-namespace-bare-name matching rule `miner.harvest.compute_theorem_mention_counts`
uses (see that function's docstring) -- this module does its own full-Mathlib statement scan
rather than threading the one `compute_theorem_mention_counts` already did through `harvest()`,
trading a second cheap (~17s, per docs/harvest_review_batch3.md §0) full-tree scan for keeping
`compute_theorem_mention_counts`'s existing signature and tests untouched.

Sampling is deterministic, not random: the first `DISCHARGE_SAMPLE_SIZE` matching statements in
file-sorted scan order, so re-running the measurement against the same corpus reproduces the
same sample.

`measure_discharge`'s `max_wall_clock_s` is a hard-won addition, not a speculative one: the
batch-4 run's first attempt, at the task-suggested 30s-per-tactic budget, ran past 7 hours
without finishing a 727-definition corpus. `DISCHARGE_TACTIC_TIMEOUT` was lowered afterward
(see `miner.config`'s comment) and this wall-clock cap was added so a slow corpus degrades to
"measured a smaller prefix, clearly reported as such" rather than "ran indefinitely."
"""

import json
import re
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path

from lean_interact import AutoLeanServer, Command

from harness.repl import run_checked, warm_import
from harness.results import CheckStatus
from miner import config as miner_cfg
from miner.rank import ManifestRecord
from miner.scan import scan_theorem_statements_with_namespace

# Environment-death recovery (see `_attempt_statement_with_recovery`'s docstring): the same
# marker-text detection `miner.verify._looks_like_env_death` uses, duplicated rather than
# imported -- that function is a private implementation detail of a different module's
# recovery path, and this codebase's own convention (see `miner.verify`'s axiom-message parser,
# duplicated from `harness.admissibility` for the same reason) is to copy small private
# detectors like this rather than reach across a module boundary for them.
_ENV_DEATH_MARKERS = ("Unknown environment", "unknown environment")


def _looks_like_env_death(detail: str) -> bool:
    return any(marker in detail for marker in _ENV_DEATH_MARKERS)


@dataclass(frozen=True)
class TacticAttempt:
    tactic: str
    status: str  # "discharged" | "not_discharged" | "errored"
    elapsed_s: float
    detail: str = ""


@dataclass(frozen=True)
class StatementDischarge:
    """The ladder's outcome for one sampled mentioning statement. `attempts` stops at the
    first `"discharged"` result -- the ladder tries tactics in order and takes the first
    success, so a statement discharged by `rfl` never also gets an `omega` attempt logged."""

    statement: str
    attempts: list[TacticAttempt]
    discharged: bool
    winning_tactic: str | None


@dataclass
class DefinitionDischarge:
    """The discharge outcome for one eligible definition: how many of its sampled mentioning
    statements were discharged, and by which tactic. `statements_sampled` and `attempted` can
    differ from `len(per_statement)` only if they're equal -- kept as separate fields (rather
    than derived) so the manifest line is self-describing without recomputing from
    `per_statement`."""

    name: str
    theorem_mention_count: int
    statements_sampled: int
    attempted: int
    discharged: int
    winning_tactic_counts: dict[str, int] = field(default_factory=dict)
    per_statement: list[StatementDischarge] = field(default_factory=list)


def scan_all_theorem_statements(mathlib_root: Path) -> list[tuple[str, str]]:
    """Every `(statement_text, namespace_prefix)` pair in Mathlib, full-tree -- the same scan
    `miner.harvest.compute_theorem_mention_counts` does internally, exposed here as its own
    function so this module doesn't need that function to change shape to reuse its data."""
    statement_records: list[tuple[str, str]] = []
    for path in sorted(mathlib_root.rglob("*.lean")):
        statement_records.extend(scan_theorem_statements_with_namespace(path.read_text(encoding="utf-8")))
    return statement_records


def find_mentioning_statements(name: str, statement_records: list[tuple[str, str]]) -> list[str]:
    """Every statement text that counts as a mention of `name`, in scan order -- qualified name
    anywhere, or bare name from within a matching namespace (identical rule to
    `miner.harvest.compute_theorem_mention_counts`; see that function's docstring for why the
    bare-name match is namespace-scoped rather than unscoped)."""
    parts = name.split(".")
    bare = parts[-1]
    namespace_prefix = ".".join(parts[:-1])
    matches = []
    for statement_text, statement_namespace in statement_records:
        if name in statement_text:
            matches.append(statement_text)
        elif namespace_prefix and statement_namespace == namespace_prefix and bare in statement_text:
            matches.append(statement_text)
    return matches


_THEOREM_HEADER_RE = re.compile(r"^(?:private\s+|protected\s+)*(?:theorem|lemma)\s+[A-Za-z_][A-Za-z0-9_'!?.]*")


def _as_example(statement: str) -> str:
    """Rewrite `statement` into a fresh, anonymous `example ... : ...` goal.

    `miner.scan.scan_theorem_statements_with_namespace` (what `find_mentioning_statements`
    actually returns in production) extracts the *whole* theorem header -- `"theorem NAME
    (binders) : TYPE"` -- not a bare proposition, since binders declared between the name and
    the final `:` are part of the statement and must stay in scope. Reusing the original name
    would collide with the real theorem (already proved, under that exact name, in this same
    pinned environment) rather than posing a fresh goal, so the `theorem`/`lemma` keyword and
    name are replaced with anonymous `example`, keeping every binder and the type verbatim. A
    bare proposition with no such header (as used directly in this module's own unit tests) is
    wrapped the simple way instead -- both shapes are valid input to this function.
    """
    stripped = statement.strip()
    match = _THEOREM_HEADER_RE.match(stripped)
    if match is not None:
        return "example" + stripped[match.end() :]
    return f"example : {statement}"


def attempt_statement(
    server: AutoLeanServer,
    env: int,
    statement: str,
    *,
    tactics: list[str] | None = None,
    timeout: float | None = None,
) -> StatementDischarge:
    """Try each tactic in the ladder, in order, against `statement` as a fresh goal in the
    pinned environment; stop at the first that discharges it. A statement extracted standalone
    (outside its original file's `variable`/`open`/section context) may fail to even elaborate
    as a goal at all -- that surfaces here as every tactic coming back `"not_discharged"` or
    `"errored"`, not a crash, and is exactly the kind of context-loss caveat flagged in the
    batch-4 report rather than special-cased in code."""
    tactics = tactics if tactics is not None else miner_cfg.TACTIC_LADDER
    timeout = timeout if timeout is not None else miner_cfg.DISCHARGE_TACTIC_TIMEOUT
    example_goal = _as_example(statement)
    attempts: list[TacticAttempt] = []
    for tactic in tactics:
        cmd = f"{example_goal} := by {tactic}"
        result = run_checked(server, Command(cmd=cmd, env=env), timeout=timeout)
        if result.status is CheckStatus.PASSED:
            attempts.append(TacticAttempt(tactic=tactic, status="discharged", elapsed_s=result.elapsed_s))
            return StatementDischarge(statement=statement, attempts=attempts, discharged=True, winning_tactic=tactic)
        status = "errored" if result.status is CheckStatus.ERRORED else "not_discharged"
        attempts.append(TacticAttempt(tactic=tactic, status=status, elapsed_s=result.elapsed_s, detail=result.detail))
    return StatementDischarge(statement=statement, attempts=attempts, discharged=False, winning_tactic=None)


def _attempt_statement_with_recovery(
    server: AutoLeanServer,
    env: int,
    statement: str,
    *,
    tactics: list[str] | None,
    timeout: float | None,
    imports: list[str] | None,
    warmup_timeout: float | None,
) -> tuple[StatementDischarge, int]:
    """Like `attempt_statement`, but detects a dead shared environment (any attempt erroring
    with an "Unknown environment" signature) and recovers by reimporting once, then retrying
    the *whole statement* against the fresh environment -- same granularity
    `miner.verify.verify_all_with_recovery` uses (retry the whole unit, not a sub-step), and
    for the same reason this measurement needed it in practice: a single slow `aesop`/`exact?`
    call across 727 definitions' worth of statements is exactly the kind of long batch that
    hit this failure mode during the real batch-4 run (confirmed there: the shared environment
    died after only 9 of 727 definitions, and every subsequent attempt failed with "Unknown
    environment" for the rest of the run, since nothing recovered it -- see the batch-4 report
    for the fix and the re-measured numbers). Returns `(result, current_env)` so the caller
    carries the possibly-refreshed environment id forward to the next statement.
    """
    result = attempt_statement(server, env, statement, tactics=tactics, timeout=timeout)
    if any(_looks_like_env_death(a.detail) for a in result.attempts):
        reimport = warm_import(server, imports=imports, timeout=warmup_timeout)
        if reimport.status is CheckStatus.PASSED:
            env = reimport.env
            result = attempt_statement(server, env, statement, tactics=tactics, timeout=timeout)
    return result, env


def measure_discharge_for_definition(
    server: AutoLeanServer,
    env: int,
    name: str,
    theorem_mention_count: int,
    statement_records: list[tuple[str, str]],
    *,
    sample_size: int | None = None,
    tactics: list[str] | None = None,
    timeout: float | None = None,
    imports: list[str] | None = None,
    warmup_timeout: float | None = None,
) -> tuple[DefinitionDischarge, int]:
    """Returns `(result, current_env)` -- see `_attempt_statement_with_recovery` for why the
    environment id can change mid-measurement and must be carried forward by the caller."""
    sample_size = sample_size if sample_size is not None else miner_cfg.DISCHARGE_SAMPLE_SIZE
    sampled = find_mentioning_statements(name, statement_records)[:sample_size]
    result = DefinitionDischarge(
        name=name,
        theorem_mention_count=theorem_mention_count,
        statements_sampled=len(sampled),
        attempted=0,
        discharged=0,
    )
    for statement in sampled:
        outcome, env = _attempt_statement_with_recovery(
            server, env, statement, tactics=tactics, timeout=timeout, imports=imports, warmup_timeout=warmup_timeout
        )
        result.attempted += 1
        result.per_statement.append(outcome)
        if outcome.discharged:
            result.discharged += 1
            tactic = outcome.winning_tactic
            result.winning_tactic_counts[tactic] = result.winning_tactic_counts.get(tactic, 0) + 1
    return result, env


def measure_discharge(
    server: AutoLeanServer,
    env: int,
    eligible_records: list[ManifestRecord],
    theorem_mention_counts: dict[str, int],
    statement_records: list[tuple[str, str]],
    *,
    sample_size: int | None = None,
    tactics: list[str] | None = None,
    timeout: float | None = None,
    imports: list[str] | None = None,
    warmup_timeout: float | None = None,
    max_wall_clock_s: float | None = None,
    on_progress: Callable[[int, int, DefinitionDischarge], None] | None = None,
) -> list[DefinitionDischarge]:
    """Measure discharge for every eligible record whose `theorem_mention_count >= 1`, in
    manifest order. Records with a zero mention count are skipped entirely (there is nothing
    to sample) rather than producing a zero-attempt row -- the corpus-wide discharge rate this
    feeds is over "definitions with supply to test," not the whole eligible set.

    Carries one environment id across the whole call, refreshing it via
    `_attempt_statement_with_recovery` whenever the shared environment dies partway through --
    without this, one death poisons every definition measured after it with cascading "Unknown
    environment" errors (exactly what happened in the batch-4 run before this fix).

    `max_wall_clock_s` (default `miner.config.DISCHARGE_MAX_WALL_CLOCK_S`, an 8-hour overnight
    budget): once elapsed, stops after whichever definition is in progress rather than
    continuing indefinitely -- a full-corpus run at the old 30s-per-tactic budget took over 7
    hours without finishing, so an unbounded run is a real, not hypothetical, risk. Definitions
    beyond the cutoff are simply not in the returned list; the caller reports `len(results)`
    against the number eligible so a partial run is legible, not silently mistaken for a
    complete one. `on_progress`, if given, is called after every definition
    `(index, total, result)` -- purely for the caller's own logging (this module does no I/O
    of its own beyond the final `write_discharge_manifest`)."""
    max_wall_clock_s = max_wall_clock_s if max_wall_clock_s is not None else miner_cfg.DISCHARGE_MAX_WALL_CLOCK_S
    deadline = time.monotonic() + max_wall_clock_s
    to_measure = [r for r in eligible_records if theorem_mention_counts.get(r.name, 0) >= 1]

    results = []
    for i, record in enumerate(to_measure, start=1):
        count = theorem_mention_counts[record.name]
        result, env = measure_discharge_for_definition(
            server, env, record.name, count, statement_records,
            sample_size=sample_size, tactics=tactics, timeout=timeout,
            imports=imports, warmup_timeout=warmup_timeout,
        )
        results.append(result)
        if on_progress is not None:
            on_progress(i, len(to_measure), result)
        if time.monotonic() >= deadline:
            break
    return results


def write_discharge_manifest(results: list[DefinitionDischarge], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for result in results:
            f.write(json.dumps(asdict(result), ensure_ascii=False))
            f.write("\n")


DEFAULT_DISCHARGE_OUTPUT_PATH = Path(__file__).resolve().parent / "output" / "discharge_manifest.jsonl"
