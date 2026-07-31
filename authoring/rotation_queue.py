"""The rotation cleanup queue (2026-07-30): `authoring/output/pending_safety_updates.json`.

Every time a task ROTATES out of a batch, `append_rotation` writes one entry carrying enough
context that a repair attempt (`authoring.cleanup`) or a human reviewer never has to re-derive
what happened from scratch: the exact rotation stage/reason, pointers into the call log and any
task directory that exists, the rejected dossier text itself (for the categories where a
dossier revision is the fix), and a `category` classifying whether an authoring-side repair
could plausibly help at all.

**One mechanism, no manual bookkeeping**: `authoring.batch.run_batch` calls `append_rotation`
itself, once, right after `author_task` returns a `ROTATED` result -- nothing else in this
codebase should ever hand-construct a queue entry for a live run. The one exception is
retroactive backfill from a run that predates this module (a real, documented, one-off need --
see `authoring/batches/`'s own retroactive-population script for the 2026-07-30 batch, not
part of this module).

**`category`** (`AGENT_FIXABLE` | `NOT_AGENT_FIXABLE`) is a closed, conservative classification:
only `dossier_consistency` rotations (dossier-leak, signature-substring, worked-example checks)
and `round_trip_scoring` rotations whose failure is genuinely a COMPILE exhaustion (never a
fact-suite failure -- see `classify_rotation`'s own docstring for why that distinction is
load-bearing) are `AGENT_FIXABLE`. Everything else -- `truth_splice` failures (harness/REPL
bugs, no dossier revision can fix a termination-checker error or an "Unknown environment"
crash), `classification`/`fact_proposal`/`mechanical_validation`/`emit` rotations, and any
round-trip fact-suite failure -- defaults to `NOT_AGENT_FIXABLE`. Misclassifying something as
fixable wastes repair-loop spend chasing a harness bug no dossier revision touches;
misclassifying the other way just leaves it for human triage. The conservative default is
deliberate.
"""

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

AGENT_FIXABLE = "agent_fixable"
NOT_AGENT_FIXABLE = "not_agent_fixable"

STATUS_PENDING = "pending"
STATUS_REPAIRED_AND_SHIPPED = "repaired_and_shipped"
STATUS_ESCALATE_TO_HUMAN = "escalate_to_human"
STATUS_BLOCKED_ON_HARNESS = "blocked_on_harness"

DEFAULT_QUEUE_PATH = Path(__file__).resolve().parent / "output" / "pending_safety_updates.json"

_DOSSIER_CALL_MARKER = "You are writing the authoritative informal dossier"
_JSON_FENCE_RE = re.compile(r"^```(?:json)?\s*\n(.*?)\n```\s*$", re.DOTALL)


def classify_rotation(stage: str | None, reason: str) -> str:
    """`stage`/`reason` are `TaskResult.rotated_at_stage` and the terminal `StageRecord.detail`.
    See module docstring for the classification rule and why a round-trip fact-suite failure
    (as opposed to a compile exhaustion) is deliberately excluded from `AGENT_FIXABLE`: a
    fact-suite failure's "fix" would mean showing the repair call fact-validation outcomes,
    which the guardrails (`authoring.cleanup`'s own docstring) forbid -- there is no
    guardrail-compliant way to make that category agent-fixable, so it isn't.

    **`mechanical_validation` flipped to `AGENT_FIXABLE` (31 July 2026).** Its original
    conservative default rested on the assumption that "no facts survived" meant the model's
    mathematics was wrong -- unfixable by a dossier revision. That assumption died with the
    `validate_global_fact` ERRORED-conflation fix: the verdict was frequently produced by REPL
    death (and, separately, by the raw-name matcher rejecting 100% of facts for referencing the
    task symbol), not by bad mathematics. Confirmed live: `Multiset.Pi.cons` carried this
    verdict, was reclassified by hand, and shipped on the first repair attempt. The repair loop
    still cannot loop blind on it -- `authoring.cleanup._feedback_text` returns None for this
    stage, so it gets exactly ONE fresh attempt and then escalates rather than iterating on
    feedback the guardrails forbid."""
    if stage in ("dossier_consistency", "mechanical_validation"):
        return AGENT_FIXABLE
    if stage == "round_trip_scoring" and reason.strip().startswith("exhausted"):
        return AGENT_FIXABLE
    return NOT_AGENT_FIXABLE


@dataclass
class RepairLogEntry:
    attempt_n: int
    what_was_changed: str
    check_result: str
    error_if_any: str | None = None


@dataclass
class QueueEntry:
    name: str
    batch: str
    rotation_stage: str | None
    rotation_reason: str
    category: str
    artifacts: dict = field(default_factory=dict)
    repair_log: list[dict] = field(default_factory=list)
    status: str = STATUS_PENDING

    def to_dict(self) -> dict:
        return asdict(self)


def _extract_call_text(record: dict) -> str:
    resp = record.get("response") or {}
    return "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")


def _strip_fence(text: str) -> str:
    text = text.strip()
    m = _JSON_FENCE_RE.match(text)
    return m.group(1).strip() if m else text


def find_rejected_dossier_md(call_log_path: Path, line_start: int, line_end: int) -> str | None:
    """Scan `call_log.jsonl` lines `[line_start, line_end)` (0-based, half-open -- the exact
    range one task's calls occupy) for the LAST dossier-call response in that range and return
    its `dossier_md` text, or `None` if no dossier call was ever made (e.g. a `truth_splice`
    rotation, which never reaches the dossier call at all). The last one, not the first: with
    the pipeline's own one-shot repair cycle, a dossier-consistency rotation's rejected dossier
    is the SECOND (retried) attempt, not the first draft."""
    if not call_log_path.exists():
        return None
    found: str | None = None
    with call_log_path.open(encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i < line_start or i >= line_end or not line.strip():
                continue
            record = json.loads(line)
            if record.get("outcome") != "success":
                continue
            system_text = (record.get("request") or {}).get("system", "") or ""
            if _DOSSIER_CALL_MARKER not in system_text:
                continue
            try:
                payload = json.loads(_strip_fence(_extract_call_text(record)))
            except json.JSONDecodeError:
                continue
            dossier_md = payload.get("dossier_md")
            if isinstance(dossier_md, str):
                found = dossier_md
    return found


def load_queue(path: Path = DEFAULT_QUEUE_PATH) -> list[dict]:
    if not Path(path).exists():
        return []
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_queue(entries: list[dict], path: Path = DEFAULT_QUEUE_PATH) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")


def append_rotation(
    result, batch_name: str, *,
    call_log_path: Path, log_line_start: int, log_line_end: int,
    queue_path: Path = DEFAULT_QUEUE_PATH,
) -> QueueEntry:
    """`result`: a `TaskResult` with `outcome == "ROTATED"`. Builds and appends one queue entry,
    persisting the queue file immediately (append-durable, not batched in memory -- a crash
    mid-batch must not lose already-recorded rotations)."""
    stage = result.rotated_at_stage
    reason = result.stage_records[-1].detail if result.stage_records else ""
    category = classify_rotation(stage, reason)
    dossier_md = find_rejected_dossier_md(call_log_path, log_line_start, log_line_end)
    entry = QueueEntry(
        name=result.definition_name,
        batch=str(batch_name),
        rotation_stage=stage,
        rotation_reason=reason,
        category=category,
        artifacts={
            "task_dir": str(result.task_dir) if result.task_dir else None,
            "call_log_lines": [log_line_start, log_line_end],
            "stage_records": [
                {"stage": sr.stage, "status": sr.status, "detail": sr.detail} for sr in result.stage_records
            ],
            "rejected_dossier_md": dossier_md,
        },
    )
    entries = load_queue(queue_path)
    entries.append(entry.to_dict())
    save_queue(entries, queue_path)
    return entry
