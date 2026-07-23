"""One-off orchestration for the batch-4 "wide mine": run the standard harvest pipeline
(scan -> verify with recovery -> gates -> richness -> rank -> curation, all unchanged --
see docs/design/definition_selection_2026-07-21.md) over the expanded corpus, then measure
tier-2 discharge over the resulting eligible set. Kept separate from `miner/harvest.py` rather
than folded into it, since discharge measurement is a one-off addition for this task, not a
standing pipeline stage -- `miner.harvest.harvest()` itself is called unmodified.

Run with: uv run python scripts/run_wide_mine_batch4.py
"""

import time

from harness.repl import get_warm_environment
from harness.results import CheckStatus
from miner import config as miner_cfg
from miner.discharge import (
    DEFAULT_DISCHARGE_OUTPUT_PATH,
    measure_discharge,
    scan_all_theorem_statements,
    write_discharge_manifest,
)
from miner.harvest import harvest


def main() -> None:
    start = time.time()
    records = harvest()
    harvest_elapsed = time.time() - start
    n_eligible = sum(1 for r in records if r.eligible)
    print(f"harvest: {len(records)} candidates scanned, {n_eligible} eligible, {harvest_elapsed:.1f}s", flush=True)

    eligible = [r for r in records if r.eligible]
    theorem_mention_counts = {
        r.name: r.proxies.theorem_mention_count
        for r in eligible
        if r.proxies is not None and r.proxies.theorem_mention_count is not None
    }

    discharge_start = time.time()
    statement_records = scan_all_theorem_statements(miner_cfg.MATHLIB_ROOT)
    server, base_import = get_warm_environment()
    if base_import.status is not CheckStatus.PASSED:
        raise RuntimeError(f"could not warm up Mathlib environment for discharge pass: {base_import.detail}")
    try:
        discharge_results = measure_discharge(
            server, base_import.env, eligible, theorem_mention_counts, statement_records
        )
    finally:
        server.kill()
    write_discharge_manifest(discharge_results, DEFAULT_DISCHARGE_OUTPUT_PATH)
    discharge_elapsed = time.time() - discharge_start
    total_attempted = sum(r.attempted for r in discharge_results)
    total_discharged = sum(r.discharged for r in discharge_results)
    print(
        f"discharge: {len(discharge_results)} definitions measured, "
        f"{total_discharged}/{total_attempted} statements discharged, {discharge_elapsed:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
