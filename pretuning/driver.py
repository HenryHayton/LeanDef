"""Driving the eight-cell pre-tuning run against a warm vLLM endpoint.

Reuses `prelim.store` unchanged: its `model_name` slot carries the CELL ID, so the tree is
`pretuning/<cell_id>/<task>/sample_NN.json` and every property that store already proved under a
real mid-run kill -- atomic write, parse-validated resume, file-existence as the sole authority --
applies here for free. Reimplementing it for a different directory name would have been the
worst kind of duplication: identical semantics, separately buggy.

**One model, eight prompts.** Unlike the prelim there are no model swaps and no pod control: the
endpoint stays warm across all eight cells, so the run is one long stream of requests.

**Per-cell first-3 gate.** Structural plausibility only, never correctness -- the same
`prelim.validity` contract. A degenerate cell is flagged and skipped so it cannot burn the run,
but a failing gate never halts the other seven: the whole point of the design is the comparison
between cells, and losing six good cells to one bad prompt would be the expensive mistake.

Every sample records its full cell configuration (`anti_sorry_level`, `scaffold`, the exact
instruction text, the prompt hash). Recovering which prompt produced a sample must never require
re-deriving it from code that has since changed.
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

from prelim import store
from prelim.client import GenerationResult, generate
from prelim.prompts import load_task
from prelim.validity import check_early_samples
from pretuning.cells import CELLS, Cell
from pretuning.prompts import build_prompt, check_prompt_leak

TEMPERATURE = 0.7          # fixed: this compares prompts, not sampling
SAMPLES_PER_TASK = 10
MAX_TOKENS = 8192
DEFAULT_CONCURRENCY = 32   # measured: ~25 s/generation single-stream; sequential would be ~23 h


@dataclass
class CellOutcome:
    cell_id: str
    status: str = "pending"          # completed | gate_failed | aborted
    generated: int = 0
    skipped: int = 0
    errors: int = 0
    gate_detail: str = ""
    wall_s: float = 0.0
    notes: list[str] = field(default_factory=list)


def _extra_for(cell: Cell, task: str) -> dict:
    return {
        "cell_id": cell.cell_id,
        "anti_sorry_level": cell.sorry_level,
        "scaffold": cell.scaffold,
        "anti_sorry_text": cell.anti_sorry_text,
        "scaffold_text": cell.scaffold_text,
        "exemplar_prose_shown": cell.uses_prose_exemplars,
        "task": task,
    }


def run_cell(
    cell: Cell,
    tasks: list[str],
    *,
    endpoint_url: str,
    samples_dir: Path,
    model_name: str,
    log=print,
    samples_per_task: int = SAMPLES_PER_TASK,
    max_tokens: int = MAX_TOKENS,
    timeout_s: float = 600.0,
    concurrency: int = DEFAULT_CONCURRENCY,
    progress_interval_s: float = 60.0,
    forbidden: dict[str, str] | None = None,
) -> CellOutcome:
    """Generate every (task, sample) for one cell, resuming over whatever is already on disk."""
    out = CellOutcome(cell_id=cell.cell_id)
    started = time.perf_counter()
    prompts: dict[str, str] = {}

    for task in tasks:
        dossier, pinned = load_task(task)
        text = build_prompt(cell, dossier, pinned)
        if forbidden and forbidden.get(task):
            ok, detail = check_prompt_leak(text, forbidden[task])
            if not ok:
                out.notes.append(f"LEAK {task}: {detail}")
                log(f"[{cell.cell_id}] LEAK GUARD FIRED on {task}: {detail}")
                continue
        prompts[task] = text

    def one(task: str, idx: int) -> GenerationResult | None:
        if store.is_complete(cell.cell_id, task, idx, samples_dir=samples_dir):
            out.skipped += 1
            return None
        messages = [{"role": "user", "content": prompts[task]}]
        t0 = time.perf_counter()
        try:
            res = generate(
                messages, temperature=TEMPERATURE, max_tokens=max_tokens,
                model_name=model_name, endpoint_style="chat", stream=True,
                timeout_s=timeout_s, endpoint_url=endpoint_url,
            )
        except Exception as e:  # noqa: BLE001 -- one sample must never sink a cell
            out.errors += 1
            log(f"[{cell.cell_id}] {task}/{idx} ERROR {type(e).__name__}: {str(e)[:120]}")
            return None
        sample = store.build_sample(
            model_name=model_name, task_name=task, sample_index=idx, temperature=TEMPERATURE,
            max_tokens=max_tokens, prompt_messages=messages, completion=res.text,
            finish_reason=res.finish_reason, prompt_tokens=res.prompt_tokens,
            completion_tokens=res.completion_tokens,
            wall_time_s=time.perf_counter() - t0, endpoint_url=endpoint_url,
            extra=_extra_for(cell, task),
        )
        # `model_slug` is derived from `model_name` inside `build_sample`; override it with the
        # cell id so the tree is keyed by CELL -- the thing that actually varies in this run.
        sample.model_slug = cell.cell_id
        store.write_sample(sample, samples_dir=samples_dir)
        out.generated += 1
        return res

    # --- first-3 gate: structural plausibility, one task's first three samples ---------------
    gate_task = tasks[0]
    gate_texts: list[tuple[str, str | None]] = []
    for idx in range(3):
        res = one(gate_task, idx)
        if res is not None:
            gate_texts.append((res.text, res.finish_reason))
    if gate_texts:
        verdict = check_early_samples(cell.cell_id, gate_texts)
        out.gate_detail = verdict.summary
        log(f"[gate] {cell.cell_id}: {'PASS' if verdict.passed else 'FAIL'} "
            f"({verdict.n_plausible}/{verdict.n_checked} plausible) -- {verdict.summary}")
        for line in verdict.report_lines():
            log(f"        {line}")
        if not verdict.passed:
            out.status = "gate_failed"
            out.wall_s = time.perf_counter() - started
            log(f"[{cell.cell_id}] GATE FAILED -- skipping this cell, continuing with the others")
            return out

    # --- the rest, concurrently -------------------------------------------------------------
    # Single-stream latency is ~25 s, so the whole 3,280-generation run would be ~23 h serially.
    # The endpoint batches happily; the client is thread-safe (each call owns its own request),
    # and the store is atomic per file, so the only shared state is the counter under `lock`.
    units = [(t, i) for t in prompts for i in range(samples_per_task)]
    lock = threading.Lock()
    started_gen = time.perf_counter()
    last = started_gen
    done = 0

    def _work(unit):
        t, i = unit
        try:
            one(t, i)
        except Exception as e:  # noqa: BLE001 -- a unit must never sink the cell
            with lock:
                out.errors += 1
            log(f"[{cell.cell_id}] {t}/{i} UNCAUGHT {type(e).__name__}: {str(e)[:120]}")

    with ThreadPoolExecutor(max_workers=max(1, concurrency)) as pool:
        futures = [pool.submit(_work, u) for u in units]
        for _ in as_completed(futures):
            with lock:
                done += 1
                now = time.perf_counter()
                if now - last >= progress_interval_s:
                    last = now
                    rate = done / max(now - started_gen, 1e-6)
                    eta = (len(units) - done) / rate if rate > 0 else float("inf")
                    log(f"[{cell.cell_id}] {done}/{len(units)} "
                        f"(gen={out.generated} skip={out.skipped} err={out.errors}) "
                        f"eta {eta/60:.0f} min")

    out.status = "completed"
    out.wall_s = time.perf_counter() - started
    return out


def run_all(
    tasks: list[str],
    *,
    endpoint_url: str,
    samples_dir: Path,
    model_name: str,
    cells: list[Cell] | None = None,
    log=print,
    **kw,
) -> list[CellOutcome]:
    """All eight cells in the pinned run order (S-A last -- see `pretuning.cells`)."""
    outcomes = []
    for cell in (cells or CELLS):
        log(f"\n=== cell {cell.cell_id} ({cell.sorry_level} x {cell.scaffold}) ===")
        outcomes.append(run_cell(cell, tasks, endpoint_url=endpoint_url, samples_dir=samples_dir,
                                 model_name=model_name, log=log, **kw))
        o = outcomes[-1]
        log(f"=== {o.cell_id}: {o.status} generated={o.generated} skipped={o.skipped} "
            f"errors={o.errors} {o.wall_s/60:.1f}min")
    return outcomes
