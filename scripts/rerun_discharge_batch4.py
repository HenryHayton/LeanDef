"""Re-run just the tier-2 discharge measurement against the already-computed batch-4 harvest
manifest (`miner/output/harvest_manifest.jsonl`) -- no need to redo the ~2.6-hour scan/verify
pass, since nothing about it is affected by the discharge-side recovery fix. Throwaway,
one-off script for this task; not a standing pipeline entry point.

Meant to run unattended overnight: logs progress after every definition (flushed immediately),
writes the accumulated manifest to disk after every definition too (not just at the end), and
passes `miner.config.DISCHARGE_MAX_WALL_CLOCK_S` through so the run is guaranteed to stop and
leave a usable (possibly partial) manifest rather than running indefinitely -- see
`miner.discharge`'s module docstring for why both of these were added after the first,
30s-per-tactic attempt ran past 7 hours without finishing.

Run with: uv run python scripts/rerun_discharge_batch4.py
"""

import json
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
from miner.harvest import DEFAULT_OUTPUT_PATH
from miner.rank import ManifestRecord
from miner.verify import VerifiedDef


def _load_eligible(path) -> tuple[list[ManifestRecord], dict[str, int]]:
    """Returns `(eligible_records, theorem_mention_counts)`. `measure_discharge` only ever
    reads `record.name` off each `ManifestRecord` (see its own signature) -- everything else
    on a real `ManifestRecord` is reconstructed here as a placeholder rather than faithfully
    round-tripped from the manifest JSON, since none of it is used downstream of this script."""
    records = []
    counts: dict[str, int] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            if not data["eligible"]:
                continue
            proxies_data = data.get("proxies")
            if proxies_data is not None and proxies_data.get("theorem_mention_count") is not None:
                counts[data["name"]] = proxies_data["theorem_mention_count"]
            records.append(
                ManifestRecord(
                    name=data["name"],
                    module_path=data["module_path"],
                    eligible=True,
                    exclusion_reason="",
                    gates_failed=[],
                    rank=data["rank"],
                    return_shape=data["return_shape"],
                    verified=VerifiedDef(
                        name=data["name"], module_path=data["module_path"], source_text="", docstring=None,
                        mention_count=0, included=True,
                    ),
                    proxies=None,
                    richness=None,
                    docstring_substance=None,
                    score=None,
                )
            )
    return records, counts


def main() -> None:
    eligible, theorem_mention_counts = _load_eligible(DEFAULT_OUTPUT_PATH)
    print(f"loaded {len(eligible)} eligible records from {DEFAULT_OUTPUT_PATH}", flush=True)
    print(
        f"config: DISCHARGE_TACTIC_TIMEOUT={miner_cfg.DISCHARGE_TACTIC_TIMEOUT}s "
        f"DISCHARGE_MAX_WALL_CLOCK_S={miner_cfg.DISCHARGE_MAX_WALL_CLOCK_S}s "
        f"DISCHARGE_SAMPLE_SIZE={miner_cfg.DISCHARGE_SAMPLE_SIZE}",
        flush=True,
    )

    statement_records = scan_all_theorem_statements(miner_cfg.MATHLIB_ROOT)
    server, base_import = get_warm_environment()
    if base_import.status is not CheckStatus.PASSED:
        raise RuntimeError(f"could not warm up Mathlib environment: {base_import.detail}")

    accumulated: list = []
    start = time.monotonic()

    def on_progress(index, total, result):
        accumulated.append(result)
        write_discharge_manifest(accumulated, DEFAULT_DISCHARGE_OUTPUT_PATH)  # resilience: write every step
        elapsed = time.monotonic() - start
        running_discharged = sum(r.discharged for r in accumulated)
        running_attempted = sum(r.attempted for r in accumulated)
        print(
            f"[{elapsed:8.1f}s] {index}/{total} {result.name!r}: "
            f"{result.discharged}/{result.attempted} discharged "
            f"(running total: {running_discharged}/{running_attempted})",
            flush=True,
        )

    try:
        results = measure_discharge(
            server, base_import.env, eligible, theorem_mention_counts, statement_records,
            on_progress=on_progress,
        )
    finally:
        server.kill()
    write_discharge_manifest(results, DEFAULT_DISCHARGE_OUTPUT_PATH)

    total_attempted = sum(r.attempted for r in results)
    total_discharged = sum(r.discharged for r in results)
    print(
        f"discharge: {len(results)}/{len(eligible)} eligible definitions measured, "
        f"{total_discharged}/{total_attempted} statements discharged",
        flush=True,
    )


if __name__ == "__main__":
    main()
