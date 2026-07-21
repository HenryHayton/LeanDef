"""Integration test: the full stage-1 pipeline (scan -> verify -> proxies -> rank ->
manifest) over one small real Mathlib module.

Slow (a couple of minutes): a genuine cold Mathlib import against the real project
environment is unavoidable here, since verification queries the live REPL. See
tests/test_miner_scan.py and tests/test_miner_proxies.py for the fast unit tests this one
deliberately doesn't duplicate.

The source file is copied into a scratch "mathlib root" so this test scans exactly one
module rather than all of Data/Nat/ -- but verification still runs against the *real*
project's warm Mathlib environment (via harness.config), since `Nat.dist` needs to actually
exist there regardless of which copy of its source text we scanned it from.
"""

import json
import shutil

from miner import config as miner_cfg
from miner.harvest import harvest


def test_harvest_over_single_module_produces_valid_manifest(tmp_path):
    scratch_root = tmp_path / "mathlib_scratch"
    scan_dir = scratch_root / "Data" / "Nat"
    scan_dir.mkdir(parents=True)
    shutil.copy(miner_cfg.MATHLIB_ROOT / "Data" / "Nat" / "Dist.lean", scan_dir / "Dist.lean")

    output_path = tmp_path / "harvest_manifest.jsonl"
    records = harvest(
        target_dirs=[scan_dir],
        mathlib_root=scratch_root,
        output_path=output_path,
        top_n=10,
    )

    assert len(records) >= 1
    dist_record = next(r for r in records if r.name == "Nat.dist")
    assert dist_record.verified.elaborates
    assert dist_record.verified.executable is True
    assert dist_record.verified.output_decidable_eq is True
    assert dist_record.verified.return_type.strip() in ("ℕ", "Nat")
    assert dist_record.proxies is not None
    assert dist_record.score is not None
    assert dist_record.rank == 1
    assert dist_record.included is True  # the only candidate; trivially inside top_n=10

    assert output_path.exists()
    lines = output_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == len(records)
    for line in lines:
        payload = json.loads(line)
        assert {"name", "module_path", "included", "exclusion_reason", "verified"} <= payload.keys()
