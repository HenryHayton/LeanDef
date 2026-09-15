## Object

`VTask.ofCard` takes a finite set `s` (of elements of some type `α`) together with a proof that `s` has exactly `n` elements, and packages them together as a member of the type `Set.powersetCard α n` — the subtype of all finite sets of type `α` that have cardinality exactly `n`. In other words, it is the canonical constructor that promotes a `Finset α` with a known cardinality into the cardinality-indexed powersetCard subtype.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofCard : {α : Type u_1} -> {n : ℕ} -> {s : Finset α} -> (s_card : s.card = n) -> ↑(Set.powersetCard α n)
<!-- PINNED-SIGNATURE:END -->


VTask.ofCard : {α : Type u_1} -> {n : ℕ} -> {s : Finset α} -> (s_card : s.card = n) -> ↑(Set.powersetCard α n)

- `α` is the implicit ambient type whose elements belong to the finite set.
- `n` is the implicit natural number specifying the required cardinality.
- `s` is the implicit finite set being promoted into the subtype.
- `s_card` is an explicit proof that the cardinality of `s` equals `n`; it is the sole piece of evidence that certifies membership in `Set.powersetCard α n`.

## Conventions

There are no junk-value conventions to declare: the function is a total constructor whose single non-implicit argument is a proof. Whenever that proof is supplied, the output is uniquely and fully determined; there is no regime in which a default or fallback value is produced.

## Worked examples

- Claim: The underlying `Finset` of `VTask.ofCard h` is the original set `s`; that is, `(VTask.ofCard h).val = s` for any proof `h : s.card = n`.

- Claim: For `s = ({1, 2} : Finset ℕ)` with proof `h : s.card = 2`, `VTask.ofCard h` is an element of `Set.powersetCard ℕ 2`, and its `val` field recovers `{1, 2}`.

- Claim: Applying `VTask.ofCard` to the proof `rfl : s.card = s.card` yields an element whose `val` is definitionally equal to `s`, and applying it again with any other proof `h` of the same equality returns the same element (subtype extensionality).

## Boundaries

- When `n = 0`, the only finite set satisfying `s.card = 0` is the empty set `∅`. `VTask.ofCard` therefore produces the unique element of `Set.powersetCard α 0`.
- The proof argument `s_card` is propositional; two calls `VTask.ofCard h₁` and `VTask.ofCard h₂` (for the same `s`) are definitionally equal regardless of which proof of `s.card = n` is supplied, because `ℕ`-equality proofs are unique (via `Nat.eq_of_beq_eq_true` / proof irrelevance).
- There is no partiality: every `Finset α` with a cardinality proof can be promoted; the function is defined for all `α`, all `n`, and all `s`.

## Not to be confused with

- `Finset.powersetCard`: a function that produces the `Finset` of all `n`-element sub-`Finset`s of a given `Finset`, rather than a constructor for the subtype.
- `Set.powersetCard α n` (the type itself): this is the subtype that `VTask.ofCard` maps *into*; `VTask.ofCard` is the constructor, not the type.
- `Finset.card`: the function that *computes* the cardinality of a `Finset`, which appears in the hypothesis of `VTask.ofCard` but is not itself the constructor.