"""Spend aggregation over `bedrock/output/call_log.jsonl` (2026-07-29). Reads the same
provenance log `bedrock.client.BedrockClient` writes; computes token totals and dollar
estimates using `bedrock.config`'s pricing constants. Pure aggregation -- no network calls,
no AWS access needed, works identically over the real log or a test fixture log.

Call-type classification is by system-prompt fingerprint (the same approach used ad hoc during
the 2026-07-29 audit session) -- each of the four contract calls
(`authoring/prompts/{classification,dossier,fact_proposal,round_trip}.txt`) has a distinctive
opening phrase in its rendered SYSTEM section, checked in `_CALL_TYPE_MARKERS` below. A call
whose system text matches none of them (e.g. the one-off `bedrock/real_roundtrip.py` smoke
test) is bucketed as `"other"`, not silently dropped.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

from bedrock import config as cfg

_CALL_TYPE_MARKERS = [
    ("classification", "classifying a Mathlib definition"),
    ("dossier", "writing the authoritative informal dossier"),
    ("fact_proposal", "proposing a fact suite"),
    ("round_trip", "given only a pinned Lean 4 signature"),
]


def _classify(system_text: str) -> str:
    for call_type, marker in _CALL_TYPE_MARKERS:
        if marker in system_text:
            return call_type
    return "other"


@dataclass(frozen=True)
class SpendTotals:
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def dollars(self) -> float:
        return (
            self.input_tokens / 1000 * cfg.PRICE_PER_1K_INPUT_TOKENS_USD
            + self.output_tokens / 1000 * cfg.PRICE_PER_1K_OUTPUT_TOKENS_USD
        )


@dataclass(frozen=True)
class SpendReport:
    total: SpendTotals
    by_call_type: dict[str, SpendTotals] = field(default_factory=dict)
    errored_calls: int = 0  # outcome != "success" -- no usage to count, tracked separately


def aggregate_spend(log_path: Path) -> SpendReport:
    """Never raises on a malformed line -- one bad log entry must not hide every other line's
    spend from the report; a line that fails to parse as JSON, or lacks the expected shape, is
    silently skipped (this is a reporting tool, not a validator of the log's own integrity)."""
    log_path = Path(log_path)
    if not log_path.exists():
        return SpendReport(total=SpendTotals())

    totals: dict[str, dict[str, int]] = {}
    grand = {"calls": 0, "input_tokens": 0, "output_tokens": 0}
    errored = 0

    with log_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("outcome") != "success":
                errored += 1
                continue
            usage = (record.get("response") or {}).get("usage") or {}
            tin = usage.get("input_tokens")
            tout = usage.get("output_tokens")
            if tin is None or tout is None:
                continue
            system_text = (record.get("request") or {}).get("system", "") or ""
            call_type = _classify(system_text)

            bucket = totals.setdefault(call_type, {"calls": 0, "input_tokens": 0, "output_tokens": 0})
            bucket["calls"] += 1
            bucket["input_tokens"] += tin
            bucket["output_tokens"] += tout
            grand["calls"] += 1
            grand["input_tokens"] += tin
            grand["output_tokens"] += tout

    by_call_type = {k: SpendTotals(**v) for k, v in totals.items()}
    return SpendReport(total=SpendTotals(**grand), by_call_type=by_call_type, errored_calls=errored)


def project_batch_cost(per_task_calls: dict[str, tuple[int, int]], n_tasks: int) -> SpendTotals:
    """`per_task_calls`: {call_type: (input_tokens, output_tokens)} for ONE task's worth of
    calls (e.g. the bounding patterns from a real run); scales linearly by `n_tasks`. Pure
    arithmetic, no log I/O -- separate from `aggregate_spend` since a projection isn't an
    aggregation of anything that's actually happened yet."""
    total_in = sum(tin for tin, _ in per_task_calls.values()) * n_tasks
    total_out = sum(tout for _, tout in per_task_calls.values()) * n_tasks
    total_calls = len(per_task_calls) * n_tasks
    return SpendTotals(calls=total_calls, input_tokens=total_in, output_tokens=total_out)
