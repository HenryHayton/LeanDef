## Object

`VTask.sigmaCongrRightHom β` is the group homomorphism from the product group `∏_{a : α} Perm(β a)` (i.e., the type of dependent functions that assign to each `a : α` a permutation of the fiber `β a`) to the symmetric group `Perm(Σ a, β a)` on the total space of the bundle. The homomorphism sends a family of fiberwise permutations to the single permutation of the sigma-type that acts on each fiber independently, leaving the base index `a` unchanged. It is the canonical way to regard independent fiberwise shuffles as a single permutation of the total space, and its range is precisely the subgroup of permutations that never move an element from one fiber to another.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sigmaCongrRightHom : {α : Type u_7} -> (β : α → Type u_8) -> ((a : α) → Equiv.Perm (β a)) →* Equiv.Perm ((a : α) × β a)
<!-- PINNED-SIGNATURE:END -->


`VTask.sigmaCongrRightHom : {α : Type u_7} -> (β : α → Type u_8) -> ((a : α) → Equiv.Perm (β a)) →* Equiv.Perm ((a : α) × β a)`

The implicit argument `α` is the index type, i.e., the base of the fiber bundle. The explicit argument `β` is the family of types indexed by `α`, assigning to each base element `a` the fiber `β a`; this determines both the domain and codomain of the homomorphism. The homomorphism itself maps a dependent function assigning a permutation to each fiber to the corresponding permutation of the total sigma-type `Σ a, β a`.

## Conventions

There are no junk-value or edge-case conventions to declare: the definition is total and well-defined for all choices of `α` and `β`, including when `α` is empty (in which case the only element of the domain is the identity function and the image is the trivial group) or when some fibers `β a` are empty.

## Worked examples

- Claim: `VTask.sigmaCongrRightHom β` is injective as a group homomorphism, meaning two distinct families of fiberwise permutations always produce distinct permutations of the total space.

- Claim: The cardinality of the range of `VTask.sigmaCongrRightHom β` equals the cardinality of `∀ a, Equiv.Perm (β a)` when both are finite, confirming that no information is lost and the homomorphism is an isomorphism onto its image.

- Claim: Applying `VTask.sigmaCongrRightHom β` to the family of identity permutations (the identity element of the domain) yields the identity permutation on `Σ a, β a`.

- Claim: The range of `VTask.sigmaCongrRightHom β` consists exactly of those permutations of `Σ a, β a` that map every element `⟨a, b⟩` to an element with the same first component `a` (i.e., permutations that never swap elements between different fibers).

## Boundaries

- When `α` is the empty type, the domain `∀ a, Equiv.Perm (β a)` is a singleton (there is exactly one dependent function from the empty type), and the codomain `Perm (Σ a, β a)` is also trivial (the sigma-type is empty). The homomorphism maps the unique element to the identity.
- When `α` has exactly one element, the homomorphism is an isomorphism between `Equiv.Perm (β a₀)` and `Equiv.Perm (Σ a, β a)` (since the sigma-type is essentially just `β a₀`).
- When some fiber `β a` is empty, the permutation group on that fiber is trivial and contributes no non-identity permutations to the total space.
- The homomorphism is always injective (regardless of the sizes of `α` and the fibers), so its range is isomorphic to the domain.

## Not to be confused with

- `Equiv.Perm.sigmaCongrRight`: the bare function (not bundled as a `MonoidHom`) that performs the same action on elements, without the group-homomorphism structure.
- `Equiv.Perm.sigmaCongrLeftHom` (or related constructions): a homomorphism that permutes the *base* indices of a sigma-type rather than acting fiberwise.
- `Equiv.Perm.sumCongrHom`: the analogous monoid homomorphism for sum types `α ⊕ β` rather than sigma/dependent-pair types.