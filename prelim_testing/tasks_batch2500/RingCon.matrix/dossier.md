## Object

`VTask.matrix` constructs, from a ring congruence `c` on a (non-unital, non-associative) semiring `R`, a ring congruence on the ring of `n × n` matrices over `R`. Two matrices are related by this congruence precisely when every corresponding pair of entries is related by `c`; in other words, the congruence is imposed entry-wise.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.matrix : {R : Type u_1} -> (n : Type u_2) -> [NonUnitalNonAssocSemiring R] -> [Fintype n] -> (c : RingCon R) -> RingCon (Matrix n n R)
<!-- PINNED-SIGNATURE:END -->


`VTask.matrix : {R : Type u_1} -> (n : Type u_2) -> [NonUnitalNonAssocSemiring R] -> [Fintype n] -> (c : RingCon R) -> RingCon (Matrix n n R)`

The implicit type `R` is the coefficient semiring. The argument `n` is the index type used to label rows and columns of the square matrices (it must be finite). The instance `NonUnitalNonAssocSemiring R` supplies the semiring structure on `R`. The instance `Fintype n` ensures that `n` is a finite type so that matrix multiplication (a finite sum) is well-defined. The argument `c` is the ring congruence on `R` from which the matrix congruence is lifted.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total construction that is well-defined for every valid `c`, every finite index type `n`, and every `NonUnitalNonAssocSemiring R`.

## Worked examples

- Claim: For the trivial ring congruence on `ℤ` (where every pair is related), `VTask.matrix n c` relates any two `n × n` integer matrices.

- Claim: For the equality ring congruence on `ℤ` (where only equal elements are related), `VTask.matrix n c` relates two `n × n` matrices if and only if they are equal entry-by-entry, i.e., if and only if the matrices themselves are equal.

- Claim: If `c` is the ring congruence on `ℤ` induced by the ideal `(m)` (i.e., `c a b ↔ m ∣ a - b`), then two integer matrices `M` and `N` are related by `VTask.matrix n c` if and only if `m` divides every entry of `M - N`.

## Boundaries

- When `n` is the empty type (e.g., `Fin 0`), there are no matrix entries, so the entry-wise condition is vacuously satisfied: every pair of `0 × 0` matrices is related by `VTask.matrix n c` regardless of what `c` is.
- When `c` is the full (trivial) congruence that relates all pairs, `VTask.matrix n c` is also the full congruence on matrices.
- When `c` is the discrete (equality) congruence, `VTask.matrix n c` is the equality congruence on matrices.
- The construction is valid even when `R` is not commutative and not unital, since it only requires `NonUnitalNonAssocSemiring`.

## Not to be confused with

- The ring congruence `RingCon.pi` (congruence on a product/pi type): that lifts a family of congruences to a product ring, whereas `VTask.matrix` specifically targets the matrix ring with its multiplication defined by finite sums.
- `Con.matrix` or a similar setoid-level construction: such a construction would only track the equivalence relation, not the compatibility with the ring operations (addition and multiplication).
- Applying a `RingHom` quotient map entry-wise to produce a map of matrix rings: that is a ring homomorphism between quotient rings, not a congruence on the original matrix ring.