"""Top-level harvest orchestration: scan -> mention counts -> verify -> proxies -> rank ->
manifest. `harvest()` is what both the integration test and `python -m miner.harvest` call.
"""

import collections
import json
import re
import subprocess
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from harness.repl import get_warm_environment
from harness.results import CheckStatus
from miner import config as miner_cfg
from miner.depindex import build_declaration_index
from miner.gates import GateConfig
from miner.rank import DEFAULT_CURATION_PATH, ManifestRecord, build_manifest, load_curation, write_manifest
from miner.scan import ScanHit, scan_all, scan_theorem_declarations_with_namespace, scan_theorem_statements_with_namespace
from miner.verified_cache import load_cache
from miner.verify import verify_all_with_recovery

DEFAULT_OUTPUT_PATH = Path(__file__).resolve().parent / "output" / "harvest_manifest.jsonl"
DEFAULT_MENTION_NAMES_OUTPUT_PATH = Path(__file__).resolve().parent / "output" / "mention_names.jsonl"


# A Lean identifier, dotted components included: `Nat.log`, `Finset.sum`, `x'`, `foo?`.
# Anchored by the character class rather than \b so that `Nat.log` inside `Nat.log_le` yields the
# single token `Nat.log_le`, not a spurious `Nat.log` -- see compute_mention_counts.
_IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_'?!]*(?:\.[A-Za-z_][A-Za-z0-9_'?!]*)*")


def compute_mention_counts(hits: list[ScanHit], mathlib_root: Path) -> None:
    """Fill in `mention_count` on each hit in place: lines mentioning its name anywhere in the
    Mathlib source tree, outside its defining module entirely (not even later uses within the
    same file count).

    Recorded as metadata only since the 22 July 2026 design-doc revision -- no gate reads this
    field anymore (see `miner.config.THEOREM_MENTION_FLOOR`'s comment for why raw mention-count
    was retired as a gate input). That is what makes the two changes below safe: neither can
    move a candidate across a gate, so neither can perturb eligibility or the monotonicity
    invariant.

    **One pass, not one per candidate (batch 5, 10 Aug 2026).** This used to shell out to
    `grep -r -F -c <name>` once PER CANDIDATE -- a full recursive walk of all 8,264 files each
    time, measured at ~0.85s. Batch 4's 3,185 candidates absorbed that (~29 min); batch 5's
    15,387 would have spent ~3.6 HOURS re-walking the same tree, to populate a field no gate
    reads. The corpus is now read once and every candidate counted against it in that single
    pass.

    **Token matching, not substring.** `grep -F` is a substring search, so `Nat.log` matched
    every `Nat.log_le`, `Nat.log_lt_of_lt_pow`, ... and the recorded counts were inflated for
    every name that prefixes a longer sibling -- which in Mathlib's naming convention is most
    of them. Counting identifier TOKENS fixes that. Counts therefore drop relative to batch 4,
    and the drop is a correction rather than a regression; the batch-5 review reports it.
    """
    by_name: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    wanted = {hit.name for hit in hits}
    for path in mathlib_root.rglob("*.lean"):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line in text.splitlines():
            # Per-LINE set: a name used three times on one line is one mentioning line, which is
            # what `grep -c` counted and what the field has always meant.
            for token in set(_IDENT_RE.findall(line)) & wanted:
                by_name[token][str(path)] += 1

    for hit in hits:
        defining_file = str(mathlib_root / hit.module_path)
        counts = by_name.get(hit.name)
        hit.mention_count = 0 if not counts else sum(
            n for path_str, n in counts.items() if path_str != defining_file)


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


@dataclass(frozen=True)
class MentionRecord:
    """One mentioning theorem, for `compute_theorem_mentions` (bundled miner repairs task,
    piece 1). Fully-qualified name + repo-relative source path (under the Mathlib package) +
    the extracted statement text -- everything `compute_theorem_mention_counts` already
    computes internally to decide a match, but previously discarded, keeping only the count."""

    theorem_name: str
    source_file: str
    statement_text: str


@dataclass
class DefinitionMentions:
    """The persisted output for one definition: every mentioning theorem, by name."""

    name: str
    mentions: list[MentionRecord] = field(default_factory=list)


def compute_theorem_mentions(hits: list[ScanHit], mathlib_root: Path) -> dict[str, list[MentionRecord]]:
    """Like `compute_theorem_mention_counts`, but returns the actual mentioning theorem
    records (fully-qualified name, source file, statement text) instead of a bare count --
    bundled miner repairs task, piece 1.

    Uses the identical matching rule `compute_theorem_mention_counts` uses (qualified name
    anywhere in the statement, or bare name from within a matching namespace -- see that
    function's docstring) against the SAME full-corpus scan, so for any hit, `len(mentions) ==
    compute_theorem_mention_counts(...)`'s count for that hit, by construction (both walk the
    same `scan_theorem_declarations_with_namespace` records with the same condition) --
    verified directly, not merely asserted, by the caller that cross-checks this against
    `compute_theorem_mention_counts`'s own count and against the frozen batch-4 manifest (see
    the task report for that verification's results and any individually-explained
    discrepancies against the frozen, pre-parser-fix manifest).

    Kept as its own full-corpus scan (like `miner.discharge.scan_all_theorem_statements`)
    rather than threading through `compute_theorem_mention_counts`'s existing call site, for
    the same reason that module gives: keeping this function's existing signature and callers
    untouched. The extra full-tree scan is cheap (~17s per `docs/harvest_review_batch3.md` §0).
    """
    declarations: list[tuple[str, str, str, str]] = []  # (qualified_name, statement_text, namespace_prefix, source_file)
    for path in sorted(mathlib_root.rglob("*.lean")):
        module_path = str(path.relative_to(mathlib_root))
        for qualified_name, statement_text, namespace_prefix in scan_theorem_declarations_with_namespace(
            path.read_text(encoding="utf-8")
        ):
            declarations.append((qualified_name, statement_text, namespace_prefix, module_path))

    mentions: dict[str, list[MentionRecord]] = {}
    for hit in hits:
        qualified = hit.name
        parts = qualified.split(".")
        bare = parts[-1]
        namespace_prefix = ".".join(parts[:-1])
        records: list[MentionRecord] = []
        for theorem_name, statement_text, statement_namespace, source_file in declarations:
            if qualified in statement_text:
                records.append(MentionRecord(theorem_name, source_file, statement_text))
            elif namespace_prefix and statement_namespace == namespace_prefix and bare in statement_text:
                records.append(MentionRecord(theorem_name, source_file, statement_text))
        mentions[hit.name] = records
    return mentions


def write_mention_names(mentions: dict[str, list[MentionRecord]], output_path: Path) -> None:
    """Write the sidecar `mention_names.jsonl` -- one line per definition, keyed by its
    fully-qualified name (option (a) of the task's two choices: a sidecar file, not a new
    manifest field, so `harvest_manifest.jsonl` -- the frozen batch-4 selection artifact --
    stays byte-identical; see the task report for the reasoning)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for name in sorted(mentions):
            record = DefinitionMentions(name=name, mentions=mentions[name])
            f.write(json.dumps(asdict(record), ensure_ascii=False))
            f.write("\n")


def harvest(
    target_dirs: list[Path] | None = None,
    mathlib_root: Path | None = None,
    output_path: Path | None = None,
    verify_timeout: float | None = None,
    curation_path: Path | None = None,
    gate_config: GateConfig | None = None,
    cache_path: Path | None = None,
    progress=None,
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

    # Batch 5: reuse already-verified records and checkpoint fresh ones. `cache_path=None`
    # (the default) keeps the pre-batch-5 behaviour -- verify everything, checkpoint nothing --
    # so existing callers and tests are unaffected.
    verified_cache = load_cache(cache_path) if cache_path is not None else None
    if verified_cache:
        print(f"verification cache: {len(verified_cache)} records available for reuse", flush=True)

    hits = scan_all(target_dirs, mathlib_root)
    compute_mention_counts(hits, mathlib_root)

    theorem_count_start = time.time()
    theorem_counts = compute_theorem_mention_counts(hits, mathlib_root)
    theorem_count_elapsed = time.time() - theorem_count_start

    declaration_index = build_declaration_index(mathlib_root)

    server, base_import = get_warm_environment()
    if base_import.status is not CheckStatus.PASSED:
        raise RuntimeError(f"could not warm up the Mathlib environment: {base_import.detail}")

    verified = verify_all_with_recovery(
        server, base_import.env, hits, timeout=verify_timeout,
        cache=verified_cache, cache_path=cache_path,
        progress=progress,
    )

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
