"""Batch-5 wide harvest, stage 1 ONLY: scan -> verify -> gates -> ranked manifest.

    uv run python scripts/run_wide_mine_batch5.py

Differences from `run_wide_mine_batch4.py`, each deliberate:

**No discharge pass.** Batch 4 chained `miner.discharge` (tier-2 tactic measurement over sampled
mentioning theorems) after the harvest; it cost 7+ hours and is capped at 8 by
`DISCHARGE_MAX_WALL_CLOCK_S`. The batch-5 brief is explicit that this task is stage 1 only --
mechanical scan, live-environment verification, gates, ranked manifest, review -- so the
discharge measurement is out of scope and skipped rather than run and ignored.

**Resumable.** Passes `cache_path`, so the ~11h verification pass reuses every record already
held (3,145 from batch 4, seeded) and checkpoints fresh ones every 50 candidates. Killed at hour
9, a re-run resumes from the last chunk instead of starting over. See `miner.verified_cache`.

**Batch 4 is preserved, not overwritten.** Output goes to `harvest_manifest_batch5.jsonl`; the
batch-4 manifest stays readable at its own path for the monotonicity check and delta reporting.

Run under `caffeinate -is` so the laptop does not sleep mid-pass.
"""

import sys
import time
from pathlib import Path

from miner.harvest import harvest
from miner.verified_cache import DEFAULT_CACHE_PATH

OUTPUT_PATH = Path("miner/output/harvest_manifest_batch5.jsonl")


def main() -> int:
    t0 = time.time()

    def progress(done: int, total: int) -> None:
        elapsed = time.time() - t0
        rate = done / max(elapsed, 1e-6)
        remaining = (total - done) / rate if rate else 0.0
        print(f"  verify {done}/{total}  {elapsed/60:.1f} min elapsed  "
              f"{rate:.2f}/s  eta {remaining/3600:.1f}h", flush=True)

    records = harvest(
        output_path=OUTPUT_PATH,
        cache_path=DEFAULT_CACHE_PATH,
        progress=progress,
        # Batch 4 ran at ~3.23s/candidate with the default 60s ceiling; the ceiling only binds on
        # pathological candidates, and lowering it would silently convert "slow but fine" into
        # "does not elaborate". Left at the default deliberately.
    )

    n_eligible = sum(1 for r in records if r.eligible)
    print(f"\nHARVEST DONE {len(records)} candidates, {n_eligible} eligible, "
          f"{(time.time()-t0)/3600:.2f}h", flush=True)
    print(f"manifest: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
