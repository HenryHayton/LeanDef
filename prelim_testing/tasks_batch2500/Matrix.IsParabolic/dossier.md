## Object

A 2×2 matrix over a commutative ring is called **parabolic** if it satisfies two conditions simultaneously:
1. It is **not a scalar matrix** — that is, it is not of the form λ·I for any scalar λ in the ring.
2. Its **discriminant is zero** — the discriminant of a 2×2 matrix M = [[a, b], [c, d]] is defined as (a − d)² + 4bc, and this quantity equals 0.

Intuitively, parabolic matrices are those whose characteristic polynomial has a repeated root (discriminant zero) but which are not multiples of the identity (they are genuinely non-trivial).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsParabolic : {R : Type u_1} -> [CommRing R] -> (m : Matrix (Fin 2) (Fin 2) R) -> Prop
<!-- PINNED-SIGNATURE:END -->


VTask.IsParabolic : {R : Type u_1} -> [CommRing R] -> (m : Matrix (Fin 2) (Fin 2) R) -> Prop

The type parameter `R` is the commutative ring over which matrix entries live; it is inferred automatically. The commutative ring instance is found automatically by type-class search. The argument `m` is the 2×2 matrix being tested for parabolicity.

## Conventions

There are no junk-value or boundary conventions declared for this definition: it is a logically total predicate, well-defined for every 2×2 matrix over any commutative ring, including degenerate rings such as the zero ring.

## Worked examples

- Claim: The matrix [[1, 1], [0, 1]] over ℤ is parabolic — it has discriminant (1−1)² + 4·0·1 = 0 and is not a scalar matrix.

- Claim: The identity matrix I₂ over ℤ is NOT parabolic — even though its discriminant is 0, it is a scalar matrix (1·I).

- Claim: The matrix [[2, 1], [0, 2]] over ℤ is parabolic — its discriminant is (2−2)² + 4·1·0 = 0, and it is not a scalar matrix since the off-diagonal entry is nonzero.

- Claim: The matrix [[0, 0], [0, 0]] over ℤ is NOT parabolic — despite having zero discriminant, it equals 0·I and is therefore a scalar matrix.

## Boundaries

- **Scalar matrices are excluded by definition**: even if a scalar matrix happens to have zero discriminant (which all scalar matrices do, since a scalar λI has discriminant (λ−λ)² + 4·0·0 = 0), scalar matrices are never parabolic.
- **Over the zero ring** (where 0 = 1), every matrix is a scalar matrix, so no matrix is parabolic.
- **Nilpotent off-diagonal matrices** such as [[0, 1], [0, 0]] are parabolic over any commutative ring, since their discriminant is 0 and they are not scalar.
- **Over fields of characteristic 2**, the discriminant condition 0 = (a−d)² + 4bc reduces to 0 = (a−d)², so a+d = a−d must be 0; the condition then becomes a = d together with non-scalarity (b ≠ 0 or c ≠ 0).

## Not to be confused with

- **`Matrix.IsScalar` / scalar matrices**: scalar matrices satisfy the discriminant-zero condition but are explicitly excluded from `VTask.IsParabolic`.
- **`Matrix.IsNilpotent`**: nilpotency for 2×2 matrices implies trace zero and determinant zero, which is a stronger condition; not all parabolic matrices are nilpotent.
- **Hyperbolic/elliptic 2×2 matrices**: those correspond to nonzero discriminant (either a perfect square or not), in contrast to the zero-discriminant condition here.