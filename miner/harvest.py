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
from miner.scan import ScanHit, scan_all, scan_theorem_statements_with_namespace
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
    `TARGET_MODULES` corpus, a known batch-1/2 limitation fixed per the 22 July 2026
    design-doc revision, since this count backs a hard gate
    (`miner.config.THEOREM_MENTION_FLOOR`) and a corpus-scoped count would make a candidate's
    eligibility depend on which other corners happened to be scanned alongside it in the same
    run, not on its true full-Mathlib supply.

    **Namespace-scoped matching (docs/theorem_mention_audit.md H1, fixed here):** a statement
    counts as a mention if it contains the candidate's fully-qualified name *anywhere*, OR its
    bare name from within a namespace block that resolves to that candidate (i.e. the
    statement's own namespace prefix, from `scan_theorem_statements_with_namespace`, equals the
    candidate's). The audit found the qualified-name-only match (the entire count before this
    fix) missed the majority of real mentions, since Lean's own namespace resolution makes
    unqualified reference the *normal* way to mention something from inside its own namespace.
    Deliberately NOT an unscoped bare-name match (a name matching anywhere as a bare
    substring): the audit quantified that as up to 98% collision noise on short, common bare
    names (`pi`, `empty`, `fix`, ...) -- an unscoped bare check would trade one measurement bug
    for a worse one.

    Cost: measured at recount time and reported by the caller; see
    `docs/harvest_review_batch3_revision2.md` for the actual run's timing.
    """
    statement_records: list[tuple[str, str]] = []
    for path in sorted(mathlib_root.rglob("*.lean")):
        statement_records.extend(scan_theorem_statements_with_namespace(path.read_text(encoding="utf-8")))

    counts: dict[str, int] = {}
    for hit in hits:
        qualified = hit.name
        parts = qualified.split(".")
        bare = parts[-1]
        namespace_prefix = ".".join(parts[:-1])
        count = 0
        for statement_text, statement_namespace in statement_records:
            if qualified in statement_text:
                count += 1
            elif namespace_prefix and statement_namespace == namespace_prefix and bare in statement_text:
                count += 1
        counts[hit.name] = count
    return counts


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
