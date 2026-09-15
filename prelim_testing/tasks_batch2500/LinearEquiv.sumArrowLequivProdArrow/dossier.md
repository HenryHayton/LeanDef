## Object

`VTask.sumArrowLequivProdArrow` is the canonical linear equivalence (over a semiring `R`) between the module of functions from a disjoint union `α ⊕ β` into an `R`-module `M`, and the product of modules of functions `(α → M) × (β → M)`. Concretely, a function `f : α ⊕ β → M` is mapped to the pair `(f ∘ Sum.inl, f ∘ Sum.inr)`, and the inverse reassembles a pair of functions `(g, h)` into a single function on `α ⊕ β` by case-splitting. This is the linear-algebraic upgrade of the set-theoretic bijection between `α ⊕ β → M` and `(α → M) × (β → M)`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumArrowLequivProdArrow : (α : Type u_5) -> (β : Type u_6) -> (R : Type u_7) -> (M : Type u_8) -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> (α ⊕ β → M) ≃ₗ[R] (α → M) × (β → M)
<!-- PINNED-SIGNATURE:END -->


`VTask.sumArrowLequivProdArrow : (α : Type u_5) -> (β : Type u_6) -> (R : Type u_7) -> (M : Type u_8) -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> (α ⊕ β → M) ≃ₗ[R] (α → M) × (β → M)`

The first argument `α` is the left summand of the index type. The second argument `β` is the right summand of the index type. The third argument `R` is the semiring of scalars. The fourth argument `M` is the module over `R` in which functions take their values. The instance arguments supply the semiring structure on `R`, the additive commutative monoid structure on `M`, and the `R`-module structure on `M`.

## Conventions

The forward direction of the equivalence sends a function `f : α ⊕ β → M` to the pair `(fun a => f (Sum.inl a), fun b => f (Sum.inr b))`; this is the canonical destructuring convention inherited from the underlying `Equiv`. The `R`-module structure on `(α → M) × (β → M)` is the pointwise–product one, and the equivalence is linear with respect to this structure.

## Worked examples

- Claim: For `f : α ⊕ β → M`, the first component of `VTask.sumArrowLequivProdArrow α β R M f` evaluated at `a : α` equals `f (Sum.inl a)`.

- Claim: For `f : α ⊕ β → M`, the second component of `VTask.sumArrowLequivProdArrow α β R M f` evaluated at `b : β` equals `f (Sum.inr b)`.

- Claim: The inverse of `VTask.sumArrowLequivProdArrow α β R M`, applied to a pair `(g, h)` and then to `Sum.inl a`, returns `g a`.

- Claim: The inverse of `VTask.sumArrowLequivProdArrow α β R M`, applied to a pair `(g, h)` and then to `Sum.inr b`, returns `h b`.

## Boundaries

- When `α` or `β` is `Empty`, the corresponding function type `Empty → M` (or `β → M`) is a trivial module with a unique element (the empty function), and the equivalence restricts correctly to that degenerate case without issue.
- When both `α` and `β` are `Empty`, the source type `Empty ⊕ Empty → M` is likewise trivial, and the equivalence still holds.
- The construction requires only `Semiring R` (not a field or even a commutative ring), and only `AddCommMonoid M` with a module action — no further algebraic assumptions are needed.
- Since the equivalence is a `LinearEquiv`, it is in particular a bijection of sets and a homomorphism of `R`-modules in both directions.

## Not to be confused with

- `Equiv.sumArrowEquivProdArrow`: the underlying bare set-theoretic equivalence, which carries no linear structure.
- `LinearEquiv.piLEquiv` or `LinearEquiv.piCongrLeft`: related linear equivalences for `Pi`-types indexed over general types, not specifically for binary sums.
- `DirectSum` decompositions: while conceptually related (splitting a module indexed over a coproduct), `DirectSum` involves finitely-supported sections and different algebraic packaging than plain function types.