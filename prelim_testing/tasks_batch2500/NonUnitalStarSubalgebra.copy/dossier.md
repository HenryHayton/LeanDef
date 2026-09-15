## Object

`VTask.copy` produces a new non-unital star subalgebra that is definitionally equal to a given one, but whose carrier set is replaced by a definitionally or propositionally equal set supplied by the caller. The resulting subalgebra carries exactly the same elements and the same algebraic and star-algebraic structure as the original; the sole purpose is to swap in a preferred presentation of the carrier for the sake of definitional equality.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {R : Type u} -> {A : Type v} -> [CommSemiring R] -> [NonUnitalNonAssocSemiring A] -> [Module R A] -> [Star A] -> (S : NonUnitalStarSubalgebra R A) -> (s : Set A) -> (hs : s = ↑S) -> NonUnitalStarSubalgebra R A
<!-- PINNED-SIGNATURE:END -->


The implicit arguments `R` and `A` are the scalar ring and the ambient algebra, respectively. The typeclass arguments equip `R` with a commutative semiring structure, `A` with a non-unital non-associative semiring structure, `A` with an `R`-module structure, and `A` with a star operation. The explicit argument `S` is the original non-unital star subalgebra being copied. The argument `s` is the new carrier set that will be used for the copy. The argument `hs` is a proof that `s` equals the coercion of `S` to a set (i.e. `s = ↑S`); this equality is what guarantees that the copy contains exactly the same elements as the original.

## Conventions

Because `hs` is required to be a proof that `s` equals the carrier of `S`, the copy is never a genuinely different subalgebra — it is always extensionally identical to `S`. No junk-value or out-of-domain convention applies here.

## Worked examples

- Claim: For any non-unital star subalgebra `S`, the copy of `S` with carrier `↑S` and the reflexivity proof contains exactly the same members as `S`: an element `a` belongs to `VTask.copy S ↑S rfl` if and only if it belongs to `S`.

- Claim: For any non-unital star subalgebra `S` and any element `a`, if `a ∈ S` then `star a ∈ VTask.copy S ↑S rfl`, because the copy preserves the star-closure property.

- Claim: For any non-unital star subalgebra `S`, `VTask.copy S ↑S rfl` and `S` have the same carrier set (i.e. `↑(VTask.copy S ↑S rfl) = ↑S`).

## Boundaries

- The proof `hs : s = ↑S` is mandatory; it is impossible to produce a copy whose carrier differs from the original's carrier, so the function is always called at a set that is provably equal to `↑S`.
- When `s` is chosen to be `↑S` and `hs` is `rfl`, the copy is the canonical identity copy and is definitionally equal to `S` in every component that is preserved by the underlying `NonUnitalSubalgebra.copy`.
- The copy operation is not a constructor for a genuinely new subalgebra; it only changes the definitional presentation of the carrier, leaving membership, closure under addition, scalar multiplication, multiplication, and the star operation unchanged.

## Not to be confused with

- `NonUnitalSubalgebra.copy`: the analogous copy operation for non-unital subalgebras without a star structure; `VTask.copy` additionally carries along the star-membership proof.
- `NonUnitalStarSubalgebra.map`: transports a subalgebra along a non-unital star algebra homomorphism, producing a potentially different subalgebra, unlike `VTask.copy` which always stays within the same ambient algebra and carrier.
- `NonUnitalStarSubalgebra.comap`: pulls back a subalgebra along a homomorphism; again, a structural transformation, not a bookkeeping rename of the carrier.
