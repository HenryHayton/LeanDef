## Object

`VTask.copy` produces a new `StarSubalgebra` that is definitionally identical to a given one, but whose underlying carrier set is supplied explicitly by the caller. Because the new carrier is required to be provably equal to the original carrier, the resulting star subalgebra has the same elements, the same algebraic operations, and the same star structure — it is merely a copy with a potentially different *syntactic* carrier, which is useful when Lean's definitional equality checker needs the carrier to have a specific normal form.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {R : Type u_2} -> {A : Type u_3} -> [CommSemiring R] -> [StarRing R] -> [Semiring A] -> [StarRing A] -> [Algebra R A] -> [StarModule R A] -> (S : StarSubalgebra R A) -> (s : Set A) -> (hs : s = ↑S) -> StarSubalgebra R A
<!-- PINNED-SIGNATURE:END -->


The typeclass arguments fix an ambient commutative semiring `R` with a star, a semiring `A` with a star, an `R`-algebra structure on `A`, and the compatibility condition that the star on `A` is `R`-linear (StarModule). `S` is the source star subalgebra being copied. `s` is the new carrier set that will be used for the resulting star subalgebra. `hs` is the proof that `s` is equal to the coercion of `S` to a set, i.e., `s = ↑S`; this equality is what guarantees the copy is mathematically identical to the original.

## Conventions

There are no junk-value or edge-case conventions specific to this definition: it is a total function requiring an explicit equality proof, so the output is always a well-formed `StarSubalgebra` equal to the input.

## Worked examples

- Claim: For any `StarSubalgebra R A` called `S`, `VTask.copy S ↑S rfl` has the same carrier as `S`.

- Claim: An element `x` belongs to `VTask.copy S s hs` if and only if it belongs to `S`; concretely, if `x ∈ S` then `x ∈ VTask.copy S ↑S rfl`.

- Claim: `VTask.copy S ↑S rfl = S` as star subalgebras (they are equal, not merely isomorphic).

## Boundaries

- The proof `hs : s = ↑S` is mandatory; without it the construction cannot proceed. There is no way to call `VTask.copy` with a set that differs from `↑S`.
- When `s` is literally `↑S` and `hs` is `rfl`, the copy is definitionally equal to the original in the carrier; this is the main intended use case.
- The construction is purely structural: no elements are added or removed, and all subalgebra axioms (closure under addition, multiplication, scalar multiplication, the algebra map, and the star) are inherited directly from `S`.

## Not to be confused with

- `StarSubalgebra.map`: produces a genuinely different star subalgebra in a different ambient algebra via a star algebra homomorphism, not a mere carrier-renaming copy.
- `StarSubalgebra.comap`: pulls back a star subalgebra along a star algebra homomorphism; again a structurally new object, not a copy.
- `Subalgebra.copy`: the analogous operation for plain subalgebras (without the star structure); `VTask.copy` wraps this but additionally preserves the `star_mem'` axiom.