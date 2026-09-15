## VTask.Subrel

### Object

Given a relation `r` on a type `α` and a predicate `p : α → Prop`, `VTask.Subrel r p` is the relation on the subtype `{x : α // p x}` obtained by restricting `r` to those elements of `α` that satisfy `p`. Concretely, two elements `a b : {x : α // p x}` are related by `VTask.Subrel r p` exactly when their underlying values in `α` are related by `r`. This is the standard notion of an *induced* or *inherited* relation on a subtype.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Subrel : {α : Type u_1} -> (r : α → α → Prop) -> (p : α → Prop) -> Subtype p → Subtype p → Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Subrel : {α : Type u_1} -> (r : α → α → Prop) -> (p : α → Prop) -> Subtype p → Subtype p → Prop`

The implicit type argument `α` is the ambient type whose elements the relation `r` originally lives over. The first explicit argument `r` is the relation on `α` being restricted. The second explicit argument `p` is the predicate carving out the subtype; only elements of `α` satisfying `p` are in the domain of the resulting relation. The final two arguments are the pair of elements of the subtype `{x : α // p x}` being compared.

### Conventions

No special junk-value or boundary conventions are declared: the definition is total and straightforward — for any relation and any predicate, `VTask.Subrel r p a b` holds if and only if `r a.1 b.1` holds, with no special cases.

### Worked examples

- Claim: For `r = (· < ·)` on `ℕ` and `p = (· % 2 = 0)`, two even natural numbers `a b : {n : ℕ // n % 2 = 0}` satisfy `VTask.Subrel (· < ·) (· % 2 = 0) a b` if and only if `a.1 < b.1`.

- Claim: `VTask.Subrel (· ∈ ·) (· ∈ x)` is the membership relation restricted to elements of a ZFSet `x`, and a ZFSet `x` is an ordinal iff this restricted membership is a well-order on `{y // y ∈ x}`.

- Claim: For the universal relation `r = fun _ _ => True` on any type, `VTask.Subrel r p a b` holds for all `a b` in the subtype, regardless of which predicate `p` is used.

- Claim: For the empty relation `r = fun _ _ => False`, `VTask.Subrel r p a b` is always false for every `p`, `a`, and `b`.

### Boundaries

- When `p = fun _ => True`, the subtype is essentially all of `α`, and `VTask.Subrel r p` is essentially the same as `r` (up to the equivalence between `α` and `{x : α // True}`).
- When `p = fun _ => False`, the subtype is empty, so `VTask.Subrel r p` is vacuously a relation on the empty type — it holds for no pairs (there are none).
- The definition makes no assumption on `r`: it works for any relation, including non-transitive, non-symmetric, and non-reflexive ones. Whatever relational properties `r` has, `VTask.Subrel r p` inherits them (e.g., if `r` is a well-order, so is the restriction).
- There is no restriction on `p`; the construction is uniform in both `r` and `p`.

### Not to be confused with

- `Subrelation r s` — this asserts that one relation on the *same* type is contained in another (`∀ a b, r a b → s a b`); it does not produce a relation on a subtype.
- `Set.sep` or subsets — `VTask.Subrel` restricts a *relation* to a *subtype*, not a set to a subset (though the two ideas are closely related when working with `Set`-valued predicates).
- `Rel.restrict` or similar ad-hoc constructions — `VTask.Subrel` is the canonical Mathlib way to inherit a relation onto a subtype via the coercion map `Subtype.val`.