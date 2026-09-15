## Object

`VTask.drop s n` is the sequence obtained by removing the first `n` elements from the (possibly infinite, possibly partial) sequence `s`. The result is the suffix of `s` starting at position `n`. If `s` has fewer than `n` elements, the result is the empty sequence.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.drop : {α : Type u} -> (s : Stream'.Seq α) -> ℕ → Stream'.Seq α
<!-- PINNED-SIGNATURE:END -->


The first argument `s` is the sequence from which elements are to be removed. The second argument is the natural number `n` specifying how many leading elements to drop.

## Conventions

Dropping zero elements from any sequence returns that sequence unchanged. When `n` exceeds the length of a finite sequence, the result is the empty sequence (there is no error or partial failure).

## Worked examples

- Claim: Dropping 0 elements from any sequence `s` yields `s` itself.

- Claim: Dropping 1 element from a sequence is the same as taking its tail.

- Claim: Dropping 2 elements from the sequence [1, 2, 3, ...] of natural numbers gives the sequence [3, 4, 5, ...].

- Claim: Dropping any number of elements from the empty sequence yields the empty sequence.

- Claim: `VTask.drop (VTask.drop s m) n = VTask.drop s (m + n)` for any sequence `s` and natural numbers `m`, `n`.

## Boundaries

- **n = 0**: `VTask.drop s 0 = s` — the sequence is returned unchanged, by definition of the base case.
- **n = 1**: `VTask.drop s 1 = Stream'.Seq.tail s` — dropping a single element is exactly taking the tail.
- **n > length of s** (finite sequences): When `n` is greater than or equal to the number of elements in a finite sequence, the result is the empty sequence `Stream'.Seq.nil`. No error is raised.
- **Infinite sequences**: Dropping any finite number of elements from an infinite sequence yields another infinite sequence of the same cardinality.
- **Partial sequences**: For lazy/partial sequences (which may or may not terminate), dropping `n` elements peels off the first `n` positions; the productivity of the result mirrors that of the input beyond position `n`.

## Not to be confused with

- `Stream'.Seq.take`: Returns the *first* `n` elements rather than removing them — the complementary operation to `drop`.
- `Stream'.Seq.tail`: Removes only the very first element (equivalent to `VTask.drop s 1`), not an arbitrary prefix.
- `List.drop`: The analogous operation on finite lists; `VTask.drop` generalises this to possibly-infinite or partial sequences.