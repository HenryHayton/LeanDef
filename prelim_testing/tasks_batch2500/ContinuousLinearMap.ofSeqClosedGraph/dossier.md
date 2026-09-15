## Object

Given a linear map `g : E →ₗ[𝕜] F` between Banach spaces over a nontrivially normed field `𝕜`, together with a proof that `g` has a *sequentially closed graph* — meaning that whenever a sequence converges and its image under `g` also converges, the limit of the image must equal `g` applied to the limit of the sequence — this construction produces a **continuous** (equivalently, bounded) linear map `E →L[𝕜] F` that agrees with `g` on all inputs. The existence of such a continuous lift is guaranteed by the **Closed Graph Theorem** (a consequence of the Baire Category Theorem applied to Banach spaces).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofSeqClosedGraph : {𝕜 : Type u_1} -> [NontriviallyNormedField 𝕜] -> {E : Type u_3} -> [NormedAddCommGroup E] -> [NormedSpace 𝕜 E] -> [CompleteSpace E] -> {F : Type u_5} -> [NormedAddCommGroup F] -> [NormedSpace 𝕜 F] -> [CompleteSpace F] -> {g : E →ₗ[𝕜] F} -> (hg :
    ∀ (u : ℕ → E) (x : E) (y : F),
      Filter.Tendsto u Filter.atTop (nhds x) → Filter.Tendsto (⇑g ∘ u) Filter.atTop (nhds y) → y = g x) -> E →L[𝕜] F
<!-- PINNED-SIGNATURE:END -->


VTask.ofSeqClosedGraph : {𝕜 : Type u_1} -> [NontriviallyNormedField 𝕜] -> {E : Type u_3} -> [NormedAddCommGroup E] -> [NormedSpace 𝕜 E] -> [CompleteSpace E] -> {F : Type u_5} -> [NormedAddCommGroup F] -> [NormedSpace 𝕜 F] -> [CompleteSpace F] -> {g : E →ₗ[𝕜] F} -> (hg : ∀ (u : ℕ → E) (x : E) (y : F), Filter.Tendsto u Filter.atTop (nhds x) → Filter.Tendsto (⇑g ∘ u) Filter.atTop (nhds y) → y = g x) -> E →L[𝕜] F

The implicit type `𝕜` is the scalar field, which must be a nontrivially normed field (e.g., `ℝ` or `ℂ`). The types `E` and `F` are the domain and codomain Banach spaces respectively, each required to carry a normed additive commutative group structure, a normed `𝕜`-module structure, and completeness. The implicit argument `g` is the underlying linear map being upgraded. The explicit argument `hg` is the sequential closed-graph hypothesis: for every sequence `u : ℕ → E`, every point `x : E`, and every point `y : F`, if `u` converges to `x` and the sequence `g ∘ u` converges to `y`, then `y = g x`. This is the only obligation the caller must supply.

## Conventions

There are no junk-value or boundary conventions to declare: the construction is defined for all inputs satisfying the stated type-class constraints and the closed-graph hypothesis, and it is genuinely total on that domain. The closed-graph hypothesis `hg` is the sole semantic gate; outside it there is no distinguished degenerate input to handle.

## Worked examples

- Claim: The coercion of `VTask.ofSeqClosedGraph hg` back to a linear map equals the original `g` (by `coeFn_ofSeqClosedGraph`, the underlying function is definitionally `g`).

- Claim: For `𝕜 = ℝ`, `E = ℝ`, `F = ℝ`, and `g` the identity linear map on `ℝ`, supplying the trivial sequential closed-graph proof yields a continuous linear map whose value at every `x : ℝ` equals `x`.

- Claim: If `g : E →ₗ[𝕜] F` is already known to be continuous, then the `hg` hypothesis holds automatically (convergent sequences have limits preserved by continuous maps), and `VTask.ofSeqClosedGraph hg` is the canonical way to package this into a `ContinuousLinearMap`.

## Boundaries

- **Completeness is essential.** Both `E` and `F` must be complete (Banach spaces). The closed graph theorem is false for incomplete spaces, and the `[CompleteSpace ...]` instances are required arguments — the construction simply does not type-check without them.
- **The field must be nontrivially normed.** Trivially normed fields (e.g., a field with the discrete norm) do not admit the functional analytic machinery underpinning the theorem.
- **`hg` must be proved by the caller.** The definition performs no checking of the hypothesis beyond what Lean's type system enforces; if a false `hg` is supplied (e.g., via `sorry`), the resulting `ContinuousLinearMap` may be unsound.
- **Coercion is the identity.** The resulting `ContinuousLinearMap`, when coerced to a function or to the underlying `LinearMap`, is definitionally equal to `g`. No information is lost or altered.

## Not to be confused with

- `ContinuousLinearMap.mk`: packages a `LinearMap` together with a separately-supplied continuity proof directly, without invoking the closed graph theorem as the route to continuity.
- `LinearMap.continuous_of_seq_closed_graph`: the intermediate lemma that extracts mere *continuity* of `g` from the sequential closed-graph hypothesis, without wrapping the result in the `ContinuousLinearMap` type.
- `ContinuousLinearMap.ofIsClosedGraph`: a related construction that uses the *topological* (non-sequential) formulation of the closed graph condition (`IsClosedMap` or closed subsets of the product space), rather than the sequential one.
