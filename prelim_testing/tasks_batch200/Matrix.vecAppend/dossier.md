## VTask.vecAppend

### Object

`VTask.vecAppend` produces a single vector (function from a finite index type to values) of length `o` by concatenating two vectors: a first vector `u` of length `m` (occupying indices `0` through `m-1`) followed by a second vector `v` of length `n` (occupying indices `m` through `m+n-1`). The output length `o` is required to equal `m + n`, but this equality is supplied explicitly as a proof argument rather than being forced definitionally, giving the caller fine-grained control over how Lean's kernel sees the length.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.vecAppend : {m n : ℕ} -> {α : Type u_1} -> {o : ℕ} -> (ho : o = m + n) -> (u : Fin m → α) -> (v : Fin n → α) -> Fin o → α
<!-- PINNED-SIGNATURE:END -->


The implicit arguments `m` and `n` are the lengths of the two input vectors; `α` is the element type; `o` is the stated length of the output vector. The explicit argument `ho` is a proof that `o` equals `m + n`, which is used to reindex the output domain. The argument `u` is the first (left) vector, a function `Fin m → α`. The argument `v` is the second (right) vector, a function `Fin n → α`. The result is a function `Fin o → α`.

### Conventions

When the index `i : Fin o` satisfies `(i : ℕ) < m`, the output is `u` evaluated at that index cast into `Fin m`; otherwise, the output is `v` evaluated at the index shifted by `m` (i.e., `(i : ℕ) - m`) cast into `Fin n`. The proof `ho` is used solely for reindexing and does not affect the values returned; any two proofs `ho₁ ho₂ : o = m + n` yield extensionally equal functions.

### Worked examples

- Claim: For `u = ![10, 20]` and `v = ![30, 40]`, `VTask.vecAppend rfl u v 0 = 10` (first element comes from `u`).
- Claim: For `u = ![10, 20]` and `v = ![30, 40]`, `VTask.vecAppend rfl u v 2 = 30` (index 2 falls in `v`, shifted to position 0 within `v`).
- Claim: Appending an empty vector on the right is the identity: `VTask.vecAppend rfl v ![] = v` for any `v : Fin n → α`.
- Claim: Appending an empty vector on the left recovers the original vector (up to the proof of `n = 0 + n`): `VTask.vecAppend n.zero_add.symm ![] v = v`.

### Boundaries

- When `m = 0`, all indices map into `v`; the proof `ho : o = 0 + n` is needed and `n.zero_add.symm` is the canonical choice. The result is extensionally equal to `v` after the trivial reindexing.
- When `n = 0`, all indices map into `u`; the result is extensionally equal to `u`.
- At the boundary index `⟨m, …⟩` (the first index not in `u`'s range), the value is `v 0`.
- The argument `ho` may be any proof of `o = m + n`, not just `rfl`; using `rfl` is valid when `o` is literally `m + n` in the context, and this is the common case in normal-form expressions like `![]`-notation.
- The `0 : Fin o` literal is valid (unlike for `Fin.append` directly) precisely because `o` need not equal `m + n` definitionally, enabling `vecAppend ho u v 0` to elaborate when `m + n` has no `Zero` instance.

### Not to be confused with

- `Fin.append`: the direct predecessor, which requires the output type to be definitionally `Fin (m + n)` and does not accept a heterogeneous length proof `ho`; `VTask.vecAppend ho u v` is `Fin.append u v` composed with a cast by `ho`.
- `Matrix.vecCons`: prepends a single element to a vector, i.e., appends a length-1 vector on the left; this is a special case of appending but with dedicated notation `vecCons x u`.
- `List.append` / `Fin.append` on `Vector`: operates on list-based or structure-based vector types rather than on bare functions `Fin n → α`.