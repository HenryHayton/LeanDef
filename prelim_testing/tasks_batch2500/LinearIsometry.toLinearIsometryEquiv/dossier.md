## VTask.toLinearIsometryEquiv

### Object

Given a linear isometry (a norm-preserving linear map) between two finite-dimensional normed modules of equal dimension over a field, this construction produces a **linear isometry equivalence** — a bijective linear map that is an isometry in both directions. The key insight is that a linear isometry between finite-dimensional spaces of equal dimension is automatically bijective (since an injective linear map between equal-dimensional finite-dimensional spaces is surjective), so the inverse map exists and the isometry can be "upgraded" to a full equivalence.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toLinearIsometryEquiv : {F : Type u_1} -> {E₁ : Type u_2} -> [SeminormedAddCommGroup F] -> [NormedAddCommGroup E₁] -> {R₁ : Type u_3} -> [Field R₁] -> [Module R₁ E₁] -> [Module R₁ F] -> [FiniteDimensional R₁ E₁] -> [FiniteDimensional R₁ F] -> (li : E₁ →ₗᵢ[R₁] F) -> (h : Module.finrank R₁ E₁ = Module.finrank R₁ F) -> E₁ ≃ₗᵢ[R₁] F
<!-- PINNED-SIGNATURE:END -->


`VTask.toLinearIsometryEquiv : {F : Type u_1} -> {E₁ : Type u_2} -> [SeminormedAddCommGroup F] -> [NormedAddCommGroup E₁] -> {R₁ : Type u_3} -> [Field R₁] -> [Module R₁ E₁] -> [Module R₁ F] -> [FiniteDimensional R₁ E₁] -> [FiniteDimensional R₁ F] -> (li : E₁ →ₗᵢ[R₁] F) -> (h : Module.finrank R₁ E₁ = Module.finrank R₁ F) -> E₁ ≃ₗᵢ[R₁] F`

The implicit type arguments `F` and `E₁` are the codomain and domain normed modules, respectively. The instance arguments supply the normed group and module structures on `E₁` and `F`, the field structure on the scalar ring `R₁`, and the finite-dimensionality of both modules over `R₁`. The explicit argument `li` is the linear isometry from `E₁` to `F` being upgraded, and `h` is the proof that `E₁` and `F` have the same finite dimension (as `R₁`-modules), which is the hypothesis making the upgrade possible.

### Conventions

There are no junk-value or edge-case conventions to declare for this definition: the construction is only invoked when the user explicitly provides a linear isometry `li` and a dimension-equality proof `h`, both of which are substantive mathematical data. The result is always a well-defined linear isometry equivalence under those hypotheses.

### Worked examples

- Claim: For any linear isometry `li : E₁ →ₗᵢ[R₁] F` and dimension hypothesis `h`, evaluating the resulting equivalence at a point `x : E₁` yields the same value as applying `li` directly: `(li.toLinearIsometryEquiv h) x = li x`.

- Claim: For any linear isometry `li : E₁ →ₗᵢ[R₁] F` and dimension hypothesis `h`, the underlying function of the resulting equivalence equals `li` as a function `E₁ → F`: `(li.toLinearIsometryEquiv h : E₁ → F) = li`.

- Claim: The norm of `(li.toLinearIsometryEquiv h) x` equals the norm of `x` for all `x : E₁`, because the equivalence inherits the norm-preservation property of `li`.

### Boundaries

- The hypothesis `h : Module.finrank R₁ E₁ = Module.finrank R₁ F` is essential: without equal dimensions, a linear isometry need not be surjective (e.g., the inclusion of a proper subspace), so the upgrade to an equivalence would fail.
- Both `E₁` and `F` must be finite-dimensional over `R₁`; in the infinite-dimensional setting, the dimension-equality trick does not apply and the construction is not available.
- The scalar type `R₁` is required to be a field (not merely a ring), as the finite-dimension rank argument relies on field-theoretic linear algebra.
- The forward direction of the resulting equivalence agrees on the nose with `li` (same underlying function), so no information is lost in the upgrade.

### Not to be confused with

- `LinearIsometry` (`E₁ →ₗᵢ[R₁] F`): the input to this construction — a norm-preserving linear map that need not be surjective or invertible.
- `LinearEquiv` (`E₁ ≃ₗ[R₁] F`): a linear bijection without the norm-preservation requirement; the output here additionally carries the isometry structure.
- `LinearIsometryEquiv.ofLinearIsometry` or similar constructors: other ways to build a linear isometry equivalence that may require surjectivity as an explicit hypothesis rather than deducing it from finite-dimensionality and dimension equality.