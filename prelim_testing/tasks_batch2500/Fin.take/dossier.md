## Object

`VTask.take` restricts a dependently-typed `n`-tuple (i.e., a function from `Fin n` to a family of types) to its first `m` entries, producing an `m`-tuple.  More precisely, if `v` assigns to each index `i : Fin n` a value of type `α i`, then `VTask.take m h v` is the `m`-tuple whose `i`-th entry is `v (Fin.castLE h i)` — the same value that `v` assigns to the canonical embedding of the smaller index `i : Fin m` into `Fin n`.  This is the dependent-type analogue of taking the first `m` elements of a list or vector.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.take : {n : ℕ} -> {α : Fin n → Sort u_1} -> (m : ℕ) -> (h : m ≤ n) -> (v : (i : Fin n) → α i) -> (i : Fin m) -> α (Fin.castLE h i)
<!-- PINNED-SIGNATURE:END -->


`{n : ℕ} -> {α : Fin n → Sort u_1} -> (m : ℕ) -> (h : m ≤ n) -> (v : (i : Fin n) → α i) -> (i : Fin m) -> α (Fin.castLE h i)`

The implicit argument `n` is the length of the source tuple.  The implicit argument `α` is the dependent type family indexed over `Fin n` that assigns a type to each position of the source tuple.  The explicit argument `m` is the number of elements to retain from the front.  The proof `h` witnesses that `m` does not exceed `n`, ensuring the first `m` positions of the source are well-defined.  The argument `v` is the source `n`-tuple, i.e., a dependent function assigning a value of type `α i` to each `i : Fin n`.  The final argument `i : Fin m` is the index into the resulting `m`-tuple; the return type is `α (Fin.castLE h i)`, the type that the source family assigns to the embedded index.

## Conventions

There are no junk-value conventions to declare: the function is total, the bound `h : m ≤ n` is an explicit proof obligation supplied by the caller, and every well-typed call produces a meaningful dependent tuple.

## Worked examples

- Claim: Taking all `n` elements of an `n`-tuple with `m = n` returns the original tuple — `VTask.take n (le_refl n) v = v` for any `v : (i : Fin n) → α i`.

- Claim: Taking zero elements of any `n`-tuple yields the empty tuple — `VTask.take 0 n.zero_le v = fun i => Fin.elim0 i`.

- Claim: Taking `m` elements and then taking a further `k ≤ m` elements is the same as taking `k` elements directly — `VTask.take k hk (VTask.take m hm v) = VTask.take k (Nat.le_trans hk hm) v`.

- Claim: For a constant (non-dependent) tuple `v : Fin 5 → ℕ` defined by `v i = i.val`, the result of `VTask.take 3 (by norm_num) v` at index `⟨1, by norm_num⟩` is `1`.

## Boundaries

- When `m = 0`, the result is the empty dependent tuple (a function from `Fin 0`, which is uninhabited), definitionally equal to `fun i => Fin.elim0 i`.
- When `m = n`, `Fin.castLE` is the identity on values and the result is definitionally equal to the original tuple `v`.
- The proof `h : m ≤ n` is required; without it the embedding `Fin.castLE h` is not available, so the call does not type-check.
- When `v` is built from `Fin.append u w`, taking the first `m ≤ n` elements recovers `VTask.take m h u`, stripping the right part entirely.
- When `v` is built from `Fin.repeat n a`, taking the first `m * n'` elements (with `m ≤ n`) recovers `Fin.repeat m a`.

## Not to be confused with

- `Fin.init` — drops only the *last* element of an `(n+1)`-tuple, whereas `VTask.take` drops an arbitrary suffix of any length.
- `List.take` — operates on `List α` (a homogeneous, runtime-length list) rather than on the dependently-typed `Fin n → α` tuple type.
- `Fin.castLE` — this is the index-embedding function used *inside* `VTask.take` to coerce smaller indices; it is not itself a tuple-truncation operation.