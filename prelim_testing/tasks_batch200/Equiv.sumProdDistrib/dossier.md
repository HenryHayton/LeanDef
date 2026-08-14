## Object

`VTask.sumProdDistrib` is a type equivalence (a canonical bijection with explicit inverse) witnessing that forming a cartesian product with a fixed type `γ` distributes over disjoint-union (coproduct) on the left. Concretely, it says that a pair whose first component is either an `α`-value or a `β`-value, together with a `γ`-value, is in canonical bijection with either a pair of an `α`-value and a `γ`-value, or a pair of a `β`-value and a `γ`-value. This is the type-theoretic analogue of the arithmetic identity `(a + b) × c = a × c + b × c`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumProdDistrib : (α : Type u_9) -> (β : Type u_10) -> (γ : Type u_11) -> (α ⊕ β) × γ ≃ α × γ ⊕ β × γ
<!-- PINNED-SIGNATURE:END -->


`VTask.sumProdDistrib : (α : Type u_9) -> (β : Type u_10) -> (γ : Type u_11) -> (α ⊕ β) × γ ≃ α × γ ⊕ β × γ`

The first argument `α` is the left summand type of the coproduct. The second argument `β` is the right summand type of the coproduct. The third argument `γ` is the type being multiplied (distributed) across the sum. The result is the equivalence itself, a record packaging the forward map, the inverse map, and proofs that both compositions are the identity.

## Conventions

No junk-value or edge conventions are declared: the equivalence is defined for arbitrary (possibly empty or singleton) types `α`, `β`, and `γ`, and every choice of types gives a well-formed equivalence with no degenerate cases requiring special treatment.

## Worked examples

- Claim: Applying `VTask.sumProdDistrib α β γ` to `(Sum.inl a, c)` yields `Sum.inl (a, c)`.
  ```lean
  example (α β γ : Type*) (a : α) (c : γ) :
      VTask.sumProdDistrib α β γ (Sum.inl a, c) = Sum.inl (a, c) := by rfl
  ```

- Claim: Applying `VTask.sumProdDistrib α β γ` to `(Sum.inr b, c)` yields `Sum.inr (b, c)`.
  ```lean
  example (α β γ : Type*) (b : β) (c : γ) :
      VTask.sumProdDistrib α β γ (Sum.inr b, c) = Sum.inr (b, c) := by rfl
  ```

- Claim: The inverse of `VTask.sumProdDistrib α β γ` sends `Sum.inl (a, c)` back to `(Sum.inl a, c)`.
  ```lean
  example (α β γ : Type*) (a : α) (c : γ) :
      (VTask.sumProdDistrib α β γ).symm (Sum.inl (a, c)) = (Sum.inl a, c) := by rfl
  ```

- Claim: The inverse of `VTask.sumProdDistrib α β γ` sends `Sum.inr (b, c)` back to `(Sum.inr b, c)`.
  ```lean
  example (α β γ : Type*) (b : β) (c : γ) :
      (VTask.sumProdDistrib α β γ).symm (Sum.inr (b, c)) = (Sum.inr b, c) := by rfl
  ```

## Boundaries

- When `α` or `β` is the empty type `Empty` (or `PEmpty`), the equivalence still holds: the coproduct collapses to the other summand, and the equivalence degenerates to the obvious bijection between e.g. `β × γ` and `Empty × γ ⊕ β × γ ≃ β × γ`.
- When `γ` is the empty type, both sides are empty, and the equivalence is the unique bijection between two empty types.
- When `γ` is `Unit`, the equivalence is essentially the identity up to the trivial isomorphism between `τ × Unit` and `τ`.
- The equivalence is definitionally computed by case-splitting on whether the first component of the input pair is a `Sum.inl` or `Sum.inr`; there is no partiality or failure mode.

## Not to be confused with

- The left-distributivity equivalence `(α × (β ⊕ γ) ≃ α × β ⊕ α × γ)`, which distributes a product over a sum on the **right** argument rather than the left.
- `Equiv.prodSumDistrib` or similar combinators that swap the roles of sum and product (product distributing over sum vs. sum distributing over product).
- The `Sum.elim`/`Sum.map` function combinators, which manipulate functions out of or into coproducts but do not themselves constitute an equivalence between product and sum types.