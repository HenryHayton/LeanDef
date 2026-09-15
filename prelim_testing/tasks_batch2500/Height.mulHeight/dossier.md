## Object

The **multiplicative height** of a tuple of field elements is a real-valued size measure that combines information from all absolute values on the field — both archimedean and non-archimedean — into a single positive real number. Concretely, it is the product of two factors: a finite product over the archimedean absolute values (each contributing the supremum of that absolute value applied to the entries of the tuple), and an infinite (finitely supported) product over the non-archimedean absolute values (each contributing the supremum of that absolute value applied to the entries). The result is always at least 1 and is independent of projective rescaling of the tuple (the product formula ensures invariance under scaling by field elements). For the zero tuple, the value is defined to be 1 by convention.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mulHeight : {K : Type u_1} -> [Field K] -> [Height.AdmissibleAbsValues K] -> {ι : Type u_2} -> (x : ι → K) -> ℝ
<!-- PINNED-SIGNATURE:END -->


`VTask.mulHeight : {K : Type u_1} -> [Field K] -> [Height.AdmissibleAbsValues K] -> {ι : Type u_2} -> (x : ι → K) -> ℝ`

The implicit type `K` is the field whose elements form the entries of the tuple. The `Field K` instance provides the algebraic structure. The `Height.AdmissibleAbsValues K` instance packages the collection of admissible archimedean and non-archimedean absolute values on `K` satisfying the product formula. The implicit type `ι` is the index type parameterising the tuple. The explicit argument `x : ι → K` is the tuple of field elements whose multiplicative height is being computed.

## Conventions

When the tuple `x` is identically zero (i.e., `x = 0` as a function `ι → K`), the multiplicative height is defined to be `1`. This is a junk value chosen for definitional convenience rather than mathematical meaning, since the zero tuple does not represent a well-defined point in projective space.

## Worked examples

- Claim: The multiplicative height of the zero tuple equals 1.

- Claim: The multiplicative height of the constant-one tuple equals 1 (since every absolute value sends 1 to 1, so each supremum is 1 and both products collapse to 1).

- Claim: The multiplicative height of any tuple `x : ι → K` is strictly positive, i.e., `0 < VTask.mulHeight x`.

- Claim: The multiplicative height of any tuple `x : ι → K` satisfies `1 ≤ VTask.mulHeight x` when the absolute values satisfy the product formula normalisation (this holds for the constant-one tuple and for the zero tuple by convention).

## Boundaries

- **Zero tuple**: `VTask.mulHeight (0 : ι → K) = 1` by definition (junk value).
- **Constant-one tuple**: `VTask.mulHeight (1 : ι → K) = 1` because every admissible absolute value sends 1 to 1.
- **Positivity**: For every tuple `x`, one has `0 < VTask.mulHeight x`; the height is never zero or negative.
- **Empty index type**: When `ι` is empty there are no entries; the supremum over an empty set may default to 0 or ⊥ depending on the order, but the overall height is still a well-defined positive real.
- **Projective invariance**: Scaling the tuple by a nonzero scalar does not change the height (product formula).

## Not to be confused with

- **`VTask.logHeight`** — the logarithmic height, which is the natural logarithm of the multiplicative height; the two carry equivalent information but live in additive vs. multiplicative form.
- **`VTask.mulHeight₁`** — the multiplicative height of a *single* field element (a scalar rather than a tuple); it is the special case `ι = Unit` of the tuple version.
- **`VTask.mulHeightBound`** — an upper-bound quantity associated to a tuple of multivariate polynomials, used in effectivity estimates, not the height of a tuple of field elements.