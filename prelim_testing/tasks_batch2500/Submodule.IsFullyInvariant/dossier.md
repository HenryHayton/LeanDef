## VTask.IsFullyInvariant

### Object

A submodule `N` of an `R`-module `M` is **fully invariant** if every `R`-linear endomorphism of `M` maps `N` into itself — that is, for every `R`-linear map `f : M →ₗ[R] M`, the image `f(N)` is contained in `N`. This is a stronger condition than being invariant under a particular map; it demands invariance under the entire endomorphism ring of `M`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsFullyInvariant : {R : Type u_5} -> {M : Type u_6} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> (N : Submodule R M) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsFullyInvariant : {R : Type u_5} -> {M : Type u_6} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> (N : Submodule R M) -> Prop`

The implicit argument `R` is the scalar semiring. The implicit argument `M` is the `R`-module in which the submodule lives; the typeclass arguments equip `R` with its semiring structure and `M` with the compatible additive-commutative-monoid and module structures. The explicit argument `N` is the submodule whose full invariance is being tested.

### Conventions

This predicate is universally quantified over all `R`-linear endomorphisms of `M`; there are no junk-value or boundary conventions declared for the definition itself.

### Worked examples

- Claim: The zero submodule of any `R`-module `M` is fully invariant, since every `R`-linear endomorphism maps `0` to `0`.

- Claim: The top submodule (all of `M`) is fully invariant, since every endomorphism maps `M` into `M` by definition.

- Claim: For a semisimple module `M`, each isotypic component of `M` is a fully invariant submodule. This follows from `VTask.IsFullyInvariant.isotypicComponent`.

- Claim: Any submodule belonging to the collection `isotypicComponents R M` is fully invariant. This follows from `VTask.IsFullyInvariant.of_mem_isotypicComponents`.

### Boundaries

- The definition uses a semiring `R` (not necessarily a ring or a field), so it applies in full generality to modules over semirings.
- Full invariance is strictly stronger than being preserved by a single chosen endomorphism; a submodule can be invariant under multiplication-by-scalars (i.e., be a submodule) without being fully invariant.
- The empty intersection of conditions (vacuously, when the endomorphism ring is trivial or when `N` is `⊥` or `⊤`) still yields valid instances.
- In the semisimple case, `VTask.IsFullyInvariant` is equivalent to `N` being expressible as a supremum of isotypic components.

### Not to be confused with

- **`Submodule.map f N ≤ N`** for a single fixed `f`: full invariance universally quantifies over *all* endomorphisms, not just one.
- **`Submodule.IsCharacteristic`** (characteristic subgroup/submodule): in group theory this refers to invariance under automorphisms only, a strictly weaker condition than invariance under all endomorphisms.
- **`Submodule.comap`**: the comap operation is used internally to express the containment condition, but the predicate is about the submodule being mapped *into itself*, not about the preimage under a map.