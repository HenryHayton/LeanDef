## VTask.tprodCoeff

### Object

`VTask.tprodCoeff R r f` is an element of the tensor product `⨂[R] i, s i` (the *Pi tensor product* of the family of modules `s` over the commutative semiring `R`). It represents the pure tensor formed by taking one vector from each factor — namely `f i ∈ s i` for each index `i` — and then multiplying the result by the scalar coefficient `r ∈ R`. Concretely, it is the scalar-weighted simple tensor `r · (⨂ᵢ f i)`. It is an auxiliary building-block for the Pi tensor product construction; the main user-facing notion is `tprod`, which corresponds to the special case where the coefficient is `1`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.tprodCoeff : {ι : Type u_1} -> (R : Type u_4) -> [CommSemiring R] -> {s : ι → Type u_7} -> [(i : ι) → AddCommMonoid (s i)] -> [(i : ι) → Module R (s i)] -> (r : R) -> (f : (i : ι) → s i) -> PiTensorProduct R fun i => s i
<!-- PINNED-SIGNATURE:END -->


The first explicit argument, `R`, is the commutative semiring of scalars over which the tensor product is taken. The implicit argument `ι` is the index type parametrising the family of modules. The implicit argument `s` is the family of `R`-modules, one per index `i : ι`. The argument `r : R` is the scalar coefficient multiplying the pure tensor. The argument `f : (i : ι) → s i` is the family of vectors, one from each module in the family; the pure tensor is formed from these vectors.

### Conventions

When the coefficient `r` is `0`, the result is the zero element of the tensor product, regardless of `f`. When any component `f i` is the zero vector of `s i`, the result is also the zero element of the tensor product, regardless of the coefficient and the other components. The canonical simple tensor `tprod R f` without an explicit coefficient coincides with `VTask.tprodCoeff R 1 f`.

### Worked examples

- Claim: For any `f`, `VTask.tprodCoeff R 0 f = 0` in the Pi tensor product.

- Claim: For any coefficient `z` and family `f`, `VTask.tprodCoeff R z f` equals `z • tprod R f`, so the coefficient acts as a scalar on the pure tensor.

- Claim: Coefficients are additive: `VTask.tprodCoeff R z₁ f + VTask.tprodCoeff R z₂ f = VTask.tprodCoeff R (z₁ + z₂) f`.

- Claim: Any element of the Pi tensor product can be written as a finite sum of terms of the form `VTask.tprodCoeff R r f`, making these elements a spanning set.

### Boundaries

- If the coefficient `r = 0`, the output is `0` regardless of `f` (by `zero_tprodCoeff`).
- If any component `f i = 0`, the output is `0` regardless of `r` and the other components (by `zero_tprodCoeff'`).
- When `r = 1`, the output equals the standard pure tensor `tprod R f`, so `tprodCoeff` strictly generalises `tprod`.
- Scalar multiplication on the outside of the expression, `r' • VTask.tprodCoeff R z f`, equals `VTask.tprodCoeff R (r' • z) f`, so the outer scalar folds into the coefficient.
- Updating a component by a scalar, `f i ↦ r • f i`, multiplies the coefficient: `VTask.tprodCoeff R z (update f i (r • f i)) = VTask.tprodCoeff R (r * z) f`.

### Not to be confused with

- `tprod R f`: The uncoefficiented pure tensor (coefficient implicitly `1`); `VTask.tprodCoeff R 1 f = tprod R f`.
- `TensorProduct.tmul` (the binary tensor product `⊗`): That construction is for two modules only; `VTask.tprodCoeff` handles an arbitrary index family.
- A general element of `⨂[R] i, s i`: Arbitrary elements are sums of terms of the form `VTask.tprodCoeff`; `VTask.tprodCoeff` itself is a single summand, not a general element.