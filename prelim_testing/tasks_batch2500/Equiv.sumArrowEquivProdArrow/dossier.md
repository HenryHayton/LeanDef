## Object

`VTask.sumArrowEquivProdArrow α β γ` is the canonical type equivalence (bijection) between the function type `α ⊕ β → γ` and the product type `(α → γ) × (β → γ)`. In plain terms: a function defined on a disjoint union type is the same data as a pair of functions, one defined on each summand. The forward direction restricts a function on the sum to each summand; the backward direction glues two functions together by case-splitting.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumArrowEquivProdArrow : (α : Type u_9) -> (β : Type u_10) -> (γ : Type u_11) -> (α ⊕ β → γ) ≃ (α → γ) × (β → γ)
<!-- PINNED-SIGNATURE:END -->


`(α : Type u_9) -> (β : Type u_10) -> (γ : Type u_11) -> (α ⊕ β → γ) ≃ (α → γ) × (β → γ)`

The first argument `α` is the left summand type of the domain. The second argument `β` is the right summand type of the domain. The third argument `γ` is the common codomain type. Together they determine both sides of the equivalence: functions from the disjoint union `α ⊕ β` to `γ` on the left, and pairs of functions `(α → γ) × (β → γ)` on the right.

## Conventions

No special junk-value or boundary conventions are declared: the equivalence is total and well-defined for all types `α`, `β`, and `γ`, including empty types, unit types, or infinite types, without any side conditions.

## Worked examples

- Claim: Applying the forward direction of `VTask.sumArrowEquivProdArrow Bool Bool Bool` to the function `Sum.elim id not` yields the pair `(id, not)`, so the first component evaluates `(Sum.inl true)` to `true`.

- Claim: For `f : α ⊕ β → γ`, the first component of `VTask.sumArrowEquivProdArrow α β γ f` evaluated at `a : α` equals `f (Sum.inl a)` — that is, the forward map simply pre-composes with `Sum.inl`.

- Claim: For functions `f : α → γ` and `g : β → γ`, applying the inverse of `VTask.sumArrowEquivProdArrow α β γ` to the pair `(f, g)` and then evaluating at `Sum.inr b` gives `g b` — the backward map recovers the original function on the right summand.

- Claim: Composing the forward map with the backward map (i.e., `(VTask.sumArrowEquivProdArrow α β γ).symm` after `VTask.sumArrowEquivProdArrow α β γ`) is the identity on `α ⊕ β → γ`, because the equivalence is a true bijection.

## Boundaries

- When `α` or `β` is the empty type `Empty`, the corresponding component of the product is the unique function from `Empty` to `γ` (of which there is exactly one), and the equivalence still holds without issue.
- When `γ` is a singleton type (e.g., `Unit`), both sides are singleton types and the equivalence is trivially the unique map between them.
- When `α ⊕ β` itself is empty (both `α` and `β` are empty), the function type `α ⊕ β → γ` is a singleton regardless of `γ`, and the product `(α → γ) × (β → γ)` is likewise a singleton; the equivalence remains valid.
- The equivalence is definitionally its own natural isomorphism: the two round-trip composites are definitionally equal to the respective identity maps.

## Not to be confused with

- `Equiv.prodArrowEquivArrowProd`: the analogous equivalence reorganising functions *into* a product type, i.e., `(α → β × γ) ≃ (α → β) × (α → γ)`, which splits on the *codomain* rather than the *domain*.
- `RingEquiv.sumArrowEquivProdArrow` / `AlgEquiv.sumArrowEquivProdArrow`: ring- or algebra-enriched versions of the same equivalence when `γ` carries extra algebraic structure; these are structured isomorphisms, not merely type equivalences.
- `Equiv.sumEquivSigmaTwo`: a different equivalence involving sum types that reorganises the sum itself rather than function types out of a sum.