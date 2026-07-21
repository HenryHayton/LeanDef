"""Hard eligibility gates (design doc `docs/design/definition_selection_2026-07-21.md` §3).

Replaces the score-dominant logic that used to live in `miner/rank.py` in miner stage 1
(quality/in-degree/dependency-footprint as additive weights). Gates are yes/no tests applied
*before* any preference score: a candidate failing any gate is excluded outright, and every
exclusion records which gate(s) fired -- no metric can compensate for another, per the design
doc's §2 rationale. Ranking among gate-survivors is `miner.rank`'s job; this module only ever
decides in or out.
"""

import re
from dataclasses import dataclass

from miner.proxies import SupplyProxies, SupplyTier
from miner.verify import VerifiedDef

_BLOCK_COMMENT_RE = re.compile(r"/-.*?-/", re.DOTALL)
_LINE_COMMENT_RE = re.compile(r"--.*")
_WHITESPACE_RE = re.compile(r"\s+")

# Markers a binder's type text can contain that make it read as a hypothesis/side-condition
# rather than plain data -- see `miner.richness`'s hypothesis-binder component, which reuses
# this same list; kept here since it's a property of binder *type text*, not of richness
# counting specifically, and both gates.py's docstring floor and richness draw on it.
_PROP_TYPE_MARKERS = ("∈", "∉", "∀", "∃", "∧", "∨", "¬", "≤", "≥", "<", ">", "≠", "∣", "=", "↔", "→", "Prop")


def looks_like_prop_type(type_text: str) -> bool:
    """Cheap textual heuristic for "this binder's type is a proposition, not plain data" --
    used to count hypothesis binders (design §4.1) without needing the elaborator's sort
    judgement for every binder. False positives/negatives exist (e.g. a `→` inside a plain
    function-typed argument like `f : α → β` also matches, so a *data* argument that happens
    to be a function type is miscounted as a hypothesis); accepted for v1, see
    `miner.richness`'s module docstring for the fuller blind-spot list."""
    return any(marker in type_text for marker in _PROP_TYPE_MARKERS)


def normalize_body(source_text: str) -> str:
    """Strip Lean comments (block `/- ... -/` and line `-- ...`) and collapse all whitespace
    runs to a single space. Used for the length-band gate's character count and as the shared
    starting point for `miner.richness`'s structural counts, so both measurements agree on
    what "the definition body" means. Collapsing whitespace means the exact count of internal
    blank lines/indentation is not preserved -- deliberate, since those are formatting, not
    content, and would otherwise make length an accident of how the original file was
    line-wrapped."""
    text = _BLOCK_COMMENT_RE.sub("", source_text)
    text = _LINE_COMMENT_RE.sub("", text)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text


def bare_name(name: str) -> str:
    """The last dotted component of a fully-qualified name, e.g. `digitsAux1` from
    `Nat.digitsAux1`. Anti-plumbing patterns match against this, not the full path, so a
    legitimately-named namespace (`Nat`) can't accidentally trigger a suffix pattern meant for
    the leaf name."""
    return name.rsplit(".", 1)[-1]


# --- Individual gates -- each returns True if the candidate PASSES. ---


def mention_floor_gate(v: VerifiedDef, floor: int) -> bool:
    """(a) Full-corpus mentions >= floor. Applied to `mention_count` (the raw, full-Mathlib-
    tree occurrence count), not `theorem_mention_count` (scoped only to the scanned corpus --
    see `miner.config.MENTION_FLOOR`'s comment for why)."""
    return v.mention_count >= floor


def length_band_gate(v: VerifiedDef, length_min: int, length_max: int) -> bool:
    """(b) Normalized body length in `[length_min, length_max]`."""
    length = len(normalize_body(v.source_text))
    return length_min <= length <= length_max


def docstring_floor_gate(v: VerifiedDef, min_length: int) -> bool:
    """(c) A docstring must exist and exceed `min_length` characters after whitespace
    normalization."""
    if not v.docstring:
        return False
    return len(_WHITESPACE_RE.sub(" ", v.docstring).strip()) >= min_length


def dependency_vocabulary_gate(
    v: VerifiedDef, declaration_index: dict[str, str], vocabulary_modules: list[str]
) -> bool:
    """(d) Every referenced constant that resolves to a known module must resolve to a module
    under one of `vocabulary_modules` (directory-prefix match). A reference that resolves to
    no module at all (common -- `referenced_constants` includes local bound-variable noise,
    see `miner.verify`'s module docstring) does not count against the candidate: this gate's
    job is to catch exotic *infrastructure*, not to penalize the extraction step's own known
    imprecision."""
    for ref in v.referenced_constants:
        module_path = declaration_index.get(ref)
        if module_path is None:
            continue
        if not any(module_path == prefix or module_path.startswith(prefix + "/") for prefix in vocabulary_modules):
            return False
    return True


def anti_plumbing_gate(v: VerifiedDef, patterns: list[str]) -> bool:
    """(e) The bare name must not match any anti-plumbing pattern."""
    leaf = bare_name(v.name)
    return not any(re.search(pattern, leaf) for pattern in patterns)


def fact_supply_gate(proxies: SupplyProxies) -> bool:
    """(f) At least one of the three supply tiers must be non-`none`."""
    return any(
        tier is not SupplyTier.NONE for tier in (proxies.casework_tier, proxies.membership_tier, proxies.global_tier)
    )


_GATE_NAMES = (
    "mention_floor",
    "length_band",
    "docstring_floor",
    "dependency_vocabulary",
    "anti_plumbing",
    "fact_supply",
)


@dataclass(frozen=True)
class GateConfig:
    mention_floor: int
    length_min: int
    length_max: int
    docstring_min_length: int
    vocabulary_modules: list[str]
    anti_plumbing_patterns: list[str]


def evaluate_gates(
    v: VerifiedDef,
    proxies: SupplyProxies,
    declaration_index: dict[str, str],
    config: GateConfig,
) -> list[str]:
    """Evaluate all six gates and return the names of every gate that FAILED (empty list ==
    passes all six, i.e. eligible). Every gate is always evaluated, even after an earlier one
    has already failed, so the manifest can record every reason a candidate was excluded, not
    just the first one found."""
    failed: list[str] = []
    if not mention_floor_gate(v, config.mention_floor):
        failed.append("mention_floor")
    if not length_band_gate(v, config.length_min, config.length_max):
        failed.append("length_band")
    if not docstring_floor_gate(v, config.docstring_min_length):
        failed.append("docstring_floor")
    if not dependency_vocabulary_gate(v, declaration_index, config.vocabulary_modules):
        failed.append("dependency_vocabulary")
    if not anti_plumbing_gate(v, config.anti_plumbing_patterns):
        failed.append("anti_plumbing")
    if not fact_supply_gate(proxies):
        failed.append("fact_supply")
    return failed
