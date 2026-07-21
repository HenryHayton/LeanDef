"""Structural richness (design doc `docs/design/definition_selection_2026-07-21.md` §4.1) --
the dominant term of the preference score, and (since 22 July 2026) a hard gate
(`RICHNESS_FLOOR`, `miner.gates.richness_floor_gate`).

A count, over the normalized definition body and its parsed binders, of conjunctions,
disjunctions, conditionals, quantifiers, comparison/inequality operators, and hypothesis
binders. This is a near-direct measurement of how many distinguishable ways a candidate
definition can be *wrong* -- a dropped conjunct, a flipped inequality, a missing side
condition are exactly the misreading classes the verifier's mutant suites exist to catch (see
`docs/design/verifier_architecture_2026-07-20.md` §2) -- and it directly attacks the
delegation problem the old dependency-count score approximated badly: a pure delegation
(`toFinset l := Multiset.toFinset l`) has ~zero structure of its own and so scores near zero
here regardless of its dependency profile.

**Textual counting over normalized source, acceptable for v1 per the design doc.**

**Fixed 22 July 2026 (batch 2's §5 item 3):** bare `=>` no longer counts as a conditional on
its own. Batch 2's assumption that this codebase's style reserves `=>` for match/pattern arms
and always uses `↦` for plain lambdas turned out to be false for anonymous-constructor
equivalence proofs (`⟨fun p => ..., fun p => ..., ...⟩`), which routinely write `fun x => ...`
-- several `Equiv.*` definitions (`Equiv.prodAssoc`, `Equiv.Set.univ`, `Equiv.sumCongr`,
`Equiv.swap`) scored artificially high on richness purely from lambda-arm `=>` tokens with no
relation to the definition's own case-based structure. A genuine match arm is now only counted
when `=>` is the close of a `| pattern => ...` clause (see `_MATCH_ARM_RE`); a bare `fun x =>`
with no preceding `|` doesn't count. The same fix also removed a second, compounding bug: `=>`
itself contains `=`, so every miscounted lambda arm was *also* being double-counted as a bare
comparison by the old `_COMPARISON_RE` (which excluded `:=` and `==` but not `=>`) -- fixed by
excluding `=>` from the comparison match too.

**Still open (not fixed this round):**
- Structure hidden behind notation or inside a *called* definition is invisible: `Monotone f`
  hides `∀ a b, a ≤ b → f a ≤ f b` behind a name with zero visible structure of its own, and
  richness only ever sees the literal text of the candidate's own body.
- Boolean/computational equivalents of the counted operators (`&&`, `||`, `!`, `cond`-based
  conditionals as in `Nat.bit`'s `cond b (2 * n + 1) (2 * n)`) are not counted -- only the
  `Prop`-level unicode operators and `if`/`bif`/match-arm forms are. Boolean-notation-heavy
  code is a real gap this misses.
- `where`-block field assignments (`toFun := ...`) were never counted as comparisons (`:=` was
  always excluded) and still aren't -- not a bug, just confirming this case was already
  correctly handled before this round's fix, since the task instructions named it explicitly.
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
# Bare `=` counts as a comparison except as part of `:=` (definition/assignment), `==` (boolean
# equality), or `=>` (match-arm/lambda-arm arrow -- excluding this is this round's fix; see the
# module docstring). The lone `>` of `=>` must also be excluded separately: `>` is itself a
# listed comparison operator, and `=>`'s `>` is a *different* character than the `=` right
# before it, so excluding `=` from matching inside `=>` does nothing to stop `>` from matching
# on its own -- both halves of the arrow need their own exclusion.
_COMPARISON_RE = re.compile(r"≤|≥|≠|∣|<|(?<!=)>|(?<!:)=(?![=>])")
_IF_RE = re.compile(r"\bif\b")
_BIF_RE = re.compile(r"\bbif\b")
# A genuine match/pattern arm: a `|` introducing a pattern, closed by `=>`, with no further `|`
# or `=` in between (so this doesn't reach across arm boundaries or swallow a comparison).
# Deliberately requires the leading `|` -- this round's fix -- so a bare `fun x => ...` lambda
# arm (no preceding `|`) is not counted; see the module docstring for why that distinction
# turned out to matter.
_MATCH_ARM_RE = re.compile(r"\|[^|=]*?=>")


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
    """`if`/`then`/`else` expressions, `bif` (Lean's Bool-`cond` notation), and genuine
    pattern-match arms (`| pattern => ...`, not a bare lambda arm -- see `_MATCH_ARM_RE`).
    `then`/`else` aren't separately counted -- they always co-occur with `if` in valid Lean, so
    counting them too would triple-count the same conditional."""
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
