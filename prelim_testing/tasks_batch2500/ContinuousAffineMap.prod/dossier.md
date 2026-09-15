## VTask.prod

### Object

Given two continuous affine maps `f` and `g` sharing the same source space `P₁`, `VTask.prod f g` is their *product map*: the continuous affine map from `P₁` to the Cartesian product `P₂ × P₃` that sends each point `x : P₁` to the pair `(f x, g x)`. It simultaneously packages the affine-map structure (the underlying `AffineMap.prod`) and the continuity of the resulting combined map.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {k : Type u_10} -> {P₁ : Type u_11} -> {P₂ : Type u_12} -> {P₃ : Type u_13} -> {V₁ : Type u_15} -> {V₂ : Type u_16} -> {V₃ : Type u_17} -> [Ring k] -> [AddCommGroup V₁] -> [Module k V₁] -> [AddTorsor V₁ P₁] -> [TopologicalSpace P₁] -> [AddCommGroup V₂] -> [Module k V₂] -> [AddTorsor V₂ P₂] -> [TopologicalSpace P₂] -> [AddCommGroup V₃] -> [Module k V₃] -> [AddTorsor V₃ P₃] -> [TopologicalSpace P₃] -> (f : P₁ →ᴬ[k] P₂) -> (g : P₁ →ᴬ[k] P₃) -> P₁ →ᴬ[k] P₂ × P₃
<!-- PINNED-SIGNATURE:END -->


The implicit arguments fix a scalar ring `k`, three affine spaces `P₁`, `P₂`, `P₃` over their respective translation vector spaces, each equipped with a topology. The first explicit argument `f` is a continuous affine map from `P₁` to `P₂`; the second explicit argument `g` is a continuous affine map from the same source `P₁` to `P₃`. The result is a single continuous affine map from `P₁` to the product space `P₂ × P₃`.

### Conventions

No special junk-value or edge-case conventions are declared for this construction: it is a total, well-typed operation that is defined for every valid pair of continuous affine maps sharing a source space.

### Worked examples

- Claim: For continuous affine maps `f : P₁ →ᴬ[k] P₂` and `g : P₁ →ᴬ[k] P₃`, the first component of `VTask.prod f g` applied to any point `x` equals `f x`.

- Claim: For continuous affine maps `f : P₁ →ᴬ[k] P₂` and `g : P₁ →ᴬ[k] P₃`, the second component of `VTask.prod f g` applied to any point `x` equals `g x`.

- Claim: The product of the identity continuous affine map on `P₁` with itself is a continuous affine map `P₁ →ᴬ[k] P₁ × P₁` sending each point `x` to `(x, x)` (the diagonal embedding).

### Boundaries

- The construction is defined for any valid continuous affine maps `f` and `g` over the same ring `k` and from the same source space `P₁`; there are no domain restrictions.
- The target is always the *product* topological space `P₂ × P₃` with the product topology, so continuity of the result follows automatically from continuity of each component.
- When `P₂ = P₃` and `f = g`, the result is the diagonal map sending every point to a pair of equal values.

### Not to be confused with

- `AffineMap.prod`: The underlying non-continuous version; `VTask.prod` additionally carries and verifies the continuity of the combined map.
- `ContinuousLinearMap.prod`: The analogous product construction for continuous *linear* (not affine) maps; affine maps generalise linear maps by allowing a translation offset.
- `ContinuousAffineMap.comp`: Composition of continuous affine maps, as opposed to the pairing/product of two maps from a common source.
