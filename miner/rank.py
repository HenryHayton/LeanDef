"""Gates-then-preference-score selection and manifest emission (design doc
`docs/design/definition_selection_2026-07-21.md`).

Replaces miner stage 1's single weighted score (quality/in-degree/dependency-footprint) with
two mechanisms that cannot compensate for one another: `miner.gates`' six hard eligibility
gates define the includable set (every exclusion records which gate(s) fired); a small
preference score, dominated by structural richness (`miner.richness`), orders only what
survives the gates. Every component is stored in the manifest record alongside the final
score -- never just a number with no way to audit it.
"""

import json
import math
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path

import yaml

from miner.gates import GateConfig, evaluate_gates
from miner.proxies import SupplyProxies, SupplyTier, compute_proxies
from miner.richness import RichnessComponents, compute_richness
from miner.verify import VerifiedDef

_TIER_VALUE = {SupplyTier.NONE: 0, SupplyTier.THIN: 1, SupplyTier.RICH: 2}

# Preference-score weights, in the order design doc §4 specifies: structural richness
# dominant, docstring substance second, supply breadth third as a soft tie-break only.
RICHNESS_WEIGHT = 10.0
DOCSTRING_WEIGHT = 2.0
BREADTH_WEIGHT = 1.0

# Curation `demote`: a fixed penalty subtracted from the sort key only (never from the
# recorded `score.total`, which stays the true, unpenalized value for auditability).
DEMOTE_PENALTY = 15.0

DEFAULT_CURATION_PATH = Path(__file__).resolve().parent / "curation.yaml"

_CURATION_ACTIONS = frozenset({"exclude", "demote", "note"})

# Docstring-substance heuristic (design §4, item 2): beyond the docstring floor gate, prefer
# docstrings whose prose states a condition or convention, not just a name restated. This
# list is deliberately small and English-prose-specific -- a dial to expand, not a claim of
# completeness.
DOCSTRING_CONDITION_MARKERS: tuple[str, ...] = (
    "if ",
    "when ",
    "unless",
    "provided",
    "assum",
    "convention",
    "condition",
    "note that",
    "otherwise",
    "undefined",
    "requires",
)


@dataclass(frozen=True)
class CurationEntry:
    name: str
    action: str  # "exclude" | "demote" | "note"
    reason: str


def load_curation(path: Path | None = None) -> list[CurationEntry]:
    """Load curation overrides from a YAML file (see `miner/curation.yaml` for the format
    and the currently-seeded entries). Returns an empty list if the file doesn't exist --
    curation is optional, not a hard dependency of the pipeline."""
    path = path if path is not None else DEFAULT_CURATION_PATH
    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    entries = []
    for raw in data.get("entries", []):
        action = raw["action"]
        if action not in _CURATION_ACTIONS:
            raise ValueError(f"{path}: unknown curation action {action!r} for {raw.get('name')!r}")
        entries.append(CurationEntry(name=raw["name"], action=action, reason=raw["reason"].strip()))
    return entries


@dataclass(frozen=True)
class DocstringSubstance:
    length_beyond_floor: int
    condition_markers: int
    score: float  # log1p(length_beyond_floor) + condition_markers


def compute_docstring_substance(docstring: str | None, floor: int) -> DocstringSubstance:
    """Docstring-substance component (design §4, item 2). `floor` is `DOCSTRING_MIN_LENGTH`
    (the gate threshold) -- length credit only accrues *beyond* what the gate already
    requires, so a docstring that barely clears the gate scores near zero here, and the
    condition-marker bonus rewards prose that states a side condition/convention regardless of
    raw length."""
    if not docstring:
        return DocstringSubstance(0, 0, 0.0)
    normalized = " ".join(docstring.split())
    length_beyond_floor = max(0, len(normalized) - floor)
    lowered = normalized.lower()
    condition_markers = sum(1 for marker in DOCSTRING_CONDITION_MARKERS if marker in lowered)
    score = math.log1p(length_beyond_floor) + condition_markers
    return DocstringSubstance(length_beyond_floor, condition_markers, score)


@dataclass(frozen=True)
class ScoreComponents:
    richness_total: int
    docstring_substance: float
    breadth_score: int  # count of non-NONE supply tiers, 0-3
    total: float


def score_definition(richness: RichnessComponents, docstring_substance: DocstringSubstance, proxies: SupplyProxies) -> ScoreComponents:
    tiers = (proxies.casework_tier, proxies.membership_tier, proxies.global_tier)
    breadth = sum(1 for t in tiers if t is not SupplyTier.NONE)
    total = RICHNESS_WEIGHT * richness.total + DOCSTRING_WEIGHT * docstring_substance.score + BREADTH_WEIGHT * breadth
    return ScoreComponents(
        richness_total=richness.total,
        docstring_substance=docstring_substance.score,
        breadth_score=breadth,
        total=total,
    )


@dataclass(frozen=True)
class ManifestRecord:
    """One line of the harvest manifest. `included` means "passed every gate and was selected
    into the final top-N set," not merely "passed verification" -- a verified candidate can be
    `included=False` either because it failed one or more gates (`gates_failed` non-empty) or
    because it was outranked among gate-survivors (`gates_failed` empty, `exclusion_reason`
    names the rank cutoff instead). `curation_applied` is set whenever a `miner/curation.yaml`
    entry matched this name, regardless of action -- including `note`, which otherwise leaves
    the record untouched."""

    name: str
    module_path: str
    included: bool
    exclusion_reason: str
    gates_failed: list[str]
    rank: int | None  # 1-based rank among gate-eligible candidates; None if excluded
    verified: VerifiedDef
    proxies: SupplyProxies | None
    richness: RichnessComponents | None
    docstring_substance: DocstringSubstance | None
    score: ScoreComponents | None
    curation_applied: dict[str, str] | None = field(default=None)


def build_manifest(
    verified_defs: list[VerifiedDef],
    declaration_index: dict[str, str],
    gate_config: GateConfig,
    theorem_mention_counts: dict[str, int] | None = None,
    top_n: int = 100,
    curation: list[CurationEntry] | None = None,
) -> list[ManifestRecord]:
    """`curation` is a list of already-loaded `CurationEntry` (see `load_curation`) -- this
    function does no file I/O itself, so it stays trivially testable. Pass `None` (the
    default) for no curation at all."""
    theorem_mention_counts = theorem_mention_counts or {}
    curation_by_name = {c.name: c for c in (curation or [])}

    eligible: list[tuple[VerifiedDef, SupplyProxies, RichnessComponents, DocstringSubstance, ScoreComponents]] = []
    gate_excluded: list[ManifestRecord] = []
    failed_records: list[ManifestRecord] = []

    for v in verified_defs:
        if not v.included:
            failed_records.append(
                ManifestRecord(
                    name=v.name,
                    module_path=v.module_path,
                    included=False,
                    exclusion_reason=v.exclusion_reason,
                    gates_failed=[],
                    rank=None,
                    verified=v,
                    proxies=None,
                    richness=None,
                    docstring_substance=None,
                    score=None,
                    curation_applied=_curation_dict(curation_by_name.get(v.name)),
                )
            )
            continue

        proxies = compute_proxies(v, theorem_mention_count=theorem_mention_counts.get(v.name))
        richness = compute_richness(v)
        docstring_substance = compute_docstring_substance(v.docstring, gate_config.docstring_min_length)
        score = score_definition(richness, docstring_substance, proxies)
        gates_failed = evaluate_gates(v, proxies, declaration_index, gate_config)

        if gates_failed:
            gate_excluded.append(
                ManifestRecord(
                    name=v.name,
                    module_path=v.module_path,
                    included=False,
                    exclusion_reason=f"failed gate(s): {', '.join(gates_failed)}",
                    gates_failed=gates_failed,
                    rank=None,
                    verified=v,
                    proxies=proxies,
                    richness=richness,
                    docstring_substance=docstring_substance,
                    score=score,
                    curation_applied=_curation_dict(curation_by_name.get(v.name)),
                )
            )
            continue

        eligible.append((v, proxies, richness, docstring_substance, score))

    # Curation, final pass: pull "exclude" entries out of the eligible pool entirely (they can
    # never be included, whatever their score); "demote" and "note" stay in the pool, with
    # "demote" applying a sort-only penalty.
    curated_excluded: list[ManifestRecord] = []
    remaining: list[tuple[VerifiedDef, SupplyProxies, RichnessComponents, DocstringSubstance, ScoreComponents]] = []
    for v, proxies, richness, docstring_substance, score in eligible:
        entry = curation_by_name.get(v.name)
        if entry is not None and entry.action == "exclude":
            curated_excluded.append(
                ManifestRecord(
                    name=v.name,
                    module_path=v.module_path,
                    included=False,
                    exclusion_reason=entry.reason,
                    gates_failed=[],
                    rank=None,
                    verified=v,
                    proxies=proxies,
                    richness=richness,
                    docstring_substance=docstring_substance,
                    score=score,
                    curation_applied=_curation_dict(entry),
                )
            )
        else:
            remaining.append((v, proxies, richness, docstring_substance, score))

    def sort_key(item: tuple[VerifiedDef, SupplyProxies, RichnessComponents, DocstringSubstance, ScoreComponents]) -> float:
        v, _, _, _, score = item
        entry = curation_by_name.get(v.name)
        penalty = DEMOTE_PENALTY if entry is not None and entry.action == "demote" else 0.0
        return score.total - penalty

    remaining.sort(key=sort_key, reverse=True)

    records: list[ManifestRecord] = []
    for rank, (v, proxies, richness, docstring_substance, score) in enumerate(remaining, start=1):
        in_top = rank <= top_n
        records.append(
            ManifestRecord(
                name=v.name,
                module_path=v.module_path,
                included=in_top,
                exclusion_reason="" if in_top else f"ranked {rank}, below top {top_n}",
                gates_failed=[],
                rank=rank,
                verified=v,
                proxies=proxies,
                richness=richness,
                docstring_substance=docstring_substance,
                score=score,
                curation_applied=_curation_dict(curation_by_name.get(v.name)),
            )
        )
    records.extend(curated_excluded)
    records.extend(gate_excluded)
    records.extend(failed_records)
    return records


def _curation_dict(entry: CurationEntry | None) -> dict[str, str] | None:
    if entry is None:
        return None
    return {"action": entry.action, "reason": entry.reason}


def _json_default(obj: object):
    if isinstance(obj, Enum):
        return obj.value
    raise TypeError(f"not JSON serializable: {obj!r}")


def write_manifest(records: list[ManifestRecord], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(asdict(record), default=_json_default, ensure_ascii=False))
            f.write("\n")
