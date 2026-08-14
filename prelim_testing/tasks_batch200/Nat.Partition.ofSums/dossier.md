## Object

`VTask.ofSums n l hl` constructs a partition of the natural number `n` from a multiset `l` of natural numbers whose entries sum to `n`. The partition is obtained by discarding all zero entries from `l`; the remaining positive entries, kept as a multiset, form the parts of the partition.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofSums : (n : ℕ) -> (l : Multiset ℕ) -> (hl : l.sum = n) -> n.Partition
<!-- PINNED-SIGNATURE:END -->


`VTask.ofSums : (n : ℕ) -> (l : Multiset ℕ) -> (hl : l.sum = n) -> n.Partition`

The first argument `n` is the natural number being partitioned. The second argument `l` is an arbitrary multiset of natural numbers whose elements are the candidate parts (possibly including zeros). The third argument `hl` is a proof that the elements of `l` sum to exactly `n`, establishing that `l` is a valid "summing witness" for `n`.

## Conventions

Zero entries in the input multiset `l` are silently dropped: a zero appearing in `l` contributes neither to the parts multiset of the resulting partition nor to the count of any value in it. Non-zero entries are preserved exactly: for any positive integer `i`, the number of times `i` appears in the resulting partition's parts equals the number of times `i` appears in `l`.

## Worked examples

- Claim: Applying `VTask.ofSums` to the multiset `{3, 0, 2, 0, 1}` (which sums to 6) yields a partition of 6 whose parts multiset is `{3, 2, 1}` (zeros removed).

- Claim: For the multiset `{0, 0, 0}` summing to 0, `VTask.ofSums 0 {0, 0, 0} rfl` gives the empty partition of 0, since all entries are zero and are filtered out.

- Claim: The count of 0 in `(VTask.ofSums n l hl).parts` is always 0, regardless of how many zeros appear in `l`.

- Claim: For a multiset `l` with `l.sum = n` and a nonzero `i`, `(VTask.ofSums n l hl).parts.count i = l.count i`.

## Boundaries

- If `l` is the empty multiset and `n = 0`, the result is the unique empty partition of 0 (with an empty parts multiset).
- If `l` consists entirely of zeros, the result is the empty partition of 0 (since all parts are filtered out and the sum of the empty multiset is 0, forcing `n = 0`).
- The multiset `l` may contain repeated values; multiplicity is preserved in the output for all nonzero values.
- There is no restriction on the size or content of `l` beyond the summation hypothesis `hl`; in particular, `l` need not be sorted or duplicate-free.

## Not to be confused with

- `Nat.Partition` (the structure itself): that is the *type* of the output, not the constructor; `VTask.ofSums` is one way to build a term of that type.
- `Multiset.filter`: the primitive operation used internally, which acts on any predicate; `VTask.ofSums` specifically filters for nonzero entries and additionally bundles the summation proof.
- A partition constructor that accepts only already-positive parts: `VTask.ofSums` accepts zeros in `l` and removes them automatically, so the caller need not pre-filter.