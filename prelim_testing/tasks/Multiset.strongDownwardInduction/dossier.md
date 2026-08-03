## Object

`VTask.strongDownwardInduction` is a **strong downward induction principle** for multisets bounded by a fixed cardinality `n`. Given a way to construct `p s` for any multiset `s` of cardinality at most `n`, provided one already has `p t` for every multiset `t` that is strictly larger than `s` (in the multiset ordering) and still has cardinality at most `n`, this combinator produces `p s` for every such `s`. The induction proceeds from the "top" (multisets of cardinality exactly `n`) downward, making it a well-founded recursion descending through the strict multiset order, bounded by `n`. It may be used both to define data (when `p` has a general `Sort`) and to prove propositions.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.strongDownwardInduction : {α : Type u_1} -> {p : Multiset α → Sort u_3} -> {n : ℕ} -> (H : (t₁ : Multiset α) → ({t₂ : Multiset α} → t₂.card ≤ n → t₁ < t₂ → p t₂) → t₁.card ≤ n → p t₁) -> (s : Multiset α) -> s.card ≤ n → p s
<!-- PINNED-SIGNATURE:END -->


`VTask.strongDownwardInduction : {α : Type u_1} -> {p : Multiset α → Sort u_3} -> {n : ℕ} -> (H : (t₁ : Multiset α) → ({t₂ : Multiset α} → t₂.card ≤ n → t₁ < t₂ → p t₂) → t₁.card ≤ n → p t₁) -> (s : Multiset α) -> s.card ≤ n → p s`

- `α` is the element type of the multisets under consideration.
- `p` is the motive: a type-valued (or sort-valued) predicate on multisets of `α` whose values one wishes to construct or prove.
- `n` is the upper bound on cardinality; only multisets whose cardinality does not exceed `n` are in scope.
- `H` is the **inductive step**: a function that, for any multiset `t₁` of cardinality at most `n`, produces `p t₁` given that `p t₂` is already available for every multiset `t₂` with `t₂.card ≤ n` and `t₁ < t₂` (i.e., every strict multiset-order successor of `t₁` within the bound).
- `s` is the particular multiset at which the result is evaluated.
- The final argument is a proof that `s.card ≤ n`, ensuring `s` lies within the bounded region.

## Conventions

When the cardinality bound `n` equals `0`, the only multiset of cardinality `≤ 0` is the empty multiset; `H` receives a vacuously-satisfied hypothesis (no strictly larger multiset has cardinality `≤ 0`), so `p ∅` is produced directly from `H` with no recursion. The well-foundedness is grounded by the fact that the strict multiset order on multisets of bounded cardinality is finite and acyclic, so the recursion always terminates.

## Worked examples

- Claim: For `p s := s.card ≤ n`, `VTask.strongDownwardInduction` with the trivial step (just returning the hypothesis `h : t₁.card ≤ n`) produces the bound `s.card ≤ n` for any `s` with `s.card ≤ n`.

- Claim: The unfolding equation holds: `VTask.strongDownwardInduction H s` equals `H s (fun ht _ => VTask.strongDownwardInduction H _ ht)`, i.e., one application of `H` followed by recursive calls on strictly larger multisets within the bound.

- Claim: For `n = 3` and any multiset `s` of natural numbers with `s.card ≤ 3`, applying `VTask.strongDownwardInduction` with a step that sums cardinalities from the top yields a well-defined value at `s`.

## Boundaries

- **At `n = 0`:** Only the empty multiset satisfies the cardinality bound; `H` is called with a hypothesis that has no inhabitants (no strict upper multiset of cardinality `≤ 0` exists), so `p ∅` is computed by `H` without any recursive call.
- **At the boundary `s.card = n`:** There is no strictly larger multiset of cardinality `≤ n`, so `H` again receives a vacuous inductive hypothesis for exactly these "top" multisets. The induction is grounded here.
- **For `s.card < n`:** The inductive hypothesis handed to `H` may be non-trivial; `p t₂` for multisets `t₂` strictly above `s` (and of cardinality `≤ n`) will be obtained by recursive applications.
- The definition is **total**: it produces a value for every `s` and every proof `s.card ≤ n`, relying purely on the well-foundedness of the strict multiset order restricted to multisets of bounded cardinality.

## Not to be confused with

- **`Multiset.strongInduction`** (or `strongInductionOn`): an upward/downward strong induction on multisets by strict submultiset inclusion (going to *smaller* sub-multisets), not bounded by a cardinality and not proceeding from larger to smaller cardinality.
- **`Multiset.strongDownwardInductionOn`**: the "flipped" variant where the multiset argument comes first (method-style), rather than the step function; mathematically identical but with a different argument order.
- **`Nat.strong_rec_on` / `Nat.strongRecOn`**: strong recursion on natural numbers; similar in spirit but applies to `ℕ` rather than to multisets, and does not involve a multiset order.