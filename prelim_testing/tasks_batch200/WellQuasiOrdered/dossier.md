## VTask.WellQuasiOrdered

### Object

A relation `r` on a type `α` is **well quasi-ordered** (WQO) if every infinite sequence of elements of `α` contains two terms that are related in the forward direction by `r`: that is, for every function `f : ℕ → α` there exist natural numbers `m < n` with `r (f m) (f n)`. Informally, no matter how you list elements of `α` in an infinite sequence, you cannot avoid eventually finding a later term that is "above" an earlier one with respect to `r`.

This captures the classical notion from combinatorics and order theory: a quasi-order is WQO precisely when it has no infinite strictly descending chains and no infinite antichains. However, the Mathlib predicate does **not** require `r` to be a preorder (reflexive and transitive); it is a purely combinatorial condition on any binary relation.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.WellQuasiOrdered : {α : Type u_1} -> (r : α → α → Prop) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.WellQuasiOrdered : {α : Type u_1} -> (r : α → α → Prop) -> Prop`

The implicit argument is the carrier type `α` whose elements the relation acts on. The explicit argument `r` is the binary relation on `α` being tested for the well quasi-order property.

### Conventions

No junk-value or edge conventions are declared: `VTask.WellQuasiOrdered` is a universally-quantified proposition that is simply true or false for any given relation, and no special output is assigned to degenerate inputs.

### Worked examples

- Claim: Every reflexive relation on a finite type is well quasi-ordered — formally, if `α` is `Finite` and `r` is reflexive, then `VTask.WellQuasiOrdered r` holds. (Any infinite sequence over a finite type must repeat some value, and the reflexivity of `r` then supplies the required related pair.)

- Claim: The coordinatewise product of two well quasi-orders is again a well quasi-order: if `VTask.WellQuasiOrdered r` and `VTask.WellQuasiOrdered s`, then `VTask.WellQuasiOrdered (fun a b : α × β => r a.1 b.1 ∧ s a.2 b.2)` holds.

- Claim: If `VTask.WellQuasiOrdered r` holds and `r` is a preorder, then any antichain with respect to `r` is a finite set. That is, well quasi-orders admit no infinite antichains.

- Claim: For the empty relation on an infinite type such as `ℕ` (where `r a b = False` for all `a b`), `VTask.WellQuasiOrdered r` is false, because the identity sequence `f n = n` has no pair `m < n` with `r (f m) (f n)`.

### Boundaries

- **Empty type**: If `α` is empty, then there is no function `f : ℕ → α` at all, so the universal quantifier is vacuously true and every relation on the empty type is well quasi-ordered.
- **Singleton type**: Any relation on a one-element type is well quasi-ordered: any sequence is constant, and any reflexive relation then witnesses the condition; even an irreflexive relation fails to be WQO here only if `r a a` is false, but the sequence is still forced to repeat, so if `r` is irreflexive on a singleton, WQO actually fails. In this case the question reduces to whether `r a a` holds.
- **Non-preorders**: The definition is stated for arbitrary relations. If `r` is neither reflexive nor transitive, `VTask.WellQuasiOrdered r` can still hold (e.g., the strict less-than on `ℕ` is not a preorder but the condition still makes sense, and in fact it does hold for `<` on `ℕ` since any sequence must eventually contain an increasing pair).
- **Relation isomorphisms**: If `r` and `s` are relationally isomorphic, then `VTask.WellQuasiOrdered r ↔ VTask.WellQuasiOrdered s`; the property is invariant under relational isomorphism.
- **Surjective homomorphisms**: WQO is preserved forwards along surjective relation homomorphisms: if `r` is WQO and `f : r →r s` is surjective, then `s` is WQO.

### Not to be confused with

- **Well-order**: A well-order is a total, well-founded strict order; WQO does not require totality or strictness, and a WQO need not be a well-order.
- **`WellQuasiOrderedLE`**: A typeclass asserting that the canonical `≤` relation on a preordered type is well quasi-ordered; this is the bundled, instance-based version of the same concept, whereas `VTask.WellQuasiOrdered` is an explicit predicate on an arbitrary relation.
- **`Set.IsPWO` (partially well-ordered set)**: The `IsPWO` predicate on a `Set α` asserts a related but set-restricted condition; `(Set.univ).IsPWO` is equivalent to `WellQuasiOrderedLE α`, but `IsPWO` applies to subsets, not to arbitrary relations on all of `α`.
