## Object

`VTask.curry` converts a finitely supported function on a product type `α × β` into a finitely supported function from `α` to finitely supported functions from `β` to `M`. In other words, it turns a single function `f : α × β →₀ M` into a "nested" finitely supported function `α →₀ (β →₀ M)`, where applying the result first to an element `a : α` and then to `b : β` recovers the original value `f (a, b)`. This is the finitely-supported-function analogue of the familiar set-theoretic currying bijection `(A × B → C) ≅ (A → B → C)`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.curry : {α : Type u_1} -> {β : Type u_2} -> {M : Type u_5} -> [Zero M] -> (f : α × β →₀ M) -> α →₀ β →₀ M
<!-- PINNED-SIGNATURE:END -->


`VTask.curry : {α : Type u_1} -> {β : Type u_2} -> {M : Type u_5} -> [Zero M] -> (f : α × β →₀ M) -> α →₀ β →₀ M`

The type parameters `α` and `β` are the two component types of the product domain. `M` is the codomain/value type, which must carry a `Zero` instance (used to declare which values count as "absent" from the support). The argument `f` is the finitely supported function on the product type that is to be curried.

## Conventions

The `Zero M` instance is used throughout: a value `m : M` is considered absent (off-support) precisely when it equals `zero`. This convention governs both the inner finitely supported function (the support of `(VTask.curry f) a` consists of those `b : β` with `f (a, b) ≠ 0`) and the outer one (the support of `VTask.curry f` consists of those `a : α` for which at least one `b` has `f (a, b) ≠ 0`).

## Worked Examples

- Claim: For any finitely supported `f : α × β →₀ M`, evaluating `(VTask.curry f) a b` gives back `f (a, b)` — i.e., `curry_apply` holds pointwise.

- Claim: The support of `VTask.curry f` is exactly the image of `f.support` under the first-projection `Prod.fst`.

- Claim: Currying and then uncurrying recovers the original function: `(VTask.curry f).uncurry = f` for any `f : α × β →₀ M`.

- Claim: Currying a single-basis element `single (a, b) m` yields `single a (single b m)` — the basis element is "split" across the two levels of the nested finsupp.

## Boundaries

- If `f` is the zero function (empty support), then `VTask.curry f` is also the zero function: both its outer and inner supports are empty.
- If `f` is supported at a single point `(a₀, b₀)`, then `VTask.curry f` is supported at the single outer index `a₀`, and the inner finsupp `(VTask.curry f) a₀` is supported only at `b₀`.
- For `a` not in the image of `f.support` under `Prod.fst`, the value `(VTask.curry f) a` is the zero element of `β →₀ M` (the finsupp with empty support).
- The operation is a bijection between `α × β →₀ M` and `α →₀ β →₀ M`; its inverse is `uncurry`. Composing curry then uncurry, or uncurry then curry, is the identity.

## Not to be confused with

- `Finsupp.uncurry`: the inverse operation, taking `α →₀ β →₀ M` back to `α × β →₀ M`.
- `Function.curry`: the plain (non-finitely-supported) currying of ordinary functions `α × β → M`; it does not track finiteness of support.
- `Finsupp.finsuppProdEquiv` or `curryLinearEquiv`: the bundled equivalence/linear equivalence form of the same correspondence, which additionally records linearity or ring structure.