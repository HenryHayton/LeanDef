## Object

`VTask.zipWith f s₁ s₂` is the pointwise combination of two (possibly finite or infinite) sequences `s₁` and `s₂` using a binary function `f`. The result is a sequence whose `n`-th element is `f a b` when both `s₁` and `s₂ ` have an `n`-th element `a` and `b` respectively, and is absent (the sequence has terminated) as soon as either input sequence has terminated at or before position `n`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.zipWith : {α : Type u} -> {β : Type v} -> {γ : Type w} -> (f : α → β → γ) -> (s₁ : Stream'.Seq α) -> (s₂ : Stream'.Seq β) -> Stream'.Seq γ
<!-- PINNED-SIGNATURE:END -->


VTask.zipWith : {α : Type u} -> {β : Type v} -> {γ : Type w} -> (f : α → β → γ) -> (s₁ : Stream'.Seq α) -> (s₂ : Stream'.Seq β) -> Stream'.Seq γ

The implicit type parameters `α`, `β`, and `γ` are the element types of the first input sequence, second input sequence, and output sequence respectively. The argument `f` is the binary combining function applied elementwise. The argument `s₁` is the first input sequence and `s₂` is the second input sequence.

## Conventions

There are no junk-value or edge conventions beyond the totality of the definition: the output sequence is always well-formed. When one or both input sequences are empty (or have terminated by position `n`), the output sequence is also terminated from that position onward, because `Option.map₂` returns `none` whenever either argument is `none`.

## Worked examples

- Claim: The 0th element of `VTask.zipWith (· + ·) [1, 2, 3] [10, 20, 30]` (viewed as sequences) is `some 11`.

- Claim: The 2nd element of `VTask.zipWith (· * ·) (Stream'.Seq.ofList [3, 4]) (Stream'.Seq.ofList [5, 6])` is `none`, because both input sequences have terminated by index 2.
  ```lean
  example : (VTask.zipWith (· * ·) (Stream'.Seq.ofList [3, 4]) (Stream'.Seq.ofList [5, 6])).get? 2 = none := by
    decide
  ```

- Claim: The 1st element of `VTask.zipWith (· + ·) (Stream'.Seq.ofList [1, 2]) (Stream'.Seq.ofList [10, 20])` is `some 22`.
  ```lean
  example : (VTask.zipWith (· + ·) (Stream'.Seq.ofList [1, 2]) (Stream'.Seq.ofList [10, 20])).get? 1 = some 22 := by
    decide
  ```

- Claim: If `s₁` terminates at index 0 (i.e., its 0th element is `none`) and `s₂` is arbitrary, then the result sequence's 0th element is `none`.

## Boundaries

- If either `s₁` or `s₂` is the empty sequence (no elements at all), then `VTask.zipWith f s₁ s₂` is also the empty sequence: every position yields `none`.
- If `s₁` has length `m` and `s₂` has length `n`, the result has length `min m n`.
- For infinite sequences (streams), the result is again infinite and coincides with the ordinary pointwise map at every index.
- The function `f` is applied only at positions where both input sequences have a value; it is never called with undefined arguments.

## Not to be confused with

- `Stream'.Seq.zip`: pairs elements into a product type `α × β` rather than applying an arbitrary combining function; equivalent to `VTask.zipWith Prod.mk`.
- `Stream'.Seq.map`: applies a *unary* function to a single sequence, whereas `VTask.zipWith` combines *two* sequences with a *binary* function.
- `List.zipWith`: the analogous operation on finite lists, which always yields a finite `List` rather than a `Stream'.Seq` and does not carry a termination proof.