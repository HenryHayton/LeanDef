## Object

`VTask.map` constructs a linear map between tensor products in the "heterobasic" (mixed-scalars) setting. Given an `A`-linear map `f : M →ₗ[A] P` and an `R`-linear map `g : N →ₗ[R] Q`, it produces an `A`-linear map `M ⊗[R] N →ₗ[A] P ⊗[R] Q` that acts on pure tensors by the rule `m ⊗ n ↦ f(m) ⊗ g(n)`. The key feature distinguishing this from the ordinary `TensorProduct.map` is that the left map is `A`-linear (for a larger algebra `A`) while the right map is only `R`-linear (for the base commutative semiring `R`), yet the output is an `A`-linear map on the tensor product — this is possible because the tensor product `M ⊗[R] N` carries an `A`-module structure via the scalar tower `R → A → M`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {R : Type uR} -> {A : Type uA} -> {M : Type uM} -> {N : Type uN} -> {P : Type uP} -> {Q : Type uQ} -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [AddCommMonoid M] -> [Module R M] -> [Module A M] -> [IsScalarTower R A M] -> [AddCommMonoid N] -> [Module R N] -> [AddCommMonoid P] -> [Module R P] -> [Module A P] -> [IsScalarTower R A P] -> [AddCommMonoid Q] -> [Module R Q] -> (f : M →ₗ[A] P) -> (g : N →ₗ[R] Q) -> TensorProduct R M N →ₗ[A] TensorProduct R P Q
<!-- PINNED-SIGNATURE:END -->


VTask.map : {R : Type uR} -> {A : Type uA} -> {M : Type uM} -> {N : Type uN} -> {P : Type uP} -> {Q : Type uQ} -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [AddCommMonoid M] -> [Module R M] -> [Module A M] -> [IsScalarTower R A M] -> [AddCommMonoid N] -> [Module R N] -> [AddCommMonoid P] -> [Module R P] -> [Module A P] -> [IsScalarTower R A P] -> [AddCommMonoid Q] -> [Module R Q] -> (f : M →ₗ[A] P) -> (g : N →ₗ[R] Q) -> TensorProduct R M N →ₗ[A] TensorProduct R P Q

`R` is the base commutative semiring over which all tensor products are formed and which acts on all modules in sight. `A` is a semiring equipped with an `R`-algebra structure, providing the larger scalar action; it acts on `M` and `P` compatibly with `R` via scalar towers. `M` is the left factor of the domain tensor product: an `A`-module (and hence an `R`-module) satisfying the scalar tower condition. `N` is the right factor of the domain tensor product: an `R`-module (no `A`-action required). `P` is the left factor of the codomain tensor product: an `A`-module satisfying the scalar tower condition. `Q` is the right factor of the codomain tensor product: an `R`-module. The argument `f` is the `A`-linear map applied to the left factor. The argument `g` is the `R`-linear map applied to the right factor.

## Conventions

There are no junk-value conventions for this definition: it is a total construction defined for all valid inputs in its domain and produces a well-defined `A`-linear map in all cases.

## Worked examples

- Claim: When both `f` and `g` are identity maps (of the appropriate linearity), `VTask.map f g` is the identity on `M ⊗[R] N`.

- Claim: `VTask.map` is functorial: for composable pairs `f₁, f₂` and `g₁, g₂`, `VTask.map (f₂ ∘ₗ f₁) (g₂ ∘ₗ g₁)` equals `(VTask.map f₂ g₂) ∘ₗ (VTask.map f₁ g₁)`.

- Claim: `VTask.map` is additive in the left argument: `VTask.map (f₁ + f₂) g = VTask.map f₁ g + VTask.map f₂ g`.

- Claim: `VTask.map` is additive in the right argument: `VTask.map f (g₁ + g₂) = VTask.map f g₁ + VTask.map f g₂`.

- Claim: On a pure tensor `m ⊗ₜ[R] n`, the map `VTask.map f g` evaluates to `f m ⊗ₜ[R] g n`.

## Boundaries

- When `A = R` (i.e., the algebra is just the base ring), `VTask.map f g` coincides with the ordinary `TensorProduct.map f g`; this is recorded as `map_eq`.
- When `f` and `g` are both the identity, the result is the identity linear map on `M ⊗[R] N` (recorded as `map_id` / `map_one`).
- Scaling `f` by a scalar `b : A` yields `b • VTask.map f g` (recorded as `map_smul_left`); scaling `g` by `r : R` yields `r • VTask.map f g` (recorded as `map_smul_right`).
- The map is defined and well-behaved even when `N` has no `A`-module structure at all; the right factor only ever needs to be an `R`-module.
- Zero maps are handled correctly since bilinearity and additivity propagate through the construction.

## Not to be confused with

- `TensorProduct.map` (the homogeneous version): both `f` and `g` are `R`-linear, and the result is only `R`-linear; `VTask.map` lifts to `A`-linearity on the output when the left map is `A`-linear.
- `TensorProduct.AlgebraTensorModule.mapBilinear`: a bilinear map packaging `VTask.map` as a function of both `f` and `g` simultaneously, rather than the linear map on the tensor product produced by a fixed pair `(f, g)`.
- `LinearMap.rTensor` / `LinearMap.lTensor`: these tensor a single linear map with the identity on one side; `VTask.map` allows independent (heterobasic) maps on both sides simultaneously.