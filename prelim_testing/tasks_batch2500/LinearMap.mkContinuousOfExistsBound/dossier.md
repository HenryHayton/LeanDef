## Object

`VTask.mkContinuousOfExistsBound` promotes a seminormed-space σ-linear map `f : E →ₛₗ[σ] F` to a *continuous* σ-linear map `E →SL[σ] F`, given a proof that some global bound `C` exists such that `‖f x‖ ≤ C * ‖x‖` for every `x`. The continuity certificate is derived entirely from the existence of such a bound; no explicit value of `C` need be supplied.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mkContinuousOfExistsBound : {𝕜 : Type u_1} -> {𝕜₂ : Type u_2} -> {E : Type u_3} -> {F : Type u_4} -> [Ring 𝕜] -> [Ring 𝕜₂] -> [SeminormedAddCommGroup E] -> [SeminormedAddCommGroup F] -> [Module 𝕜 E] -> [Module 𝕜₂ F] -> {σ : 𝕜 →+* 𝕜₂} -> (f : E →ₛₗ[σ] F) -> (h : ∃ C, ∀ (x : E), ‖f x‖ ≤ C * ‖x‖) -> E →SL[σ] F
<!-- PINNED-SIGNATURE:END -->


`VTask.mkContinuousOfExistsBound : {𝕜 : Type u_1} -> {𝕜₂ : Type u_2} -> {E : Type u_3} -> {F : Type u_4} -> [Ring 𝕜] -> [Ring 𝕜₂] -> [SeminormedAddCommGroup E] -> [SeminormedAddCommGroup F] -> [Module 𝕜 E] -> [Module 𝕜₂ F] -> {σ : 𝕜 →+* 𝕜₂} -> (f : E →ₛₗ[σ] F) -> (h : ∃ C, ∀ (x : E), ‖f x‖ ≤ C * ‖x‖) -> E →SL[σ] F`

The scalar fields `𝕜` and `𝕜₂` are rings equipped with the ring structure needed for module scalar multiplication. `E` and `F` are seminormed additive commutative groups carrying `𝕜`- and `𝕜₂`-module structures respectively. `σ` is the ring homomorphism mediating the scalar action, making the linearity *semilinear*. The argument `f` is the underlying σ-semilinear map whose continuity is to be established. The argument `h` is an existence proof: there is at least one constant `C` such that the norm of `f x` is bounded above by `C` times the norm of `x` for every vector `x` in `E`.

## Conventions

No special junk-value or edge-case conventions are declared for this constructor: it is a total function whose output is fully determined whenever the inputs typecheck, and it imposes no additional side conditions beyond what the type already enforces.

## Worked examples

- Claim: Applying `VTask.mkContinuousOfExistsBound f h` to a vector `x` gives the same result as applying the underlying linear map `f` to `x`.

- Claim: The coercion of `VTask.mkContinuousOfExistsBound f h` back to a semilinear map recovers `f` definitionally — that is, `(VTask.mkContinuousOfExistsBound f h : E →ₛₗ[σ] F) = f`.

- Claim: If `f` is the zero semilinear map on a seminormed space, then the bound `∃ C, ∀ x, ‖f x‖ ≤ C * ‖x‖` is witnessed by `C = 0`, and `VTask.mkContinuousOfExistsBound f h` is the zero continuous linear map.

## Boundaries

- The bound constant `C` need not be non-negative; the proof only needs the inequality to hold, and any witness suffices. The operator norm of the resulting continuous linear map is then determined separately by the infimum of valid bounds, not by the particular `C` supplied in `h`.
- If `E` is the zero module (every vector has norm 0), the bound `‖f x‖ ≤ C * ‖x‖` holds trivially for any `C`, so `h` is easily satisfied.
- The function is total: it does not require `C ≥ 0` or `C` to be canonical in any way.

## Not to be confused with

- `LinearMap.mkContinuous`: a variant that takes an *explicit* bound constant `C` together with a proof `∀ x, ‖f x‖ ≤ C * ‖x‖`, and from which norm estimates on the resulting map follow automatically.
- `ContinuousLinearMap.mk`: a lower-level constructor that packages a linear map with a raw continuity proof, without going through a norm-bound argument.
- `LinearMap.toContinuousLinearMap`: available only in special situations (e.g., finite-dimensional spaces) where continuity is automatic and no bound proof is needed at all.