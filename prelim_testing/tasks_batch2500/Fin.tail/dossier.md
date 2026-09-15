## VTask.tail

### Object

Given a dependent tuple `q` of length `n+1` — that is, a function assigning to each index `i : Fin (n+1)` a value in the type `α i` — `VTask.tail q` is the dependent tuple of length `n` consisting of the last `n` entries of `q`. Concretely, it drops the zeroth element and re-indexes: the `i`-th entry of the tail is the `(i+1)`-th entry of the original tuple.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.tail : {n : ℕ} -> {α : Fin (n + 1) → Sort u} -> (q : (i : Fin (n + 1)) → α i) -> (i : Fin n) -> α i.succ
<!-- PINNED-SIGNATURE:END -->


```
VTask.tail : {n : ℕ} -> {α : Fin (n + 1) → Sort u} -> (q : (i : Fin (n + 1)) → α i) -> (i : Fin n) -> α i.succ
```

The implicit argument `n` is the length of the resulting tail (so the original tuple has length `n+1`). The implicit argument `α` is the dependent type family indexed over `Fin (n+1)`, specifying the type of each slot. The explicit argument `q` is the `(n+1)`-tuple from which the tail is extracted. The final argument `i : Fin n` is the index into the tail; when supplied, the result is the value at position `i.succ` in `q`.

### Conventions

No special junk-value or edge conventions are declared for this definition: it is a total function on all valid inputs, with no boundary choices required.

### Worked examples

- Claim: For the constant tuple `q = fun _ => 42 : Fin 4 → ℕ`, the tail at index `⟨0, _⟩` is `42`.
  ```lean
  example : VTask.tail (fun (_ : Fin 4) => (42 : ℕ)) ⟨0, by omega⟩ = 42 := by decide
  ```

- Claim: If `q : Fin 3 → ℕ` is defined by `q i = i.val`, then `VTask.tail q ⟨1, _⟩ = 2` (since `Fin.succ ⟨1, _⟩ = ⟨2, _⟩`).
  ```lean
  example : VTask.tail (fun (i : Fin 3) => i.val) ⟨1, by omega⟩ = 2 := by decide
  ```

- Claim: Prepending a head `x` to a tuple `p` of length `n` with `Fin.cons` and then taking the tail recovers `p`; i.e., `VTask.tail (Fin.cons x p) = p`.

- Claim: Conversely, reconstructing a tuple from its head and tail gives back the original: `Fin.cons (q 0) (VTask.tail q) = q`.

### Boundaries

- When `n = 0`, the tail has length `0`, so `VTask.tail q` is a function from `Fin 0` — the empty type — and is vacuously well-defined with no values to compute.
- When `n = 1`, the original tuple has length `2` and the tail has length `1`, containing only the second element `q 1`.
- The tail does **not** include the zeroth element `q 0`; that element is the head, not part of the tail.
- Each entry `VTask.tail q i` lives in the type `α i.succ`, which is the type family `α` evaluated at the successor index, correctly reflecting the dependent structure.

### Not to be confused with

- `Fin.init`: extracts the *first* `n` entries of an `(n+1)`-tuple (the complement operation, dropping the *last* element rather than the first).
- `Matrix.vecTail`: the non-dependent analogue operating on `Fin (n+1) → α` for a fixed type `α`; coincides with `VTask.tail` when `α` is constant.
- `Fin.cons`: the constructor that *prepends* a head element to a tuple, forming an `(n+1)`-tuple from a single value and an `n`-tuple; this is the left inverse of `VTask.tail` (together with evaluation at `0`).