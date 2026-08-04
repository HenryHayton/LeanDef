"""Persistence for candidate verdicts: one JSON file per scored sample.

Mirrors `prelim/store.py`'s contract exactly, for reasons that survived a real mid-run kill on
2026-08-04:

- **Atomic write** -- temp file in the same directory, then `os.replace`. A partially-written
  file can never be observed.
- **Parse-validated resume** -- `is_complete` is true iff the file exists AND parses as JSON AND
  carries the required keys. File existence alone is not enough; a truncated file that merely
  looks present must not be mistaken for finished work.
- **The filesystem IS the state.** No separate index, nothing to drift. This is also what makes
  the tree rsync-friendly: the box scores, you rsync down, and a re-run scores only what is
  missing regardless of which machine has which files.

Layout mirrors the samples tree one-for-one, so joining scores back to samples is a path
substitution rather than a lookup:

    scoring_output/scores/<model_slug>/<task_name>/sample_NN.json
"""

import json
import os
import tempfile
from pathlib import Path

from scoring import config as cfg

REQUIRED_KEYS = ("schema_version", "model_slug", "task_name", "sample_index", "fact_verdicts")


def verdict_path(model_slug: str, task_name: str, sample_index: int, *, scores_dir: Path | None = None) -> Path:
    root = scores_dir if scores_dir is not None else cfg.scores_dir()
    return Path(root) / model_slug / task_name / f"sample_{sample_index:02d}.json"


def write_verdict(record: dict, *, scores_dir: Path | None = None) -> Path:
    """Atomically write one verdict record. Returns the path."""
    path = verdict_path(
        record["model_slug"], record["task_name"], record["sample_index"], scores_dir=scores_dir
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=f".{path.stem}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise
    return path


def read_verdict(path: Path) -> dict | None:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def is_complete(
    model_slug: str,
    task_name: str,
    sample_index: int,
    *,
    scores_dir: Path | None = None,
    require_mechanisms: tuple[str, ...] = ("decide", "proof"),
) -> bool:
    """Exists AND parses AND has the required keys AND covers `require_mechanisms`.

    The mechanism clause exists because the run is deliberately split: Stage D scores decide
    facts over every candidate, Stage E fills in the proof facts later. Without it a Stage D
    record would satisfy every other test of doneness and Stage E would skip the very
    candidates it exists to finish -- silently, and looking exactly like a successful resume.

    A record whose candidate never reached the fact walk at all (inadmissible, or certified
    wholesale by the tier-4 equivalence path) is complete for EVERY mechanism: in the first case
    there is nothing further to attempt, in the second every fact already has a verdict.
    """
    record = read_verdict(verdict_path(model_slug, task_name, sample_index, scores_dir=scores_dir))
    if record is None:
        return False
    if not all(key in record for key in REQUIRED_KEYS):
        return False
    attempted = set(record.get("mechanisms_attempted") or [])
    return set(require_mechanisms) <= attempted


def iter_verdicts(*, scores_dir: Path | None = None):
    """Every parseable verdict record under the tree. Unparseable files are skipped rather than
    raised on -- a scoring run in progress may be mid-write, and a reader must never crash on
    that."""
    root = scores_dir if scores_dir is not None else cfg.scores_dir()
    root = Path(root)
    if not root.exists():
        return
    for path in sorted(root.rglob("sample_*.json")):
        record = read_verdict(path)
        if record is not None:
            yield record
