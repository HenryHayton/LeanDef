"""Mechanical fact-supply proxies -- no LLM, pure heuristics over `VerifiedDef` data.

Estimates, per verified definition, how much material for each of the three fact types
(reward-structure design §2) that object's *facts* could plausibly draw on. This produces no
fact text at all -- only a rough supply estimate to help rank candidates for a later,
LLM-driven stage. Coarse tiers (none | thin | rich) with the raw numbers alongside, per the
task that introduced this module: never just a tier with no way to audit it.

**A `Prop`-valued, decidable definition can legitimately be both casework-rich and
membership-rich at once** (e.g. `Nat.Prime`). This is deliberate, not a bug: at this stage we
only estimate *supply* -- whether the machinery exists to check concrete instances of the
predicate at all. Whether a specific instance ends up authored as a casework fact
(`Nat.Prime 7`, a bare pointwise check) or a membership fact (`Nat.Prime 7` as an "accept"
instance, paired with a tagged "reject" near-miss) is a judgment call about how to *use* that
supply -- made per-fact by the stage-2 fact-authoring agent, not something stage 1's
verification data can or should disambiguate. The two tiers here answer different questions
("can casework work at all" / "can membership classification work at all") that happen to
have the same answer for a decidable predicate.
"""

from dataclasses import dataclass
from enum import Enum

from miner.verify import VerifiedDef

# Types whose canonical-input registry (miner.verify.CANONICAL_INPUTS) supports cheap,
# enumerable trivial cases -- the same set miner.verify can actually construct a canonical
# application for.
_ENUMERABLE_TYPES = frozenset({"ℕ", "Nat", "ℤ", "Int", "Bool", "List ℕ", "List Nat", "List Bool"})

_PREDICATE_RETURN_TYPES = frozenset({"Prop", "Bool"})
_STRUCTURE_HINT_TYPES = ("Finset", "Set", "List", "Multiset")

# Global-supply tier boundaries (raw mention/theorem-mention count). A dial, not a
# commitment -- see docs/design/task_schema_v1.md's own precedent for calling out tunable
# thresholds explicitly rather than burying them.
GLOBAL_THIN_MIN = 1
GLOBAL_RICH_MIN = 5


class SupplyTier(Enum):
    NONE = "none"
    THIN = "thin"
    RICH = "rich"


@dataclass(frozen=True)
class SupplyProxies:
    casework_tier: SupplyTier
    membership_tier: SupplyTier
    global_tier: SupplyTier

    # Raw numbers behind the tiers above, for auditability.
    mention_count: int
    theorem_mention_count: int | None  # None if the refinement (scan_theorem_statements
    # over the scanned corpus) wasn't run for this definition; falls back to mention_count.
    enumerable_arg_count: int
    is_predicate_shaped: bool
    classifies_structure: bool


def _is_concretely_checkable(v: VerifiedDef) -> bool:
    """Whether a concrete instance of this definition can actually be checked -- via either
    of the two mechanisms `miner.verify` measures. Mechanism `eval` (concrete, non-`Prop`
    return type): requires `output_decidable_eq`, since casework/membership facts for these
    compare *output values* for equality. Mechanism `decide` (`Prop`-valued, and Lean's own
    `#eval`-decide-fallback succeeded, i.e. individually decidable in practice): sufficient on
    its own -- `DecidableEq Prop` is not a real instance and was never a meaningful gate here
    (previously this function *did* require it literally, which is why `Nat.Prime` -- despite
    being genuinely decidable -- came out `casework_tier = none` in harvest batch 1)."""
    if v.exec_mechanism == "eval":
        return v.output_decidable_eq is True
    if v.exec_mechanism == "decide":
        return True
    return False


def _casework_tier(v: VerifiedDef) -> SupplyTier:
    if not v.included or not v.elaborates:
        return SupplyTier.NONE
    if not _is_concretely_checkable(v):
        return SupplyTier.NONE
    if not v.explicit_arg_types:
        # A nullary computable constant still gives exactly one case -- thin, not rich:
        # there's no room to spend casework on boundaries or degenerate inputs.
        return SupplyTier.THIN
    if any(t not in _ENUMERABLE_TYPES for t in v.explicit_arg_types):
        return SupplyTier.THIN
    return SupplyTier.RICH


def _is_predicate_shaped(return_type: str) -> bool:
    return return_type.strip() in _PREDICATE_RETURN_TYPES


def _classifies_structure(explicit_arg_types: list[str], return_type: str) -> bool:
    haystack = " ".join([*explicit_arg_types, return_type])
    return any(hint in haystack for hint in _STRUCTURE_HINT_TYPES)


def _membership_tier(v: VerifiedDef) -> tuple[SupplyTier, bool, bool]:
    if not v.included or not v.elaborates:
        return SupplyTier.NONE, False, False
    predicate_shaped = _is_predicate_shaped(v.return_type)
    structure_shaped = _classifies_structure(v.explicit_arg_types, v.return_type)
    if not predicate_shaped and not structure_shaped:
        return SupplyTier.NONE, predicate_shaped, structure_shaped
    if predicate_shaped and _is_concretely_checkable(v):
        return SupplyTier.RICH, predicate_shaped, structure_shaped
    return SupplyTier.THIN, predicate_shaped, structure_shaped


def _global_tier(count: int) -> SupplyTier:
    if count < GLOBAL_THIN_MIN:
        return SupplyTier.NONE
    if count < GLOBAL_RICH_MIN:
        return SupplyTier.THIN
    return SupplyTier.RICH


def compute_proxies(v: VerifiedDef, *, theorem_mention_count: int | None = None) -> SupplyProxies:
    """Compute all three supply proxies for one verified definition. `theorem_mention_count`
    is supplied by the harvest orchestration when available (refined global-supply signal,
    scoped to the scanned corpus -- see `miner.scan.scan_theorem_statements`); falls back to
    the raw `mention_count` from the pre-filter stage when not supplied."""
    casework_tier = _casework_tier(v)
    membership_tier, is_pred, classifies = _membership_tier(v)
    global_count = theorem_mention_count if theorem_mention_count is not None else v.mention_count
    global_tier = _global_tier(global_count)
    enumerable_arg_count = sum(1 for t in v.explicit_arg_types if t in _ENUMERABLE_TYPES)
    return SupplyProxies(
        casework_tier=casework_tier,
        membership_tier=membership_tier,
        global_tier=global_tier,
        mention_count=v.mention_count,
        theorem_mention_count=theorem_mention_count,
        enumerable_arg_count=enumerable_arg_count,
        is_predicate_shaped=is_pred,
        classifies_structure=classifies,
    )
