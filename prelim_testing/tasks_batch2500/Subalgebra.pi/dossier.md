## Object

Given an index type `ι`, a commutative semiring `R`, a family of `R`-algebras `S i` (one for each `i : ι`), a subset `s` of indices, and a family `t i` of subalgebras of `S i`, `VTask.pi s t` is the subalgebra of the product algebra `Π i, S i` consisting of all functions `f : Π i, S i` such that, for every index `i` belonging to `s`, the value `f i` lies in the subalgebra `t i`. Indices outside `s` are unconstrained.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {ι : Type u_1} -> {R : Type u_2} -> {S : ι → Type u_3} -> [CommSemiring R] -> [(i : ι) → Semiring (S i)] -> [(i : ι) → Algebra R (S i)] -> (s : Set ι) -> (t : (i : ι) → Subalgebra R (S i)) -> Subalgebra R ((i : ι) → S i)
<!-- PINNED-SIGNATURE:END -->


`VTask.pi : {ι : Type u_1} -> {R : Type u_2} -> {S : ι → Type u_3} -> [CommSemiring R] -> [(i : ι) → Semiring (S i)] -> [(i : ι) → Algebra R (S i)] -> (s : Set ι) -> (t : (i : ι) → Subalgebra R (S i)) -> Subalgebra R ((i : ι) → S i)`

The implicit argument `ι` is the index type parametrising the product. The implicit argument `R` is the base commutative semiring over which all algebras are defined. The implicit family `S` assigns to each index `i` the fiber algebra type. The instance arguments supply the semiring structure on each fiber and the `R`-algebra structure on each fiber. The explicit argument `s` is the set of "active" indices: only at indices in `s` is the subalgebra constraint enforced. The explicit argument `t` is the family assigning to each index `i` a subalgebra of `S i`; only the subalgebras `t i` for `i ∈ s` actually restrict membership.

## Conventions

For an index `i` not in `s`, the fiber condition is vacuous: any value in `S i` is permitted at position `i`, regardless of `t i`. There are no junk-value conventions beyond this design choice; the construction is total over all inputs.

## Worked examples

- Claim: Taking `s = Set.univ` makes membership equivalent to `∀ i, f i ∈ t i`, i.e., every coordinate is constrained by its respective subalgebra.

- Claim: Taking `s = ∅` gives the full product `Π i, S i` as a subalgebra (all functions belong, since no index is active), regardless of the family `t`.

- Claim: If `s₁ ⊆ s₂` then `VTask.pi s₂ t ≤ VTask.pi s₁ t` (a larger active index set gives a smaller, more restrictive subalgebra).

- Claim: If `t i = ⊤` for every `i ∈ s`, then `VTask.pi s t` equals the full product subalgebra (all fibers are unrestricted).

## Boundaries

- When `ι` is empty the product `Π i, S i` has a unique element (the empty function), and `VTask.pi s t` is necessarily the whole (one-element) algebra for any `s` and `t`.
- When `s = ∅`, every function belongs to `VTask.pi ∅ t`; the family `t` has no effect on membership.
- When `s = Set.univ`, every index is active and membership is the full pointwise condition `∀ i, f i ∈ t i`.
- The `algebraMap` elements (scalar multiples of 1) always belong to `VTask.pi s t`, consistent with it being an `R`-subalgebra.

## Not to be confused with

- `Submodule.pi`: the analogous construction for submodules, which enforces only `R`-module structure and does not require multiplicative or algebraic closure.
- The `Pi` instance that equips `Π i, S i` with its product algebra structure: that is the ambient algebra, not a subalgebra of it.
- A subalgebra of a single fiber `S i`: `VTask.pi s t` lives in the full product type, not in any individual fiber.