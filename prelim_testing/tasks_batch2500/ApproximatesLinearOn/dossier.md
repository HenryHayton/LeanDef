## VTask.ApproximatesLinearOn

### Object

This is a predicate asserting that a function `f : E → F` between normed spaces is well-approximated by a continuous linear map `f' : E →L[𝕜] F` on a set `s ⊆ E`, with the quality of approximation controlled by a non-negative real constant `c`. Concretely, `f` approximates `f'` on `s` with constant `c` if the residual `f(x) - f(y) - f'(x - y)` is uniformly small relative to `‖x - y‖`: for every pair of points `x, y ∈ s`, one has `‖f(x) - f(y) - f'(x - y)‖ ≤ c · ‖x - y‖`. This is the condition that `f` behaves like `f'` up to an error that is at most `c`-Lipschitz in the displacement. The predicate is central to the proof of the inverse function theorem and related results.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ApproximatesLinearOn : {𝕜 : Type u_1} -> [NontriviallyNormedField 𝕜] -> {E : Type u_2} -> [NormedAddCommGroup E] -> [NormedSpace 𝕜 E] -> {F : Type u_3} -> [NormedAddCommGroup F] -> [NormedSpace 𝕜 F] -> (f : E → F) -> (f' : E →L[𝕜] F) -> (s : Set E) -> (c : NNReal) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.ApproximatesLinearOn : {𝕜 : Type u_1} -> [NontriviallyNormedField 𝕜] -> {E : Type u_2} -> [NormedAddCommGroup E] -> [NormedSpace 𝕜 E] -> {F : Type u_3} -> [NormedAddCommGroup F] -> [NormedSpace 𝕜 F] -> (f : E → F) -> (f' : E →L[𝕜] F) -> (s : Set E) -> (c : NNReal) -> Prop
```

The scalar field `𝕜` is a nontrivially normed field (for example, the reals or the complexes); it governs the linear structure. `E` is the domain normed space (source of `f`) and `F` is the codomain normed space (target of `f`), both normed `𝕜`-modules. The argument `f` is the (possibly nonlinear) function being approximated. The argument `f'` is the continuous linear map serving as the reference approximation. The set `s` is the subset of `E` on which the approximation condition is required to hold. The constant `c`, a non-negative real number (of type `NNReal`), is the uniform approximation quality: smaller `c` means `f` is closer to linear on `s`.

### Conventions

The predicate holds vacuously on the empty set: for any `f`, `f'`, and `c`, `VTask.ApproximatesLinearOn f f' ∅ c` is true, since there are no pairs of points to check. The predicate is monotone in `c`: if `f` approximates `f'` on `s` with constant `c`, it also approximates `f'` on `s` with any larger constant `c' ≥ c`. The predicate is monotone (downward) in the set: if `f` approximates `f'` on a larger set `t` with constant `c`, it also approximates `f'` on any subset `s ⊆ t` with the same constant.

### Worked examples

- Claim: Any continuous linear map `f'` approximates itself on any set `s` with constant `0`, since `‖f'(x) - f'(y) - f'(x - y)‖ = 0 ≤ 0 · ‖x - y‖` for all `x, y`.

- Claim: `VTask.ApproximatesLinearOn f f' ∅ c` holds for every `f`, `f'`, and `c`, because the universal quantification over points in the empty set is vacuously true.

- Claim: If `VTask.ApproximatesLinearOn f f' s c` holds and `c' ≥ c`, then `VTask.ApproximatesLinearOn f f' s c'` holds, since `c · ‖x - y‖ ≤ c' · ‖x - y‖`.

- Claim: If `VTask.ApproximatesLinearOn f f' s c` holds and `s' ⊆ s`, then `VTask.ApproximatesLinearOn f f' s' c` holds, since the inequality is required only for pairs in the smaller set.

### Boundaries

- **Empty set**: The condition holds vacuously for `s = ∅` regardless of `f`, `f'`, and `c`.
- **`c = 0`**: When `c = 0`, the condition requires `‖f(x) - f(y) - f'(x - y)‖ = 0` for all `x, y ∈ s`, meaning `f` and `f'` agree up to an additive constant on `s` (in particular, `f` is itself affine on `s` with linear part `f'`).
- **Singleton set**: When `s` is a singleton `{p}`, the only pair is `(p, p)`, and the inequality reduces to `‖f(p) - f(p) - f'(0)‖ = 0 ≤ c · 0`, which holds trivially.
- **Large `c`**: As `c → ∞` the condition becomes trivially satisfiable; as `c` decreases toward `0` it becomes increasingly restrictive.
- **Subsingleton domain**: When `E` is a subsingleton (all points equal), the condition holds trivially for any `f`, `f'`, `s`, `c`.

### Not to be confused with

- **`HasFDerivAt f f' x`**: This says `f'` is the Fréchet derivative of `f` at a *single point* `x` (a local, infinitesimal condition), whereas `VTask.ApproximatesLinearOn` is a *global* condition on a whole set `s` with an explicit Lipschitz-type error bound `c`.
- **`LipschitzOnWith c f s`**: This bounds `‖f(x) - f(y)‖` directly, whereas `VTask.ApproximatesLinearOn` bounds the residual after subtracting the linear part `f'(x - y)`, making it a statement about how close `f` is to *affine*, not just how Lipschitz it is.
- **`AffineMap`**: An affine map exactly satisfies `f(x) - f(y) = f'(x - y)` (making the residual zero), which corresponds to `VTask.ApproximatesLinearOn` with `c = 0`; the predicate generalises this to an approximate version with positive `c`.
