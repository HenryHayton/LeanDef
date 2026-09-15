## Object

This is a canonical linear equivalence (an invertible `R`-linear, in fact `S`-linear, map) between the tensor product of two matrix spaces and a matrix space whose entries are tensor products. Concretely, given a matrix with entries in `M` of shape `l × m` and a matrix with entries in `N` of shape `n × p`, their tensor product (as `R`-modules) is canonically identified, in an `S`-linear fashion, with a matrix of shape `(l × n) × (m × p)` whose entries lie in `M ⊗[R] N`. The underlying map is the Kronecker-tensor product construction: it sends the tensor product of two matrices to the matrix whose `((i₁, i₂), (j₁, j₂))`-entry is `A i₁ j₁ ⊗ B i₂ j₂`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.kroneckerTMulLinearEquiv : (l : Type u_1) -> (m : Type u_2) -> (n : Type u_3) -> (p : Type u_4) -> (R : Type u_5) -> (S : Type u_6) -> (M : Type u_9) -> (N : Type u_10) -> [CommSemiring R] -> [Semiring S] -> [AddCommMonoid M] -> [AddCommMonoid N] -> [Algebra R S] -> [Module R M] -> [Module S M] -> [Module R N] -> [IsScalarTower R S M] -> [Fintype l] -> [Fintype m] -> [Fintype n] -> [Fintype p] -> [DecidableEq l] -> [DecidableEq m] -> [DecidableEq n] -> [DecidableEq p] -> TensorProduct R (Matrix l m M) (Matrix n p N) ≃ₗ[S] Matrix (l × n) (m × p) (TensorProduct R M N)
<!-- PINNED-SIGNATURE:END -->


VTask.kroneckerTMulLinearEquiv : (l : Type u_1) -> (m : Type u_2) -> (n : Type u_3) -> (p : Type u_4) -> (R : Type u_5) -> (S : Type u_6) -> (M : Type u_9) -> (N : Type u_10) -> [CommSemiring R] -> [Semiring S] -> [AddCommMonoid M] -> [AddCommMonoid N] -> [Algebra R S] -> [Module R M] -> [Module S M] -> [Module R N] -> [IsScalarTower R S M] -> [Fintype l] -> [Fintype m] -> [Fintype n] -> [Fintype p] -> [DecidableEq l] -> [DecidableEq m] -> [DecidableEq n] -> [DecidableEq p] -> TensorProduct R (Matrix l m M) (Matrix n p N) ≃ₗ[S] Matrix (l × n) (m × p) (TensorProduct R M N)

`l`, `m`, `n`, `p` are the index types determining matrix dimensions: `l × m` is the shape of the first matrix and `n × p` is the shape of the second, with the result having shape `(l × n) × (m × p)`. `R` is the base commutative semiring over which the tensor product is formed. `S` is a (possibly non-commutative) semiring that is an `R`-algebra and acts on `M` from the left, making the equivalence `S`-linear (not merely `R`-linear). `M` and `N` are the entry types for the two matrix factors, carrying the `R`-module structures needed to form the tensor product. The scalar-tower hypothesis ensures the `R`- and `S`-actions on `M` are compatible.

## Conventions

No special junk-value or edge conventions are declared for this definition. All index types are required to be `Fintype` with `DecidableEq`, so the empty-index edge cases (empty matrices) are handled by the general algebraic structure: the tensor product of zero-row or zero-column matrix modules is the zero module, and the equivalence transports this correctly without any special-casing.

## Worked examples

- Claim: When `A` is the `1 × 1` identity matrix over `R` (as an `R`-module-valued matrix) and `B` is similarly `1 × 1`, the image of `A ⊗ₜ B` under `VTask.kroneckerTMulLinearEquiv` is the unique `(Fin 1 × Fin 1) × (Fin 1 × Fin 1)`-matrix whose sole entry is `A (0,0) ⊗ B (0,0)`.

- Claim: For elementary matrices `e_{ij}` (a matrix with a single nonzero entry equal to `m : M` at position `(i,j)`) and `e_{kl}` (entry `n : N` at `(k,l)`), the image of `e_{ij} ⊗ₜ e_{kl}` is the elementary matrix with entry `m ⊗ n` at position `((i,k),(j,l))` and zero elsewhere.

- Claim: The forward and inverse maps are mutual inverses on all elements, so `VTask.kroneckerTMulLinearEquiv.toEquiv` is a genuine set-theoretic bijection.

## Boundaries

- If any index type is empty (e.g., `l = Fin 0`), the matrix space `Matrix (Fin 0) m M` is the zero module, the tensor product is the zero module, and the target matrix space is likewise zero; the equivalence restricts to the unique isomorphism between zero modules.
- The equivalence is `S`-linear (not merely `R`-linear), which is strictly stronger when `S ≠ R`. If `S = R`, the two notions coincide.
- The `IsScalarTower R S M` hypothesis is essential: without it one cannot consistently interpret the `S`-module structure on the tensor product side.
- The entry type `N` carries only an `R`-module structure (not necessarily an `S`-module), so the `S`-linearity comes entirely from the `M`-factor side.

## Not to be confused with

- `Matrix.kroneckerTMul`: the underlying bilinear map sending a pair of matrices to a Kronecker-tensor product matrix, without the bundled equivalence structure.
- The classical Kronecker product for square matrices over a commutative ring: that operation lives entirely in `Matrix (l × n) (m × p) R` and does not involve a tensor product of the coefficient modules.
- `TensorProduct.congr` or `TensorProduct.map`: general functoriality maps on tensor products that do not encode the Kronecker index-interleaving structure.
