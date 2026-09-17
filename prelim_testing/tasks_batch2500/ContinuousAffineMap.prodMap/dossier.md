## VTask.prodMap

### Object

Given two continuous affine maps — one from affine space $P_1$ to $P_2$ and another from $P_3$ to $P_4$ (all over a common ring $k$) — `VTask.prodMap f g` is the continuous affine map from the product space $P_1 \times P_3$ to the product space $P_2 \times P_4$ that applies $f$ to the first component and $g$ to the second component simultaneously. In other words, it is the product (or "diagonal") construction on continuous affine maps, entirely analogous to `Prod.map` for ordinary functions.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prodMap : {k : Type u_10} -> {P₁ : Type u_11} -> {P₂ : Type u_12} -> {P₃ : Type u_13} -> {P₄ : Type u_14} -> {V₁ : Type u_15} -> {V₂ : Type u_16} -> {V₃ : Type u_17} -> {V₄ : Type u_18} -> [Ring k] -> [AddCommGroup V₁] -> [Module k V₁] -> [AddTorsor V₁ P₁] -> [TopologicalSpace P₁] -> [AddCommGroup V₂] -> [Module k V₂] -> [AddTorsor V₂ P₂] -> [TopologicalSpace P₂] -> [AddCommGroup V₃] -> [Module k V₃] -> [AddTorsor V₃ P₃] -> [TopologicalSpace P₃] -> [AddCommGroup V₄] -> [Module k V₄] -> [AddTorsor V₄ P₄] -> [TopologicalSpace P₄] -> (f : P₁ →ᴬ[k] P₂) -> (g : P₃ →ᴬ[k] P₄) -> P₁ × P₃ →ᴬ[k] P₂ × P₄
<!-- PINNED-SIGNATURE:END -->


VTask.prodMap : {k : Type u_10} -> {P₁ : Type u_11} -> {P₂ : Type u_12} -> {P₃ : Type u_13} -> {P₄ : Type u_14} -> {V₁ : Type u_15} -> {V₂ : Type u_16} -> {V₃ : Type u_17} -> {V₄ : Type u_18} -> [Ring k] -> [AddCommGroup V₁] -> [Module k V₁] -> [AddTorsor V₁ P₁] -> [TopologicalSpace P₁] -> [AddCommGroup V₂] -> [Module k V₂] -> [AddTorsor V₂ P₂] -> [TopologicalSpace P₂] -> [AddCommGroup V₃] -> [Module k V₃] -> [AddTorsor V₃ P₃] -> [TopologicalSpace P₃] -> [AddCommGroup V₄] -> [Module k V₄] -> [AddTorsor V₄ P₄] -> [TopologicalSpace P₄] -> (f : P₁ →ᴬ[k] P₂) -> (g : P₃ →ᴬ[k] P₄) -> P₁ × P₃ →ᴬ[k] P₂ × P₄

The scalar ring `k` is shared across all four affine spaces. Each implicit type `Vᵢ` is the translation vector space for the corresponding affine space `Pᵢ`, and every `Pᵢ` is equipped with both an affine-torsor structure over `Vᵢ` and a topology. The first explicit argument `f` is a continuous affine map from $P_1$ to $P_2$. The second explicit argument `g` is a continuous affine map from $P_3$ to $P_4$. The result is the continuous affine map acting on product spaces that applies `f` to the first component and `g` to the second.

### Conventions

No junk-value or edge conventions have been declared for this definition: it is a total constructor whose output is fully determined by two continuous affine maps, and there are no degenerate or boundary inputs requiring special treatment.

### Worked examples

- Claim: For any continuous affine maps `f : P₁ →ᴬ[k] P₂` and `g : P₃ →ᴬ[k] P₄`, applying `VTask.prodMap f g` to a pair `(p, q)` yields `(f p, g q)`.

- Claim: `VTask.prodMap` of two identity continuous affine maps is the identity continuous affine map on the product space.

- Claim: If `f₁ : P₁ →ᴬ[k] P₂`, `f₂ : P₂ →ᴬ[k] P₃`, `g₁ : P₄ →ᴬ[k] P₅`, `g₂ : P₅ →ᴬ[k] P₆`, then composing `VTask.prodMap f₂ g₂` after `VTask.prodMap f₁ g₁` equals `VTask.prodMap (f₂ ∘ f₁) (g₂ ∘ g₁)` (as continuous affine maps), reflecting that product-map respects composition componentwise.

### Boundaries

- When `f` or `g` is a constant affine map, the result is a continuous affine map on the product that is constant in the corresponding component.
- The product topology on `P₁ × P₃` is used, and continuity of the result is automatically inherited from the continuity of `f` and `g` individually; no extra topological hypotheses beyond those already required of `f` and `g` are needed.
- There is no restriction on the dimensions or types of the affine spaces involved beyond the typeclass assumptions; in particular, the two factors may belong to entirely different geometric settings so long as they share the ring `k`.

### Not to be confused with

- `AffineMap.prodMap`: The purely algebraic (non-topological) product of two affine maps, which does not carry the continuity datum that `VTask.prodMap` packages.
- `ContinuousLinearMap.prodMap`: The analogous product construction for continuous *linear* maps, which requires vector-space (not just affine-space) structure on the domain and codomain.
- `ContinuousAffineMap.fst` / `ContinuousAffineMap.snd`: The projection maps out of a product affine space, which are the "other half" of the universal property that `VTask.prodMap` satisfies.