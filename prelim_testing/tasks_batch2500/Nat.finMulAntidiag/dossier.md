## VTask.finMulAntidiag

### Object

`VTask.finMulAntidiag d n` is the finite set of all functions `f : Fin d → ℕ` (i.e., all ordered `d`-tuples of natural numbers) whose product `f 0 * f 1 * ⋯ * f (d-1)` equals `n`. When `n = 0` the set is defined to be empty, reflecting the convention that no tuple of natural numbers with a zero product is tracked.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.finMulAntidiag : (d n : ℕ) -> Finset (Fin d → ℕ)
<!-- PINNED-SIGNATURE:END -->


`(d n : ℕ) -> Finset (Fin d → ℕ)`

The first argument `d` is the length (arity) of the tuples: elements of the resulting `Finset` are functions from `{0, 1, …, d-1}` to `ℕ`. The second argument `n` is the target product: we collect exactly those `d`-tuples whose componentwise product equals `n`.

### Conventions

When `n = 0` the result is defined to be the empty set `∅`, even though there do exist `d`-tuples of natural numbers (involving zero entries) whose product is 0. This is a deliberate junk-value choice: every element of a tuple in `VTask.finMulAntidiag d n` is required to be nonzero, so the case `n = 0` is excluded by fiat rather than by accident.

When `d = 0` and `n ≠ 1`, the result is also `∅`, because the empty product equals 1, not any other natural number.

When `d = 0` and `n = 1`, the result is the singleton containing the unique empty function.

### Worked examples

- Claim: `VTask.finMulAntidiag 0 0 = ∅` (zero target with zero arity is empty by the n = 0 convention).

- Claim: `VTask.finMulAntidiag 1 6` contains exactly the functions `![6]`, i.e., the singleton whose only tuple is `(6)`, since the only 1-tuple with product 6 is `(6)` itself.

- Claim: `VTask.finMulAntidiag 2 6` contains the functions corresponding to `(1,6), (2,3), (3,2), (6,1)` — all ordered pairs of positive naturals whose product is 6.

- Claim: `VTask.finMulAntidiag d 1 = {fun _ => 1}` for any `d` — the only `d`-tuple of positive natural numbers with product 1 is the all-ones tuple.

- Claim: For any `f ∈ VTask.finMulAntidiag 3 n`, we have `f 0 * f 1 * f 2 = n`.

### Boundaries

- **`n = 0`**: the set is empty by definition, regardless of `d`. This is a deliberate convention: no tuple of positive integers can have product 0.
- **`d = 0, n = 1`**: the set is a singleton containing the unique function from the empty type, because the empty product is 1.
- **`d = 0, n ≠ 1` (and `n ≠ 0`)**: the set is empty, because the unique 0-tuple has product 1.
- **`n` squarefree**: the cardinality of `VTask.finMulAntidiag d n` equals `d ^ ω(n)`, where `ω(n)` is the number of distinct prime factors of `n`.
- Every entry `f i` of any tuple `f` in `VTask.finMulAntidiag d n` divides `n` and is nonzero.

### Not to be confused with

- `Nat.divisorsAntidiagonal n` — the `Finset` of *pairs* `(a, b)` with `a * b = n`; this is the specialization to `d = 2` (up to repackaging), not the general `d`-ary version.
- `Nat.finAddAntidiag` / `Finset.finAntidiagonal` — the additive analogue collecting `d`-tuples of naturals whose *sum* is `n`, not their product.
- `Finset.piFinset` — a product of finsets indexed by `Fin d`, which provides a universe for tuples but does not impose any product constraint.