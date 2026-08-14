## Object

`VTask.choose` extracts the unique element from a multiset that satisfies a given decidable predicate, given a proof that exactly one such element exists. The result is a concrete element of the underlying type — not a subtype or a proof — and it is guaranteed to belong to the multiset and to satisfy the predicate.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.choose : {α : Type u_1} -> (p : α → Prop) -> [DecidablePred p] -> (l : Multiset α) -> (hp : ∃! a, a ∈ l ∧ p a) -> α
<!-- PINNED-SIGNATURE:END -->


`VTask.choose : {α : Type u_1} -> (p : α → Prop) -> [DecidablePred p] -> (l : Multiset α) -> (hp : ∃! a, a ∈ l ∧ p a) -> α`

The implicit type parameter `α` is the element type. The argument `p` is the predicate used to identify the unique element. The instance `[DecidablePred p]` supplies computability evidence allowing membership in `p` to be decided. The argument `l` is the multiset being searched. The argument `hp` is the proof that there exists exactly one element of `l` satisfying `p`; this uniqueness hypothesis is what makes the extraction well-defined.

## Conventions

The function is total on its stated domain: whenever the unique-existence proof `hp` is provided, `VTask.choose` always returns a well-defined value. No junk values or fallback behavior is involved because the hypothesis rules out the degenerate cases (empty multiset or multiple witnesses).

## Worked examples

- Claim: For the multiset `{1, 2, 3}` with predicate `(· = 2)`, `VTask.choose` returns `2`, and the result belongs to the multiset and satisfies the predicate.

- Claim: If `l = {0, 1, 2, 3}` and `p n ↔ n = 3`, then `VTask.choose p l hp = 3`.

- Claim: `VTask.choose (· = 2) {1, 2, 3} hp ∈ ({1, 2, 3} : Multiset ℕ)` — guaranteed by `choose_mem`.

- Claim: `VTask.choose (· = 2) {1, 2, 3} hp` satisfies `p` — guaranteed by `choose_property`.

## Boundaries

- The hypothesis `hp : ∃! a, a ∈ l ∧ p a` simultaneously rules out the empty case (no element satisfies `p`) and the ambiguous case (more than one element satisfies `p`). Both degenerate situations are excluded by the type of the function; no fallback default is ever consulted.
- Membership is in the multiset sense: if an element appears multiple times in `l` and it is the unique element satisfying `p`, the function still returns it once (as a value of type `α`, not a multiplicity).
- The predicate `p` must be `DecidablePred`; this is a computability requirement and does not restrict the mathematical content.
- The element returned satisfies both `choose p l hp ∈ l` and `p (choose p l hp)`, and furthermore it is the *only* element of `l` with this property (by the hypothesis).

## Not to be confused with

- `Finset.choose` — the analogous operation on `Finset` rather than `Multiset`; same intent but the container is a duplicate-free finite set.
- `Classical.choose` — extracts a witness from any existential proposition without a decidability requirement or membership constraint, but gives no membership or uniqueness guarantees without additional lemmas.
- `Multiset.find?` — searches a multiset for *any* element satisfying a predicate and returns an `Option`; does not require or exploit uniqueness.