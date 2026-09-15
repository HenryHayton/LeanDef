## Object

`VTask.inclusion` constructs the canonical inclusion morphism from a non-unital subalgebra `S` into a larger non-unital subalgebra `T`, whenever `S ⊆ T`. It is the non-unital subalgebra analogue of the standard inclusion map between submodules or subrings: it sends every element of `S` to the same element viewed as a member of `T`, and does so as a morphism of non-unital `R`-algebras (i.e., it is `R`-linear and multiplicative).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inclusion : {R : Type u} -> {A : Type v} -> [CommSemiring R] -> [NonUnitalNonAssocSemiring A] -> [Module R A] -> {S T : NonUnitalSubalgebra R A} -> (h : S ≤ T) -> ↥S →ₙₐ[R] ↥T
<!-- PINNED-SIGNATURE:END -->


The scalar ring `R` is a commutative semiring; `A` is a non-unital, non-associative semiring that also carries an `R`-module structure compatible in the expected way, making `A` a module over `R`. The subobjects `S` and `T` are non-unital subalgebras of `A` over `R`. The argument `h` is a proof that `S ≤ T`, i.e., that `S` is contained in `T` as a set. The result is a non-unital `R`-algebra homomorphism from `S` to `T`.

## Conventions

There are no junk-value or boundary conventions to declare: the definition is total over all valid inputs, and every component of the morphism is canonically determined by the containment hypothesis — the underlying function is the identity on elements, with no arbitrary choices.

## Worked examples

- Claim: For any non-unital subalgebra `S` of `A`, the inclusion `VTask.inclusion (le_refl S)` sends every element `x : S` to the same element viewed in `S` (the underlying map is the identity on elements).

- Claim: If `S ≤ T ≤ U` are non-unital subalgebras of `A` over `R`, then `VTask.inclusion (le_trans h₁ h₂)` and the composite `(VTask.inclusion h₂).comp (VTask.inclusion h₁)` agree on every element, since both send `x : S` to the same element of `U`.

- Claim: The inclusion `VTask.inclusion h` is injective for any `h : S ≤ T`, because distinct elements of `S` are distinct elements of `A` and hence of `T`.

## Boundaries

- When `S = T` (i.e., `h : S ≤ T` and `T ≤ S` both hold), the inclusion is an isomorphism on elements but is still typed as a morphism `S →ₙₐ[R] T`, not as an automorphism or equivalence.
- The morphism is well-defined regardless of whether `R` or `A` are unital, associative, or commutative, because `NonUnitalSubalgebra` imposes only closure under addition, scalar multiplication, and multiplication.
- Composing two inclusions `VTask.inclusion h₁ : S →ₙₐ[R] T` and `VTask.inclusion h₂ : T →ₙₐ[R] U` yields a morphism that agrees pointwise with `VTask.inclusion (h₁.trans h₂) : S →ₙₐ[R] U`.

## Not to be confused with

- `Submodule.inclusion`: the analogous map for submodules; it is an `R`-linear map rather than a non-unital algebra homomorphism, and carries no multiplicative structure.
- `Subalgebra.inclusion`: the unital subalgebra version, which works under the assumption that `A` is a unital (and typically associative) `R`-algebra.
- `NonUnitalSubalgebra.subtype`: the canonical embedding of a subalgebra into the ambient algebra `A` itself, rather than into a larger subalgebra.