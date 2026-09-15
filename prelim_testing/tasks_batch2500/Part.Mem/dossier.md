## Object

`VTask.Mem o a` is the membership predicate for partial values: it asserts that the partial value `o` is *defined* (i.e., has a concrete value) and that this concrete value is exactly `a`. In other words, `a ∈ o` holds precisely when `o` is not "undefined" and its unique contained value is `a`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Mem : {α : Type u_1} -> (o : Part α) -> (a : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Mem : {α : Type u_1} -> (o : Part α) -> (a : α) -> Prop`

The type parameter `α` is the carrier type of the partial value, inferred implicitly. The argument `o` is the partial value (an element of `Part α`) whose membership is being tested. The argument `a` is the candidate element of type `α` that is being checked for membership in `o`.

## Conventions

No junk-value or out-of-domain conventions are declared: the predicate is meaningful for every `o : Part α` and every `a : α`. When `o` is undefined (has no element), the predicate is simply `False` for all `a`; this is the natural mathematical behaviour, not a convention.

## Worked examples

- Claim: For `o := Part.some 3`, we have `3 ∈ o` (the defined partial value containing 3 has 3 as its member).

- Claim: For `o := Part.none` (the undefined partial value), no element `a : ℕ` satisfies `a ∈ o`.

- Claim: If `a ∈ o` and `b ∈ o`, then `a = b` — membership in a partial value is unique, since a defined `Part α` contains exactly one element.

- Claim: For `o := Part.some 5`, `7 ∈ o` is `False` — the only member of `Part.some 5` is `5`, not `7`.

## Boundaries

- **Undefined partial value (`Part.none`):** `a ∈ Part.none` is `False` for every `a`, because `Part.none` is never defined.
- **Defined partial value (`Part.some x`):** `a ∈ Part.some x` holds if and only if `a = x`.
- **Uniqueness:** Because a `Part α` can hold at most one value, `a ∈ o` and `b ∈ o` together imply `a = b`.
- **No restriction on `α`:** The predicate is well-formed for any type `α`, including `Prop`, `Nat`, function types, etc.

## Not to be confused with

- **`Part.Dom o`** — this asserts only that `o` is defined, without specifying which value it contains; `a ∈ o` is strictly stronger.
- **`Option.isSome` / `Option` membership** — `Option α` is a related but distinct type; membership for `Part α` additionally carries a proof of definedness that is propositionally richer.
- **Set membership (`a ∈ s` for `s : Set α`)** — set membership is about a predicate on `α`, whereas `Part α` membership is about a single partial value and whether it is defined and equal to `a`.