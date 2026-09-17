## VTask.maximum_of_length_pos

### Object

Given a non-empty list `l` over a linearly ordered type, `VTask.maximum_of_length_pos h` is the greatest element of `l` — an actual element of `l` (of type `α`) that is at least as large as every other element of the list.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.maximum_of_length_pos : {α : Type u_1} -> [LinearOrder α] -> {l : List α} -> (h : 0 < l.length) -> α
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `α` is the element type, which must carry a linear order. The implicit argument `l` is the list whose maximum is sought. The explicit argument `h` is a proof that the list is non-empty (its length is positive); this proof is the formal witness that the maximum is well-defined.

### Conventions

The proof `h` of `0 < l.length` is required only to guarantee well-definedness; the actual value returned depends only on the contents of `l`, not on the specific proof term supplied.

### Worked examples

- Claim: `VTask.maximum_of_length_pos (l := [3, 1, 4, 1, 5, 9, 2, 6]) (by decide) = 9`
  ```lean
  example : VTask.maximum_of_length_pos (l := [3, 1, 4, 1, 5, 9, 2, 6]) (by decide) = 9 := by decide
  ```

- Claim: `VTask.maximum_of_length_pos (l := [7]) (by decide) = 7`
  ```lean
  example : VTask.maximum_of_length_pos (l := [7]) (by decide) = 7 := by decide
  ```

- Claim: For any non-empty list `l : List α` with linear order, `VTask.maximum_of_length_pos h ∈ l`.

- Claim: For any element `a ∈ l` where `l` is non-empty, `a ≤ VTask.maximum_of_length_pos h`.

### Boundaries

- The function is only defined when `l` is non-empty (i.e., `0 < l.length`). There is no junk value for the empty list; the caller must supply the positivity proof.
- For a singleton list `[x]`, the result is exactly `x`.
- If the list contains duplicate copies of its maximum value, the result is still that maximum value; it is an element of the list in the usual membership sense.
- The result is provably a member of `l` (not merely a value that equals some member — it is literally contained in `l`).

### Not to be confused with

- `List.maximum` — returns a value of type `WithBot α`, which equals `⊥` on the empty list; `VTask.maximum_of_length_pos` unwraps this to a plain `α` using the non-emptiness proof.
- `List.maximum_of_ne_nil` — a similar extractor that takes a proof that the list is not `[]` (i.e., `l ≠ []`) rather than a positivity-of-length proof; the two are interchangeable in practice.
- `List.argmax` — finds the index of the maximum element rather than the maximum element's value itself.
