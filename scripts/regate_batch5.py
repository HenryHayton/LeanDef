"""Re-gate the harvest from RECORDED metadata -- no Lean, no re-scan, no re-verification.

    uv run python scripts/regate_batch5.py --out miner/output/harvest_manifest_batch5.jsonl

This is the "one expensive pass, cheap iterations after" half of the batch-5 brief. Verification
is the only step that needs a REPL; gates read fields already on `VerifiedDef`, so a vocabulary
change (or any other gate-config change) is answerable in minutes from `miner/output/
verified_cache.jsonl` alone.

Deliberately REPL-free rather than "harvest() with a warm cache": `harvest()` calls
`get_warm_environment()` unconditionally, which would hold ~5.7GB for a pass that needs none of
it -- unaffordable while the tier-5 check phase holds its own Mathlib server on the same laptop.
"""

import argparse
import collections
import json
import sys
import time
from pathlib import Path

from miner import config as miner_cfg
from miner.depindex import build_declaration_index
from miner.gates import GateConfig
from miner.harvest import compute_theorem_mention_counts
from miner.rank import DEFAULT_CURATION_PATH, build_manifest, load_curation, write_manifest
from miner.scan import scan_all
from miner.verified_cache import cache_key, load_cache


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="miner/output/harvest_manifest_batch5.jsonl")
    ap.add_argument("--compare", default=None,
                    help="manifest to diff against (reports recovered/lost eligibility)")
    args = ap.parse_args()
    t0 = time.time()

    cache = load_cache()
    hits = scan_all(miner_cfg.target_dirs(), miner_cfg.MATHLIB_ROOT)
    verified, missing = [], 0
    for hit in hits:
        rec = cache.get(cache_key(hit.name, hit.module_path, hit.source_text))
        if rec is None:
            missing += 1
            continue
        verified.append(rec)
    print(f"{len(verified)} verified records from cache ({missing} scan hits not cached -- "
          f"re-run the harvest if this is not 0)", flush=True)

    theorem_counts = compute_theorem_mention_counts(hits, miner_cfg.MATHLIB_ROOT)
    records = build_manifest(
        verified,
        declaration_index=build_declaration_index(miner_cfg.MATHLIB_ROOT),
        gate_config=GateConfig(
            theorem_mention_floor=miner_cfg.THEOREM_MENTION_FLOOR,
            length_min=miner_cfg.LENGTH_MIN,
            length_max=miner_cfg.LENGTH_MAX,
            docstring_min_length=miner_cfg.DOCSTRING_MIN_LENGTH,
            vocabulary_modules=miner_cfg.COMMON_VOCABULARY_MODULES,
            anti_plumbing_patterns=miner_cfg.ANTI_PLUMBING_PATTERNS,
            richness_floor=miner_cfg.RICHNESS_FLOOR,
        ),
        theorem_mention_counts=theorem_counts,
        curation=load_curation(DEFAULT_CURATION_PATH),
    )

    eligible = [r for r in records if r.eligible]
    print(f"{len(records)} records, {len(eligible)} eligible  ({time.time()-t0:.0f}s)")

    if args.compare and Path(args.compare).exists():
        before = {}
        for line in Path(args.compare).read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                before[(r["name"], r["module_path"])] = r["eligible"]
        now = {(r.name, r.module_path): r.eligible for r in records}
        recovered = [k for k, v in now.items() if v and not before.get(k, False)]
        lost = [k for k, v in before.items() if v and not now.get(k, False)]
        print(f"vs {args.compare}: +{len(recovered)} recovered, -{len(lost)} lost")
        by_area = collections.Counter(k[1].split("/")[0] for k in recovered)
        for a, n in by_area.most_common(12):
            print(f"   +{n:<5} {a}")
        for k in lost[:10]:
            print(f"   LOST {k[0]}")

    write_manifest(records, Path(args.out))
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
