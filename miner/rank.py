"""Ranking, curation, and manifest emission.

Score prefers high in-degree (mention count), low dependency footprint (best-available
proxy: count of referenced constants -- see `miner.verify`'s module docstring for why this
isn't a true dependency-closure size), and breadth across the three supply tiers. Breadth is
a soft, tie-breaking preference only: well-rounded beats lopsided *at equal quality*, but
lopsided-and-excellent survives, per the task that introduced this module. Every component
is stored in the manifest record alongside the final score -- never just a number with no
way to audit it.

After mechanical ranking, `build_manifest` applies human curation overrides (`CurationEntry`,
normally loaded from `miner/curation.yaml` by the harvest orchestrator, not by this module --
see `load_curation`) as a final pass. Every application is recorded on the affected record's
`curation_applied` field, so curation's effect is auditable from the manifest alone.
"""

import json
import math
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path

import yaml

from miner.proxies import SupplyProxies, SupplyTier, compute_proxies
from miner.verify import VerifiedDef

_TIER_VALUE = {SupplyTier.NONE: 0, SupplyTier.THIN: 1, SupplyTier.RICH: 2}

# Weights: quality (tier excellence) dominates; breadth is deliberately the smallest weight
# so it only decides near-ties, not outcomes -- see module docstring.
QUALITY_WEIGHT = 10.0
IN_DEGREE_WEIGHT = 3.0
DEPENDENCY_WEIGHT = 2.0
BREADTH_WEIGHT = 1.0

# Curation `demote`: a fixed penalty subtracted from the sort key only (never from the
# recorded `score.total`, which stays the true, unpenalized value for auditability). A dial,
# not a commitment -- large enough to move a mid-pack entry well down the list, small enough
# that a sufficiently excellent lopsided entry could still survive it, consistent with how
# `BREADTH_WEIGHT` is deliberately small relative to `QUALITY_WEIGHT` above.
DEMOTE_PENALTY = 15.0

DEFAULT_CURATION_PATH = Path(__file__).resolve().parent / "curation.yaml"

_CURATION_ACTIONS = frozenset({"exclude", "demote", "note"})


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
class ScoreComponents:
    quality_score: int  # sum of the three tier values, 0-6
    breadth_score: int  # count of non-NONE tiers, 0-3
    in_degree_raw: int
    in_degree_normalized: float  # log1p(in_degree_raw), compresses outliers
    dependency_raw: int  # len(referenced_constants) -- see miner.verify limitation note
    dependency_normalized: float  # log1p(dependency_raw)
    total: float


def score_definition(proxies: SupplyProxies, dependency_count: int) -> ScoreComponents:
    tiers = (proxies.casework_tier, proxies.membership_tier, proxies.global_tier)
    quality = sum(_TIER_VALUE[t] for t in tiers)
    breadth = sum(1 for t in tiers if t is not SupplyTier.NONE)
    in_degree_raw = (
        proxies.theorem_mention_count if proxies.theorem_mention_count is not None else proxies.mention_count
    )
    in_degree_norm = math.log1p(max(in_degree_raw, 0))
    dep_norm = math.log1p(max(dependency_count, 0))
    total = (
        QUALITY_WEIGHT * quality
        + IN_DEGREE_WEIGHT * in_degree_norm
        - DEPENDENCY_WEIGHT * dep_norm
        + BREADTH_WEIGHT * breadth
    )
    return ScoreComponents(
        quality_score=quality,
        breadth_score=breadth,
        in_degree_raw=in_degree_raw,
        in_degree_normalized=in_degree_norm,
        dependency_raw=dependency_count,
        dependency_normalized=dep_norm,
        total=total,
    )


@dataclass(frozen=True)
class ManifestRecord:
    """One line of the harvest manifest. `included` means "selected into the final top-N
    set," not merely "passed verification" -- a verified-but-low-ranked definition is
    `included=False` with an exclusion_reason explaining it was outranked, not that
    anything about it failed. `curation_applied` is set (to `{"action": ..., "reason": ...}`)
    whenever a `miner/curation.yaml` entry matched this name, regardless of which action --
    including `note`, which otherwise leaves the record untouched."""

    name: str
    module_path: str
    included: bool
    exclusion_reason: str
    rank: int | None  # 1-based rank among verified candidates; None if verification failed
    verified: VerifiedDef
    proxies: SupplyProxies | None
    score: ScoreComponents | None
    curation_applied: dict[str, str] | None = field(default=None)


def build_manifest(
    verified_defs: list[VerifiedDef],
    theorem_mention_counts: dict[str, int] | None = None,
    top_n: int = 100,
    curation: list[CurationEntry] | None = None,
) -> list[ManifestRecord]:
    """`curation` is a list of already-loaded `CurationEntry` (see `load_curation`) -- this
    function does no file I/O itself, so it stays trivially testable without the real
    `miner/curation.yaml` on disk. Pass `None` (the default) for no curation at all."""
    theorem_mention_counts = theorem_mention_counts or {}
    curation_by_name = {c.name: c for c in (curation or [])}

    scored: list[tuple[VerifiedDef, SupplyProxies, ScoreComponents]] = []
    failed_records: list[ManifestRecord] = []

    for v in verified_defs:
        if not v.included:
            failed_records.append(
                ManifestRecord(
                    name=v.name,
                    module_path=v.module_path,
                    included=False,
                    exclusion_reason=v.exclusion_reason,
                    rank=None,
                    verified=v,
                    proxies=None,
                    score=None,
                    curation_applied=_curation_dict(curation_by_name.get(v.name)),
                )
            )
            continue
        proxies = compute_proxies(v, theorem_mention_count=theorem_mention_counts.get(v.name))
        score = score_definition(proxies, dependency_count=len(v.referenced_constants))
        scored.append((v, proxies, score))

    # Curation, final pass: pull "exclude" entries out of the ranking pool entirely (they can
    # never be included, whatever their score); everything else (including "demote" and
    # "note") stays in the pool and gets ranked, with "demote" applying a sort-only penalty.
    curated_excluded: list[ManifestRecord] = []
    remaining: list[tuple[VerifiedDef, SupplyProxies, ScoreComponents]] = []
    for v, proxies, score in scored:
        entry = curation_by_name.get(v.name)
        if entry is not None and entry.action == "exclude":
            curated_excluded.append(
                ManifestRecord(
                    name=v.name,
                    module_path=v.module_path,
                    included=False,
                    exclusion_reason=entry.reason,
                    rank=None,
                    verified=v,
                    proxies=proxies,
                    score=score,
                    curation_applied=_curation_dict(entry),
                )
            )
        else:
            remaining.append((v, proxies, score))

    def sort_key(item: tuple[VerifiedDef, SupplyProxies, ScoreComponents]) -> float:
        v, _, score = item
        entry = curation_by_name.get(v.name)
        penalty = DEMOTE_PENALTY if entry is not None and entry.action == "demote" else 0.0
        return score.total - penalty

    remaining.sort(key=sort_key, reverse=True)

    records: list[ManifestRecord] = []
    for rank, (v, proxies, score) in enumerate(remaining, start=1):
        in_top = rank <= top_n
        records.append(
            ManifestRecord(
                name=v.name,
                module_path=v.module_path,
                included=in_top,
                exclusion_reason="" if in_top else f"ranked {rank}, below top {top_n}",
                rank=rank,
                verified=v,
                proxies=proxies,
                score=score,
                curation_applied=_curation_dict(curation_by_name.get(v.name)),
            )
        )
    records.extend(curated_excluded)
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
