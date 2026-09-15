## VTask.sumLexComplLeft

### Object

This is a relation isomorphism (order-preserving bijection) that decomposes a given relation `r` on a type `α` into a lexicographic sum of two sub-relations determined by a pivot element `x`. Concretely, it identifies `r` with the lexicographic combination of: (1) the restriction of `r` to those elements that are `r`-less-than `x`, and (2) the restriction of `r` to those elements that are **not** `r`-less-than `x`. In the lexicographic sum, every element of the first part (the "below-`x`" part) is considered smaller than every element of the second part (the "not-below-`x`" part), and within each part the original relation is inherited. The isomorphism asserts that this lexicographic structure exactly reconstructs `r`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumLexComplLeft : {α : Type u_1} -> (r : α → α → Prop) -> (x : α) -> [IsTrans α r] -> [Std.Trichotomous r] -> [DecidableRel r] -> Sum.Lex (Subrel r fun x_1 => r x_1 x) (Subrel r fun x_1 => ¬r x_1 x) ≃r r
<!-- PINNED-SIGNATURE:END -->


`VTask.sumLexComplLeft : {α : Type u_1} -> (r : α → α → Prop) -> (x : α) -> [IsTrans α r] -> [Std.Trichotomous r] -> [DecidableRel r] -> Sum.Lex (Subrel r fun x_1 => r x_1 x) (Subrel r fun x_1 => ¬r x_1 x) ≃r r`

- `α` is the ambient type on which the relation lives.
- `r` is the relation on `α` being decomposed; it is the target of the isomorphism.
- `x` is the pivot element used to split `α` into two parts: those elements `a` with `r a x` (strictly less than `x` in the sense of `r`) and those with `¬ r a x`.
- The `IsTrans α r` instance supplies transitivity of `r`, which is needed to verify that cross-part comparisons in the lexicographic sum agree with `r`.
- The `Std.Trichotomous r` instance supplies trichotomy (for any two elements, one of `r a b`, `a = b`, or `r b a` holds), also needed for cross-part compatibility.
- The `DecidableRel r` instance makes the membership predicate `r · x` decidable, enabling the underlying set-complement equivalence on `Sum`.

### Conventions

No special junk-value or out-of-domain conventions are declared for this definition, because it is a total construction: every type `α`, every relation `r`, and every element `x` (given the required typeclass instances) yield a valid relation isomorphism with no degenerate edge cases that would require special treatment.

### Worked examples

- Claim: For `r = (· < ·)` on `ℕ` and pivot `x = 3`, the domain of the left summand consists exactly of `{0, 1, 2}` and the domain of the right summand consists of `{n : ℕ | ¬ n < 3}` = `{3, 4, 5, …}`.

- Claim: For `r = (· < ·)` on `ℕ` with pivot `x = 0`, the left summand (elements `n` with `n < 0`) is empty, so `VTask.sumLexComplLeft (· < ·) 0` is an isomorphism between `Sum.Lex (Subrel (· < ·) (· < 0)) (Subrel (· < ·) (¬ · < 0))` and `(· < ·)`, where the left summand contributes nothing and the right summand carries all of `ℕ`.

- Claim: For any `a` in the left summand (i.e., satisfying `r a x`) and any `b` in the right summand (i.e., satisfying `¬ r b x`), the image of `Sum.inl ⟨a, _⟩` under `VTask.sumLexComplLeft r x` equals `a` as an element of `α`, and `r a b` holds in `r` (since by transitivity and trichotomy, an element below the pivot is below any element not below the pivot).

- Claim: For `r = (· < ·)` on `Fin 4` and pivot `x = 2`, the map sends `Sum.inl ⟨⟨1, _⟩, _⟩` and `Sum.inr ⟨⟨3, _⟩, _⟩` to elements satisfying `(1 : Fin 4) < 3`, consistent with the `Sum.Lex` ordering.

### Boundaries

- **Empty left summand**: When no element satisfies `r a x` (e.g., `x` is a minimum element), the left summand is an empty sub-relation and the isomorphism restricts entirely to the right summand, which then carries all of `α`.
- **Empty right summand**: When every element satisfies `r a x` (impossible for a strict order since `¬ r x x`, but possible for other relations), the right summand carries only those elements; since `r x x` would be needed for `x` itself to be in the left part, the exact membership of `x` depends on whether `r x x` holds.
- **Pivot element `x` itself**: For a strict order, `¬ r x x`, so `x` always lands in the right summand (elements not `r`-below `x`). The isomorphism places `x` in the second component of the sum.
- **Non-strict or reflexive relations**: The typeclass assumptions (`IsTrans`, `Trichotomous`) are required but do not force strictness; for reflexive `r`, an element may satisfy `r a x` even when `a = x`.

### Not to be confused with

- `Sum.Lex` itself: that is just the lexicographic order on a sum type, not the isomorphism splitting a given relation around a pivot.
- `Subrel`: that is the restriction of a relation to a subtype, one of the two ingredients combined here, not the full isomorphism.
- `RelIso.sumLexComplRight` (if it existed): a hypothetical variant splitting by elements *greater* than `x` versus *not greater*, which would yield a different decomposition.