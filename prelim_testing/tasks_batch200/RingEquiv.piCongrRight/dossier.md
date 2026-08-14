## Object

`VTask.piCongrRight` constructs a ring isomorphism between two dependent product types `(∀ i, R i)` and `(∀ i, S i)` from a family of ring isomorphisms `e i : R i ≃+* S i`, one for each index `i`. In other words, if every fibre `R i` is isomorphic to the corresponding fibre `S i` as a (non-unital, non-associative) semiring, then the product rings `∀ i, R i` and `∀ i, S i` are themselves isomorphic as rings. The isomorphism acts pointwise: the forward map sends a tuple `x` to the tuple `λ j, e j (x j)`, and the inverse map sends a tuple `y` to `λ j, (e j)⁻¹ (y j)`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piCongrRight : {ι : Type u_7} -> {R : ι → Type u_8} -> {S : ι → Type u_9} -> [(i : ι) → NonUnitalNonAssocSemiring (R i)] -> [(i : ι) → NonUnitalNonAssocSemiring (S i)] -> (e : (i : ι) → R i ≃+* S i) -> ((i : ι) → R i) ≃+* ((i : ι) → S i)
<!-- PINNED-SIGNATURE:END -->


`VTask.piCongrRight : {ι : Type u_7} -> {R : ι → Type u_8} -> {S : ι → Type u_9} -> [(i : ι) → NonUnitalNonAssocSemiring (R i)] -> [(i : ι) → NonUnitalNonAssocSemiring (S i)] -> (e : (i : ι) → R i ≃+* S i) -> ((i : ι) → R i) ≃+* ((i : ι) → S i)`

The implicit type `ι` is the index type parametrising the family. The implicit dependent types `R` and `S` assign a type to each index; both families are required to carry a `NonUnitalNonAssocSemiring` structure pointwise (provided as instance arguments). The explicit argument `e` is the family of ring isomorphisms, one for each index `i ∈ ι`, witnessing that `R i` and `S i` are isomorphic as semirings.

## Conventions

There are no junk-value conventions for this definition: it is a total construction whose inputs are well-typed semiring isomorphisms, and every valid input produces a meaningful result.

## Worked examples

- Claim: Applying `VTask.piCongrRight` to the constant family of identity isomorphisms `RingEquiv.refl (R i)` yields the identity ring isomorphism on `∀ i, R i`.

- Claim: The inverse of `VTask.piCongrRight e` equals `VTask.piCongrRight (fun i => (e i).symm)`, so inverting the whole-product isomorphism is the same as inverting each fibre isomorphism.

- Claim: Composing `VTask.piCongrRight e` with `VTask.piCongrRight f` (via `RingEquiv.trans`) equals `VTask.piCongrRight (fun i => (e i).trans (f i))`, so composition distributes through the pointwise family.

- Claim: For the constant index type `ι = Fin 2` with `R i = ℤ` and `S i = ℤ` and each `e i = RingEquiv.refl ℤ`, the forward map of `VTask.piCongrRight e` sends any tuple `x : Fin 2 → ℤ` back to itself.

## Boundaries

- When `ι` is the empty type `Empty`, both `∀ i, R i` and `∀ i, S i` are singleton types (carrying only the trivial tuple), and `VTask.piCongrRight e` is the unique isomorphism between them regardless of `e`.
- When `ι` is a `Fintype`, the product types are finite products of semirings; the construction works uniformly and coincides with the iterated binary-product case.
- No assumption stronger than `NonUnitalNonAssocSemiring` is required on the fibres: neither commutativity, unitality, nor associativity is assumed, so the construction is valid in this maximally general semiring setting.
- The construction is strictly functorial: `refl` is preserved (the identity family gives the identity isomorphism), `symm` distributes pointwise, and `trans` distributes pointwise.

## Not to be confused with

- `RingEquiv.arrowCongr` — the non-dependent version, where both domain and codomain families are constant (i.e., `R i = R` and `S i = S` do not depend on `i`); `VTask.piCongrRight` is the genuinely dependent generalisation.
- `Equiv.piCongrRight` — the plain (non-algebraic) version living in `Equiv`, which only tracks the set-theoretic bijection and does not package ring-homomorphism data.
- `MulEquiv.piCongrRight` / `AddEquiv.piCongrRight` — analogous constructions for multiplicative or additive equivalences alone, without the combined ring structure.