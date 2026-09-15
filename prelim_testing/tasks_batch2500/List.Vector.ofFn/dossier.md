## VTask.ofFn

### Object

`VTask.ofFn f` constructs a vector of length `n` whose `i`-th entry is `f i`, for every index `i : Fin n`. It is the canonical way to build a length-indexed vector from a function on index positions, and is the inverse of extracting a vector's indexing function via `get`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofFn : {α : Type u_1} -> {n : ℕ} -> (Fin n → α) → List.Vector α n
<!-- PINNED-SIGNATURE:END -->


The implicit argument `α` is the element type of the resulting vector. The implicit argument `n` is the length of the resulting vector and also the size of the finite index type. The explicit argument is a function from `Fin n` to `α`, specifying the value at each position.

### Conventions

There are no junk-value conventions to declare: the function is total and well-defined for every possible length `n` (including `n = 0`, which produces the empty vector) and every function `f : Fin n → α`.

### Worked examples

- Claim: `VTask.ofFn (fun i : Fin 3 => (i : ℕ) * 2)` is a vector of length 3 with entries `[0, 2, 4]`.
  Specifically, its underlying list equals `[0, 2, 4]`.

- Claim: For `n = 0`, `VTask.ofFn (fun i : Fin 0 => (42 : ℕ))` is the empty vector of length 0.

- Claim: Applying `VTask.ofFn` to the `get` function of any vector `v : List.Vector α n` recovers `v` exactly, i.e., `VTask.ofFn (List.Vector.get v) = v`.

- Claim: The `i`-th element of `VTask.ofFn f` is `f i`, i.e., `List.Vector.get (VTask.ofFn f) i = f i` for all `i : Fin n`.

- Claim: The underlying list of `VTask.ofFn f` equals `List.ofFn f`, connecting the vector constructor to the list-level analogue.

### Boundaries

- **Empty case (`n = 0`):** `VTask.ofFn f` is the unique empty vector of type `List.Vector α 0`, regardless of `f` (since there are no elements of `Fin 0`, `f` is vacuous).
- **Singleton case (`n = 1`):** Produces a length-1 vector whose sole entry is `f ⟨0, Nat.lt.base 0⟩`.
- **General `n`:** The head of `VTask.ofFn f` is `f 0`, and the tail is `VTask.ofFn (fun i => f i.succ)`.
- The function is defined for all types `α` including `Prop`, and for all natural numbers `n`; there are no domain restrictions.

### Not to be confused with

- `List.ofFn`: The list-level analogue that produces a plain `List α` (not length-indexed) from a function on `Fin n`; `VTask.ofFn` wraps this in a `List.Vector` carrying the length in the type.
- `List.Vector.get`: The inverse operation — extracts the indexing function from an existing vector; `VTask.ofFn (List.Vector.get v) = v` is the roundtrip identity.
- `List.Vector.mOfFn`: A monadic generalisation that lifts a function `Fin n → m α` into `m (List.Vector α n)`; `VTask.ofFn` is the pure (non-monadic) special case.
