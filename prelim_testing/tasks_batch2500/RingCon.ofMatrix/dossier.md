## Object

`VTask.ofMatrix` takes a ring congruence `c` on the matrix ring `Matrix n n R` and produces a ring congruence on the scalar ring `R`. Two elements `x, y : R` are considered congruent under this induced relation if and only if, for every pair of indices `(i, j)`, the scalar matrices `single i j x` and `single i j y` are congruent under `c`. Here `single i j r` is the matrix that is `r` in position `(i, j)` and zero everywhere else.

Intuitively, `VTask.ofMatrix c` is the coarsest congruence on `R` such that the embedding `r ↦ single i j r` is compatible with `c` for every position `(i, j)`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofMatrix : {R : Type u_1} -> {n : Type u_2} -> [NonUnitalNonAssocSemiring R] -> [Fintype n] -> [DecidableEq n] -> (c : RingCon (Matrix n n R)) -> RingCon R
<!-- PINNED-SIGNATURE:END -->


`VTask.ofMatrix : {R : Type u_1} -> {n : Type u_2} -> [NonUnitalNonAssocSemiring R] -> [Fintype n] -> [DecidableEq n] -> (c : RingCon (Matrix n n R)) -> RingCon R`

- `R` is the implicit scalar type, which must carry a `NonUnitalNonAssocSemiring` structure.
- `n` is the implicit index type for the matrix dimensions; it must be a `Fintype` with decidable equality, so that `Matrix n n R` is well-formed and matrix operations are computable.
- `c` is the ring congruence on the full matrix ring `Matrix n n R` from which the induced congruence on `R` is constructed.

## Conventions

There are no special junk-value or boundary conventions declared for this definition: the construction is well-defined for any `NonUnitalNonAssocSemiring R`, any `Fintype n` with `DecidableEq n`, and any ring congruence `c` on `Matrix n n R`, so no degenerate inputs arise that require a special-case convention.

## Worked examples

- Claim: For the universal congruence `⊤` on `Matrix n n R` (where every pair of matrices is related), the induced congruence `VTask.ofMatrix ⊤` on `R` is also `⊤` (every pair of scalars is related), because `single i j x` and `single i j y` are always related under `⊤`.

- Claim: For the trivial congruence `⊥` on `Matrix n n R` (only equal matrices are related), the induced congruence `VTask.ofMatrix ⊥` on `R` relates `x` and `y` if and only if `single i j x = single i j y` for all `i j`, which holds precisely when `x = y`; hence `VTask.ofMatrix ⊥ = ⊥` on `R`.

- Claim: If `c₁ ≤ c₂` as ring congruences on `Matrix n n R` (i.e., `c₁` is finer than `c₂`), then `VTask.ofMatrix c₁ ≤ VTask.ofMatrix c₂` as ring congruences on `R`, because whenever `single i j x` and `single i j y` are related under `c₁`, they are also related under `c₂`.

## Boundaries

- When `n` is empty (a `Fintype` with no elements), the universal quantification `∀ i j` is vacuously true, so every pair `(x, y)` is related under `VTask.ofMatrix c` regardless of `c`; the induced congruence is `⊤`.
- When `n` is a singleton type, there is only one matrix position `(i, j)`, so the induced relation on `R` exactly mirrors whether `c` relates the corresponding single-entry matrices.
- The construction is defined for `NonUnitalNonAssocSemiring`, the weakest semiring-like structure available, so it applies in very general algebraic settings.

## Not to be confused with

- `RingCon.toMatrix` (or analogous constructions): goes in the opposite direction, extracting a congruence on matrices from one on scalars, rather than pulling back from matrices to scalars.
- `Matrix.mapRingHom` or similar: a ring homomorphism applied entry-wise to matrices, which is a map between rings, not a congruence.
- `RingCon.comap`: the general pullback of a ring congruence along a ring homomorphism; `VTask.ofMatrix` is a specific instance of this idea using the family of maps `r ↦ single i j r`, but is not literally spelled as `comap`.