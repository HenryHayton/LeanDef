## Object

`VTask.attachFin s h` converts a finite set `s` of natural numbers — all of which are assumed to be strictly less than some bound `n` — into the corresponding finite set of elements of the type `Fin n` (i.e., natural numbers that carry a proof of being less than `n`). The underlying set of values is unchanged; only the type is refined from `ℕ` to `Fin n`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.attachFin : (s : Finset ℕ) -> {n : ℕ} -> (h : ∀ m ∈ s, m < n) -> Finset (Fin n)
<!-- PINNED-SIGNATURE:END -->


`VTask.attachFin : (s : Finset ℕ) -> {n : ℕ} -> (h : ∀ m ∈ s, m < n) -> Finset (Fin n)`

The first argument `s` is the finite set of natural numbers to be retyped. The implicit argument `n` is the upper bound that defines the `Fin n` target type; it is inferred from context or from `h`. The third argument `h` is the proof obligation that every element of `s` is strictly less than `n`, which is exactly the data needed to wrap each element as a `Fin n` value.

## Conventions

There are no junk-value conventions to declare: the function is total — as long as the proof `h` is supplied the result is well-defined — and there is no boundary regime in which the output defaults to some canonical value.

## Worked examples

- Claim: The set `{0, 1, 2}` of naturals, viewed as a `Finset (Fin 5)` via `attachFin`, has cardinality 3.
  (This follows directly from the card-preservation theorem: `(s.attachFin h).card = s.card`.)

- Claim: An element `a : Fin n` belongs to `VTask.attachFin s h` if and only if `(a : ℕ)` belongs to `s`.
  (This is the membership characterisation: `a ∈ s.attachFin h ↔ (a : ℕ) ∈ s`.)

- Claim: Mapping `Fin.valEmbedding` over `VTask.attachFin s h` recovers the original set `s` as a `Finset ℕ`.
  (The round-trip theorem `map Fin.valEmbedding (s.attachFin h) = s` confirms the construction is lossless.)

- Claim: If `s ⊆ t` (both contained in `{0, …, n−1}`), then `s.attachFin hs ⊆ t.attachFin ht` as `Finset (Fin n)`.
  (Subset and strict-subset structure is exactly reflected by `attachFin`.)

## Boundaries

- **Empty set:** When `s = ∅` the proof obligation `h` is vacuously true, and `attachFin ∅ h` returns `∅ : Finset (Fin n)`, whatever `n` is.
- **n = 0:** If `n = 0` the only valid input is `s = ∅` (since no natural number is less than 0), and the result is `∅ : Finset (Fin 0)`.
- **s fills the range:** When `s = {0, 1, …, n−1}` and `h` witnesses this, `attachFin s h` is `Finset.univ : Finset (Fin n)` (up to definitional equality and the relevant simp lemmas).
- **Cardinality is preserved exactly:** `(VTask.attachFin s h).card = s.card` in all cases; no elements are lost or duplicated during the type change.

## Not to be confused with

- `Finset.fin` / `Finset.range n` — produces `{0, 1, …, n−1}` as a `Finset ℕ`, not a retyping of an arbitrary set.
- `Finset.image Fin.val` applied in reverse — the image of `attachFin s h` under `Fin.val` is `s`, but `image` goes the other direction and can produce a different set if the function is not injective on its domain.
- `Finset.subtype` — attaches a subtype proof to elements satisfying a predicate; `attachFin` specifically refines the natural-number type to `Fin n` using a strict-less-than bound, rather than a general predicate membership proof.