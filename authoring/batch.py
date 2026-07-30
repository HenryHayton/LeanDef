"""General batch runner (2026-07-29), promoted from the batch-50 scratchpad session's
`run_batch_50.py`. Generalized to any name-list file -- no `BATCH_50` naming anywhere here;
the batch-50-specific list lives as data (`authoring/batches/batch_2026-07-29.txt`), not code.

Ported behavior: credential liveness check (`aws sts get-caller-identity`) before every chunk;
on failure, write a resume file listing unprocessed names and return with a distinct status
rather than raising (real spend already happened -- this is a normal, expected outcome, not
an error); carry-on mode within a chunk (`authoring.pipeline.author_batch`'s own contract: "a
failed task NEVER halts the batch"); one aggregate review across the whole run via the
existing `render_batch_review`.

New in this promotion: the batch refuses to start at all (before any Bedrock spend) unless
every name in the list has a `status: "pass"` entry in the given preflight JSON
(`authoring.preflight.run_preflight`'s output) AND is not curated out
(`miner/curation.yaml`, `action: exclude`) -- belt-and-braces on the curation check
specifically, since `harvest_manifest.jsonl` could in principle be stale relative to
`curation.yaml` (confirmed a real, if minor, instance of exactly that drift on 2026-07-29,
before this session's `miner/rank.py` re-run fixed it -- see that commit's report)."""

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from authoring.pipeline import PipelineConfig, TaskResult, _count_log_lines, author_task, render_batch_review
from authoring.rotation_queue import DEFAULT_QUEUE_PATH, append_rotation

DEFAULT_CHUNK_SIZE = 8


class BatchRefused(Exception):
    """Raised before any Bedrock spend when the batch cannot start at all -- missing/incomplete
    preflight coverage, or a curated-out name in the list. Distinct from a mid-batch credential
    expiry (`BatchRunResult.status == "credentials_expired"`), which DOES leave real spend
    behind and is reported as partial progress, never raised as an exception."""


@dataclass(frozen=True)
class BatchRunResult:
    results: list[TaskResult]
    status: str  # "completed" | "credentials_expired"
    review_path: Path | None
    resume_path: Path | None = None
    processed_names: list[str] = field(default_factory=list)
    unprocessed_names: list[str] = field(default_factory=list)


def load_name_list(names_file: Path) -> list[str]:
    """One name per line; blank lines and lines starting with '#' ignored."""
    names = []
    for line in Path(names_file).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        names.append(line)
    return names


def load_curated_out_names(curation_yaml_path: Path) -> set[str]:
    """Names with `action: exclude` in `miner/curation.yaml`."""
    import yaml

    data = yaml.safe_load(Path(curation_yaml_path).read_text(encoding="utf-8")) or {}
    return {e["name"] for e in data.get("entries", []) if e.get("action") == "exclude"}


def _default_credentials_alive() -> bool:
    try:
        proc = subprocess.run(
            ["aws", "sts", "get-caller-identity"], capture_output=True, timeout=15, text=True
        )
        return proc.returncode == 0
    except Exception:
        return False


def _validate_preflight_and_curation(
    names: list[str], preflight_path: Path, curation_yaml_path: Path | None
) -> None:
    if not preflight_path.exists():
        raise BatchRefused(f"no preflight file at {preflight_path} -- refusing to run without one")
    preflight_data = json.loads(preflight_path.read_text(encoding="utf-8"))

    missing_or_failed = [
        n for n in names
        if n not in preflight_data or preflight_data[n].get("status") != "pass"
    ]
    if missing_or_failed:
        raise BatchRefused(
            f"{len(missing_or_failed)} name(s) missing a passing preflight entry in {preflight_path}: "
            f"{missing_or_failed}"
        )

    if curation_yaml_path is not None and curation_yaml_path.exists():
        curated_out = load_curated_out_names(curation_yaml_path)
        blocked = [n for n in names if n in curated_out]
        if blocked:
            raise BatchRefused(
                f"{len(blocked)} name(s) are curated out in {curation_yaml_path} and must not "
                f"be run: {blocked}"
            )


def run_batch(
    names_file: Path,
    config: PipelineConfig,
    *,
    preflight_path: Path,
    curation_yaml_path: Path | None = None,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    resume_dir: Path | None = None,
    credentials_check: Callable[[], bool] = _default_credentials_alive,
    queue_path: Path = DEFAULT_QUEUE_PATH,
) -> BatchRunResult:
    """Refuses to start (`BatchRefused`, no spend) if `preflight_path` doesn't cover every name
    in `names_file` with a passing entry, or if `curation_yaml_path` is given and any name is
    curated out. Otherwise runs `names` in chunks of `chunk_size`, checking `credentials_check()`
    before every chunk; on a failed check, writes the unprocessed-names resume file into
    `resume_dir` (default: alongside `names_file`) and returns with
    `status="credentials_expired"` rather than continuing.

    **Rotation queue (2026-07-30)**: every `ROTATED` result gets one entry appended to
    `queue_path` (`authoring.rotation_queue.append_rotation`) -- the one mechanism, no manual
    bookkeeping (see that module's own docstring). `queue_path` is a parameter, not hardcoded,
    so tests can point it at a scratch file rather than the real
    `authoring/output/pending_safety_updates.json`."""
    names = load_name_list(names_file)
    _validate_preflight_and_curation(names, preflight_path, curation_yaml_path)

    resume_dir = resume_dir if resume_dir is not None else Path(names_file).parent
    all_results: list[TaskResult] = []
    processed: list[str] = []
    chunks = [names[i:i + chunk_size] for i in range(0, len(names), chunk_size)]

    for chunk in chunks:
        if not credentials_check():
            # Positional slice, not a membership filter: `processed` is always a PREFIX of
            # `names` (chunks run strictly in order), and `names` may contain duplicate entries
            # (a real 41-name batch shouldn't, but nothing here assumes uniqueness) -- a
            # membership filter would incorrectly drop every occurrence of a name that appears
            # more than once anywhere earlier in the list, not just the ones actually run.
            unprocessed = names[len(processed):]
            # Plain one-name-per-line, matching `load_name_list`'s own input format -- a resume
            # is just `run_batch(resume_path, ...)` again, no separate "resume mode" needed.
            resume_path = resume_dir / f"{Path(names_file).stem}_resume.txt"
            resume_path.parent.mkdir(parents=True, exist_ok=True)
            resume_path.write_text(
                f"# Resume file: unprocessed names from {names_file} after a credential check "
                f"failed mid-batch.\n" + "\n".join(unprocessed) + "\n",
                encoding="utf-8",
            )
            review_path = None
            if all_results:
                review_path = _write_partial_review(all_results, config)
            return BatchRunResult(
                results=all_results, status="credentials_expired", review_path=review_path,
                resume_path=resume_path, processed_names=list(processed), unprocessed_names=unprocessed,
            )

        for name in chunk:
            log_line_start = _count_log_lines(config.client.log_path)
            result = author_task(name, config)
            all_results.append(result)
            processed.append(name)
            if result.outcome == "ROTATED":
                log_line_end = _count_log_lines(config.client.log_path)
                append_rotation(
                    result, names_file, call_log_path=config.client.log_path,
                    log_line_start=log_line_start, log_line_end=log_line_end, queue_path=queue_path,
                )

    review_path = _write_partial_review(all_results, config)
    return BatchRunResult(
        results=all_results, status="completed", review_path=review_path,
        processed_names=list(processed), unprocessed_names=[],
    )


def _write_partial_review(results: list[TaskResult], config: PipelineConfig) -> Path:
    from datetime import UTC, datetime

    config.batch_review_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    path = config.batch_review_dir / f"batch_review_{timestamp}.md"
    path.write_text(render_batch_review(results), encoding="utf-8")
    return path
