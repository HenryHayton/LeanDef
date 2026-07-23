"""Resume the tier-2 discharge measurement from wherever `scripts/rerun_discharge_batch4.py`'s
run left off, instead of restarting from scratch -- for continuing past its 8-hour wall-clock
cutoff without throwing away definitions already measured. Reads the existing
`miner/output/discharge_manifest.jsonl`, keeps every already-measured definition's line
verbatim, and measures only the eligible definitions not yet covered, under a fresh
`extra_wall_clock_s` budget (default: 2 hours, passed via `RESUME_WALL_CLOCK_S` below since
this is a one-off script, not a standing config value). Same progress logging and per-step
disk writes as the original script.

Run with: uv run python scripts/resume_discharge_batch4.py
"""

import json
import time
from dataclasses import asdict

from harness.repl import get_warm_environment
from harness.results import CheckStatus
from miner import config as miner_cfg
from miner.discharge import DEFAULT_DISCHARGE_OUTPUT_PATH, measure_discharge, scan_all_theorem_statements
from miner.harvest import DEFAULT_OUTPUT_PATH
from miner.rank import ManifestRecord
from scripts.rerun_discharge_batch4 import _load_eligible

DISCHARGE_OUTPUT_PATH = DEFAULT_DISCHARGE_OUTPUT_PATH
RESUME_WALL_CLOCK_S = 2 * 60 * 60.0  # 2 more hours, per this task's own instruction


def _load_already_covered(path) -> dict[str, str]:
    """name -> raw JSON line (kept verbatim, never re-parsed into dataclasses -- there is
    nothing to change about an already-measured definition's record)."""
    covered: dict[str, str] = {}
    if not path.is_file():
        return covered
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            data = json.loads(line)
            covered[data["name"]] = line
    return covered


def main() -> None:
    already_covered = _load_already_covered(DISCHARGE_OUTPUT_PATH)
    print(f"{len(already_covered)} definitions already measured, kept as-is", flush=True)

    eligible, theorem_mention_counts = _load_eligible(DEFAULT_OUTPUT_PATH)
    remaining: list[ManifestRecord] = [r for r in eligible if r.name not in already_covered]
    print(f"{len(remaining)} of {len(eligible)} eligible definitions remain to measure", flush=True)
    print(f"config: DISCHARGE_TACTIC_TIMEOUT={miner_cfg.DISCHARGE_TACTIC_TIMEOUT}s RESUME_WALL_CLOCK_S={RESUME_WALL_CLOCK_S}s", flush=True)

    if not remaining:
        print("nothing left to measure", flush=True)
        return

    statement_records = scan_all_theorem_statements(miner_cfg.MATHLIB_ROOT)
    server, base_import = get_warm_environment()
    if base_import.status is not CheckStatus.PASSED:
        raise RuntimeError(f"could not warm up Mathlib environment: {base_import.detail}")

    new_lines: list[str] = []
    start = time.monotonic()

    def _write_combined() -> None:
        DISCHARGE_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with DISCHARGE_OUTPUT_PATH.open("w", encoding="utf-8") as f:
            for line in already_covered.values():
                f.write(line + "\n")
            for line in new_lines:
                f.write(line + "\n")

    def on_progress(index, total, result):
        new_lines.append(json.dumps(asdict(result), ensure_ascii=False))
        _write_combined()  # resilience: write every step
        elapsed = time.monotonic() - start
        print(
            f"[{elapsed:8.1f}s] {index}/{total} {result.name!r}: {result.discharged}/{result.attempted} discharged",
            flush=True,
        )

    try:
        results = measure_discharge(
            server, base_import.env, remaining, theorem_mention_counts, statement_records,
            max_wall_clock_s=RESUME_WALL_CLOCK_S, on_progress=on_progress,
        )
    finally:
        server.kill()
    _write_combined()

    print(
        f"resume pass: {len(results)}/{len(remaining)} newly measured "
        f"({len(already_covered) + len(results)}/{len(eligible)} total)",
        flush=True,
    )


if __name__ == "__main__":
    main()
