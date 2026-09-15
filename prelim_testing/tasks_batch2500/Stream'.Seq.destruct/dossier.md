## Object

`VTask.destruct` is the **destructor** for a possibly-infinite, possibly-partial sequence (`Stream'.Seq α`). Given a sequence, it peeks at the first element:
- If the sequence is empty (nil), it returns `none`.
- If the sequence has a head `a`, it returns `some (a, t)` where `t` is the tail of the sequence.

The result type `Stream'.Seq1 α` is a pair `(α × Stream'.Seq α)`, i.e., a non-empty sequence represented as a head element together with a remaining sequence. This function is the standard way to case-split on a sequence without unwrapping its internal representation directly.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.destruct : {α : Type u} -> (s : Stream'.Seq α) -> Option (Stream'.Seq1 α)
<!-- PINNED-SIGNATURE:END -->


`VTask.destruct : {α : Type u} -> (s : Stream'.Seq α) -> Option (Stream'.Seq1 α)`

The implicit argument `α` is the type of elements in the sequence. The explicit argument `s` is the sequence being destructed. The return value is an `Option`: `none` when `s` is the empty (nil) sequence, or `some (a, t)` when `a` is the first element of `s` and `t` is its tail.

## Conventions

When the sequence is nil (the empty sequence), `destruct` returns `none`. There is no junk value in the usual sense — `none` is the fully canonical signal that the sequence is empty, and `some (a, t)` is the fully canonical signal that it is non-empty with head `a` and tail `t`.

## Worked examples

- Claim: `VTask.destruct Stream'.Seq.nil = none` — destructing the empty sequence yields `none`.

- Claim: For any element `a` and sequence `t`, `VTask.destruct (Stream'.Seq.cons a t) = some (a, t)` — destructing a cons-cell recovers the head and tail.

- Claim: If `VTask.destruct s = none`, then `s` is equivalent to `Stream'.Seq.nil`.

- Claim: If `VTask.destruct s = some (a, t)`, then `Stream'.Seq.get? s 0 = some a` and the tail of `s` equals `t`.

## Boundaries

- **Nil input**: `VTask.destruct Stream'.Seq.nil = none`. This is the defining base case.
- **Cons input**: `VTask.destruct (Stream'.Seq.cons a t) = some (a, t)` for any `a : α` and `t : Stream'.Seq α`.
- **Partial/lazy sequences**: Because `Stream'.Seq` is a coinductive/lazy type, the function inspects only the very first position (`get? s 0`); the rest of the sequence is returned unevaluated as the tail component of the result.
- **Round-tripping**: Applying `destruct` to a sequence and then using the result to reconstruct via `cons` (in the `some` branch) yields a sequence definitionally equal to the original.

## Not to be confused with

- `Stream'.Seq.head`: Returns `Option α` — just the first element, discarding the tail entirely, rather than returning a `Seq1` pair.
- `Stream'.Seq.tail`: Returns `Stream'.Seq α` — just the tail of the sequence, discarding the head, rather than pairing both.
- `Stream'.Seq1` (the type): The non-empty-sequence type `α × Stream'.Seq α` that appears in the codomain; `destruct` *produces* a value of this type (wrapped in `Option`), it is not this type itself.
