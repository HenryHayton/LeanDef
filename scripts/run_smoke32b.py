"""32B base-model smoke: one model per pod lifetime, driven from the laptop.

    uv run python scripts/run_smoke32b.py --endpoint URL --model goedel-prover-v2-32b

**Reuses `pretuning.driver` rather than adding a fourth driver.** That driver already carries
every property this run needs and each was paid for once already: the first-3 validity gate, the
leak guard over fully assembled prompts, atomic write + parse-validated resume, bounded
concurrency, and the ban wiring with its refuse-to-run-without-resolved-variants guard. Keying
its `cell_id` to the MODEL slug puts the tree at `smoke32b/<model>/<task>/sample_NN.json`, which
is the shape `scripts/score_cells.py` already reads.

**One prompt for all three models, and it carries no exemplars** (operator decision, 2026-08-07).

Two brief premises about the prompt did not survive contact:

- StepFun was to get a one-exemplar variant because its context limit is 16,384 and the
  3-exemplar prompt "(~16k)" would not fit. Its `config.json` reports
  `max_position_embeddings: 131072`, and the assembled prompt measures **4,496 tokens** -- the
  ~16k figure was CHARACTERS. Neither half of the premise holds.
- The exemplar dose itself. The A-battery verdict landed after the brief was written and found
  zero exemplars beat both three-exemplar and reframed: A1 won on every criterion, and A3's
  single exemplar produced MORE contamination than A2's three (32 vs 10 substitutions). Running
  the brief's dose would have measured three base models through a prompt already known to be
  the worse of the two available.

So every cell runs A1's stack -- prohibition instruction, conformance instruction, notation
glossary, no exemplars -- identically. A base-selection comparison needs the prompt held fixed
across models; the only thing that varies between cells is the model.
"""

import argparse
import json
import sys
import time
from pathlib import Path

from prelim.prompts import available_tasks
from pretuning.battery import BatteryCell
from pretuning.decode import ban_variants, dump_resolution, resolve_bad_words
from pretuning.driver import run_all
from pretuning.prompts import ZERO

# `ban` is on only for StepFun, per the brief: its trained task is statement emission, so it is
# the cell where a punt is most likely to arrive as a bodyless `theorem`. Ban variants are
# resolved against ITS tokenizer at pre-flight rather than assumed -- an unresolved list would
# leave the intervention silently absent, which is indistinguishable in the output from an
# intervention that did nothing.
#
# This is the ONLY decode intervention in the run. No prefill on any cell: the 8B battery measured
# prefill as actively harmful (sorry bodies 38.8% -> 56.3%, admissibility halved), and stacking
# further interventions would obscure what the models can actually construct.
MODELS = {
    "goedel-prover-v2-32b": {
        "hf": "Goedel-LM/Goedel-Prover-V2-32B",
        "ban": False,
        "note": "Qwen3ForCausalLM, 40960 ctx, prover-trained",
    },
    "stepfun-formalizer-32b": {
        "hf": "stepfun-ai/StepFun-Formalizer-32B",
        "ban": True,
        "note": "Qwen2ForCausalLM, 131072 ctx (NOT 16384), statement-emission trained",
    },
    "qwen3-32b": {
        "hf": "Qwen/Qwen3-32B",
        "ban": False,
        "note": "general instruct, reasoning mode per card default",
    },
}

# 16384, not 8192. The 8B run lost 22-30% of ban-cell samples to truncation at 8192 and these
# families think long; the brief calls this non-negotiable.
MAX_TOKENS = 16384


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", required=True)
    ap.add_argument("--model", required=True, choices=sorted(MODELS))
    ap.add_argument("--samples-dir", default="prelim_testing/output/smoke32b")
    ap.add_argument("--samples-per-task", type=int, default=10)
    ap.add_argument("--concurrency", type=int, default=16)
    ap.add_argument("--max-tokens", type=int, default=MAX_TOKENS)
    ap.add_argument("--allow-degenerate", action="store_true",
                    help="run even if the first-3 gate fails -- only when the failure mode is "
                         "itself the thing being measured")
    ap.add_argument("--exemplar-mode", default=ZERO,
                    help="ZERO by default -- the A-battery winner. Changing this makes the cell "
                         "non-comparable to the others unless every cell changes with it.")
    args = ap.parse_args()

    spec = MODELS[args.model]
    tasks = available_tasks()
    reals = {p.parent.name: (json.loads(p.read_text()).get("provenance") or {}).get("mathlib_name")
             for p in Path("prelim_testing/tasks").glob("*/task.json")}

    def log(*a):
        print(*a, flush=True)

    log(f"\n{'=' * 78}\n32B SMOKE -- {args.model}\n{'=' * 78}")
    log(f"hf={spec['hf']}  ({spec['note']})")
    log(f"tasks={len(tasks)}  samples/task={args.samples_per_task}  max_tokens={args.max_tokens}")

    variants = None
    if spec["ban"]:
        log(f"\nresolving {len(ban_variants())} ban variants against THIS model's tokenizer...")
        resolved = resolve_bad_words(args.endpoint, spec["hf"])
        for t in resolved:
            log(t.log_line())
        n_uncond = sum(1 for t in resolved if t.unconditional)
        log(f"  -> {len(resolved)} variants, {n_uncond} unconditional, "
            f"{len(resolved) - n_uncond} conditional")
        Path("scoring_output").mkdir(exist_ok=True)
        Path(f"scoring_output/smoke32b_ban_{args.model}.json").write_text(
            dump_resolution(resolved), encoding="utf-8")
        variants = [t.variant for t in resolved]

    cell = BatteryCell(cell_id=args.model, battery="S", exemplar_mode=args.exemplar_mode,
                       ban=spec["ban"], prefill=False, rationale=spec["note"])
    log(f"exemplar_mode={args.exemplar_mode}  ban={spec['ban']}")

    t0 = time.perf_counter()
    outs = run_all(tasks, endpoint_url=args.endpoint, samples_dir=Path(args.samples_dir),
                   model_name=spec["hf"], cells=[cell], log=log,
                   concurrency=args.concurrency, forbidden=reals, ban_variants=variants,
                   samples_per_task=args.samples_per_task, max_tokens=args.max_tokens,
                   timeout_s=1800.0, allow_degenerate=args.allow_degenerate)

    o = outs[0]
    log(f"\n{o.cell_id}: {o.status} generated={o.generated} skipped={o.skipped} "
        f"errors={o.errors} {o.wall_s/60:.1f}min  (total {(time.perf_counter()-t0)/60:.1f} min)")

    summary = Path("scoring_output/smoke32b_run_summary.json")
    existing = json.loads(summary.read_text()) if summary.exists() else []
    by_id = {e["cell_id"]: e for e in existing}
    by_id[o.cell_id] = {**o.__dict__, "hf": spec["hf"], "max_tokens": args.max_tokens}
    summary.write_text(json.dumps(list(by_id.values()), indent=1), encoding="utf-8")
    return 0 if o.status == "completed" else 1


if __name__ == "__main__":
    sys.exit(main())
