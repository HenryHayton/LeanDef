## Object

`VTask.mapDomain f v` is the finitely supported function obtained by "pushing forward" a finitely supported function `v : α →₀ M` along a map `f : α → β`. Its value at any `b : β` is the sum of all `v(x)` over every `x` in the support of `v` satisfying `f(x) = b`. If no such `x` exists, the value is zero. In other words, it accumulates (sums) the weights of `v` at all preimage points of each `b`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mapDomain : {α : Type u_1} -> {β : Type u_2} -> {M : Type u_5} -> [AddCommMonoid M] -> (f : α → β) -> (v : α →₀ M) -> β →₀ M
<!-- PINNED-SIGNATURE:END -->


VTask.mapDomain : {α : Type u_1} -> {β : Type u_2} -> {M : Type u_5} -> [AddCommMonoid M] -> (f : α → β) -> (v : α →₀ M) -> β →₀ M

The implicit type arguments `α` and `β` are the source and target index types. The implicit type `M` is the coefficient type, which must be an additive commutative monoid (so that summing coefficients over fibres makes sense). The explicit argument `f` is the function used to relabel or push forward the index set. The explicit argument `v` is the finitely supported function whose support and values are being pushed forward.

## Conventions

When `f` is injective the operation behaves like a renaming: each element of the support of `v` simply gets a new label, and no two elements collapse together, so the values are preserved exactly. When `f` is not injective, coefficients of `v` at points sharing the same image under `f` are summed together at that image point.

## Worked examples

- Claim: Applying `VTask.mapDomain` with the constant function `fun _ => 0` to a finsupp `v` with support `{1, 2}` and values `v(1) = 3, v(2) = 5` (in `ℕ`) yields a finsupp whose value at `0` is `8` and is zero elsewhere, because all contributions accumulate at the single image point `0`.

- Claim: Applying `VTask.mapDomain id v` for any finsupp `v : α →₀ M` yields a result equal to `v`, because the identity map sends each point to itself and no accumulation occurs.

- Claim: For `v : Fin 3 →₀ ℕ` defined by `v(0) = 1, v(1) = 2, v(2) = 4` and `f : Fin 3 → Fin 2` with `f(0) = 0, f(1) = 0, f(2) = 1`, the result `VTask.mapDomain f v` has value `3` at `0` (namely `1 + 2`) and value `4` at `1`.

- Claim: `VTask.mapDomain f (VTask.mapDomain g v) = VTask.mapDomain (f ∘ g) v` for any composable pair of functions and any finsupp `v`, expressing functoriality (composition law).

## Boundaries

- If `v` is the zero finsupp (empty support), then `VTask.mapDomain f v` is also the zero finsupp regardless of `f`, since there are no points to push forward.
- If `f` is surjective, the support of the result can cover all of `β` (subject to the fibre sums not being zero), but finiteness is still guaranteed because only finitely many fibres contain points from the finite support of `v`.
- If multiple points in the support of `v` share the same image under `f`, their `M`-values are combined by the additive operation of `M`; in a general additive commutative monoid (not a group) there is no cancellation, so values only grow or stay the same in the nonneg case.
- The support of the result is a subset of the image of the support of `v` under `f`; it may be strictly smaller if some fibre sums happen to equal zero.

## Not to be confused with

- `Finsupp.comapDomain`: pulls back a finsupp along an injective function in the other direction, restricting the index set rather than pushing it forward.
- `Finsupp.lmapDomain`: the linear-map version of the same push-forward construction, which packages the same operation as an `M`-linear map between finsupp modules.
- `Finsupp.equivMapDomain`: a variant restricted to bijections `f`, where the push-forward is invertible and yields an equivalence (no coefficient accumulation can occur).