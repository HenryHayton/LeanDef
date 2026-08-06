"""Per-task notation glossary, generated mechanically from the pinned signature.

**Meaning-level only, never implementation advice.** A glossary entry says what a piece of
notation *means* mathematically; it never says what to write. The distinction is load-bearing:
telling a model "`→o` is a bundled monotone map" is describing the signature it was already
given, while telling it "use `OrderHom.mk`" would be answering the question. The former is
reading support, the latter is a leak of the answer's shape.

Generated per task rather than pinned globally so a prompt only ever carries entries for
notation that actually appears in that task's signature -- an unused entry is noise that teaches
the model the notation is expected.

Motivated by measurement: on the prelim run, missing typeclass assumptions were 7% of one
model's failures, bundled-vs-unbundled morphisms and binder explicitness a large share of
`WRONG_TYPE`. Those are all *reading* failures of the pinned signature, which is exactly what a
meaning-level glossary addresses.
"""

import re

# (regex over the pinned type, glossary line). Order is display order.
_ENTRIES: list[tuple[str, str]] = [
    (r"⦃",
     "`⦃x : T⦄` is a *strict implicit* binder: `x` is inferred from later arguments, and the "
     "binder is only solved for once a subsequent explicit argument forces it. It is a different "
     "binder from `{x : T}` and from `(x : T)`."),
    (r"→o",
     "`α →o β` is a *bundled* monotone map: a single object carrying both the function and a "
     "proof that it is monotone. It is not the same as a plain function `α → β` accompanied by a "
     "separate monotonicity hypothesis."),
    (r"≃",
     "`α ≃ β` is an *equivalence*: a bundled object carrying a function, an inverse, and proofs "
     "that the two compose to the identity in both directions."),
    (r"↑|⇑",
     "`↑x` (and `⇑f`) is a *coercion*: the same underlying object viewed at a different type, "
     "e.g. an element of a subtype viewed in the ambient type."),
    (r"∀ᶠ",
     "`∀ᶠ x in f, P x` means `P` holds *eventually* along the filter `f` -- the set where `P` "
     "holds belongs to `f`. It is a statement about the filter, not about every `x`."),
    (r"\{[^}]*//",
     "`{x : T // P x}` is a *subtype*: an element is a pair of a value and a proof that it "
     "satisfies `P`. Constructing one requires supplying that proof."),
    (r"\bSort\b",
     "`Sort u` ranges over `Prop` as well as every `Type u`. A definition pinned at `Sort` must "
     "work for propositions too, not only for types."),
    (r"\[[^\]]+\]",
     "`[C α]` is an *instance* binder: an assumption that the typeclass `C` holds of `α`, "
     "supplied automatically by instance search. Only the assumptions written in the signature "
     "are available."),
    (r"Set\s",
     "`Set α` is a predicate on `α` (a subset of `α`), not a finite container; membership "
     "`x ∈ s` is a proposition."),
    (r"Finset",
     "`Finset α` is a *finite* set with computable membership and cardinality."),
    (r"Multiset",
     "`Multiset α` is a finite multiset -- order does not matter, but multiplicity does."),
]


def glossary_for(pinned_type: str) -> list[str]:
    """Glossary lines for the notation actually present in `pinned_type`, in display order."""
    return [line for pattern, line in _ENTRIES if re.search(pattern, pinned_type or "")]


def render_glossary(pinned_type: str) -> str:
    """The glossary block, or `""` when the signature uses no notation needing a gloss."""
    lines = glossary_for(pinned_type)
    if not lines:
        return ""
    body = "\n".join(f"- {ln}" for ln in lines)
    return (
        "# Notation in this signature\n"
        "\n"
        "These entries explain what the notation in the signature above *means*. They do not "
        "tell you what to write.\n"
        "\n"
        f"{body}\n"
    )
