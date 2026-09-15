## Object

A continuous linear map between normed spaces over a normed field is **conformal** if it equals a nonzero scalar multiple of a linear isometry. Geometrically (over the reals), conformal maps are precisely those that preserve angles between vectors and uniformly scale all lengths by a common positive factor.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsConformalMap : {R : Type u_1} -> {X : Type u_2} -> {Y : Type u_3} -> [NormedField R] -> [SeminormedAddCommGroup X] -> [SeminormedAddCommGroup Y] -> [NormedSpace R X] -> [NormedSpace R Y] -> (f' : X →L[R] Y) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsConformalMap : {R : Type u_1} -> {X : Type u_2} -> {Y : Type u_3} -> [NormedField R] -> [SeminormedAddCommGroup X] -> [SeminormedAddCommGroup Y] -> [NormedSpace R X] -> [NormedSpace R Y] -> (f' : X →L[R] Y) -> Prop`

The implicit type `R` is the scalar field, which must carry the structure of a normed field. The implicit types `X` and `Y` are the domain and codomain, both seminormed additive commutative groups equipped with a normed `R`-module structure. The explicit argument `f'` is the continuous `R`-linear map under examination.

## Conventions

No special junk-value or boundary conventions are declared for this predicate: it is a well-defined `Prop` for every continuous linear map in scope, and no particular degenerate inputs are given a non-obvious value by convention.

## Worked examples

- Claim: The identity map `ContinuousLinearMap.id R M` satisfies `VTask.IsConformalMap`.

- Claim: For any nonzero scalar `c : R`, the scalar multiple `c • ContinuousLinearMap.id R M` satisfies `VTask.IsConformalMap`.

- Claim: Any linear isometry `li : X →ₗᵢ[R] Y`, viewed as a continuous linear map, satisfies `VTask.IsConformalMap li.toContinuousLinearMap`.

- Claim: If `f` and `g` both satisfy `VTask.IsConformalMap`, then so does their composition `g.comp f`.

- Claim: Over `ℝ`-inner product spaces, `f' : E →L[ℝ] F` satisfies `VTask.IsConformalMap f'` if and only if there exists a real `c > 0` such that the inner product satisfies `⟪f' u, f' v⟫ = c * ⟪u, v⟫` for all `u v : E`.

## Boundaries

- On a **subsingleton** domain the predicate holds vacuously for every continuous linear map (since every map on a subsingleton is the zero map, yet the subsingleton convention yields truth).
- The predicate requires the scalar `c` to be **nonzero**: the zero map is never conformal on a nontrivial space.
- A conformal map on a nontrivial domain is always **injective**, since it is a nonzero rescaling of an isometry.
- Over `ℂ` viewed as an `ℝ`-normed space, complex-linear maps and their compositions with complex conjugation both give conformal maps, but no other real-linear map from `ℂ` to `ℂ` can be conformal.

## Not to be confused with

- **`ConformalAt f x`**: the pointwise predicate on a map between normed spaces asserting that the Fréchet derivative of `f` at `x` is conformal; `VTask.IsConformalMap` applies to the derivative itself, not to the original map.
- **`LinearIsometry`**: an isometry is conformal (with scale factor 1), but `VTask.IsConformalMap` strictly generalises this by allowing any nonzero scalar multiple.
- **`ContinuousLinearEquiv`**: a continuous linear equivalence need not be conformal unless it also preserves norms up to a common scalar factor.