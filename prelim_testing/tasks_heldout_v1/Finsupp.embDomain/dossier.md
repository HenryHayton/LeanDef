## Object

`VTask.embDomain f v` is the finitely supported function on `β` obtained by "pushing forward" a finitely supported function `v : α →₀ M` along an injective map `f : α ↪ β`. Concretely, its value at any point `f a` in the image of `f` is `v a`, and its value at every point of `β` not in the image of `f` is `0`. Because `f` is injective the value at `f a` is unambiguous. The support of the result is exactly the image of the support of `v` under `f`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.embDomain : {α : Type u_1} -> {β : Type u_2} -> {M : Type u_4} -> [Zero M] -> (f : α ↪ β) -> (v : α →₀ M) -> β →₀ M
<!-- PINNED-SIGNATURE:END -->


`VTask.embDomain : {α : Type u_1} -> {β : Type u_2} -> {M : Type u_4} -> [Zero M] -> (f : α ↪ β) -> (v : α →₀ M) -> β →₀ M`

The type parameters `α` and `β` are the source and target index types. `M` is the value type, which need only carry a distinguished zero element. The argument `f` is an injective embedding of index types, determining how the domain is extended. The argument `v` is the finitely supported function on the smaller domain `α` whose values are to be transported.

## Conventions

For any element `b : β` that does not lie in the range of `f`, `VTask.embDomain f v` evaluates to `0` (the zero of `M`). This is the only junk-value convention; the function is fully defined on all of `β` with out-of-range points silently assigned zero.

## Worked examples

- Claim: For the identity embedding on `Fin 3`, `VTask.embDomain (Function.Embedding.refl (Fin 3))` acts as the identity on finitely supported functions, so applying it to any `v : Fin 3 →₀ ℕ` returns `v`.

- Claim: If `f : Fin 2 ↪ Fin 5` sends `0 ↦ 1` and `1 ↦ 3`, and `v : Fin 2 →₀ ℕ` has `v 0 = 7` and `v 1 = 4`, then `(VTask.embDomain f v) 1 = 7`, `(VTask.embDomain f v) 3 = 4`, and `(VTask.embDomain f v) 0 = 0`.

- Claim: `VTask.embDomain f (0 : α →₀ M) = 0` for any embedding `f`; embedding the everywhere-zero function yields the everywhere-zero function.

- Claim: `VTask.embDomain f` is injective as a map `(α →₀ M) → (β →₀ M)`: two distinct finitely supported functions on `α` always produce distinct results after embedding into `β`.

## Boundaries

- **Zero input**: `VTask.embDomain f 0 = 0`; the zero finsupp maps to the zero finsupp, regardless of `f`.
- **Identity embedding**: `VTask.embDomain (Function.Embedding.refl α) = id`; the result is unchanged.
- **Out-of-range evaluation**: For `b : β` with `b ∉ Set.range f`, `VTask.embDomain f v b = 0`.
- **Zero iff zero**: `VTask.embDomain f v = 0` if and only if `v = 0`; the embedding cannot collapse a nonzero finsupp to zero.
- **Support**: The support of `VTask.embDomain f v` is exactly `v.support.map f`, the image of `v`'s support under `f`.
- **Agrees with mapDomain**: When `M` is an additive commutative monoid, `VTask.embDomain f v = mapDomain f v`; the two constructions coincide for injective `f`.

## Not to be confused with

- `Finsupp.mapDomain`: extends a finsupp along any function `f : α → β`, not necessarily injective; values at collisions are added, so it is not injective in general.
- `Finsupp.comapDomain`: goes the other direction, pulling a finsupp on `β` back to `α` by precomposing with `f`.
- `Finsupp.mapRange`: changes the value type `M` rather than the index type, leaving the support domain unchanged.