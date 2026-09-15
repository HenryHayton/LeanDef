## Object

A multivariate polynomial over a commutative semiring is **symmetric** if it is unchanged when its variables are permuted in any way. Concretely, applying any bijection on the index set of variables to the polynomial's variables yields the same polynomial.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsSymmetric : {σ : Type u_1} -> {R : Type u_3} -> [CommSemiring R] -> (φ : MvPolynomial σ R) -> Prop
<!-- PINNED-SIGNATURE:END -->


The type parameter `σ` is the index type of the variables; `R` is the coefficient ring, assumed to be a commutative semiring. The argument `φ` is the multivariate polynomial being tested for symmetry. The proposition asserts that `φ` is symmetric.

## Conventions

No special junk-value or out-of-range conventions are declared: the predicate is meaningful and total for every choice of `σ`, `R`, and `φ`.

## Worked examples

- Claim: The polynomial `X 0 + X 1 : MvPolynomial (Fin 2) ℤ` is symmetric, because swapping the two variables sends `X 0 + X 1` to `X 1 + X 0`, which equals `X 0 + X 1`.

- Claim: The polynomial `X 0 * X 1 : MvPolynomial (Fin 2) ℤ` is symmetric, as any permutation of two variables either fixes both or swaps them, and the product is invariant under that swap.

- Claim: The polynomial `X 0 : MvPolynomial (Fin 2) ℤ` is NOT symmetric, because the transposition swapping `0` and `1` sends it to `X 1 ≠ X 0`.

- Claim: Every constant polynomial (one whose coefficients define a polynomial independent of all variables) satisfies `VTask.IsSymmetric`, since renaming variables has no effect on a polynomial that does not involve them.

## Boundaries

- When `σ` is empty (no variables), there are no permutations to check, so the universal quantification is vacuously true: every polynomial over the empty variable set is symmetric.
- When `σ` is a singleton, the only permutation is the identity, so every polynomial in a single variable is symmetric.
- The predicate is defined over all commutative semirings, including those of characteristic 2 or nonzero characteristic; no field or cancellation assumptions are needed.
- The predicate is about the full group of permutations of `σ`, so it is strictly stronger than invariance under any proper subgroup of permutations.

## Not to be confused with

- `MvPolynomial.rename e φ` — this is the operation of renaming variables by a permutation `e`; `VTask.IsSymmetric` asserts this operation is the identity for all `e`.
- Symmetric functions in the sense of formal power series or the ring of symmetric functions — `VTask.IsSymmetric` is the analogous predicate on ordinary multivariate polynomials, not on formal series.
- Invariance under a fixed single transposition — `VTask.IsSymmetric` requires invariance under *all* permutations, not just one generator.