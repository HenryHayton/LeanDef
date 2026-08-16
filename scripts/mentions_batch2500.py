"""Build the mentioning-theorem sidecar for the batch-2500 pool.

    uv run python scripts/mentions_batch2500.py

**Why this exists.** `authoring.resolve.make_resolver` reads three committed artifacts, one of
which is the mention sidecar -- the mentioning theorems that are the feedstock for global
theorem-fact anchors. The only sidecars on disk (`mention_names.jsonl`,
`mention_names_batch4.jsonl`, byte-identical) index 727 names: the batch-4 eligible pool. Batch 5
widened the mine to 24 subtrees and its stage-1 script deliberately ran the harvest only, so no
sidecar was ever produced for it.

Of the 693 batch-2500 names that pass preflight, **75 appear in the batch-4 sidecar and 618 do
not**. Authoring those 618 against a missing sidecar is not an error -- `resolve` defaults to an
empty mention list -- so it would have run to completion and quietly produced suites with no
anchor feedstock at all, systematically weaker than batch 200's. That is a silent quality
regression, which is why this runs before authoring rather than after.

This is a text scan (`compute_theorem_mentions` walks the tree once, ~17s, then matches each name
against the declarations), NOT the tier-2 discharge measurement that cost batch 4 seven hours.

Merges into the existing batch-4 sidecar rather than replacing it, so the 75 overlapping names
keep byte-identical records and batch-200 reproductions are unaffected.
"""

import json
import sys
import time
from pathlib import Path

from miner.config import MATHLIB_ROOT
from miner.harvest import compute_theorem_mentions, write_mention_names, MentionRecord

PASSING = Path("authoring/batches/batch2500_passing.txt")
BASE = Path("miner/output/mention_names_batch4.jsonl")
OUT = Path("miner/output/mention_names_batch5.jsonl")


class _Hit:
    """`compute_theorem_mentions` reads only `.name` off each hit (verified by reading it), so a
    full ScanHit -- which would require re-running the miner's scan stage -- is not needed."""

    def __init__(self, name: str):
        self.name = name


def main() -> int:
    names = [n.strip() for n in PASSING.read_text(encoding="utf-8").splitlines() if n.strip()]
    existing = {}
    for line in BASE.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            existing[r["name"]] = [MentionRecord(**m) for m in (r.get("mentions") or [])]

    todo = [n for n in names if n not in existing]
    print(f"{len(names)} passing names; {len(names) - len(todo)} already in the batch-4 sidecar; "
          f"scanning {len(todo)}", flush=True)

    t0 = time.perf_counter()
    fresh = compute_theorem_mentions([_Hit(n) for n in todo], MATHLIB_ROOT)
    print(f"scan done in {(time.perf_counter() - t0) / 60:.1f} min", flush=True)

    merged = dict(existing)
    merged.update(fresh)
    write_mention_names(merged, OUT)

    got = sum(1 for n in todo if fresh.get(n))
    counts = sorted((len(fresh[n]) for n in todo), reverse=True)
    print(f"{got}/{len(todo)} newly-scanned names have >=1 mentioning theorem")
    print(f"mentions per name: max {counts[0] if counts else 0}, "
          f"median {counts[len(counts) // 2] if counts else 0}")
    print(f"-> {OUT} ({len(merged)} names total)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
