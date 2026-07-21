"""Return-shape classification -- metadata only, no gate reads this (per this task's explicit
scope: a classification for the manifest and future review docs to draw on, not a selection
decision).

Classifies a verified definition's return type into one of three shapes:

- `"prop"`: the return type is exactly `Prop` -- a predicate/proposition-valued definition.
- `"bundled"`: the return type is itself a type-former (`Type`, `Type u_1`, `Sort _`) or a
  bundled structure that carries a function together with the property making it well-behaved
  -- an equivalence (`≃`), embedding (`↪`), or a named bundled-hom/iso type (`Equiv`,
  `Embedding`, `PartialEquiv`, `RingHom`, `MonoidHom`, `GroupHom`, `AlgHom`, `OrderIso`,
  `RelEmbedding`, `RelIso`) -- Mathlib's own term for this shape of object, distinct from a
  plain value both in what it *is* and in what a dossier/fact suite for it looks like.
- `"value"`: everything else -- a concrete/plain data type (`ℕ`, `Finset α`, `List β`, ...).
"""

import re

_BUNDLED_RE = re.compile(
    r"\bType\b|\bSort\b|≃|↪|\b(?:Equiv|Embedding|PartialEquiv|RingHom|MonoidHom|GroupHom|AlgHom|OrderIso|"
    r"RelEmbedding|RelIso)\b"
)


def classify_return_shape(return_type: str) -> str:
    stripped = return_type.strip()
    if stripped == "Prop":
        return "prop"
    if _BUNDLED_RE.search(stripped):
        return "bundled"
    return "value"
