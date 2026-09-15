## Object

`VTask.setPreimage f` is the complete-lattice homomorphism from the power-set lattice of `β` to the power-set lattice of `α` whose underlying function is preimage under `f`. Concretely, it packages the operation `s ↦ f ⁻¹' s` (the set of all `a : α` for which `f a ∈ s`) together with the proof that this operation preserves arbitrary suprema (unions) and arbitrary infima (intersections), making it a morphism of complete lattices.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.setPreimage : {α : Type u_2} -> {β : Type u_3} -> (f : α → β) -> CompleteLatticeHom (Set β) (Set α)
<!-- PINNED-SIGNATURE:END -->


`VTask.setPreimage : {α : Type u_2} -> {β : Type u_3} -> (f : α → β) -> CompleteLatticeHom (Set β) (Set α)`

The two universe-polymorphic type parameters `α` and `β` are the domain and codomain types of the function, inferred implicitly. The explicit argument `f` is the function along which preimages are taken; it determines both the direction of the lattice homomorphism (from sets of `β` back to sets of `α`) and the element-level action.

## Conventions

There are no junk-value or edge conventions to record: the construction is defined for every function `f : α → β` without restriction, and every set-theoretic edge case (empty set, full set, arbitrary union, arbitrary intersection) is handled uniformly by the preimage operation itself.

## Worked examples

- Claim: For any `f : α → β`, applying `VTask.setPreimage f` to a set `s : Set β` yields exactly `f ⁻¹' s`.

- Claim: `VTask.setPreimage (id : α → α)` equals the identity complete-lattice homomorphism on `Set α`, because the preimage of any set under the identity function is the set itself.

- Claim: For composable functions `g : β → γ` and `f : α → β`, `VTask.setPreimage (g ∘ f)` equals the composition of `VTask.setPreimage f` after `VTask.setPreimage g`, reflecting the contravariance of preimage: `(g ∘ f)⁻¹' s = f ⁻¹' (g ⁻¹' s)`.

- Claim: `VTask.setPreimage f` maps the empty set in `Set β` to the empty set in `Set α`, since no element `a` can satisfy `f a ∈ ∅`.

- Claim: `VTask.setPreimage f` maps the universal set `Set.univ : Set β` to `Set.univ : Set α`, since every `a : α` satisfies `f a ∈ Set.univ`.

## Boundaries

- **Empty family of sets:** Applied to the supremum of an empty family (i.e., `∅` as a set in the lattice), `VTask.setPreimage f` returns the empty set, consistent with `f ⁻¹' ∅ = ∅`.
- **Full lattice:** Applied to the infimum of an empty family (i.e., `Set.univ`), `VTask.setPreimage f` returns `Set.univ`, consistent with `f ⁻¹' Set.univ = Set.univ`.
- **Non-injective `f`:** The homomorphism is well-defined for any `f`, even if `f` is neither injective nor surjective; surjectivity is not required for preservation of infima, and injectivity is not required for preservation of suprema.
- **Constant `f`:** For a constant function `f a = b₀`, `VTask.setPreimage f s` is `Set.univ` if `b₀ ∈ s` and `∅` otherwise — a valid complete-lattice homomorphism output in each case.

## Not to be confused with

- **`sSupHom.setImage`**: the companion construction packaging `Set.image` (direct image) as a supremum-preserving map, which goes in the covariant direction `Set α → Set β` and does not in general preserve infima.
- **`Set.preimage f s`** (the bare function `f ⁻¹' s`): the raw set-theoretic preimage without any bundled lattice-homomorphism structure.
- **`CompleteLatticeHom.id`**: the identity complete-lattice homomorphism on a fixed power-set lattice, which `VTask.setPreimage` specialises to when `f = id`.