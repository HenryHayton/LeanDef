"""Launch the decode/exemplar battery against a warm vLLM endpoint.

    uv run python scripts/run_battery.py --endpoint URL                    # T0-T3, A1-A3
    uv run python scripts/run_battery.py --endpoint URL --cells T1 T3      # a subset
    uv run python scripts/run_battery.py --endpoint URL --compose T3 A2    # the C1 cell, last

Pre-flight, before a single sample is generated:

1. **Ban variants are resolved against the SERVED tokenizer** and their id sequences printed. A
   ban that silently covered nothing would leave T1/T3 indistinguishable from T0 for a reason
   invisible in the output, so this refuses to start rather than guessing.
2. **The prefill is rendered and echoed** for a sample task, so the exact prefix is in the log
   next to the samples it produced.
3. **The leak guard runs over every assembled prompt**, exemplar text included, as it does for
   every generation run here.
"""

import argparse
import json
import sys
import time
from pathlib import Path

from harness.signature import PinnedSignature
from prelim.prompts import available_tasks, load_task
from pretuning.battery import BATTERY_CELLS, CELL_BY_ID, compose
from pretuning.decode import ban_variants, dump_resolution, prefill_text, resolve_bad_words
from pretuning.driver import run_all


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", required=True)
    ap.add_argument("--samples-dir", default="prelim_testing/output/decode_exemplar")
    ap.add_argument("--model", default="Goedel-LM/Goedel-Formalizer-V2-8B")
    ap.add_argument("--concurrency", type=int, default=32)
    ap.add_argument("--cells", nargs="*", default=None, help="cell ids; default T0-T3 then A1-A3")
    ap.add_argument("--compose", nargs=2, metavar=("T_WINNER", "A_WINNER"), default=None,
                    help="run ONLY the composition cell, built from the two named winners")
    args = ap.parse_args()

    def log(*a):
        print(*a, flush=True)

    if args.compose:
        cells = [compose(args.compose[0], args.compose[1])]
        log(f"composition cell C1 = {cells[0].rationale}")
    elif args.cells:
        cells = [CELL_BY_ID[c] for c in args.cells]
    else:
        cells = list(BATTERY_CELLS)

    tasks = available_tasks()
    reals = {p.parent.name: (json.loads(p.read_text()).get("provenance") or {}).get("mathlib_name")
             for p in Path("prelim_testing/tasks").glob("*/task.json")}

    log(f"\n{'=' * 78}\nPRE-FLIGHT\n{'=' * 78}")
    log(f"tasks={len(tasks)}  cells={[c.cell_id for c in cells]}  model={args.model}")

    # 1. Ban variants -- resolved, never guessed.
    variants = None
    if any(c.ban for c in cells):
        log(f"\nresolving {len(ban_variants())} ban variants against the served tokenizer...")
        resolved = resolve_bad_words(args.endpoint, args.model)
        for t in resolved:
            log(t.log_line())
        n_uncond = sum(1 for t in resolved if t.unconditional)
        log(f"  -> {len(resolved)} variants, {n_uncond} banned unconditionally, "
            f"{len(resolved) - n_uncond} conditional on their own prefix")
        Path("scoring_output").mkdir(exist_ok=True)
        Path("scoring_output/battery_ban_resolution.json").write_text(
            dump_resolution(resolved), encoding="utf-8")
        variants = [t.variant for t in resolved]

    # 2. The prefill, echoed verbatim for a sample task.
    if any(c.prefill for c in cells):
        name, _, type_sig = load_task(tasks[0])[1].partition(" : ")
        log(f"\nprefill for {tasks[0]}:\n  {prefill_text(PinnedSignature(name.strip(), type_sig.strip()))!r}")

    t0 = time.perf_counter()
    outs = run_all(tasks, endpoint_url=args.endpoint, samples_dir=Path(args.samples_dir),
                   model_name=args.model, cells=cells, log=log,
                   concurrency=args.concurrency, forbidden=reals, ban_variants=variants)

    log("\n" + "=" * 78)
    for o in outs:
        log(f"  {o.cell_id:<8} {o.status:<12} generated={o.generated:<5} skipped={o.skipped:<5} "
            f"errors={o.errors:<4} {o.wall_s/60:.1f}min")
    log(f"TOTAL {(time.perf_counter()-t0)/60:.1f} min")

    summary_path = Path("scoring_output/battery_run_summary.json")
    existing = json.loads(summary_path.read_text()) if summary_path.exists() else []
    by_id = {o["cell_id"]: o for o in existing}
    by_id.update({o.cell_id: o.__dict__ for o in outs})
    summary_path.write_text(json.dumps(list(by_id.values()), indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
