## VTask.changeOriginSeriesTerm

### Object

Given a formal multilinear series `p : FormalMultilinearSeries 𝕜 E F` and natural numbers `k`, `l`, together with a subset `s` of `{0, 1, …, k+l-1}` of cardinality exactly `l`, `VTask.changeOriginSeriesTerm p k l s hs` is a continuous multilinear map of type `E[×l]→L[𝕜] E[×k]→L[𝕜] F`. Concretely, it is the curried form of the `(k+l)`-th coefficient `p(k+l)` of the series, where the `l` positions indexed by `s` receive the first argument block (the "origin shift" variables) and the remaining `k` positions receive the second argument block (the "new variable" block). Summing this object over all size-`l` subsets `s` of `Fin(k+l)` yields the `k`-th term of `p.changeOriginSeries l`, the series whose sum, when evaluated at a point `x`, gives the `k`-th coefficient of the re-expanded series `p.changeOrigin x`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.changeOriginSeriesTerm : {𝕜 : Type u_1} -> {E : Type u_2} -> {F : Type u_3} -> [NontriviallyNormedField 𝕜] -> [NormedAddCommGroup E] -> [NormedSpace 𝕜 E] -> [NormedAddCommGroup F] -> [NormedSpace 𝕜 F] -> (p : FormalMultilinearSeries 𝕜 E F) -> (k l : ℕ) -> (s : Finset (Fin (k + l))) -> (hs : s.card = l) -> E [×l]→L[𝕜] E [×k]→L[𝕜] F
<!-- PINNED-SIGNATURE:END -->


`VTask.changeOriginSeriesTerm : {𝕜 : Type u_1} -> {E : Type u_2} -> {F : Type u_3} -> [NontriviallyNormedField 𝕜] -> [NormedAddCommGroup E] -> [NormedSpace 𝕜 E] -> [NormedAddCommGroup F] -> [NormedSpace 𝕜 F] -> (p : FormalMultilinearSeries 𝕜 E F) -> (k l : ℕ) -> (s : Finset (Fin (k + l))) -> (hs : s.card = l) -> E [×l]→L[𝕜] E [×k]→L[𝕜] F`

- `𝕜` is the scalar field, required to be a nontrivially normed field (e.g. `ℝ` or `ℂ`).
- `E` and `F` are the source and target normed spaces over `𝕜`.
- `p` is the formal multilinear series being re-expanded around a shifted origin.
- `k` is the arity of the outer ("new variable") layer of the resulting curried map; it is also the degree index of the term in `changeOriginSeries`.
- `l` is the arity of the inner ("shift") layer; together with `k` it selects the coefficient `p(k+l)` of the original series.
- `s` is a finite subset of `Fin (k + l)` that selects which `l` of the `k+l` slots are fed the shift variables.
- `hs` is the proof that `s` has exactly `l` elements, ensuring the partition of the `k+l` slots is valid.

### Conventions

The resulting map is determined entirely by the coefficient `p(k+l)` and the subset `s`; different choices of `s` with the same cardinality `l` yield the same norm but generally different maps. When `p(k+l) = 0` (e.g. when `p` is a polynomial of degree less than `k+l`), the term is the zero map regardless of `s`.

### Worked examples

- Claim: For any `p`, `k`, `l`, `s`, `hs`, the operator norm of `VTask.changeOriginSeriesTerm p k l s hs` equals `‖p (k + l)‖`.

- Claim: Evaluating `VTask.changeOriginSeriesTerm p k l s hs` on constant vectors `(fun _ => x)` for the first `l` inputs and `(fun _ => y)` for the remaining `k` inputs gives `p (k + l) (s.piecewise (fun _ => x) (fun _ => y))`.

- Claim: For `k = 1`, `l = 1`, the subset `s = {0} ⊆ Fin 2` of cardinality 1, evaluating `VTask.changeOriginSeriesTerm p 1 1 {0} (by simp) (fun _ => x) (fun _ => y)` yields `p 2` applied to the vector `(x, y)` (slot 0 receives `x`, slot 1 receives `y`).

- Claim: For `k = 1`, `l = 1`, the subset `s = {1} ⊆ Fin 2` of cardinality 1, evaluating `VTask.changeOriginSeriesTerm p 1 1 {1} (by simp) (fun _ => x) (fun _ => y)` yields `p 2` applied to the vector `(y, x)` (slot 1 receives `x`, slot 0 receives `y`).

### Boundaries

- When `l = 0`, the subset `s` must be the empty set (the unique set of cardinality 0), and the result is a continuous multilinear map `E[×0]→L[𝕜] E[×k]→L[𝕜] F`; the shift layer is trivial, and the map is essentially (a curried form of) `p(k)` itself.
- When `k = 0`, the result is a continuous multilinear map `E[×l]→L[𝕜] E[×0]→L[𝕜] F`; the new-variable layer is trivial and the map extracts `p(l)` evaluated at the shift variables.
- When both `k = 0` and `l = 0`, the term is a scalar-valued constant determined by `p(0)`, the zeroth coefficient.
- The norm of the term always equals `‖p(k+l)‖`, independent of the choice of `s`.
- If `n ≤ k + l` and `p` vanishes on all coefficients of degree at least `n` (i.e. `p` is a polynomial of degree less than `n`), then the term is zero.

### Not to be confused with

- `FormalMultilinearSeries.changeOriginSeries`: the series obtained by *summing* `changeOriginSeriesTerm` over all subsets `s` of the appropriate cardinality; `changeOriginSeriesTerm` is one summand, not the full sum.
- `FormalMultilinearSeries.changeOrigin`: the re-expanded series in the new variable `y`, obtained from `changeOriginSeries` by further summing; two levels of summation above `changeOriginSeriesTerm`.
- `ContinuousMultilinearMap.curryFinFinset`: the general currying isomorphism for continuous multilinear maps along a finset partition; `changeOriginSeriesTerm` applies this isomorphism to a specific coefficient of `p` and is not the isomorphism itself.