## Object

`VTask.rid R A M` is the canonical linear equivalence (over the ring `A`) between the tensor product `M ⊗[R] R` and `M` itself. It is the "right identity" isomorphism for the tensor product: tensoring a module `M` with the base ring `R` on the right yields a module that is naturally (and `A`-linearly) isomorphic to `M`. This is the heterobasic generalisation of the usual `TensorProduct.rid`, allowing the tensor product to be taken over `R` while the resulting equivalence is `A`-linear, where `A` is an `R`-algebra that also acts on `M` compatibly.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.rid : (R : Type uR) -> (A : Type uA) -> (M : Type uM) -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [AddCommMonoid M] -> [Module R M] -> [Module A M] -> [IsScalarTower R A M] -> TensorProduct R M R ≃ₗ[A] M
<!-- PINNED-SIGNATURE:END -->


`VTask.rid : (R : Type uR) -> (A : Type uA) -> (M : Type uM) -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [AddCommMonoid M] -> [Module R M] -> [Module A M] -> [IsScalarTower R A M] -> TensorProduct R M R ≃ₗ[A] M`

- `R` is the commutative semiring over which the tensor product is formed; it also plays the role of the "right factor" being tensored.
- `A` is a semiring that is also an `R`-algebra; the resulting equivalence is `A`-linear rather than merely `R`-linear.
- `M` is the module being tensored; it carries both an `R`-module structure, an `A`-module structure, and the two are compatible in the sense of the scalar tower condition.
- The instance arguments enforce that `R` is a commutative semiring, `A` is a semiring and an `R`-algebra, `M` is an additive commutative monoid with compatible `R`- and `A`-module structures, and that the scalar actions of `R`, `A`, and `M` form a scalar tower.

## Conventions

There are no junk-value or default-output conventions declared for this definition: it is a total construction on well-typed inputs, and every valid tuple `(R, A, M)` satisfying the type-class hypotheses yields a fully defined linear equivalence.

## Worked examples

- Claim: Applying `VTask.rid R A M` to a pure tensor `m ⊗ₜ r` yields `r • m`.

- Claim: The inverse of `VTask.rid R A M` sends `m : M` to `m ⊗ₜ[R] (1 : R)`.

- Claim: When `A = R`, `VTask.rid R R M` coincides with the standard `TensorProduct.rid R M` (as a linear equivalence over `R`), as witnessed by the theorem `rid_eq_rid`.

- Claim: For `R = ℤ`, `A = ℚ` (with the canonical algebra structure), and `M = ℚ`, applying `VTask.rid ℤ ℚ ℚ` to `(3 : ℚ) ⊗ₜ[ℤ] (2 : ℤ)` gives `(6 : ℚ)`, since the result is `(2 : ℤ) • (3 : ℚ) = 6`.

## Boundaries

- The equivalence is defined for any `M` satisfying the scalar tower condition `IsScalarTower R A M`; in particular it applies when `A = R` (recovering the standard right unitor), or when `M = A` itself.
- The tensor product on the left is taken strictly over `R` (written `M ⊗[R] R`), not over `A`; this is essential for the heterobasic setting.
- The `A`-linearity of the equivalence is strictly stronger than `R`-linearity, and relies on the scalar tower and the `A`-module structure on `M`.
- Both the forward map and the inverse are explicitly given by simple formulas (scalar multiplication and the elementary tensor map), so the equivalence is computationally transparent.

## Not to be confused with

- `TensorProduct.rid R M`: the standard right unitor, which is only `R`-linear (not `A`-linear) and does not involve a separate algebra `A`; recovered as a special case when `A = R`.
- `TensorProduct.AlgebraTensorModule.lid`: the analogous left-identity isomorphism `R ⊗[R] M ≃ₗ[A] M`, acting on the left factor rather than the right.
- `TensorProduct.rid` applied with `A` as the base ring: that would form `M ⊗[A] A ≃ₗ[A] M`, tensoring over the larger ring `A` rather than over `R`.