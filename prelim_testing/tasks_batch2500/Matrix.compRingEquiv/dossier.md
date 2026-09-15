## Object

`VTask.compRingEquiv` is the canonical ring isomorphism that identifies a matrix of matrices with a single larger block matrix. Concretely, it sends an `I×I` matrix whose entries are themselves `J×J` matrices (with coefficients in `R`) to a single `(I×J)×(I×J)` matrix over `R`, by "flattening" the two-level structure. The inverse operation "blocks" a large matrix back into a matrix of matrices. This upgrade of the underlying additive equivalence to a ring equivalence asserts that the flattening operation is compatible with both addition and multiplication of matrices.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.compRingEquiv : (I : Type u_1) -> (J : Type u_2) -> (R : Type u_5) -> [AddCommMonoid R] -> [Mul R] -> [Fintype I] -> [Fintype J] -> Matrix I I (Matrix J J R) ≃+* Matrix (I × J) (I × J) R
<!-- PINNED-SIGNATURE:END -->


`VTask.compRingEquiv : (I : Type u_1) -> (J : Type u_2) -> (R : Type u_5) -> [AddCommMonoid R] -> [Mul R] -> [Fintype I] -> [Fintype J] -> Matrix I I (Matrix J J R) ≃+* Matrix (I × J) (I × J) R`

The first argument `I` is the outer index type, labelling rows and columns of the matrix-of-matrices. The second argument `J` is the inner index type, labelling rows and columns within each block entry. The third argument `R` is the coefficient ring over which the entries of every inner matrix live. The `AddCommMonoid` and `Mul` instances supply addition and multiplication on `R`, while the `Fintype` instances on `I` and `J` are needed to form matrix products (sums over index sets).

## Conventions

There are no declared junk-value or boundary conventions for this definition: it is a bundled isomorphism between two well-typed algebraic structures, defined for all `Fintype` index types and all `AddCommMonoid`+`Mul` coefficient types, so no silent defaults or out-of-domain behaviours arise.

## Worked examples

- Claim: For `I = J = Fin 1` and `R = ℤ`, applying `VTask.compRingEquiv` to the `1×1` matrix containing the `1×1` integer identity matrix yields the `1×1` integer identity matrix over `(Fin 1 × Fin 1)`.

- Claim: For `I = Fin 2`, `J = Fin 2`, `R = ℤ`, applying `VTask.compRingEquiv` and then its inverse recovers the original matrix-of-matrices (round-trip via `symm`).

- Claim: `VTask.compRingEquiv` preserves multiplication, i.e., for any two `Matrix (Fin 2) (Fin 2) (Matrix (Fin 2) (Fin 2) R)` matrices `A` and `B`, `VTask.compRingEquiv _ _ _ (A * B) = VTask.compRingEquiv _ _ _ A * VTask.compRingEquiv _ _ _ B`.

## Boundaries

- When `I` or `J` is an empty type (`Fintype` with zero elements), both sides of the equivalence are the unique `0×0` (empty) matrix, and the isomorphism is trivially the unique map between them.
- When `I` or `J` has a single element (`Fin 1`), the equivalence is essentially the identity: a `1×1` matrix of `1×1` matrices is the same as a `1×1` matrix.
- The isomorphism is definitionally the same underlying function as `compAddEquiv` on the additive side; the ring structure (multiplicativity) is the additional content.
- The inverse (`symm`) correspondingly takes a `(I×J)×(I×J)` matrix and recovers the blocked `I×I` matrix of `J×J` blocks.

## Not to be confused with

- `Matrix.reindex` — a ring equivalence induced by a mere reindexing (bijection on the index type), which does not change the "depth" of the matrix structure.
- `Matrix.compAddEquiv` — the underlying additive group isomorphism doing the same flattening, but without the multiplicative compatibility (not a ring equivalence).
- `Matrix.blockDiag` / `Matrix.fromBlocks` — operations that arrange matrices into block form by concatenation rather than by the Kronecker-product-style flattening that `compRingEquiv` performs.