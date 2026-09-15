## Object

`VTask.orthonormalBasisOneI` is the specific orthonormal basis `![1, I]` for the complex numbers `ℂ` regarded as a two-dimensional real inner product space. Concretely, the first basis vector (index `0`) is the real number `1` embedded in `ℂ`, and the second basis vector (index `1`) is the imaginary unit `I`. These two vectors are mutually orthogonal and each has unit norm with respect to the standard real inner product on `ℂ`, and together they span all of `ℂ` over `ℝ`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.orthonormalBasisOneI : OrthonormalBasis (Fin 2) ℝ ℂ
<!-- PINNED-SIGNATURE:END -->


`VTask.orthonormalBasisOneI : OrthonormalBasis (Fin 2) ℝ ℂ`

This is a zero-argument constant (a term, not a function). The index type `Fin 2` records that there are exactly two basis vectors, `ℝ` is the scalar field, and `ℂ` is the inner product space being given a basis.

## Conventions

No junk-value conventions apply here: the object is a fully determined, closed constant with no inputs and no edge cases requiring convention.

## Worked examples

- Claim: The coercion of `VTask.orthonormalBasisOneI` to a function `Fin 2 → ℂ` equals the vector `![1, I]`.

- Claim: Evaluating `VTask.orthonormalBasisOneI` at index `0` gives the complex number `1`.

- Claim: Evaluating `VTask.orthonormalBasisOneI` at index `1` gives the complex number `I`.

- Claim: The representation (coordinate map) of a complex number `z` in this basis is `![z.re, z.im]`, i.e., the real part is the coefficient of `1` and the imaginary part is the coefficient of `I`.

- Claim: The inverse of the representation map sends a pair `(a, b) : EuclideanSpace ℝ (Fin 2)` to the complex number `a + b * I`.

## Boundaries

- The basis has exactly two elements; `Fin 2` cannot be extended or restricted.
- The scalars must be `ℝ`; `ℂ` as a `ℂ`-inner-product space would be one-dimensional and is a different object entirely.
- Orthonormality is with respect to the real inner product `⟪z, w⟫_ℝ = Re(z * conj(w))`; using a different inner product would change which bases are orthonormal.
- The underlying (non-orthonormal) basis `basisOneI` carries the same vectors; `VTask.orthonormalBasisOneI` adds the orthonormality certificate on top of it.

## Not to be confused with

- `Complex.basisOneI`: the same two vectors `![1, I]` packaged as a plain `Basis` (not an `OrthonormalBasis`), without the orthonormality proof bundled in.
- `EuclideanSpace.basisFun ℝ (Fin 2)`: the standard orthonormal basis of `ℝ²`, which lives in a different type from `ℂ`.
- The complex numbers regarded as a one-dimensional `ℂ`-inner-product space: that is a different structure where `{1}` alone forms a basis.