## VTask.cons

### Object
`VTask.cons a s` is a new infinite stream obtained by inserting the element `a` at position 0, with every subsequent position `n` (for `n ≥ 1`) occupied by what was at position `n − 1` in the original stream `s`. Informally, it is the stream `a, s(0), s(1), s(2), …`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cons : {α : Type u} -> (a : α) -> (s : Stream' α) -> Stream' α
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `α` is the element type shared by the new element and the stream. The explicit argument `a` is the element to be prepended — it becomes the new head of the resulting stream. The argument `s` is the existing infinite stream that is shifted one position to the right to form the tail.

### Conventions

The resulting object is a total infinite stream (a function `ℕ → α`), so there are no junk values or undefined positions.

### Worked examples

- Claim: The first element (index 0) of `VTask.cons a s` is `a`.
  ```lean
  example (α : Type*) (a : α) (s : Stream' α) : VTask.cons a s 0 = a := rfl
  ```

- Claim: The element at index `n + 1` of `VTask.cons a s` is `s n`.
  ```lean
  example (α : Type*) (a : α) (s : Stream' α) (n : ℕ) : VTask.cons a s (n + 1) = s n := rfl
  ```

- Claim: Prepending to the constant stream of `0 : ℕ` at index 3 gives `0`.
  ```lean
  example : VTask.cons (1 : ℕ) (fun _ => 0) 3 = 0 := by decide
  ```

- Claim: Prepending `5` to the stream of natural numbers `(fun n => n)` gives the stream `5, 0, 1, 2, …`; in particular, `VTask.cons 5 id 0 = 5` and `VTask.cons 5 id 3 = 2`.
  ```lean
  example : VTask.cons 5 id 0 = 5 := by decide
  ```
  ```lean
  example : VTask.cons 5 id 3 = 2 := by decide
  ```

### Boundaries

- At index `0`, the result is always the prepended element `a`, regardless of what `s` contains.
- At every positive index `n + 1`, the result is exactly `s n`; the original stream is shifted by exactly one position.
- The operation is total: it is defined for every natural-number index without restriction on `α`, `a`, or `s`.
- Prepending to a stream that is already of the form `VTask.cons b t` gives a stream whose index-0 value is `a`, index-1 value is `b`, and index `n + 2` value is `t (n)`.

### Not to be confused with

- `Stream'.tail` — the operation that *removes* the head of a stream, which is the left inverse of `VTask.cons` when applied to the tail.
- `List.cons` — prepending to a *finite* list; `VTask.cons` prepends to an infinite stream and the resulting object is still an infinite stream.
- `Stream'.get` (or plain indexing) — accessing a single element of a stream at a given position, rather than constructing a new stream.