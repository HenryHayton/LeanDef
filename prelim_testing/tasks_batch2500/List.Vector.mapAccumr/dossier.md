## VTask.mapAccumr

### Object

`VTask.mapAccumr f v s` is a right-to-left accumulating map over a fixed-length vector. Starting from an initial accumulator value `s`, it processes the elements of the vector `v` from right to left, feeding each element and the current accumulator into the step function `f`. At each step `f a c` returns a pair: the updated accumulator and the output element. The final result is a pair consisting of the final accumulator (after all elements have been processed) and a new vector of the same length whose entries are the output elements produced at each step.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mapAccumr : {α : Type u_1} -> {β : Type u_2} -> {σ : Type u_3} -> {n : ℕ} -> (f : α → σ → σ × β) -> List.Vector α n → σ → σ × List.Vector β n
<!-- PINNED-SIGNATURE:END -->


`f` is the step function: given an input element of type `α` and the current accumulator of type `σ`, it returns a pair of the new accumulator and an output element of type `β`. The second argument is the input vector of length `n` over type `α`. The third argument `σ` is the initial accumulator value from which traversal begins (at the rightmost element).

### Conventions

No special junk-value or edge-case conventions are declared beyond the natural behavior of the underlying list operation: when the input vector is empty (`n = 0`), the step function `f` is never called, the accumulator is returned unchanged, and the output vector is the empty vector of length 0.

### Worked examples

- Claim: Applying `VTask.mapAccumr` to the empty vector with any step function and initial accumulator `s` returns `(s, #v[])` — the accumulator is unchanged and the result vector is empty.

- Claim: For the vector `#v[1, 2, 3]` with step function `f a c := (a + c, a * c)` and initial accumulator `0`, processing right-to-left gives: step on 3 with acc 0 → acc becomes 3, output 0; step on 2 with acc 3 → acc becomes 5, output 6; step on 1 with acc 5 → acc becomes 6, output 5. So the result is `(6, #v[5, 6, 0])`.

- Claim: `VTask.mapAccumr` preserves the length of the vector: if the input vector has length `n`, the output vector also has length `n`.

- Claim: The first component of `VTask.mapAccumr f v s` (the final accumulator) equals the first component of running the corresponding list accumulating map on the underlying list of `v` with the same `f` and `s`.

### Boundaries

- **Empty vector (`n = 0`)**: `f` is never invoked. The result is `(s, empty_vector)` where `s` is the initial accumulator, unchanged.
- **Single-element vector**: `f` is called exactly once on the sole element and the initial accumulator; the returned accumulator and single-element output vector form the result.
- **Direction**: Traversal is strictly right-to-left; the rightmost element of the input vector is processed first (sees the original accumulator `s`), and the leftmost element is processed last (produces the final accumulator in the output pair).
- **Length invariant**: The output vector always has the same length as the input vector; this is enforced by the type.

### Not to be confused with

- **`List.mapAccumr`**: The list-level analogue operating on `List α` instead of `List.Vector α n`; `VTask.mapAccumr` wraps this operation while enforcing the length invariant at the type level.
- **`Vector.mapAccumL` / `VTask.mapAccumL`**: The left-to-right variant, which processes elements from left to right, so the leftmost element sees the initial accumulator first; here the rightmost does.
- **`Vector.map`**: A plain map over vectors with no accumulator threading; it does not carry state between elements.