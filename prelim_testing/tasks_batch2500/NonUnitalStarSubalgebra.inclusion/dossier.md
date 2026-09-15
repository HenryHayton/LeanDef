## Object

`VTask.inclusion` produces the canonical inclusion map from a non-unital star subalgebra `S` into a larger non-unital star subalgebra `T`, given evidence that `S ≤ T`. The resulting map is a non-unital star algebra homomorphism over the base ring `R`: it sends each element of `S` to the same element viewed as a member of `T`, preserving the ring operations, the `R`-module structure, and the star involution.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inclusion : {R : Type u} -> {A : Type v} -> [CommSemiring R] -> [NonUnitalSemiring A] -> [StarRing A] -> [Module R A] -> {S T : NonUnitalStarSubalgebra R A} -> (h : S ≤ T) -> ↥S →⋆ₙₐ[R] ↥T
<!-- PINNED-SIGNATURE:END -->


`VTask.inclusion : {R : Type u} -> {A : Type v} -> [CommSemiring R] -> [NonUnitalSemiring A] -> [StarRing A] -> [Module R A] -> {S T : NonUnitalStarSubalgebra R A} -> (h : S ≤ T) -> ↥S →⋆ₙₐ[R] ↥T`

`R` is the commutative semiring of scalars. `A` is the ambient non-unital star algebra in which both subalgebras live. The type-class arguments supply the algebraic structure on `R` and `A`. `S` and `T` are non-unital star subalgebras of `A`. The explicit argument `h` is proof that `S` is contained in `T` (i.e., every element of `S` also belongs to `T`). The output is the corresponding non-unital star algebra homomorphism from `S` to `T`.

## Conventions

No junk-value or edge conventions are declared for this definition: it is a total map whose only input is a proof `h : S ≤ T`, and the result is fully determined and well-behaved for any valid such proof.

## Worked examples

- Claim: For any non-unital star subalgebras `S ≤ T` of `A`, the inclusion map sends every element `x : S` to an element of `T` whose underlying value in `A` equals that of `x`.

- Claim: For any `S ≤ T` and any `x : S`, `(VTask.inclusion h x : A) = (x : A)` — the inclusion is the identity on underlying elements.

- Claim: For any `S ≤ T`, `x y : S`, the inclusion satisfies `VTask.inclusion h (x * y) = VTask.inclusion h x * VTask.inclusion h y` — it preserves multiplication.

- Claim: For any `S ≤ T` and `x : S`, `VTask.inclusion h (star x) = star (VTask.inclusion h x)` — it commutes with the star involution.

## Boundaries

- When `S = T` (i.e., `h : S ≤ T` is actually an equality), `VTask.inclusion h` is the identity map expressed as an inclusion; it is still a valid non-unital star homomorphism.
- The map is always injective, because distinct elements of `S` have distinct images in `T` (the underlying values in `A` are unchanged).
- `VTask.inclusion` requires `h : S ≤ T` as a proof object; if no such proof exists (i.e., `S ⊄ T`), the map cannot be formed.
- The definition does not require `A` to be unital, nor `S` or `T` to contain a unit, consistent with the non-unital setting.

## Not to be confused with

- `Submodule.inclusion`: The analogous inclusion for submodules, which is only a linear map, not a star algebra homomorphism.
- `NonUnitalSubalgebra.inclusion`: The inclusion for non-unital subalgebras without the star structure; does not preserve the star involution.
- The identity morphism on `S`: `VTask.inclusion` targets a (potentially larger) subalgebra `T`, not `S` itself.