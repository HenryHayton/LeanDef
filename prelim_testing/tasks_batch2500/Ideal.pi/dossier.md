## Object

Given a family of semirings `R i` indexed by a type `ι`, and a family of ideals `I i ⊆ R i`, `VTask.pi I` is the ideal of the product ring `Πᵢ R i` consisting of all elements `r` such that each component `r i` belongs to the corresponding ideal `I i`. In other words, it is the "componentwise" or "pointwise" product of the ideals: the largest ideal of the product ring contained in every "cylinder" ideal `{r | r i ∈ I i}`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {ι : Type u_1} -> {R : ι → Type u_5} -> [(i : ι) → Semiring (R i)] -> (I : (i : ι) → Ideal (R i)) -> Ideal ((i : ι) → R i)
<!-- PINNED-SIGNATURE:END -->


`VTask.pi : {ι : Type u_1} -> {R : ι → Type u_5} -> [(i : ι) → Semiring (R i)] -> (I : (i : ι) → Ideal (R i)) -> Ideal ((i : ι) → R i)`

The index type `ι` determines the shape of the product; it is implicit. The family `R` assigns a type to each index and is also implicit. The typeclass argument provides a semiring structure on each `R i`. The explicit argument `I` is the family of ideals — for each index `i`, `I i` is an ideal of `R i` — whose pointwise intersection is being formed in the product ring.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a genuinely total construction well-defined for any family of ideals over any family of semirings, including the case where `ι` is empty (giving the whole ring) or where some `I i` is the zero ideal or the unit ideal.

## Worked examples

- Claim: An element `r : Π i, R i` belongs to `VTask.pi I` if and only if `r i ∈ I i` for every index `i`. This is the defining membership characterisation: `r ∈ VTask.pi I ↔ ∀ i, r i ∈ I i`.

- Claim: When `ι = Fin 2` and both `R 0` and `R 1` are `ℤ`, taking `I 0 = span {2}` and `I 1 = span {3}`, the element `(2, 3)` belongs to `VTask.pi I` because `2 ∈ span {2}` and `3 ∈ span {3}`.

- Claim: The zero element of `Π i, R i` always belongs to `VTask.pi I` for any family `I`, since each ideal `I i` contains zero.

- Claim: If every `I i` is the zero ideal of `R i`, then `VTask.pi I` is the zero ideal of `Π i, R i`.

- Claim: If every `I i` equals `R i` (the unit ideal), then `VTask.pi I` equals the whole ring `Π i, R i`.

## Boundaries

- **Empty index type**: When `ι` is empty (`ι = PEmpty` or `Fin 0`), every function `Fin 0 → R` trivially satisfies `∀ i, r i ∈ I i`, so `VTask.pi I` is the whole product ring (which itself is the trivial ring).
- **Single index**: When `ι = Fin 1`, the product ring is isomorphic to `R 0`, and `VTask.pi I` corresponds to `I 0` under that isomorphism.
- **Mixed ideals**: The construction handles any combination of zero ideals, unit ideals, and proper ideals across different indices; the resulting ideal is the full pointwise intersection.

## Not to be confused with

- `Ideal.span (Set.range f)`: The span of a set of elements, a different way to generate an ideal, not a componentwise product construction.
- The *direct sum* of ideals or the *external product* of rings, which have different universal properties from the pointwise product ideal.
- `Pi.ideal` or any construction that takes a *single* ideal and lifts it to the product along a projection, rather than specifying one ideal per component.