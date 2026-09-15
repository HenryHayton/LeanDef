## Object

Given a sequence `s` of `GenContFract.Pair K` values (each pair holding a numerator `a` and denominator `b`) and a natural number `n`, `VTask.squashSeq s n` produces a new sequence that is identical to `s` everywhere except at position `n`, where the pair `⟨aₙ, bₙ⟩` is replaced by the combined value `⟨aₙ, bₙ + aₙ₊₁ / bₙ₊₁⟩`. Intuitively, this "squashes" two consecutive continued-fraction pairs into one, folding the contribution of position `n+1` into position `n`. If position `n+1` does not exist in `s` (the sequence has already terminated there), the sequence is returned unchanged.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.squashSeq : {K : Type u_1} -> [DivisionRing K] -> (s : Stream'.Seq (GenContFract.Pair K)) -> (n : ℕ) -> Stream'.Seq (GenContFract.Pair K)
<!-- PINNED-SIGNATURE:END -->


VTask.squashSeq : {K : Type u_1} -> [DivisionRing K] -> (s : Stream'.Seq (GenContFract.Pair K)) -> (n : ℕ) -> Stream'.Seq (GenContFract.Pair K)

The implicit type parameter `K` is the coefficient field (or, more precisely, any type carrying a division-ring structure). The instance argument supplies the division-ring operations needed to form the quotient `aₙ₊₁ / bₙ₊₁`. The argument `s` is the input sequence of continued-fraction pairs `(a, b)`. The argument `n` is the index at which the squashing operation is applied.

## Conventions

When position `n+1` is absent from `s` (i.e., `s.TerminatedAt (n+1)` holds), `VTask.squashSeq s n` is defined to equal `s` itself — no modification is performed. There are no other junk-value conventions; the function is total and well-defined for all inputs.

## Worked examples

- Claim: For a sequence `s` with `s.get? n = some ⟨aₙ, bₙ⟩` and `s.get? (n+1) = some ⟨aₙ₊₁, bₙ₊₁⟩`, the element at position `n` in `VTask.squashSeq s n` equals `⟨aₙ, bₙ + aₙ₊₁ / bₙ₊₁⟩`. (This is `squashSeq_nth_of_not_terminated`.)

- Claim: For any `m < n`, the element at position `m` in `VTask.squashSeq s n` equals the element at position `m` in `s` — positions strictly before the squash index are unchanged. (This is `squashSeq_nth_of_lt`.)

- Claim: If `s.TerminatedAt (n + 1)`, then `VTask.squashSeq s n = s`. (This is `squashSeq_eq_self_of_terminated`.)

- Claim: The tail of `VTask.squashSeq s (n + 1)` equals `VTask.squashSeq s.tail n` — squashing commutes with taking tails in the sense that shifting the squash index by 1 corresponds to moving to the tail sequence. (This is `squashSeq_succ_n_tail_eq_squashSeq_tail_n`.)

## Boundaries

- If both `s.get? n` and `s.get? (n+1)` are `some`, the squash is performed and only position `n` is modified; all other positions retain their original values.
- If `s.get? n` is `none` (sequence has already terminated at or before `n`), the sequence is returned unchanged.
- If `s.get? n` is `some` but `s.get? (n+1)` is `none` (sequence terminates exactly at `n+1`), the sequence is returned unchanged.
- For positions `m > n`, the elements of `VTask.squashSeq s n` are the same as those of `s` (no change beyond position `n`).
- The squashed value uses division in `K`; if `bₙ₊₁ = 0` in a field, the division is the field's own definition of division by zero (typically zero in Mathlib's `DivisionRing`), so the result is still well-typed.

## Not to be confused with

- `GenContFract.squashGCF`: operates on an entire generalized continued fraction structure (including its leading term), not just on a raw sequence of pairs.
- `Stream'.Seq.zipWith`: a general sequence combinator used internally; it does not encode the continued-fraction squashing logic.
- Taking the tail of a sequence (`Stream'.Seq.tail`): shifts all indices by one, whereas `VTask.squashSeq` modifies only a specific index.