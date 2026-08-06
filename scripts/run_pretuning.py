"""Launch the eight-cell pre-tuning run against a warm vLLM endpoint."""
import argparse
import json
import sys
import time
from pathlib import Path
from prelim.prompts import available_tasks
from pretuning.cells import CELLS
from pretuning.driver import run_all

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", required=True)
    ap.add_argument("--samples-dir", default="prelim_testing/output/pretuning")
    ap.add_argument("--model", default="Goedel-LM/Goedel-Formalizer-V2-8B")
    ap.add_argument("--concurrency", type=int, default=32)
    ap.add_argument("--cells", nargs="*", default=None, help="cell ids; default all eight in order")
    args = ap.parse_args()

    tasks = available_tasks()
    reals = {p.parent.name: (json.loads(p.read_text()).get("provenance") or {}).get("mathlib_name")
             for p in Path("prelim_testing/tasks").glob("*/task.json")}
    cells = [c for c in CELLS if c.cell_id in args.cells] if args.cells else CELLS

    def log(*a):
        print(*a, flush=True)

    t0 = time.perf_counter()
    outs = run_all(tasks, endpoint_url=args.endpoint, samples_dir=Path(args.samples_dir),
                   model_name=args.model, cells=cells, log=log,
                   concurrency=args.concurrency, forbidden=reals)
    log("\n" + "=" * 78)
    for o in outs:
        log(f"  {o.cell_id:<8} {o.status:<12} generated={o.generated:<5} skipped={o.skipped:<5} "
            f"errors={o.errors:<4} {o.wall_s/60:.1f}min")
    log(f"TOTAL {(time.perf_counter()-t0)/60:.1f} min")
    Path("scoring_output/pretuning_run_summary.json").write_text(json.dumps(
        [o.__dict__ for o in outs], indent=1), encoding="utf-8")
    return 0

if __name__ == "__main__":
    sys.exit(main())
