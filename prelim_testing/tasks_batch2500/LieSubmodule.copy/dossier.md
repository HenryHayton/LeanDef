## VTask.copy

### Object

Given a Lie submodule `N` over a commutative ring `R`, a Lie ring `L`, and an `R`-module `M` that is also a Lie ring module for `L`, `VTask.copy` produces a new Lie submodule whose underlying carrier set is exactly `s`, where `s` is a set that is definitionally (or propositionally) equal to the carrier of `N`. The result is a Lie submodule that is identical to `N` in every mathematical sense, but whose carrier is literally `s` rather than `↑N`. The purpose is to repair definitional equalities in formal proofs without changing any mathematical content.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {R : Type u} -> {L : Type v} -> {M : Type w} -> [CommRing R] -> [LieRing L] -> [AddCommGroup M] -> [Module R M] -> [LieRingModule L M] -> (N : LieSubmodule R L M) -> (s : Set M) -> (hs : s = ↑N) -> LieSubmodule R L M
<!-- PINNED-SIGNATURE:END -->


The implicit arguments `R`, `L`, and `M` are the coefficient ring, the Lie ring acting on the module, and the ambient module, respectively; the type-class instances supply the required algebraic structures. The argument `N` is the source Lie submodule being copied. The argument `s` is the new carrier set that will be used in the resulting Lie submodule. The argument `hs` is a proof that `s` is equal (as a set) to the coercion of `N` to a subset of `M`; it certifies that the new carrier really does coincide with the old one.

### Conventions

There are no junk-value or boundary conventions to declare: the function is total and every input satisfying the type is meaningful. The proof `hs` is required to be definitionally or propositionally equal, not merely logically equivalent; this is what makes the copy useful for fixing definitional equalities in downstream proofs.

### Worked examples

- Claim: For any Lie submodule `N`, `VTask.copy N (↑N) rfl` has the same carrier as `N`.

- Claim: Every element `x` that belongs to `N` also belongs to `VTask.copy N (↑N) rfl`, and vice versa, because the carriers are definitionally equal after the copy.

- Claim: `VTask.copy N s hs` equals `N` as a Lie submodule whenever `s = ↑N` (i.e., the copy operation is the identity up to the carrier substitution).

### Boundaries

- The proof `hs : s = ↑N` is the only condition; there are no restrictions on what the set `s` looks like beyond that equation. If `s` happens to be definitionally equal to `↑N` (for instance `s = ↑N` by `rfl`), then the copy is definitionally interchangeable with `N`.
- When `hs` is `rfl` (i.e., `s` is literally `↑N`), the copy is a trivially equal clone of `N`.
- The construction does not create a mathematically new or different submodule; it only changes the syntactic form of the carrier field.

### Not to be confused with

- `LieSubmodule.map`: transports a Lie submodule along a Lie module homomorphism, genuinely producing a (potentially different) submodule in a different ambient module.
- `LieSubmodule.comap`: pulls a Lie submodule back along a homomorphism, again potentially producing a mathematically distinct submodule.
- Subtype coercions of `LieSubmodule`: merely viewing the submodule as a set or type, not constructing a new `LieSubmodule` structure.