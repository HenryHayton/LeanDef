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

import dataclasses
import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from lean_interact import AutoLeanServer

from authoring.pipeline import PipelineConfig, TaskResult, _count_log_lines, author_task, render_batch_review
from authoring.rotation_queue import DEFAULT_QUEUE_PATH, append_rotation
from harness.repl import is_unknown_environment_error

DEFAULT_CHUNK_SIZE = 8


class BatchRefused(Exception):
    """Raised before any Bedrock spend when the batch cannot start at all -- missing/incomplete
    preflight coverage, or a curated-out name in the list. Distinct from a mid-batch credential
    expiry (`BatchRunResult.status == "credentials_expired"`), which DOES leave real spend
    behind and is reported as partial progress, never raised as an exception."""


@dataclass(frozen=True)
class BatchRunResult:
    results: list[TaskResult]
    status: str  # "completed" | "credentials_expired" | "repl_unrecoverable"
    review_path: Path | None
    resume_path: Path | None = None
    processed_names: list[str] = field(default_factory=list)
    unprocessed_names: list[str] = field(default_factory=list)
    # REPL-death recoveries (2026-07-31): {"name": str, "input_tokens": int, "output_tokens": int}
    # per dead attempt written off and retried -- visibility into spend that happened but whose
    # TaskResult was superseded by a successful retry, so it's not silently invisible, without
    # double-counting the name in `results`/`processed_names`.
    repl_recoveries: list[dict] = field(default_factory=list)


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


def _write_resume_file(
    names_file: Path, resume_dir: Path, unprocessed: list[str], reason: str,
) -> Path:
    resume_path = resume_dir / f"{Path(names_file).stem}_resume.txt"
    resume_path.parent.mkdir(parents=True, exist_ok=True)
    resume_path.write_text(
        f"# Resume file: unprocessed names from {names_file} after {reason}.\n" + "\n".join(unprocessed) + "\n",
        encoding="utf-8",
    )
    return resume_path


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
    repl_warmup: Callable[[], tuple[AutoLeanServer, int]] | None = None,
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
    `authoring/output/pending_safety_updates.json`.

    **REPL death recovery (2026-07-31), `repl_warmup`**: a zero-argument callable returning a
    fresh `(server, base_env)` (typically `lambda: get_warm_environment(max_total_memory=0.95)`)
    -- OPTIONAL, `None` by default, so existing callers (and every test sharing one warm
    `mathlib_env` fixture across many cases) are unaffected; a real production batch run should
    always supply it. Three layers, all gated on `repl_warmup is not None`:
    - **Prevent**: the server is killed and re-warmed at the start of every chunk (a real
      Mathlib re-import, ~1 min -- capping the memory growth a long-running server accumulates
      before it dies on its own).
    - **Detect**: `harness.repl.is_unknown_environment_error` reads a rotated result's terminal
      stage-record detail -- Lean's own "Unknown environment" text, the signature of a server
      that died and silently restarted mid-task (every environment id it held is gone).
    - **Recover**: on detection, re-warm (up to twice, since the first re-warm attempt can
      itself land on a still-unhealthy process) and retry the SAME name once, fresh, against
      the new environment; the dead attempt's real spend is not hidden (`repl_recoveries` on the
      returned `BatchRunResult`) but its `TaskResult` is superseded, not double-counted in
      `results`. Two consecutive re-warm failures stop the batch cleanly (`status=
      "repl_unrecoverable"`, a resume file) -- a real machine problem, not a blip worth costing
      more names to discover."""
    names = load_name_list(names_file)
    _validate_preflight_and_curation(names, preflight_path, curation_yaml_path)

    resume_dir = resume_dir if resume_dir is not None else Path(names_file).parent
    all_results: list[TaskResult] = []
    processed: list[str] = []
    repl_recoveries: list[dict] = []
    chunks = [names[i:i + chunk_size] for i in range(0, len(names), chunk_size)]

    for chunk in chunks:
        if not credentials_check():
            # Positional slice, not a membership filter: `processed` is always a PREFIX of
            # `names` (chunks run strictly in order), and `names` may contain duplicate entries
            # (a real 41-name batch shouldn't, but nothing here assumes uniqueness) -- a
            # membership filter would incorrectly drop every occurrence of a name that appears
            # more than once anywhere earlier in the list, not just the ones actually run.
            unprocessed = names[len(processed):]
            resume_path = _write_resume_file(names_file, resume_dir, unprocessed, "a credential check failed mid-batch")
            review_path = None
            if all_results:
                review_path = _write_partial_review(all_results, config)
            return BatchRunResult(
                results=all_results, status="credentials_expired", review_path=review_path,
                resume_path=resume_path, processed_names=list(processed), unprocessed_names=unprocessed,
                repl_recoveries=repl_recoveries,
            )

        if repl_warmup is not None:
            # Prevent: fresh server every chunk, caps memory growth before it dies on its own.
            try:
                config.server.kill()
            except Exception:  # noqa: BLE001 -- best-effort; a dead server can't be killed twice
                pass
            new_server, new_env = repl_warmup()
            config = dataclasses.replace(config, server=new_server, base_env=new_env)

        for name in chunk:
            log_line_start = _count_log_lines(config.client.log_path)
            result = author_task(name, config)

            if repl_warmup is not None and result.outcome == "ROTATED" and result.stage_records and is_unknown_environment_error(result.stage_records[-1].detail):
                # Detect + Recover: the dead attempt's spend is real and already logged in the
                # call log (visible there, and in repl_recoveries below) -- written off here
                # means its TaskResult is superseded by the retry, never appended to `results`.
                repl_recoveries.append({
                    "name": name, "input_tokens": result.input_tokens, "output_tokens": result.output_tokens,
                })
                recovered = False
                for _ in range(2):  # up to two re-warm attempts before giving up
                    try:
                        config.server.kill()
                    except Exception:  # noqa: BLE001
                        pass
                    try:
                        new_server, new_env = repl_warmup()
                        config = dataclasses.replace(config, server=new_server, base_env=new_env)
                        recovered = True
                        break
                    except Exception:  # noqa: BLE001 -- re-warm itself failing is exactly what triggers the stop below
                        continue
                if not recovered:
                    unprocessed = names[len(processed):]  # this name is still unprocessed -- never appended below
                    resume_path = _write_resume_file(
                        names_file, resume_dir, unprocessed,
                        "the REPL server died and two consecutive re-warm attempts also failed",
                    )
                    review_path = _write_partial_review(all_results, config) if all_results else None
                    return BatchRunResult(
                        results=all_results, status="repl_unrecoverable", review_path=review_path,
                        resume_path=resume_path, processed_names=list(processed), unprocessed_names=unprocessed,
                        repl_recoveries=repl_recoveries,
                    )
                # Retry the whole task from its start, once, fresh -- its spliced environments
                # died with the old server, so nothing about the dead attempt can be resumed.
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
        processed_names=list(processed), unprocessed_names=[], repl_recoveries=repl_recoveries,
    )


def _write_partial_review(results: list[TaskResult], config: PipelineConfig) -> Path:
    from datetime import UTC, datetime

    config.batch_review_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    path = config.batch_review_dir / f"batch_review_{timestamp}.md"
    path.write_text(render_batch_review(results), encoding="utf-8")
    return path
