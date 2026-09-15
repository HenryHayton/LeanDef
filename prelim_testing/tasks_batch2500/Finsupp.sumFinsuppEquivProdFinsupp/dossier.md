## Object

`VTask.sumFinsuppEquivProdFinsupp` is a canonical equivalence (bijection) between the type of finitely-supported functions on a disjoint-union index type `α ⊕ β` with values in `γ`, and the Cartesian product of two finitely-supported function types: one indexed by `α` and one indexed by `β`. Informally, a function that is finitely supported on a disjoint union is uniquely determined by its restriction to each summand, and any pair of finitely-supported functions on the two summands can be combined into one on the disjoint union. This is the finitely-supported analogue of the elementary set-theoretic fact that `(α ⊕ β) → γ ≅ (α → γ) × (β → γ)`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumFinsuppEquivProdFinsupp : {α : Type u_12} -> {β : Type u_13} -> {γ : Type u_14} -> [Zero γ] -> (α ⊕ β →₀ γ) ≃ (α →₀ γ) × (β →₀ γ)
<!-- PINNED-SIGNATURE:END -->


`VTask.sumFinsuppEquivProdFinsupp : {α : Type u_12} -> {β : Type u_13} -> {γ : Type u_14} -> [Zero γ] -> (α ⊕ β →₀ γ) ≃ (α →₀ γ) × (β →₀ γ)`

The implicit type `α` is the left summand of the index type; `β` is the right summand. The implicit type `γ` is the value type, which must carry a distinguished zero element (supplied by the `[Zero γ]` instance) so that "finitely supported" is meaningful. The result is a bundled equivalence (`≃`), packaging the forward map, the inverse map, and proofs of both inverse conditions.

## Conventions

The zero element of `γ` is used to define what it means for a function to have finite support: a function `f : α ⊕ β →₀ γ` has support `{x | f x ≠ 0}`, which must be finite. No additional algebraic structure on `γ` beyond `Zero` is assumed.

## Worked examples

- Claim: For a finitely-supported function `f : α ⊕ β →₀ γ`, the first component of `VTask.sumFinsuppEquivProdFinsupp f` evaluated at `a : α` equals `f (Sum.inl a)`.

- Claim: For a finitely-supported function `f : α ⊕ β →₀ γ`, the second component of `VTask.sumFinsuppEquivProdFinsupp f` evaluated at `b : β` equals `f (Sum.inr b)`.

- Claim: For a pair `fg : (α →₀ γ) × (β →₀ γ)`, the inverse `VTask.sumFinsuppEquivProdFinsupp.symm fg` evaluated at `Sum.inl a` equals `fg.1 a`.

- Claim: For a pair `fg : (α →₀ γ) × (β →₀ γ)`, the inverse `VTask.sumFinsuppEquivProdFinsupp.symm fg` evaluated at `Sum.inr b` equals `fg.2 b`.

- Claim: The support of the first component `(VTask.sumFinsuppEquivProdFinsupp f).1` consists precisely of those `a : α` for which `f (Sum.inl a) ≠ 0`.

## Boundaries

- When `γ` has only one element (i.e., `γ` is a singleton type where every value equals zero), every finitely-supported function is the zero function, and the equivalence maps the unique zero function on `α ⊕ β` to the pair of zero functions on `α` and `β` respectively.
- When `α` or `β` is empty, the corresponding component in the product is trivially the unique finitely-supported function from the empty type, and the equivalence still holds.
- The equivalence is defined for any `[Zero γ]` — no commutativity, associativity, or group structure is required.
- The forward direction restricts a function on the sum to each summand; the reverse direction glues two functions together by case analysis on `Sum.inl`/`Sum.inr`.

## Not to be confused with

- `Equiv.sum_arrow_equiv_prod_arrow`: The analogous equivalence for plain functions `α ⊕ β → γ` without any finiteness-of-support condition; `VTask.sumFinsuppEquivProdFinsupp` is the finitely-supported specialization.
- `Finsupp.prodEquiv` or product-indexed Finsupps: Deals with `α × β →₀ γ` (a product index type) rather than a sum index type; the splitting is across a product rather than a disjoint union.
- `Finsupp.sumElim`: The raw function that merges a pair of Finsupps into a Finsupp on a sum type; it is the underlying map used in the inverse direction of this equivalence, not the full bundled equivalence with its inverse.