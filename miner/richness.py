"""Structural richness (design doc `docs/design/definition_selection_2026-07-21.md` §4.1) --
the dominant term of the preference score.

A count, over the normalized definition body and its parsed binders, of conjunctions,
disjunctions, conditionals, quantifiers, comparison/inequality operators, and hypothesis
binders. This is a near-direct measurement of how many distinguishable ways a candidate
definition can be *wrong* -- a dropped conjunct, a flipped inequality, a missing side
condition are exactly the misreading classes the verifier's mutant suites exist to catch (see
`docs/design/verifier_architecture_2026-07-20.md` §2) -- and it directly attacks the
delegation problem the old dependency-count score approximated badly: a pure delegation
(`toFinset l := Multiset.toFinset l`) has ~zero structure of its own and so scores near zero
here regardless of its dependency profile.

**Textual counting over normalized source, acceptable for v1 per the design doc -- known
blind spots, not fixed here:**
- Structure hidden behind notation or inside a *called* definition is invisible: `Monotone f`
  hides `∀ a b, a ≤ b → f a ≤ f b` behind a name with zero visible structure of its own, and
  richness only ever sees the literal text of the candidate's own body.
- Boolean/computational equivalents of the counted operators (`&&`, `||`, `!`, `cond`-based
  conditionals as in `Nat.bit`'s `cond b (2 * n + 1) (2 * n)`) are not counted -- only the
  `Prop`-level unicode operators and `if`/`bif`/match-arm forms listed below are.
  Boolean-notation-heavy code is a real gap this misses.
- `=` counting (see `_COMPARISON_RE`) is a bare textual match excluding `:=` and `==`; it does
  not distinguish a genuinely propositional equality (`a % n = b % n`) from an equality that
  happens to appear inside, say, a notation macro -- vanishingly rare in this corpus, but not
  ruled out by construction.
- Hypothesis-binder detection (`miner.gates.looks_like_prop_type`) is a textual heuristic over
  binder *type text*, not a sort check: a plain function-typed data argument (`f : α → β`)
  also contains `→` and is miscounted as a hypothesis.
"""

import re
from dataclasses import dataclass

from miner.gates import looks_like_prop_type, normalize_body
from miner.verify import VerifiedDef

_CONJUNCTION_RE = re.compile(r"∧")
_DISJUNCTION_RE = re.compile(r"∨")
_QUANTIFIER_RE = re.compile(r"∀|∃")
# Bare `=` counts as a comparison except as part of `:=` (definition/assignment) or `==`
# (boolean equality) -- see the module docstring's note on this heuristic's limits.
_COMPARISON_RE = re.compile(r"≤|≥|≠|∣|<|>|(?<!:)=(?!=)")
_IF_RE = re.compile(r"\bif\b")
_BIF_RE = re.compile(r"\bbif\b")
_MATCH_ARM_RE = re.compile(r"=>")


@dataclass(frozen=True)
class RichnessComponents:
    conjunctions: int
    disjunctions: int
    conditionals: int
    quantifiers: int
    comparisons: int
    hypothesis_binders: int
    total: int


def _count_conditionals(normalized: str) -> int:
    """`if`/`then`/`else` expressions, `bif` (Lean's Bool-`cond` notation), and pattern-match
    arms. `then`/`else` aren't separately counted -- they always co-occur with `if` in valid
    Lean, so counting them too would triple-count the same conditional. Match arms are
    approximated by counting `=>` occurrences: in this codebase's style, `=>` is used for
    match/pattern arms and `fun`-lambdas consistently use `↦` instead (confirmed against every
    batch-1/2 example inspected while building this), so the two notations don't collide in
    practice, though nothing enforces that convention structurally."""
    return len(_IF_RE.findall(normalized)) + len(_BIF_RE.findall(normalized)) + len(_MATCH_ARM_RE.findall(normalized))


def _count_hypothesis_binders(v: VerifiedDef) -> int:
    """Explicit binder groups whose type text reads as a proposition (side condition) rather
    than plain data -- see `miner.gates.looks_like_prop_type`. Reuses the already-parsed
    `binder_groups` from the type-derived arity work (`miner.verify`) rather than re-deriving
    binder structure from raw text."""
    return sum(1 for g in v.binder_groups if g.kind == "explicit" and looks_like_prop_type(g.type_text))


def compute_richness(v: VerifiedDef) -> RichnessComponents:
    normalized = normalize_body(v.source_text)
    conjunctions = len(_CONJUNCTION_RE.findall(normalized))
    disjunctions = len(_DISJUNCTION_RE.findall(normalized))
    conditionals = _count_conditionals(normalized)
    quantifiers = len(_QUANTIFIER_RE.findall(normalized))
    comparisons = len(_COMPARISON_RE.findall(normalized))
    hypothesis_binders = _count_hypothesis_binders(v)
    total = conjunctions + disjunctions + conditionals + quantifiers + comparisons + hypothesis_binders
    return RichnessComponents(
        conjunctions=conjunctions,
        disjunctions=disjunctions,
        conditionals=conditionals,
        quantifiers=quantifiers,
        comparisons=comparisons,
        hypothesis_binders=hypothesis_binders,
        total=total,
    )
