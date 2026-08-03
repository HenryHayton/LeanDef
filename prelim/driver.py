"""The prelim-testing driver: the Mac-side orchestration of an unattended overnight run.

One model at a time, in order. For each: a validity gate on the first three completions, then
every remaining (task, sample) pair generated with bounded concurrency, each result extracted
(recorded, never gating) and written to the store as it arrives. When a model's set is complete
the driver asks the pod to advance and waits for the next model to report loaded.

**The driver owns sequencing; the pod is dumb.** The pod knows only "load the next thing in my
list"; every decision about when that happens, and every judgement about whether output is
usable, lives here. That split is what makes the whole thing resumable: the Mac holds all the
state worth holding, and it holds it on disk rather than in memory.

**Resume-safety is by construction, not by bookkeeping.** The unit of work is a (model, task,
sample) triple, and `store.is_complete` is the only authority on whether one is done. There is no
progress file to fall out of sync -- the samples on disk ARE the progress. A relaunch after any
failure, at any point, does the right thing with no flags.

**What halts what.** A failed validity gate halts THAT MODEL and moves to the next (one bad
wrapper must not cost the other six their night). A generation failure costs its own sample and
nothing else. Only a pod-control failure -- the thing that would silently generate against the
wrong model -- halts the whole run.
"""

import argparse
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from prelim import config as cfg
from prelim import store
from prelim.client import PrelimClientError, generate
from prelim.extract import Extraction, extract_definition
from prelim.models import MODEL_SLUGS, get_model
from prelim.podcontrol import PodControl, PodControlError
from prelim.prompts import assemble_prompt, available_tasks
from prelim.validity import GATE_SAMPLE_COUNT, check_early_samples

DEFAULT_CONCURRENCY = 16  # vLLM batches server-side; this is how many we keep in flight
PROGRESS_INTERVAL_S = 60.0


@dataclass
class ModelOutcome:
    slug: str
    status: str  # "completed" | "gate_failed" | "aborted"
    completed: int = 0
    attempted: int = 0
    extraction_failures: int = 0
    detail: str = ""


@dataclass
class RunResult:
    outcomes: list[ModelOutcome] = field(default_factory=list)
    summary_path: Path | None = None
    stopped_reason: str | None = None


class RunLog:
    """Append-only human-facing log. Every line is timestamped and flushed immediately -- this is
    what the human reads with coffee, and a buffered line in a killed process is a line lost."""

    def __init__(self, path: Path, *, echo: bool = True):
        self.path = Path(path)
        self.echo = echo
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, message: str) -> None:
        line = f"{datetime.now(UTC).isoformat()}  {message}"
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
            f.flush()
        if self.echo:
            print(line, flush=True)


@dataclass
class _Unit:
    """One (task, sample_index) of work for the current model."""

    task: str
    index: int

    @property
    def temperature(self) -> float:
        return cfg.temperature_for_sample(self.index)


def _generate_and_store(
    slug: str, unit: _Unit, *, samples_dir: Path, tasks_root: Path | None,
    endpoint_url: str | None, log_path: Path | None, max_tokens: int, timeout_s: float | None,
) -> tuple[_Unit, str | None, bool]:
    """Generate one sample and persist it. Returns `(unit, error_or_None, extraction_ok)`.

    Never raises: a failure here must cost exactly one sample. The exception text is returned so
    the caller can log it and count it, and no sample file is written -- which means the resume
    logic will naturally retry this unit on a later relaunch.
    """
    spec = get_model(slug)
    try:
        prompt = assemble_prompt(slug, unit.task, root=tasks_root)
        result = generate(
            prompt,
            temperature=unit.temperature,
            max_tokens=max_tokens,
            model_name=spec.hf_name,
            endpoint_style=spec.endpoint_style,
            # Streaming is mandatory against RunPod's proxy: it 524s any non-streaming
            # request slow to produce its first byte, which at 8192 max_tokens (~246s on
            # this A40) is every long generation. Measured live 2026-08-03.
            stream=True,
            endpoint_url=endpoint_url,
            timeout_s=timeout_s,
            log_path=log_path,
        )
    except (PrelimClientError, FileNotFoundError, OSError) as e:
        return unit, f"{type(e).__name__}: {e}", False

    extraction = extract_definition(slug, result.text, finish_reason=result.finish_reason)
    ok = isinstance(extraction, Extraction)
    # Extraction is RECORDED, never gating: a model that cannot produce an extractable
    # definition is reporting its score, and discarding the sample would erase that measurement.
    extra = {
        "extraction_ok": ok,
        "top_p": cfg.TOP_P,
        "card_sampling": spec.card_sampling,
        "endpoint_style": spec.endpoint_style,
        # Recorded so samples stay comparable within a run even though the budget is per-model
        # (Herald's architecture caps it at 4096 context; everything else gets 16384/8192).
        "max_model_len": spec.max_model_len,
    }
    if ok:
        extra.update(
            extracted_code=extraction.code,
            declared_name=extraction.declared_name,
            renamed_symbol=extraction.renamed_symbol,
            from_fence=extraction.from_fence,
            n_candidates=extraction.n_candidates,
        )
    else:
        extra.update(extraction_failure_reason=extraction.reason, extraction_detail=extraction.detail)

    sample = store.build_sample(
        model_name=spec.hf_name, task_name=unit.task, sample_index=unit.index,
        temperature=unit.temperature, max_tokens=max_tokens,
        prompt_messages=prompt if isinstance(prompt, list) else [{"role": "user", "content": prompt}],
        completion=result.text, finish_reason=result.finish_reason,
        prompt_tokens=result.prompt_tokens, completion_tokens=result.completion_tokens,
        wall_time_s=result.wall_time_s, attempts=result.attempts, endpoint_url=endpoint_url,
        extra=extra,
    )
    store.write_sample(sample, samples_dir=samples_dir)
    return unit, None, ok


def _pending_units(slug: str, tasks: list[str], samples_per_task: int, samples_dir: Path) -> list[_Unit]:
    """Every unit not already complete on disk. Ordered task-major so the gate's first three
    samples come from the first task, which is what makes an early gate failure cheap."""
    model_slug = store.model_slug(get_model(slug).hf_name)
    return [
        _Unit(task, i)
        for task in tasks
        for i in range(samples_per_task)
        if not store.is_complete(model_slug, task, i, samples_dir=samples_dir)
    ]


def _gate_samples_from_disk(slug: str, tasks: list[str], samples_dir: Path, n: int) -> list[tuple[str, str | None]]:
    """Completions already on disk for the gate, in unit order -- so a relaunch re-gates on the
    same evidence rather than spending fresh generations to re-answer a settled question."""
    model_slug = store.model_slug(get_model(slug).hf_name)
    out: list[tuple[str, str | None]] = []
    for task in tasks:
        for i in range(cfg.SAMPLES_PER_TASK):
            if len(out) >= n:
                return out
            path = store.sample_path(model_slug, task, i, samples_dir=samples_dir)
            data = store.read_sample(path)
            if data and data.get("completion") is not None:
                out.append((data["completion"], data.get("finish_reason")))
    return out


def run_model(
    slug: str,
    tasks: list[str],
    *,
    samples_per_task: int = cfg.SAMPLES_PER_TASK,
    samples_dir: Path,
    tasks_root: Path | None = None,
    endpoint_url: str | None = None,
    call_log_path: Path | None = None,
    max_tokens: int | None = None,   # None => the model's own spec.max_tokens
    timeout_s: float | None = None,
    concurrency: int = DEFAULT_CONCURRENCY,
    run_log: RunLog,
    progress_interval_s: float = PROGRESS_INTERVAL_S,
    clock=time.monotonic,
) -> ModelOutcome:
    """Generate one model's whole set. Returns without raising for any per-model failure."""
    spec = get_model(slug)
    # Per-model budget unless the caller forces one. A single global cap cannot serve a set
    # spanning 4k-64k context models (see ModelSpec.max_model_len).
    max_tokens = spec.max_tokens if max_tokens is None else max_tokens
    pending = _pending_units(slug, tasks, samples_per_task, samples_dir)
    total = len(tasks) * samples_per_task
    already = total - len(pending)
    run_log.write(f"[{slug}] starting: {already}/{total} already complete, {len(pending)} to generate")

    if not pending:
        run_log.write(f"[{slug}] nothing to do -- already complete")
        return ModelOutcome(slug, "completed", completed=total, attempted=total)

    # --- validity gate ---------------------------------------------------------------------
    # Generated sequentially and deliberately: the whole point is to spend as little as possible
    # before deciding whether this model's wrapper works at all.
    gate_units = pending[:GATE_SAMPLE_COUNT]
    errors = 0
    extraction_failures = 0
    completed = 0
    for unit in gate_units:
        _, err, ok = _generate_and_store(
            slug, unit, samples_dir=samples_dir, tasks_root=tasks_root, endpoint_url=endpoint_url,
            log_path=call_log_path, max_tokens=max_tokens, timeout_s=timeout_s,
        )
        if err:
            errors += 1
            run_log.write(f"[{slug}] gate sample {unit.task}#{unit.index} errored: {err}")
        else:
            completed += 1
            extraction_failures += 0 if ok else 1

    gate_input = _gate_samples_from_disk(slug, tasks, samples_dir, GATE_SAMPLE_COUNT)
    gate = check_early_samples(slug, gate_input)
    for line in gate.report_lines():
        run_log.write(line)
    if not gate.passed:
        run_log.write(
            f"[{slug}] !!! GATE FAILED -- halting this model and continuing with the next. "
            f"Suspect this model's prompt wrapper or endpoint style BEFORE concluding anything "
            f"about the model itself."
        )
        return ModelOutcome(
            slug, "gate_failed", completed=completed, attempted=len(gate_units),
            extraction_failures=extraction_failures, detail=gate.summary,
        )

    # --- the rest, concurrently -------------------------------------------------------------
    remaining = pending[GATE_SAMPLE_COUNT:]
    run_log.write(f"[{slug}] gate passed; generating {len(remaining)} more at concurrency {concurrency}")
    started = clock()
    last_progress = started
    lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=max(1, concurrency)) as pool:
        futures = {
            pool.submit(
                _generate_and_store, slug, u, samples_dir=samples_dir, tasks_root=tasks_root,
                endpoint_url=endpoint_url, log_path=call_log_path, max_tokens=max_tokens,
                timeout_s=timeout_s,
            ): u
            for u in remaining
        }
        for fut in as_completed(futures):
            unit, err, ok = fut.result()
            with lock:
                if err:
                    errors += 1
                    run_log.write(f"[{slug}] {unit.task}#{unit.index} errored: {err}")
                else:
                    completed += 1
                    extraction_failures += 0 if ok else 1
                now = clock()
                if now - last_progress >= progress_interval_s:
                    last_progress = now
                    done = already + completed
                    rate = completed / max(now - started, 1e-6)
                    eta_s = (total - done) / rate if rate > 0 else float("inf")
                    run_log.write(
                        f"[{slug}] progress {done}/{total} "
                        f"({extraction_failures} extraction failures, {errors} errors) "
                        f"eta {eta_s / 60:.0f} min"
                    )

    done = already + completed
    run_log.write(
        f"[{slug}] done: {done}/{total} stored, {extraction_failures} extraction failures, {errors} errors"
    )
    return ModelOutcome(
        slug, "completed", completed=done, attempted=total, extraction_failures=extraction_failures
    )


def run_prelim(
    models: list[str],
    tasks: list[str],
    *,
    samples_per_task: int = cfg.SAMPLES_PER_TASK,
    samples_dir: Path | None = None,
    tasks_root: Path | None = None,
    endpoint_url: str | None = None,
    call_log_path: Path | None = None,
    run_log_path: Path | None = None,
    summary_path: Path | None = None,
    pod: PodControl | None = None,
    max_tokens: int | None = None,
    timeout_s: float | None = None,
    concurrency: int = DEFAULT_CONCURRENCY,
    progress_interval_s: float = PROGRESS_INTERVAL_S,
    wait_timeout_s: float = 900.0,
    echo: bool = True,
    clock=time.monotonic,
) -> RunResult:
    """Run every model in sequence. See the module docstring for what halts what."""
    samples_dir = samples_dir if samples_dir is not None else cfg.SAMPLES_DIR
    run_log = RunLog(run_log_path or (cfg.OUTPUT_DIR / "run_log.txt"), echo=echo)
    summary_path = summary_path or (cfg.OUTPUT_DIR / "run_summary.json")

    run_log.write("=" * 78)
    run_log.write(
        f"PRELIM RUN START: {len(models)} model(s) x {len(tasks)} task(s) x {samples_per_task} "
        f"samples = {len(models) * len(tasks) * samples_per_task} generations"
    )
    run_log.write(f"models: {', '.join(models)}")
    run_log.write("=" * 78)

    result = RunResult()
    for i, slug in enumerate(models):
        spec = get_model(slug)
        if pod is not None:
            # Confirm the pod is actually serving THIS model before generating anything against
            # it. Without this a mis-sequenced pod would silently attribute one model's output to
            # another -- the one failure mode that corrupts the measurement rather than reducing it.
            try:
                pod.wait_for_model(spec.hf_name, timeout_s=wait_timeout_s)
                run_log.write(f"[{slug}] pod confirms {spec.hf_name} is loaded")
            except PodControlError as e:
                run_log.write(f"!!! POD FAILURE before {slug}: {e}")
                run_log.write("!!! halting the whole run -- generating against an unknown model would corrupt the results")
                result.stopped_reason = f"pod failure before {slug}: {e}"
                break

        try:
            outcome = run_model(
                slug, tasks, samples_per_task=samples_per_task, samples_dir=samples_dir,
                tasks_root=tasks_root, endpoint_url=endpoint_url, call_log_path=call_log_path,
                max_tokens=max_tokens, timeout_s=timeout_s, concurrency=concurrency,
                run_log=run_log, progress_interval_s=progress_interval_s, clock=clock,
            )
        except Exception as e:  # noqa: BLE001 -- one model must never sink the run
            run_log.write(f"[{slug}] UNEXPECTED failure: {type(e).__name__}: {e}")
            outcome = ModelOutcome(slug, "aborted", detail=f"{type(e).__name__}: {e}")
        result.outcomes.append(outcome)

        if pod is not None:
            is_last = i == len(models) - 1
            try:
                report = pod.advance()
                if is_last:
                    run_log.write(f"[{slug}] final advance requested; pod reports {report}")
                else:
                    run_log.write(f"[{slug}] advance requested; pod reports {report}")
            except PodControlError as e:
                run_log.write(f"!!! POD ADVANCE FAILED after {slug}: {e}")
                result.stopped_reason = f"pod advance failed after {slug}: {e}"
                break

    counts = store.summarize(samples_dir=samples_dir)
    payload = {
        "finished_at": datetime.now(UTC).isoformat(),
        "stopped_reason": result.stopped_reason,
        "models": [
            {
                "slug": o.slug, "status": o.status, "completed": o.completed,
                "attempted": o.attempted, "extraction_failures": o.extraction_failures,
                "detail": o.detail,
            }
            for o in result.outcomes
        ],
        "counts": counts,
        "totals": {m: sum(t.values()) for m, t in counts.items()},
    }
    Path(summary_path).parent.mkdir(parents=True, exist_ok=True)
    Path(summary_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    result.summary_path = Path(summary_path)

    run_log.write("=" * 78)
    for o in result.outcomes:
        run_log.write(f"  {o.slug:30s} {o.status:12s} {o.completed}/{o.attempted}  ext-fail={o.extraction_failures}")
    if result.stopped_reason:
        run_log.write(f"!!! RUN STOPPED EARLY: {result.stopped_reason}")
    run_log.write(f"ALL DONE -- summary written to {summary_path}")
    run_log.write("=" * 78)
    return result


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Run prelim testing generation across models.")
    p.add_argument("--models", nargs="*", default=list(MODEL_SLUGS), help="model slugs (default: all 7)")
    p.add_argument("--tasks", nargs="*", default=None, help="task names (default: all available)")
    p.add_argument("--samples", type=int, default=cfg.SAMPLES_PER_TASK)
    p.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    p.add_argument("--endpoint-url", default=None, help=f"default: ${cfg.ENV_ENDPOINT_URL}")
    p.add_argument("--control-url", default=None, help="pod control server (port 8001); omit to skip pod handshakes")
    p.add_argument("--models-url", default=None, help="vLLM /v1/models URL; derived from --endpoint-url if omitted")
    p.add_argument("--smoke", action="store_true", help="1 task (Nat.clog) x 1 sample x every model")
    p.add_argument("--max-tokens", type=int, default=None, help="override the per-model default")
    args = p.parse_args(argv)

    tasks = args.tasks if args.tasks else available_tasks()
    samples = args.samples
    if args.smoke:
        tasks = ["Nat.clog"] if "Nat.clog" in tasks else tasks[:1]
        samples = 1

    pod = None
    if args.control_url:
        models_url = args.models_url
        if not models_url:
            base = (args.endpoint_url or cfg.endpoint_url() or "").split("/v1/")[0]
            models_url = f"{base}/v1/models"
        pod = PodControl(control_url=args.control_url, models_url=models_url)

    result = run_prelim(
        args.models, tasks, samples_per_task=samples, endpoint_url=args.endpoint_url,
        pod=pod, concurrency=args.concurrency, max_tokens=args.max_tokens,
        summary_path=cfg.OUTPUT_DIR / ("smoke_summary.json" if args.smoke else "run_summary.json"),
        run_log_path=cfg.OUTPUT_DIR / ("smoke_log.txt" if args.smoke else "run_log.txt"),
    )
    return 1 if result.stopped_reason else 0


if __name__ == "__main__":
    sys.exit(main())
