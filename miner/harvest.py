"""Top-level harvest orchestration: scan -> mention counts -> verify -> proxies -> rank ->
manifest. `harvest()` is what both the integration test and `python -m miner.harvest` call.
"""

import subprocess
import time
from pathlib import Path

from harness.repl import get_warm_environment
from harness.results import CheckStatus
from miner import config as miner_cfg
from miner.depindex import build_declaration_index
from miner.gates import GateConfig
from miner.rank import DEFAULT_CURATION_PATH, ManifestRecord, build_manifest, load_curation, write_manifest
from miner.scan import ScanHit, scan_all, scan_theorem_statements
from miner.verify import verify_all_with_recovery

DEFAULT_OUTPUT_PATH = Path(__file__).resolve().parent / "output" / "harvest_manifest.jsonl"


def compute_mention_counts(hits: list[ScanHit], mathlib_root: Path) -> None:
    """Fill in `mention_count` on each hit in place: occurrences of its name in the Mathlib
    source tree, outside its defining module entirely (not even later uses within the same
    file count). Uses `grep` rather than a Python-level scan over ~8800 files -- a
    fixed-string occurrence count across the whole corpus is exactly what `grep -c` does.

    Recorded as metadata only since the 22 July 2026 design-doc revision -- no gate reads this
    field anymore (see `miner.config.THEOREM_MENTION_FLOOR`'s comment for why raw mention-count
    was retired as a gate input).
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


def compute_theorem_mention_counts(hits: list[ScanHit], mathlib_root: Path) -> dict[str, int]:
    """Full-corpus global-supply signal: how many theorem/lemma *statements* (not raw text
    occurrences, not proof bodies) anywhere in Mathlib mention each candidate's name.

    Scans every `.lean` file under `mathlib_root` -- previously scoped only to the scanned
    `TARGET_MODULES` corpus, a known batch-1/2 limitation now fixed per the 22 July 2026
    design-doc revision, since this count now backs a hard gate
    (`miner.config.THEOREM_MENTION_FLOOR`) and a corpus-scoped count would make a candidate's
    eligibility depend on which other corners happened to be scanned alongside it in the same
    run, not on its true full-Mathlib supply. Measured cost: ~2s to scan all ~176k theorem
    statements across ~8300 files, ~10-15s to match ~1000 candidate names against them --
    comfortably cheap next to the REPL-verification stage, so no caching was added.
    """
    statement_texts: list[str] = []
    for path in sorted(mathlib_root.rglob("*.lean")):
        statement_texts.extend(scan_theorem_statements(path.read_text(encoding="utf-8")))

    return {hit.name: sum(1 for s in statement_texts if hit.name in s) for hit in hits}


def harvest(
    target_dirs: list[Path] | None = None,
    mathlib_root: Path | None = None,
    output_path: Path | None = None,
    verify_timeout: float | None = None,
    curation_path: Path | None = None,
    gate_config: GateConfig | None = None,
) -> list[ManifestRecord]:
    """Run the full stage-1 pipeline and write the manifest. Returns the records too, so
    callers (including tests) don't have to re-read the file they just wrote.

    `verify_timeout` is passed through to every REPL call in `miner.verify` (default
    `harness.config.DECIDE_TIMEOUT`, 60s). Worth shortening for a large batch: these are all
    expected to be fast decidable-scale checks, so a much shorter timeout still gives any
    genuinely fine definition plenty of headroom while bounding how long one pathological
    candidate (times a retry) can stall a big run.

    `curation_path` defaults to the committed `miner/curation.yaml` (see `miner.rank`); pass
    an explicit path (or a path to a nonexistent file) to run without the real overrides.

    `gate_config` defaults to the config-module thresholds (see `miner.config`); pass an
    explicit `GateConfig` to override for testing.

    No `top_n`: the manifest is two populations (eligible, ranked in full; excluded, with the
    gate(s) that fired) per the 22 July 2026 design-doc revision, item (c). How many of the
    ranked eligible set to consume is a stage-2 decision, not a mining parameter.
    """
    mathlib_root = mathlib_root if mathlib_root is not None else miner_cfg.MATHLIB_ROOT
    target_dirs = target_dirs if target_dirs is not None else miner_cfg.target_dirs(mathlib_root)
    output_path = output_path if output_path is not None else DEFAULT_OUTPUT_PATH
    curation_path = curation_path if curation_path is not None else DEFAULT_CURATION_PATH
    gate_config = (
        gate_config
        if gate_config is not None
        else GateConfig(
            theorem_mention_floor=miner_cfg.THEOREM_MENTION_FLOOR,
            length_min=miner_cfg.LENGTH_MIN,
            length_max=miner_cfg.LENGTH_MAX,
            docstring_min_length=miner_cfg.DOCSTRING_MIN_LENGTH,
            vocabulary_modules=miner_cfg.COMMON_VOCABULARY_MODULES,
            anti_plumbing_patterns=miner_cfg.ANTI_PLUMBING_PATTERNS,
            richness_floor=miner_cfg.RICHNESS_FLOOR,
        )
    )

    hits = scan_all(target_dirs, mathlib_root)
    compute_mention_counts(hits, mathlib_root)

    theorem_count_start = time.time()
    theorem_counts = compute_theorem_mention_counts(hits, mathlib_root)
    theorem_count_elapsed = time.time() - theorem_count_start

    declaration_index = build_declaration_index(mathlib_root)

    server, base_import = get_warm_environment()
    if base_import.status is not CheckStatus.PASSED:
        raise RuntimeError(f"could not warm up the Mathlib environment: {base_import.detail}")

    verified = verify_all_with_recovery(server, base_import.env, hits, timeout=verify_timeout)

    curation = load_curation(curation_path)
    records = build_manifest(
        verified,
        declaration_index=declaration_index,
        gate_config=gate_config,
        theorem_mention_counts=theorem_counts,
        curation=curation,
    )
    write_manifest(records, output_path)
    print(f"full-corpus theorem-mention scan: {theorem_count_elapsed:.1f}s")
    return records


if __name__ == "__main__":
    result_records = harvest()
    n_eligible = sum(1 for r in result_records if r.eligible)
    print(f"harvested {len(result_records)} candidates, {n_eligible} eligible")
