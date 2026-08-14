## Object

Given two predicates `p` and `q` on a type `α`, `VTask.subtypeOrLeftEmbedding p q` is an injective function (an embedding) from the subtype `{x // p x ∨ q x}` — elements satisfying at least one of `p` or `q` — into the disjoint-sum type `{x // p x} ⊕ {x // q x}`. The routing rule is: an element is sent to the **left** (`Sum.inl`) when `p x` holds, and to the **right** (`Sum.inr`) when `p x` fails (in which case `q x` must hold, since `p x ∨ q x` was given). The function is injective because distinct elements of the domain are distinguishable by their underlying value regardless of which summand they land in.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.subtypeOrLeftEmbedding : {α : Type u_1} -> (p q : α → Prop) -> [DecidablePred p] -> { x // p x ∨ q x } ↪ { x // p x } ⊕ { x // q x }
<!-- PINNED-SIGNATURE:END -->


`VTask.subtypeOrLeftEmbedding : {α : Type u_1} -> (p q : α → Prop) -> [DecidablePred p] -> { x // p x ∨ q x } ↪ { x // p x } ⊕ { x // q x }`

The implicit type argument `α` is the ambient type whose elements are being classified. The argument `p` is the "left" predicate that controls routing: elements satisfying `p` are sent to the left summand. The argument `q` is the "right" predicate: elements that satisfy `p x ∨ q x` but not `p x` are sent to the right summand. The instance `[DecidablePred p]` provides the decision procedure needed to branch on whether `p x` holds for a given element.

## Conventions

When `p x` holds, the element is routed to `Sum.inl ⟨x, h⟩` in the left summand, regardless of whether `q x` also holds. When `p x` does not hold (but `q x` must, since the element belongs to the domain), the element is routed to `Sum.inr ⟨x, _⟩` in the right summand. There is an inherent asymmetry: `p` takes priority over `q`, and only `p` needs a `Decidable` instance.

## Worked examples

- Claim: For `p = (· = 0)` and `q = (· = 1)` on `ℕ`, the element `⟨0, Or.inl rfl⟩` is sent to `Sum.inl ⟨0, rfl⟩` because `p 0` holds.
  ```lean
  example : VTask.subtypeOrLeftEmbedding (· = 0) (· = 1) ⟨0, Or.inl rfl⟩ = Sum.inl ⟨0, rfl⟩ := by
    simp [VTask.subtypeOrLeftEmbedding]
  ```

- Claim: For `p = (· = 0)` and `q = (· = 1)` on `ℕ`, the element `⟨1, Or.inr rfl⟩` is sent to `Sum.inr ⟨1, rfl⟩` because `p 1` does not hold.
  ```lean
  example : VTask.subtypeOrLeftEmbedding (· = 0) (· = 1) ⟨1, Or.inr rfl⟩ = Sum.inr ⟨1, rfl⟩ := by
    simp [VTask.subtypeOrLeftEmbedding]
  ```

- Claim: If `x : {x // p x ∨ q x}` satisfies both `p x` and `q x`, it is still sent to the left summand.

- Claim: The embedding `VTask.subtypeOrLeftEmbedding p q` is injective for any `p`, `q`, and `DecidablePred p`.

## Boundaries

- If `p x` and `q x` both hold, the element goes to `Sum.inl` (the left summand); `q x` is ignored. The routing is purely governed by `p`.
- If neither `p x` nor `q x` holds, the element cannot belong to the domain `{x // p x ∨ q x}`, so this case does not arise.
- The function is an embedding (injective function), not necessarily surjective: elements of `{x // p x} ⊕ {x // q x}` where `p x` holds but are wrapped in `Sum.inr` are not in the image.
- The predicates `p` and `q` may overlap; the left-priority convention handles the overlap consistently.

## Not to be confused with

- `Equiv.subtypeOrEquiv`: a related construction that produces a full **equivalence** (bijection) `{x // p x ∨ q x} ≃ {x // p x} ⊕ {x // q x}`, but only when `p` and `q` are mutually exclusive (i.e., `∀ x, ¬(p x ∧ q x)`).
- `Sum.inl`/`Sum.inr` directly: these are constructors of the sum type, not embeddings from a disjunction-subtype.
- A symmetric version that routes on `q` first (there is no standard Mathlib counterpart called `subtypeOrRightEmbedding`): the left-priority asymmetry of `VTask.subtypeOrLeftEmbedding` is a defining feature, not an oversight.