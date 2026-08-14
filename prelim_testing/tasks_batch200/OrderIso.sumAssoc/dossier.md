## Object

`VTask.sumAssoc` is the canonical order isomorphism witnessing associativity of the disjoint-union (coproduct) of ordered types. Given three types `α`, `β`, `γ` each equipped with a `≤` relation, it produces a bijection `(α ⊕ β) ⊕ γ ≃o α ⊕ (β ⊕ γ)` that is simultaneously a set-level bijection and an order isomorphism: `x ≤ y` in the left-bracketed sum if and only if the images satisfy `≤` in the right-bracketed sum.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumAssoc : (α : Type u_10) -> (β : Type u_11) -> (γ : Type u_12) -> [LE α] -> [LE β] -> [LE γ] -> (α ⊕ β) ⊕ γ ≃o α ⊕ β ⊕ γ
<!-- PINNED-SIGNATURE:END -->


The first three arguments are the carrier types `α`, `β`, `γ` whose disjoint unions are being reassociated. The next three arguments (in square brackets) are the `LE` (less-than-or-equal) instances for `α`, `β`, and `γ` respectively, which endow each type with the order structure that must be preserved by the isomorphism.

## Conventions

No junk-value or edge-case conventions are declared for this definition: it is a total construction on all triples of ordered types, and the ordering on a disjoint sum `α ⊕ β` compares two elements only when they come from the same summand (elements from different summands are incomparable), so there are no special boundary conventions beyond what that order itself specifies.

## Worked examples

- Claim: Applying `VTask.sumAssoc` to `inl (inl a)` (an element of `α` wrapped twice on the left) yields `inl a` (the same element of `α` wrapped once on the left in the re-bracketed sum).

- Claim: Applying `VTask.sumAssoc` to `inl (inr b)` (an element of `β` wrapped as the right component of the inner left summand) yields `inr (inl b)` (the element of `β` now injected into the right summand, then further into the left of that right summand).

- Claim: Applying `VTask.sumAssoc` to `inr c` (an element of `γ` injected on the right) yields `inr (inr c)` (the same element of `γ`, now doubly injected on the right).

- Claim: The inverse `(VTask.sumAssoc α β γ).symm` sends `inl a` back to `inl (inl a)`, `inr (inl b)` back to `inl (inr b)`, and `inr (inr c)` back to `inr c`, making the round-trips the identity.

## Boundaries

- If any of `α`, `β`, or `γ` is the empty type `Empty`, the disjoint sum on that side is trivially isomorphic to the remaining type, but `VTask.sumAssoc` still constructs a well-defined order isomorphism; it simply has an empty domain for the missing summand's constructor.
- When `α`, `β`, or `γ` carries only a partial or discrete (equality-only) order, the isomorphism still holds; the ordering on `⊕` only relates elements within the same summand, so elements from different summands are incomparable on both sides, and the bijection faithfully preserves this.
- The isomorphism is definitionally the identity on underlying elements modulo re-bracketing: no elements are reordered, only the parenthesisation changes.

## Not to be confused with

- `OrderIso.sumComm`: the order isomorphism `α ⊕ β ≃o β ⊕ α` witnessing *commutativity* of the sum, not associativity.
- `Equiv.sumAssoc`: the plain type equivalence (bijection) `(α ⊕ β) ⊕ γ ≃ α ⊕ (β ⊕ γ)` with no order structure; `VTask.sumAssoc` upgrades this to an order isomorphism.
- `OrderIso.prodAssoc`: the analogous associativity isomorphism for the *product* `(α × β) × γ ≃o α × (β × γ)` rather than the sum.