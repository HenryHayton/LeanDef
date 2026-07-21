"""Ranking and manifest emission.

Score prefers high in-degree (mention count), low dependency footprint (best-available
proxy: count of referenced constants -- see `miner.verify`'s module docstring for why this
isn't a true dependency-closure size), and breadth across the three supply tiers. Breadth is
a soft, tie-breaking preference only: well-rounded beats lopsided *at equal quality*, but
lopsided-and-excellent survives, per the task that introduced this module. Every component
is stored in the manifest record alongside the final score -- never just a number with no
way to audit it.
"""

import json
import math
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path

from miner.proxies import SupplyProxies, SupplyTier, compute_proxies
from miner.verify import VerifiedDef

_TIER_VALUE = {SupplyTier.NONE: 0, SupplyTier.THIN: 1, SupplyTier.RICH: 2}

# Weights: quality (tier excellence) dominates; breadth is deliberately the smallest weight
# so it only decides near-ties, not outcomes -- see module docstring.
QUALITY_WEIGHT = 10.0
IN_DEGREE_WEIGHT = 3.0
DEPENDENCY_WEIGHT = 2.0
BREADTH_WEIGHT = 1.0


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
    anything about it failed."""

    name: str
    module_path: str
    included: bool
    exclusion_reason: str
    rank: int | None  # 1-based rank among verified candidates; None if verification failed
    verified: VerifiedDef
    proxies: SupplyProxies | None
    score: ScoreComponents | None


def build_manifest(
    verified_defs: list[VerifiedDef],
    theorem_mention_counts: dict[str, int] | None = None,
    top_n: int = 100,
) -> list[ManifestRecord]:
    theorem_mention_counts = theorem_mention_counts or {}
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
                )
            )
            continue
        proxies = compute_proxies(v, theorem_mention_count=theorem_mention_counts.get(v.name))
        score = score_definition(proxies, dependency_count=len(v.referenced_constants))
        scored.append((v, proxies, score))

    scored.sort(key=lambda t: t[2].total, reverse=True)

    records: list[ManifestRecord] = []
    for rank, (v, proxies, score) in enumerate(scored, start=1):
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
            )
        )
    records.extend(failed_records)
    return records


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
