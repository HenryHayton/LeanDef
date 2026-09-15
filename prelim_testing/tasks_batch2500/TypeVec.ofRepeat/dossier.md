## VTask.ofRepeat

### Object

`VTask.ofRepeat` extracts the single component type from a *repeat vector*. A repeat vector `TypeVec.repeat n α` is a length-`n` type vector in which every position holds the same type `α`. Given an element at any position `i` of such a repeat vector (i.e., a value of type `(TypeVec.repeat n α) i`), `VTask.ofRepeat` recovers the underlying value of type `α`. In other words, it is the canonical projection that "forgets" the positional bookkeeping and returns the plain `α`-value.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofRepeat : {α : Type u_1} -> {n : ℕ} -> {i : Fin2 n} -> TypeVec.repeat n α i → α
<!-- PINNED-SIGNATURE:END -->


`VTask.ofRepeat : {α : Type u_1} -> {n : ℕ} -> {i : Fin2 n} -> TypeVec.repeat n α i → α`

The implicit argument `α` is the common type repeated across all positions of the vector. The implicit argument `n` is the length of the type vector. The implicit argument `i` is the position (a `Fin2 n` index) being projected. The explicit argument is the element at position `i` of `TypeVec.repeat n α`, which is definitionally equal to `α`; `VTask.ofRepeat` unwraps it to a plain value of type `α`.

### Conventions

This definition is structurally recursive on the `Fin2` index `i` and has no junk-value conventions; it is defined at every valid index and always returns a well-typed value of `α`.

### Worked examples

- Claim: For a repeat vector of length 1 at position `Fin2.fz`, `VTask.ofRepeat` extracts the value, so applying it to the element `(42 : ℕ)` packaged at position `fz` returns `42`.

- Claim: `VTask.ofRepeat` respects the `TypeVec.const` construction: `VTask.ofRepeat (TypeVec.const p α i x)` is logically equivalent to `p`, as expressed by `TypeVec.const_iff_true`.

- Claim: `VTask.ofRepeat` respects the `repeatEq` construction: `VTask.ofRepeat (repeatEq α i (prod.mk _ x y))` is logically equivalent to `x = y`, as expressed by `TypeVec.repeatEq_iff_eq`.

### Boundaries

- The function is total: it is defined for every type `α`, every length `n ≥ 1` (since `i : Fin2 n` being inhabitable forces `n ≥ 1`), and every index `i : Fin2 n`.
- Because `TypeVec.repeat n α i` is definitionally `α` at every position, the function is essentially a (recursive) identity; no information is lost or created.
- The recursion bottoms out at `Fin2.fz` and recurses through `Fin2.fs`, mirroring the inductive structure of `Fin2`.

### Not to be confused with

- `TypeVec.repeat n α` itself — this is the *type* of the repeat vector, not the projection out of it.
- `TypeVec.const` — constructs a *natural transformation into* a repeat vector from any type vector, rather than projecting out of one.
- `TypeVec.repeatEq` — produces an element of a repeat-vector of propositions encoding pointwise equality, rather than extracting a plain value from a repeat vector.