## Object

`VTask.restr` constructs a **continuous multilinear map on `k` variables** from a continuous multilinear map `f` on `n` variables, a size-`k` subset `s` of the index set `{0, 1, …, n−1}`, and a fixed value `z`. The new map is obtained by "restricting" `f` to the variables indexed by `s` — those `k` variables are allowed to vary freely, while the remaining `n − k` variables are all held equal to `z`. The domain of the new map is `Fin k`, identified with `s` via the canonical order-preserving bijection.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.restr : {𝕜 : Type u} -> {G : Type wG} -> {G' : Type wG'} -> [NontriviallyNormedField 𝕜] -> [SeminormedAddCommGroup G] -> [NormedSpace 𝕜 G] -> [SeminormedAddCommGroup G'] -> [NormedSpace 𝕜 G'] -> {k n : ℕ} -> (f : G [×n]→L[𝕜] G') -> (s : Finset (Fin n)) -> (hk : s.card = k) -> (z : G) -> G [×k]→L[𝕜] G'
<!-- PINNED-SIGNATURE:END -->


The scalar field `𝕜` is a nontrivially normed field. `G` is the common input space (a seminormed additive commutative group with a `𝕜`-normed space structure) and `G'` is the output space (similarly structured). The natural numbers `k` and `n` give the arities of the resulting and original maps respectively. The argument `f` is the original continuous `𝕜`-multilinear map taking `n` copies of `G` to `G'`. The argument `s` is a finite subset of `Fin n` — the indices of the variables to be kept free. The argument `hk` is a proof that `s` has exactly `k` elements, linking the cardinality of `s` to the arity `k` of the output map. The argument `z` is the fixed value substituted for all variables whose index is **not** in `s`.

## Conventions

When evaluating the restricted map at a `k`-tuple `m : Fin k → G`, the argument at each position `i : Fin n` is set to `m (s.orderIsoOfFin hk).symm i` if `i ∈ s`, and to `z` otherwise; here `s.orderIsoOfFin hk` is the canonical increasing bijection from `Fin k` to `s`.

## Worked examples

- Claim: For a continuous multilinear map `f : G [×2]→L[𝕜] G'`, taking `s = {0}` (with `hk : s.card = 1`) and fixing `z`, the restriction `f.restr s hk z` is a continuous linear map that evaluates `f` at the free variable in position `0` and `z` in position `1`.

- Claim: The norm of `f.restr s hk z` is at most `‖f‖ * ‖z‖ ^ (n − k)`. In particular, when all variables are kept free (`k = n`, `s = Finset.univ`), the norm bound reduces to `‖f‖ * ‖z‖ ^ 0 = ‖f‖`.

- Claim: When `k = 0` (i.e. `s = ∅`), `f.restr ∅ hk z` is a continuous multilinear map on zero variables, and its single value is `f (fun _ => z)` (all `n` inputs equal to `z`).

## Boundaries

- **`k = n`, `s = Finset.univ`:** Every variable is free; no variable is fixed to `z`. The restriction is essentially `f` itself (re-indexed via the identity), and the norm bound is just `‖f‖`.
- **`k = 0`, `s = ∅`:** All variables are fixed to `z`. The resulting map is a continuous multilinear map on zero variables (a constant), whose unique value is `f` evaluated at the all-`z` tuple.
- **`z = 0`:** The norm bound becomes `‖f‖ * 0 ^ (n − k)`, which is `0` whenever `n > k` (i.e. at least one variable is fixed), reflecting that the restriction is the zero map when the frozen value is `0` and at least one variable is frozen.
- The proof `hk` is required only to type-check and identify `Fin k` with `s`; the construction is well-defined for any `s` and matching `k`.

## Not to be confused with

- `ContinuousMultilinearMap.restrictScalars`: changes the scalar field of the map, not the set of free variables.
- `MultilinearMap.restr`: the purely algebraic (non-continuous) version of the same restriction construction, without norm or continuity data.
- Partial application / currying of a multilinear map: fixes one variable to a specific value at a specific position, yielding a map of lower arity, as opposed to selecting a subset of free indices.
