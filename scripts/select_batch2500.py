"""Select the batch-2500 authoring pool from the batch-5 wide-mine manifest.

    uv run python scripts/select_batch2500.py

Same discipline as the 11 Aug batch-200 selection: deterministic, manifest RANK order, no
sampling, and **committed before authoring starts** so the selection cannot be fitted to
results.

Source is `harvest_manifest_batch5.jsonl` (24 widened TARGET_MODULES subtrees, 2609 eligible)
rather than batch 4's 721 -- batch 4's pool is a strict subset of the work already done plus a
tail too small for a run of this size.

**Exclusions are by NAME, from four sources**, because no single one is complete:
  * task directories under `prelim_testing/tasks_batch200/` -- what actually shipped (172)
  * the full 200-name batch-200 list -- catches names ATTEMPTED and rotated, which leave no
    task.json behind and would otherwise be re-authored and re-paid for
  * task directories under `prelim_testing/tasks/` -- the 29 July batch (41)
  * the 29 July 50-name list, same rotation reasoning as above

Batch 5 re-mined from scratch and recomputed ranks, so 172 of its eligible names are definitions
already authored in batch 200; they are removed here, not deduplicated later.
"""

import json
import sys
from pathlib import Path

MANIFEST = Path("miner/output/harvest_manifest_batch5.jsonl")
OUT = Path("authoring/batches/batch2500_2026-08-16.txt")
META = Path("authoring/batches/batch2500_2026-08-16_meta.json")


def _names(path: Path) -> set:
    if not path.exists():
        return set()
    return {n.strip() for n in path.read_text(encoding="utf-8").splitlines()
            if n.strip() and not n.startswith("#")}


def _dirs(path: Path) -> set:
    return {p.name for p in path.iterdir() if p.is_dir()} if path.exists() else set()


def main() -> int:
    sources = {
        "shipped_batch200_dirs": _dirs(Path("prelim_testing/tasks_batch200")),
        "attempted_batch200_list": _names(Path("authoring/batches/batch200_2026-08-11.txt")),
        "shipped_july_dirs": _dirs(Path("prelim_testing/tasks")),
        "attempted_july_list": _names(Path("authoring/batches/batch_2026-07-29.txt")),
    }
    excluded = set().union(*sources.values())

    eligible = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        if d.get("eligible"):
            eligible.append((d["rank"], d["name"]))
    eligible.sort()

    pool = [(r, n) for r, n in eligible if n not in excluded]
    OUT.write_text("\n".join(n for _, n in pool) + "\n", encoding="utf-8")
    META.write_text(json.dumps({
        "generated": "2026-08-16",
        "source_manifest": str(MANIFEST),
        "eligible_total": len(eligible),
        "excluded_total": len({n for _, n in eligible} & excluded),
        "exclusion_sources": {k: len(v) for k, v in sources.items()},
        "pool_after_exclusions": len(pool),
        "rank_min": pool[0][0], "rank_max": pool[-1][0],
        "order": "manifest rank, ascending; no sampling, no cutoff",
    }, indent=1), encoding="utf-8")

    print(f"eligible {len(eligible)} -> pool {len(pool)} "
          f"(ranks {pool[0][0]}..{pool[-1][0]}) -> {OUT}")
    print(f"overlap with already-authored names: "
          f"{len({n for _, n in eligible} & excluded)} removed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
