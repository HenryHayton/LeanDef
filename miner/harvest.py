"""Top-level harvest orchestration: scan -> mention counts -> verify -> proxies -> rank ->
manifest. `harvest()` is what both the integration test and `python -m miner.harvest` call.
"""

import subprocess
from pathlib import Path

from harness.repl import get_warm_environment
from harness.results import CheckStatus
from miner import config as miner_cfg
from miner.rank import ManifestRecord, build_manifest, write_manifest
from miner.scan import ScanHit, scan_all, scan_theorem_statements
from miner.verify import verify_all_with_recovery

DEFAULT_OUTPUT_PATH = Path(__file__).resolve().parent / "output" / "harvest_manifest.jsonl"


def compute_mention_counts(hits: list[ScanHit], mathlib_root: Path) -> None:
    """Fill in `mention_count` on each hit in place: occurrences of its name in the Mathlib
    source tree, outside its defining module entirely (not even later uses within the same
    file count). Uses `grep` rather than a Python-level scan over ~8800 files -- a
    fixed-string occurrence count across the whole corpus is exactly what `grep -c` does.
    """
    for hit in hits:
        defining_file = mathlib_root / hit.module_path
        try:
            result = subprocess.run(
                ["grep", "-r", "-F", "-c", hit.name, str(mathlib_root)],
                capture_output=True,
                text=True,
                timeout=60,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            hit.mention_count = 0
            continue

        total = 0
        for line in result.stdout.splitlines():
            path_str, sep, count_str = line.rpartition(":")
            if not sep or not count_str.isdigit():
                continue
            if Path(path_str) == defining_file:
                continue
            total += int(count_str)
        hit.mention_count = total


def compute_theorem_mention_counts(hits: list[ScanHit], target_dirs: list[Path]) -> dict[str, int]:
    """Refined global-supply signal: how many theorem/lemma *statements* (not raw text
    occurrences, not proof bodies) mention each candidate's name. Scoped to the same scanned
    corpus as the pre-filter, not the full ~8800-file Mathlib tree -- unlike the raw
    `mention_count`, this one requires parsing theorem statements out of every file, which
    this stage only does for the corners it already reads (see `miner.config.TARGET_MODULES`
    and `miner.scan.scan_theorem_statements`).
    """
    statement_texts: list[str] = []
    for target_dir in target_dirs:
        for path in sorted(target_dir.rglob("*.lean")):
            statement_texts.extend(scan_theorem_statements(path.read_text(encoding="utf-8")))

    return {hit.name: sum(1 for s in statement_texts if hit.name in s) for hit in hits}


def harvest(
    target_dirs: list[Path] | None = None,
    mathlib_root: Path | None = None,
    output_path: Path | None = None,
    top_n: int = 100,
    verify_timeout: float | None = None,
) -> list[ManifestRecord]:
    """Run the full stage-1 pipeline and write the manifest. Returns the records too, so
    callers (including tests) don't have to re-read the file they just wrote.

    `verify_timeout` is passed through to every REPL call in `miner.verify` (default
    `harness.config.DECIDE_TIMEOUT`, 60s). Worth shortening for a large batch: these are all
    expected to be fast decidable-scale checks, so a much shorter timeout still gives any
    genuinely fine definition plenty of headroom while bounding how long one pathological
    candidate (times a retry) can stall a big run.
    """
    mathlib_root = mathlib_root if mathlib_root is not None else miner_cfg.MATHLIB_ROOT
    target_dirs = target_dirs if target_dirs is not None else miner_cfg.target_dirs(mathlib_root)
    output_path = output_path if output_path is not None else DEFAULT_OUTPUT_PATH

    hits = scan_all(target_dirs, mathlib_root)
    compute_mention_counts(hits, mathlib_root)
    theorem_counts = compute_theorem_mention_counts(hits, target_dirs)

    server, base_import = get_warm_environment()
    if base_import.status is not CheckStatus.PASSED:
        raise RuntimeError(f"could not warm up the Mathlib environment: {base_import.detail}")

    verified = verify_all_with_recovery(server, base_import.env, hits, timeout=verify_timeout)

    records = build_manifest(verified, theorem_mention_counts=theorem_counts, top_n=top_n)
    write_manifest(records, output_path)
    return records


if __name__ == "__main__":
    result_records = harvest()
    n_included = sum(1 for r in result_records if r.included)
    print(f"harvested {len(result_records)} candidates, {n_included} in the top set")
