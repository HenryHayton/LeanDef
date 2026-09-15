## Object

`VTask.subtype p s` is the finite set of all inhabitants of the subtype `{x : α // p x}` whose underlying value belongs to the finite set `s`. Concretely, it packages every element of `s` that satisfies the predicate `p` into a dependent pair `⟨a, ha⟩`, yielding a `Finset` whose type is `Finset {x : α // p x}`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.subtype : {α : Type u_4} -> (p : α → Prop) -> [DecidablePred p] -> (s : Finset α) -> Finset (Subtype p)
<!-- PINNED-SIGNATURE:END -->


VTask.subtype : {α : Type u_4} -> (p : α → Prop) -> [DecidablePred p] -> (s : Finset α) -> Finset (Subtype p)

The implicit type `α` is the ambient type whose elements populate both `s` and the predicate. `p` is the predicate defining the subtype; it plays the role of the membership condition for the resulting dependent-type elements. The `DecidablePred p` instance is required so that membership of `p` can be computably tested when filtering `s`. Finally, `s` is the source finite set of plain `α`-values; only those elements of `s` satisfying `p` appear (wrapped as subtypes) in the output.

## Conventions

There are no junk-value or edge-case conventions requiring special documentation: the operation is a total, computable construction that works uniformly for all inputs, including the empty finset and the always-false or always-true predicate.

## Worked examples

- Claim: For `s = {0, 1, 2, 3, 4}` in `Finset ℕ` and `p n := n % 2 = 0`, `(VTask.subtype p s).card = 3` (the elements `⟨0,_⟩`, `⟨2,_⟩`, `⟨4,_⟩`).
  ```lean
  example : (VTask.subtype (fun n : ℕ => n % 2 = 0) {0,1,2,3,4}).card = 3 := by decide
  ```

- Claim: For the empty finset `∅ : Finset ℕ` and any decidable predicate `p`, `VTask.subtype p ∅ = ∅`.
  ```lean
  example : VTask.subtype (fun n : ℕ => n < 10) ∅ = ∅ := by decide
  ```

- Claim: If every element of `s` satisfies `p`, then mapping `VTask.subtype p s` back to `α` via the subtype coercion recovers `s.filter p = s`.

- Claim: A subtype element `⟨a, ha⟩` belongs to `VTask.subtype p s` if and only if `a ∈ s` (and `p a` holds, which is already encoded in `ha`).

## Boundaries

- **Empty source set**: `VTask.subtype p ∅ = ∅` for any `p`; there are no elements to filter.
- **Predicate always false**: If no element of `s` satisfies `p`, the result is the empty `Finset (Subtype p)`.
- **Predicate always true**: Every element of `s` is wrapped into a subtype, so the result has the same cardinality as `s`.
- **Relationship to `filter`**: Mapping the result back through the subtype embedding recovers exactly `s.filter p`; this is a key identity.
- **Monotonicity**: The construction is monotone in `s` — if `s ⊆ t` then `VTask.subtype p s ⊆ VTask.subtype p t`.

## Not to be confused with

- `Finset.filter p s` — this keeps the satisfying elements as plain `α`-values rather than packaging them into the subtype `{x // p x}`.
- `Finset.attach s` — this wraps every element of `s` into the subtype `{x // x ∈ s}`, using membership in `s` as the predicate rather than an arbitrary `p`.
- `Finset.univ` for a `Fintype {x // p x}` — the universe of all subtype inhabitants, not restricted to those coming from a particular source set `s`.
