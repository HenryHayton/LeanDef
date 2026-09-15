## VTask.filter

### Object

`VTask.filter p s` is the sub-multiset of `s` obtained by retaining exactly those elements that satisfy the predicate `p`, each kept with its original multiplicity. Elements that do not satisfy `p` are discarded entirely. The result is again a multiset (so order does not matter, but repetitions are preserved).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.filter : {α : Type u_1} -> (p : α → Prop) -> [DecidablePred p] -> (s : Multiset α) -> Multiset α
<!-- PINNED-SIGNATURE:END -->


The first argument `p` is a decidable predicate on the element type; it determines which elements are kept. The instance argument `[DecidablePred p]` provides the computational witness needed to test `p` on each element. The second argument `s` is the multiset being filtered.

### Conventions

There are no declared junk-value or boundary conventions for this definition: the function is total and well-defined on every multiset, including the empty multiset (where it simply returns the empty multiset).

### Worked examples

- Claim: Filtering `{1, 2, 3, 2, 1}` (as a multiset) by the predicate `(· > 1)` yields `{2, 3, 2}`, i.e. the two copies of `2` and the single `3` are kept.

- Claim: `VTask.filter (fun n => n % 2 = 0) {0, 1, 2, 3, 4}` (as a multiset of naturals) equals `{0, 2, 4}`.
  ```lean
  example : VTask.filter (fun n : ℕ => decide (n % 2 = 0) = true)
      ({0, 1, 2, 3, 4} : Multiset ℕ) = {0, 2, 4} := by decide
  ```

- Claim: Filtering any multiset by the always-true predicate returns the multiset itself, i.e. `VTask.filter (fun _ => True) s = s`.

- Claim: Filtering any multiset by the always-false predicate returns the empty multiset, i.e. `VTask.filter (fun _ => False) s = 0`.

- Claim: `VTask.filter p 0 = 0` for any predicate `p` — filtering the empty multiset always yields the empty multiset.
  ```lean
  example (p : ℕ → Prop) [DecidablePred p] : VTask.filter p (0 : Multiset ℕ) = 0 := by
    simp [VTask.filter]
  ```

### Boundaries

- Applied to the empty multiset `0`, `VTask.filter p 0 = 0` regardless of the predicate.
- If every element of `s` satisfies `p`, then `VTask.filter p s = s`.
- If no element of `s` satisfies `p`, then `VTask.filter p s = 0`.
- The result is always a sub-multiset of `s`: `VTask.filter p s ≤ s` (with respect to the submultiset ordering) and also `VTask.filter p s ⊆ s` (setwise).
- Membership characterisation: an element `a` belongs to `VTask.filter p s` if and only if `a ∈ s` and `p a` holds.
- Multiplicity is preserved: if `a` appears `k` times in `s` and `p a` holds, then `a` appears exactly `k` times in `VTask.filter p s`.
- If `s` has no duplicate elements (is a `Nodup` multiset), then `VTask.filter p s` is also `Nodup`.

### Not to be confused with

- `Multiset.filterMap`: maps each element through an `Option`-valued function and collects the `some` results; can change element type and is not a pure subselection.
- `Finset.filter`: the analogous operation on finite sets, which additionally requires decidable equality and enforces that no element appears more than once.
- `List.filter`: operates on ordered lists and preserves order; `VTask.filter` is its quotient-lifted, order-agnostic multiset counterpart.
