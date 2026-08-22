"""Generate candidate definitions from a trained model against a held-out task set.

    uv run python scripts/run_heldout_eval.py \
        --endpoint https://8cceyvk6sc0hkw-8000.proxy.runpod.net \
        --served recipe_v2 --hf /data/merged_v2 \
        --tasks-dir prelim_testing/tasks_heldout_v1

**Reuses `pretuning.driver.run_all`**, exactly as `run_smoke32b.py` does, so the generation path
carries the properties already paid for: the first-3 validity gate, the leak guard over fully
assembled prompts, atomic write + parse-validated resume, and bounded concurrency.

**Why a separate runner rather than a flag on `run_smoke32b.py`.** That script builds the leak
guard's forbidden-name map by globbing `prelim_testing/tasks/*/task.json` -- the July 41 -- which
is hardcoded and independent of the task set actually being generated for. Pointed at a held-out
corpus it would guard the wrong names: the real Mathlib names of the tasks being evaluated would
not be forbidden, so a completion echoing one would pass the guard silently. Here the forbidden
map is derived from the SAME directory the tasks come from.

Decode settings match the established A1 stack -- prohibition + conformance instructions, notation
glossary, zero exemplars, no token ban. Zero exemplars won the A-battery on every criterion, and
bans are left off deliberately: the operator preference on this project is to observe capability
rather than suppress failure modes, and a ban that covers nothing is indistinguishable in the
output from one that did nothing.

Scoring is a separate step (`scripts/score_cells.py`), so a generation run can be inspected
before hours of kernel time are committed to it.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from pretuning.battery import BatteryCell
from pretuning.driver import run_all
from pretuning.prompts import ZERO


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", required=True)
    ap.add_argument("--served", required=True,
                    help="model id as vLLM serves it (see /v1/models)")
    ap.add_argument("--hf", default=None,
                    help="tokenizer/model path for the prompt builder; defaults to --served")
    ap.add_argument("--tasks-dir", default="prelim_testing/tasks_heldout_v1")
    ap.add_argument("--samples-dir", default="prelim_testing/output/heldout_eval")
    ap.add_argument("--samples-per-task", type=int, default=10)
    ap.add_argument("--concurrency", type=int, default=16)
    ap.add_argument("--max-tokens", type=int, default=16384)
    ap.add_argument("--allow-degenerate", action="store_true")
    args = ap.parse_args()

    # The driver loads each task through `prelim.prompts.load_task`, which resolves the corpus
    # root from $PRELIM_TASKS_DIR -- NOT from anything passed down the call chain. Setting it
    # here keeps enumeration and loading pointed at the same directory; without it the driver
    # silently falls back to the default corpus and every task fails to load.
    os.environ["PRELIM_TASKS_DIR"] = args.tasks_dir
    tasks_root = Path(args.tasks_dir)
    tasks = sorted(p.name for p in tasks_root.iterdir()
                   if p.is_dir() and (p / "dossier.md").is_file() and (p / "task.json").is_file())
    if not tasks:
        print(f"no tasks with both dossier.md and task.json under {tasks_root}")
        return 1

    # Leak guard feedstock, from the SAME directory as the tasks -- see the module docstring.
    reals = {}
    for p in tasks_root.glob("*/task.json"):
        real = (json.loads(p.read_text(encoding="utf-8")).get("provenance") or {}).get("mathlib_name")
        if real:
            reals[p.parent.name] = real
    missing = [t for t in tasks if t not in reals]

    def log(*a):
        print(*a, flush=True)

    log(f"\n{'=' * 78}\nHELD-OUT EVAL -- {args.served}\n{'=' * 78}")
    log(f"tasks_dir={tasks_root}  tasks={len(tasks)}")
    log(f"leak-guard names resolved: {len(reals)}/{len(tasks)}"
        + (f"  MISSING: {missing}" if missing else ""))
    log(f"samples/task={args.samples_per_task}  max_tokens={args.max_tokens}  "
        f"concurrency={args.concurrency}")
    log(f"exemplar_mode={ZERO}  ban=False")

    cell = BatteryCell(cell_id=args.served, battery="H", exemplar_mode=ZERO,
                       ban=False, prefill=False,
                       rationale=f"held-out evaluation of {args.served}")

    t0 = time.perf_counter()
    outs = run_all(tasks, endpoint_url=args.endpoint, samples_dir=Path(args.samples_dir),
                   model_name=args.hf or args.served, cells=[cell], log=log,
                   concurrency=args.concurrency, forbidden=reals, ban_variants=None,
                   samples_per_task=args.samples_per_task, max_tokens=args.max_tokens,
                   timeout_s=1800.0, allow_degenerate=args.allow_degenerate)

    o = outs[0]
    log(f"\n{o.cell_id}: {o.status} generated={o.generated} skipped={o.skipped} "
        f"errors={o.errors} {o.wall_s / 60:.1f}min "
        f"(total {(time.perf_counter() - t0) / 60:.1f} min)")
    log(f"\nsamples -> {args.samples_dir}/{args.served}/<task>/sample_NN.json")
    log(f"score with: uv run python scripts/score_cells.py "
        f"--root {args.samples_dir} --out scoring_output/heldout_eval_funnel.json")
    return 0 if o.status not in ("failed",) else 1


if __name__ == "__main__":
    sys.exit(main())
