## Object

`VTask.piEquivPiSubtypeProd` is a type equivalence (a bijection with explicit inverse) between the dependent function type `(i : α) → β i` — functions assigning to each index in `α` a value of type `β i` — and the product of two dependent function types: one restricted to indices satisfying the predicate `p`, and one restricted to indices not satisfying `p`. In short, it says that a dependent function on all of `α` is canonically the same thing as a pair of dependent functions, one on the "positive" part `{x // p x}` and one on the "negative" part `{x // ¬p x}`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piEquivPiSubtypeProd : {α : Type u_9} -> (p : α → Prop) -> (β : α → Type u_10) -> [DecidablePred p] -> ((i : α) → β i) ≃ ((i : { x // p x }) → β ↑i) × ((i : { x // ¬p x }) → β ↑i)
<!-- PINNED-SIGNATURE:END -->


`VTask.piEquivPiSubtypeProd : {α : Type u_9} -> (p : α → Prop) -> (β : α → Type u_10) -> [DecidablePred p] -> ((i : α) → β i) ≃ ((i : { x // p x }) → β ↑i) × ((i : { x // ¬p x }) → β ↑i)`

The implicit argument `α` is the index type being split. The argument `p` is the predicate on `α` that determines which side of the partition each index falls into. The argument `β` is the type family over `α` giving the fiber at each index. The instance `[DecidablePred p]` provides the ability to decide, for any given index, whether it satisfies `p` or not — this is needed to steer the inverse map.

## Conventions

There are no junk-value conventions to declare: the equivalence is total and both its forward and inverse directions are defined on all inputs without any special casing for degenerate choices of `α`, `p`, or `β`.

## Worked examples

- Claim: For the constant predicate `fun _ => True` on `Fin 3` with constant fiber `ℕ`, applying the forward direction to a function `f` yields `(f ∘ Subtype.val, isEmptyElim ∘ Subtype.val)`, i.e., the second component is vacuously empty.

- Claim: For the predicate `Even` on `Fin 4` with constant fiber `Bool`, the forward map of `VTask.piEquivPiSubtypeProd Even (fun _ => Bool)` sends a function `f : Fin 4 → Bool` to the pair `(fun ⟨i, h⟩ => f i, fun ⟨i, h⟩ => f i)`, so evaluating the first component at `⟨⟨2, by omega⟩, by decide⟩` returns the same value as `f ⟨2, by omega⟩`.

- Claim: For `α = Bool`, `p = id`, `β = fun _ => ℕ`, the equivalence witnesses a bijection between `(Bool → ℕ)` and `({b // b = true} → ℕ) × ({b // b = false} → ℕ)`, and in particular the composite `(VTask.piEquivPiSubtypeProd id (fun _ => ℕ)).symm ∘ (VTask.piEquivPiSubtypeProd id (fun _ => ℕ))` is the identity.

- Claim: The preimage under the inverse of `VTask.piEquivPiSubtypeProd p β` of a product of `univ`-pi sets factors as the product of the individual restricted pi sets; this is consistent with the theorem `Equiv.preimage_piEquivPiSubtypeProd_symm_pi`.

## Boundaries

- If `α` is empty, then `p` partitions it into two empty subtypes; the equivalence still holds and both components of the product are functions from an empty type, making the whole product a singleton (there is exactly one such pair of functions, and exactly one function from `α`).
- If `p` is the constantly-true predicate, then `{x // ¬p x}` is empty; the second component of the product is a function from an empty subtype, vacuously determined, and the first component carries all the information.
- If `p` is the constantly-false predicate, the dual situation applies: the first component is vacuous and the second carries all the information.
- The instance requirement `[DecidablePred p]` is essential for constructing the inverse; in classical mathematics this is always available, but in Lean it must be provided explicitly or inferred.

## Not to be confused with

- `Equiv.piCongrLeft` — reindexes a pi type along an equivalence of index types, rather than splitting it into a product by a predicate.
- `Equiv.prodEquivPiSubtypeProd` or similar product-splitting equivalences — some variants split a *non-dependent* product type or use a decidable subtype in a different way.
- `Finset.prod_compl` — a statement about products (in the monoid sense) over a finset and its complement, which is a different kind of splitting related to `∑`/`∏` rather than function types.