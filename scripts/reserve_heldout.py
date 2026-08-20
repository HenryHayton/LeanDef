"""Reserve a held-out slate: definitions withheld from training authoring, authored fresh later.

    uv run python scripts/reserve_heldout.py [--size 80] [--seed 20260819]

Held-out data for the mid-size run is authored FRESH during training rather than carved out of
the training corpus, so that a held-out task cannot have leaked into the model. That plan has a
failure mode this file exists to close: fresh tasks come from the SAME batch-5 pool the training
corpus is drawing from, so unless specific definitions are reserved up front, ongoing authoring
simply consumes them and there is nothing uncontaminated left to author at training time.

So the slate is chosen NOW, from names that are preflight-passing but not yet authored, and
`resume_batch2500.py` excludes them from every future authoring run. The definitions are named
and pinned here; their tasks do not exist yet and are not authored until training time.

**Sized by expected T3 yield, not by task count.** Only ~37% of attempted names become T3 tasks
(schema-valid, >=3 facts, >=1 accept fact, >=1 CERTIFIED reject fact), so a slate of N names
yields roughly 0.37N usable held-out tasks. The default 80 targets ~30 usable, about 13% of a
225-task training corpus.

**Stratified against the training corpus, seeded and deterministic.** Return shape is matched to
the batch-2500 T3 population, and a per-namespace cap keeps one family from dominating.
"""

import argparse
import json
import random
import sys
from pathlib import Path

POOL_MANIFEST = Path("miner/output/harvest_manifest_batch5.jsonl")
PASSING = Path("authoring/batches/batch2500_passing.txt")
LEDGER = Path("authoring/batches/batch2500_rotated.txt")
TASKS = Path("prelim_testing/tasks_batch2500")
TRAINING = Path("training/config/midsize_training_v1.json")
OUT = Path("training/config/heldout_slate_v1.json")
NS_CAP = 3


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=80)
    ap.add_argument("--seed", type=int, default=20260819)
    args = ap.parse_args()

    manifest = {}
    for line in POOL_MANIFEST.read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        if d.get("eligible"):
            manifest[d["name"]] = d

    passing = [n.strip() for n in PASSING.read_text(encoding="utf-8").splitlines() if n.strip()]
    shipped = {p.name for p in TASKS.iterdir() if (p / "task.json").exists()}
    rotated = {l.split("\t")[0] for l in LEDGER.read_text(encoding="utf-8").splitlines() if l.strip()}
    available = [n for n in passing if n not in shipped and n not in rotated and n in manifest]

    # Match the shape mix of the batch-2500 tasks already at T3.
    train = json.loads(TRAINING.read_text(encoding="utf-8"))
    t3 = [e["name"] for e in train["tasks"] if e["corpus"] == "batch2500_2026-08-16"]
    mix = {}
    for n in t3:
        if n in manifest:
            s = manifest[n]["return_shape"]
            mix[s] = mix.get(s, 0) + 1
    total = sum(mix.values()) or 1
    quota = {s: round(args.size * c / total) for s, c in mix.items()}

    rng = random.Random(args.seed)
    picked, ns_used = [], {}
    for shape in sorted(quota, key=lambda s: -quota[s]):
        cands = [n for n in available if manifest[n]["return_shape"] == shape]
        rng.shuffle(cands)
        for n in cands:
            if len(picked) >= args.size or sum(1 for p in picked
                                               if manifest[p]["return_shape"] == shape) >= quota[shape]:
                break
            ns = n.split(".")[0] if "." in n else n
            if ns_used.get(ns, 0) >= NS_CAP:
                continue
            ns_used[ns] = ns_used.get(ns, 0) + 1
            picked.append(n)
    # Top up if per-namespace caps left the slate short of its size.
    if len(picked) < args.size:
        rest = [n for n in available if n not in picked]
        rng.shuffle(rest)
        for n in rest:
            if len(picked) >= args.size:
                break
            ns = n.split(".")[0] if "." in n else n
            if ns_used.get(ns, 0) >= NS_CAP:
                continue
            ns_used[ns] = ns_used.get(ns, 0) + 1
            picked.append(n)

    picked.sort()
    entries = [{
        "name": n,
        "return_shape": manifest[n]["return_shape"],
        "module_path": manifest[n].get("module_path"),
        "manifest_rank": manifest[n].get("rank"),
        "richness_total": (manifest[n].get("richness") or {}).get("total"),
        "casework_tier": (manifest[n].get("proxies") or {}).get("casework_tier"),
        "authored": False,
    } for n in picked]

    shapes = {}
    for e in entries:
        shapes[e["return_shape"]] = shapes.get(e["return_shape"], 0) + 1

    OUT.write_text(json.dumps({
        "slate_id": "heldout_slate_v1",
        "created": "2026-08-19",
        "seed": args.seed,
        "status": "RESERVED — definitions chosen, tasks NOT yet authored",
        "purpose": ("Held-out evaluation set for the mid-size training run "
                    "(training/config/midsize_training_v1.json). These definitions are withheld "
                    "from training authoring and authored FRESH at training time, so a held-out "
                    "task cannot have leaked into the trained model."),
        "n_reserved_definitions": len(entries),
        "expected_usable_t3": round(len(entries) * 0.373),
        "expected_yield_basis": ("37.3% of attempted names reach T3, measured over 308 attempted "
                                 "names in batch 2500 (115 T3 from 282 shipped + 26 rotated)"),
        "drawn_from": str(PASSING),
        "selection": {
            "eligible_at_selection_time": len(available),
            "rule": ("preflight-passing, not yet authored, not content-rotated; return shape "
                     "matched to the batch-2500 T3 population; max 3 per namespace"),
            "shape_quota": quota,
            "shape_actual": shapes,
            "namespace_cap": NS_CAP,
        },
        "enforcement": ("scripts/resume_batch2500.py excludes every name here from all future "
                        "authoring runs. Without that, training authoring would consume the "
                        "slate and there would be nothing uncontaminated left to author."),
        "how_to_author_at_training_time": [
            "uv run python scripts/run_batch200.py --limit 80 \\",
            "  --names training/config/heldout_slate_v1_names.txt \\",
            "  --preflight authoring/batches/batch2500_preflight.json \\",
            "  --manifest miner/output/harvest_manifest_batch5.jsonl \\",
            "  --mentions miner/output/mention_names_batch5.jsonl \\",
            "  --out prelim_testing/tasks_heldout",
            "then filter to T3 with scripts/build_midsize_training.py's bar.",
        ],
        "definitions": entries,
    }, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    names_file = OUT.with_name("heldout_slate_v1_names.txt")
    names_file.write_text("\n".join(picked) + "\n", encoding="utf-8")

    print(f"{len(entries)} definitions reserved -> {OUT}")
    print(f"  names list  -> {names_file}")
    print(f"  shapes: {shapes} (quota {quota})")
    print(f"  namespaces: {len(ns_used)}, max per namespace {max(ns_used.values())}")
    print(f"  expected usable T3 held-out tasks: ~{round(len(entries) * 0.373)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
