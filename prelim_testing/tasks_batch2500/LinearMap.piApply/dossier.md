## VTask.piApply

### Object

`VTask.piApply` is a bilinear map (presented as a curried pair of linear maps) that takes a family of linear forms — one linear form `eₓ : V x →ₗ[R] R` for each index `x : M` — and a family of vectors — one vector `sₓ : V x` for each index `x : M` — and produces the function `M → R` obtained by applying each linear form pointwise to the corresponding vector: `x ↦ eₓ(sₓ)`. Both the dependence on the family of linear forms and the dependence on the family of vectors are encoded as `R`-linear maps, making the overall object a curried `R`-bilinear map.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piApply : {R : Type u_1} -> {M : Type u_5} -> {V : M → Type u_9} -> [CommSemiring R] -> [(x : M) → AddCommMonoid (V x)] -> [(x : M) → Module R (V x)] -> ((x : M) → V x →ₗ[R] R) →ₗ[R] ((x : M) → V x) →ₗ[R] M → R
<!-- PINNED-SIGNATURE:END -->


`VTask.piApply : {R : Type u_1} -> {M : Type u_5} -> {V : M → Type u_9} -> [CommSemiring R] -> [(x : M) → AddCommMonoid (V x)] -> [(x : M) → Module R (V x)] -> ((x : M) → V x →ₗ[R] R) →ₗ[R] ((x : M) → V x) →ₗ[R] M → R`

- `R` is the commutative semiring of scalars.
- `M` is the index type ranging over the family.
- `V` is the dependent type family, assigning to each index `x : M` a type `V x` that is an `R`-module.
- The `CommSemiring R` instance provides the scalar arithmetic.
- The `AddCommMonoid (V x)` and `Module R (V x)` instances (for each `x`) equip every fiber with the necessary module structure.
- The first explicit argument is a family of linear forms: for each `x : M`, a linear map `V x →ₗ[R] R`. The outer `→ₗ[R]` records that the result is linear in this family.
- The second (curried) explicit argument is a family of vectors: for each `x : M`, an element of `V x`. The inner `→ₗ[R]` records that the result is linear in this family.
- The output is the function `M → R` sending each index `x` to the scalar `eₓ(sₓ)`.

### Conventions

No junk-value or edge-case conventions are declared for this definition: it is a total construction whose behavior is fully determined by the module structure and pointwise application for every possible input.

### Worked examples

- Claim: For the family of linear forms on `ℚ` indexed by `Fin 2` given by scalar multiplication by `2` and `3` respectively, applied to the constant family `1`, `VTask.piApply` produces the function `![2, 3]` (i.e., `fun i => [2, 3].get i`).

- Claim: When the family of linear forms is the zero family (all forms are `0`), `VTask.piApply 0 s = 0` for any family of vectors `s`.

- Claim: `VTask.piApply` is linear in its first argument: for linear-form families `e₁` and `e₂` and any vector family `s`, `VTask.piApply (e₁ + e₂) s = VTask.piApply e₁ s + VTask.piApply e₂ s`.

- Claim: `VTask.piApply` is linear in its second argument: for a fixed family of linear forms `e` and vector families `s₁, s₂`, `VTask.piApply e (s₁ + s₂) = VTask.piApply e s₁ + VTask.piApply e s₂`.

### Boundaries

- When `M` is the empty type, both the domain families are trivially inhabited only by the empty function, and the output function `M → R` is also the empty function; the linearity conditions are satisfied vacuously.
- When `M` is a singleton `{pt}`, `VTask.piApply` reduces to ordinary evaluation of a single linear form at a single vector.
- When `R = 0` (the zero ring), all linear forms and vectors are zero, and the output is identically zero.
- The definition is total: no assumptions beyond the module-structure instances are required, and it is defined for any commutative semiring `R`, any index type `M`, and any dependent module family `V`.

### Not to be confused with

- `LinearMap.pi`: constructs a single linear map into a product type from a family of linear maps, rather than applying a family of forms to a family of vectors pointwise.
- `Matrix.dotProduct` or `Finsupp`-based inner products: those require finiteness and a sum over the index, whereas `VTask.piApply` produces a function indexed by `M` rather than a single scalar sum.
- `LinearMap.applyₗ`: the universal evaluation map `(E →ₗ[R] F) →ₗ[R] E →ₗ[R] F` for a fixed module, rather than a dependent family of evaluations indexed by `M`.
