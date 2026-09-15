## Object

The **operator norm** (also called the **operator norm** or **induced norm**) of a continuous linear map $f : E \to F$ between seminormed spaces over (possibly different) nontrivially normed fields is the smallest non-negative real number $\|f\|$ satisfying $\|f(x)\| \leq \|f\| \cdot \|x\|$ for every $x \in E$. Concretely, it is the infimum of the set of all $c \geq 0$ such that $\|f(x)\| \leq c \|x\|$ holds for all $x$. This quantity measures how much $f$ can stretch vectors.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.opNorm : {𝕜 : Type u_1} -> {𝕜₂ : Type u_2} -> {E : Type u_4} -> {F : Type u_5} -> [SeminormedAddCommGroup E] -> [SeminormedAddCommGroup F] -> [NontriviallyNormedField 𝕜] -> [NontriviallyNormedField 𝕜₂] -> [NormedSpace 𝕜 E] -> [NormedSpace 𝕜₂ F] -> {σ₁₂ : 𝕜 →+* 𝕜₂} -> (f : E →SL[σ₁₂] F) -> ℝ
<!-- PINNED-SIGNATURE:END -->


`VTask.opNorm : {𝕜 : Type u_1} -> {𝕜₂ : Type u_2} -> {E : Type u_4} -> {F : Type u_5} -> [SeminormedAddCommGroup E] -> [SeminormedAddCommGroup F] -> [NontriviallyNormedField 𝕜] -> [NontriviallyNormedField 𝕜₂] -> [NormedSpace 𝕜 E] -> [NormedSpace 𝕜₂ F] -> {σ₁₂ : 𝕜 →+* 𝕜₂} -> (f : E →SL[σ₁₂] F) -> ℝ`

The scalar fields `𝕜` and `𝕜₂` are the base fields for the domain and codomain spaces respectively, and both must be nontrivially normed fields (fields with a non-trivial absolute value, e.g. ℝ or ℂ). The types `E` and `F` are the domain and codomain seminormed additive commutative groups, which are also normed vector spaces over their respective fields. The ring homomorphism `σ₁₂ : 𝕜 →+* 𝕜₂` is the scalar-transfer map relating the two fields (for maps between spaces over the same field, this is the identity). The argument `f` is the continuous linear map whose operator norm is being computed. The result is a real number.

## Conventions

The operator norm is always non-negative: `VTask.opNorm f ≥ 0` for every continuous linear map `f`. The operator norm of the zero map is zero. If the domain `E` is a subsingleton (has at most one element), the operator norm is zero regardless of the map. Junk values do not arise because the definition is total and well-defined for all continuous linear maps in the stated type class context.

## Worked examples

- Claim: The operator norm of the zero continuous linear map from any seminormed space to any seminormed space is 0, i.e., `VTask.opNorm (0 : E →SL[σ₁₂] F) = 0`.

- Claim: For any continuous linear map `f`, the fundamental bound holds: `‖f x‖ ≤ VTask.opNorm f * ‖x‖` for all `x`.

- Claim: For any continuous linear maps `f g : E →SL[σ₁₂] F`, the triangle inequality holds: `VTask.opNorm (f + g) ≤ VTask.opNorm f + VTask.opNorm g`.

- Claim: The operator norm satisfies `VTask.opNorm (-f) = VTask.opNorm f` for any continuous linear map `f`.

## Boundaries

- When the domain `E` is the zero space (a subsingleton), every continuous linear map must send the unique element to zero, so the operator norm is 0 even if the codomain is non-trivial.
- The operator norm is always non-negative; it equals 0 if and only if `f` is the zero map (when `E` is a genuine normed space, not merely a seminormed one with non-trivial null space).
- For a unit-norm vector `x` (i.e., `‖x‖ ≤ 1`), the output satisfies `‖f x‖ ≤ VTask.opNorm f`.
- The ratio `‖f x‖ / ‖x‖` never exceeds `VTask.opNorm f` for any `x`.
- The infimum is actually attained as a minimum (i.e., the bound set is non-empty because `f` is continuous), so the operator norm is a genuine bound, not merely an infimum that is approached but not achieved in the bound set.

## Not to be confused with

- **`ContinuousLinearMap.nnnorm`**: the non-negative real (`ℝ≥0`) version of the operator norm; same value, different type.
- **`LinearMap.norm`**: not a Mathlib object in general; a linear map (without the continuity assumption) need not have a finite operator norm, and the operator norm is only defined for *continuous* linear maps.
- **`‖f x‖`** (the norm of the output): this is the norm of a specific value of `f`, not the supremum/infimum over all inputs that defines the operator norm.