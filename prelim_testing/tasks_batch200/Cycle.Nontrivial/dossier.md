## VTask.Nontrivial

### Object

A predicate on a cycle (a list considered up to cyclic rotation) that holds exactly when the cycle contains at least two **distinct** elements. In other words, a cycle is *nontrivial* if it cannot be a singleton or the empty cycle — it must have at least two different members.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Nontrivial : {α : Type u_1} -> (s : Cycle α) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit argument `α` is the element type of the cycle. The explicit argument `s` is the cycle being tested for nontriviality.

### Conventions

There are no special junk-value or boundary conventions declared for this predicate: it is a straightforward existential proposition that is simply false on the empty cycle, false on any cycle whose elements are all equal, and true whenever two distinct elements can be witnessed.

### Worked examples

- Claim: The cycle `(↑[1, 2] : Cycle ℕ)` is nontrivial, since `1 ≠ 2` and both belong to the cycle.

- Claim: The cycle `(↑[1, 1] : Cycle ℕ)` is **not** nontrivial, because there are no two distinct elements in it.

- Claim: The empty cycle `(↑([] : List ℕ) : Cycle ℕ)` is **not** nontrivial, since it contains no elements at all.

- Claim: If `s : Cycle α` is nontrivial, then `s.reverse` is also nontrivial (the property is invariant under reversal).

- Claim: If `s : Cycle α` has no duplicate elements (`Nodup s`) and is nontrivial, then `2 ≤ s.length`.

### Boundaries

- The **empty cycle** is not nontrivial: no elements exist to witness the existential.
- A **singleton cycle** `↑[x]` is not nontrivial: only one element is present, so no pair of distinct elements can be found.
- A cycle containing the **same value repeated** (e.g., `↑[a, a]`) is not nontrivial, because no two *distinct* elements are present even though the length exceeds one.
- Under the `Nodup` (no-duplicate) assumption, nontriviality is equivalent to the cycle not being a subsingleton (i.e., having at least two elements), since duplicates are excluded.
- Nontriviality is preserved under reversal: `s.reverse.Nontrivial ↔ s.Nontrivial`.

### Not to be confused with

- `Cycle.Nodup`: asserts that a cycle has no repeated elements; a cycle can satisfy `Nodup` while still being trivial (e.g., a singleton or empty cycle).
- `List.Nontrivial` or general `Nontrivial` typeclass: the ambient Mathlib `Nontrivial` on a type asserts the type has at least two distinct elements, which is a global property of the type, not a property of a particular cycle.
- Cycle length ≥ 2: this is a weaker condition when duplicates are allowed — a cycle of length 2 with both entries equal is **not** `VTask.Nontrivial`, even though its length is 2.