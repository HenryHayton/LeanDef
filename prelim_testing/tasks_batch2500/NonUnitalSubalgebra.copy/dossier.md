## VTask.copy

### Object

Given a non-unital subalgebra `S` over a commutative semiring `R` acting on a non-unital, non-associative semiring `A`, `VTask.copy` produces a new non-unital subalgebra that is mathematically identical to `S` but whose carrier set is replaced by a provably equal set `s`. The sole purpose is to substitute one presentation of the carrier for another, enabling Lean's definitional equality checker to see the carrier in a preferred form without changing the algebraic content.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {R : Type u} -> {A : Type v} -> [CommSemiring R] -> [NonUnitalNonAssocSemiring A] -> [Module R A] -> (S : NonUnitalSubalgebra R A) -> (s : Set A) -> (hs : s = ↑S) -> NonUnitalSubalgebra R A
<!-- PINNED-SIGNATURE:END -->


The first argument `S` is the source non-unital subalgebra being copied. The second argument `s` is the new set that will serve as the carrier of the resulting subalgebra. The third argument `hs` is a proof that `s` equals the coercion of `S` to a set; this equality witness is what justifies the substitution and guarantees the copy is mathematically the same object.

### Conventions

When `hs` is `rfl` (i.e., `s` is definitionally equal to `↑S`), the copy is definitionally equal to the original; the operation is a no-op up to definitional equality. There are no junk-value conventions because the inputs are fully constrained by the type and the proof `hs`.

### Worked examples

- Claim: An element belongs to `VTask.copy S s hs` if and only if it belongs to `S`.

- Claim: `VTask.copy S (↑S) rfl` has the same carrier as `S`, namely `↑S`.

- Claim: For any `r : R` and `a : A`, if `a ∈ S` then `r • a ∈ VTask.copy S s hs`, whenever `hs : s = ↑S`.

### Boundaries

- The proof `hs` must be provided; there is no default. If `s ≠ ↑S` there is no way to construct `hs`, so the operation is only applicable when the sets are propositionally equal.
- When `s` is literally `↑S` and `hs` is `rfl`, the copy is definitionally identical to `S` in all its algebraic structure (addition, multiplication, scalar multiplication), not merely propositionally equal.
- The operation does not create a subalgebra with a larger or smaller set of elements; the algebraic structure (closure under addition, multiplication, and scalar multiplication) is fully inherited from `S` via `hs`.

### Not to be confused with

- `NonUnitalSubalgebra.map`: transports a subalgebra along an algebra homomorphism to a genuinely different subalgebra, potentially with different elements.
- `NonUnitalSubalgebra.comap`: pulls a subalgebra back along a homomorphism, again producing a structurally different object.
- Subtype coercion `↑S : Set A`: this is just the underlying carrier set of `S`, not a new subalgebra object.
