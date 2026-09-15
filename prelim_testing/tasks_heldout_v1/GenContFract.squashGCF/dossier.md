## Object

Given a generalised continued fraction `g = [h; (a₀, b₀), (a₁, b₁), (a₂, b₂), …]` over a division ring, `squashGCF g n` is the generalised continued fraction obtained by *squashing* (collapsing) the pair at position `n` into the immediately preceding level.

- At level `n = 0`, the first partial-quotient pair `(a₀, b₀)` is absorbed into the head: the head becomes `h + a₀/b₀`, and the sequence is otherwise left intact. If no first pair exists the fraction is returned unchanged.
- At level `n + 1`, the head `h` is preserved and the sequence is replaced by `squashSeq g.s n`, which performs the analogous absorption one step deeper inside the sequence.

The operation underpins the equivalence between the two standard evaluations (`convs` and `convs'`) of a generalised continued fraction.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.squashGCF : {K : Type u_1} -> [DivisionRing K] -> (g : GenContFract K) -> ℕ → GenContFract K
<!-- PINNED-SIGNATURE:END -->


`VTask.squashGCF : {K : Type u_1} -> [DivisionRing K] -> (g : GenContFract K) -> ℕ → GenContFract K`

The type parameter `K` is the coefficient field (any division ring). The instance argument provides division-ring operations on `K`. The argument `g` is the generalised continued fraction being squashed. The natural number argument selects the *depth* at which the squashing is performed: depth `0` acts on the head and the first sequence entry, while depth `n + 1` delegates the squashing one level deeper into the sequence.

## Conventions

If the squashing is requested at depth `0` but the sequence of partial quotients is empty (i.e., `g.s.get? 0 = none`), then `squashGCF g 0` returns `g` unchanged, acting as the identity. No junk value in the strict sense is introduced; the function is total and falls back gracefully to the identity.

## Worked examples

- Claim: For a GCF whose sequence is empty, `squashGCF g 0 = g` (the fraction is returned unchanged).

- Claim: For `g = [h; (a₀, b₀), (a₁, b₁)]`, `(squashGCF g 0).h = h + a₀ / b₀`, the head absorbs the ratio of the first pair.

- Claim: For `g = [h; (a₀, b₀), (a₁, b₁)]`, `squashGCF g 1` has head equal to `g.h` and its sequence is `squashSeq g.s 0`, leaving the head unchanged while squashing inside the sequence.

- Claim: The convergent identity `g.convs' (n + 1) = (squashGCF g n).convs' n` holds for any `g` and `n`, confirming that squashing reduces the depth of the alternative convergent by one.

## Boundaries

- **Empty sequence at depth 0**: if `g.s.get? 0 = none`, the result is exactly `g` (identity behaviour).
- **Terminated fraction**: if `g` is terminated at position `n` (i.e., `g.s.get? n = none`), then `squashGCF g n = g`.
- **Sequence entries before the squash depth are preserved**: for any `m < n`, the `m`-th entry of `(squashGCF g (n + 1)).s` equals the `m`-th entry of `g.s`; only the entry at position `n` (or its effect on the head) is modified.
- The head `g.h` is never modified when `n ≥ 1`; only `squashSeq` acts on the sequence in that case.

## Not to be confused with

- `squashSeq`: the analogous operation on the raw sequence `g.s` alone, without the head; `squashGCF` wraps this for the depth-≥1 case.
- `GenContFract.convs`: the standard (forward-recurrence) convergent function, which is related to `squashGCF` but computes a scalar value rather than returning a new fraction.
- `GenContFract.convs'`: the alternative (backward) convergent function; `squashGCF` is precisely the bridge between `convs'` at depth `n+1` and `convs'` at depth `n`, but is not itself a convergent.