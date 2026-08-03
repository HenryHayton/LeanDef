## VTask.bitCasesOn

### Object

`VTask.bitCasesOn` is a dependent eliminator (case-analysis principle) for natural numbers based on their binary representation. Every natural number `n` can be uniquely written as `Nat.bit b m` for some boolean `b` (the least significant bit) and natural number `m` (the remaining bits, i.e., `n` right-shifted by one). Given a type family `motive` over `ℕ`, if one can construct an element of `motive (Nat.bit b m)` for every choice of bit `b : Bool` and tail `m : ℕ`, then one obtains an element of `motive n` for any `n : ℕ`. It is the binary-representation analogue of `Nat.casesOn` (which decomposes into `0` and `n+1`).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.bitCasesOn : {motive : ℕ → Sort u} -> (n : ℕ) -> (bit : (b : Bool) → (n : ℕ) → motive (Nat.bit b n)) -> motive n
<!-- PINNED-SIGNATURE:END -->


`{motive : ℕ → Sort u} -> (n : ℕ) -> (bit : (b : Bool) → (n : ℕ) → motive (Nat.bit b n)) -> motive n`

The implicit argument `motive` is the type family indexed by natural numbers whose value at `n` is being constructed. The first explicit argument `n` is the natural number being eliminated. The second explicit argument `bit` is the constructor case: a function that, given a boolean `b` and a natural number `m`, produces an element of `motive (Nat.bit b m)`; it covers every possible binary decomposition.

### Conventions

The eliminator computes by decomposing `n` into its least-significant bit (the boolean `b = n.testBit 0`) and its right-shift by one (the natural number `m = n >>> 1`), then applying the `bit` argument to `b` and `m`. In the non-dependent (motive-constant) case this is definitionally equal to simply applying `bit` to these two components, with no observable transport overhead.

### Worked examples

- Claim: Applying `VTask.bitCasesOn` to `6` with the case function `H b m ↦ (b, m)` yields `(false, 3)`, because `6 = Nat.bit false 3` (i.e., 6 = 2 × 3).

- Claim: Applying `VTask.bitCasesOn` to `7` with the case function `H b m ↦ (b, m)` yields `(true, 3)`, because `7 = Nat.bit true 3` (i.e., 7 = 2 × 3 + 1).

- Claim: `VTask.bitCasesOn (Nat.bit b n) h = h b n` for all `b : Bool` and `n : ℕ` — i.e., when the input is already in `Nat.bit` form, the eliminator reduces to applying `h` directly to `b` and `n`.

- Claim: `VTask.bitCasesOn (2 * n) H = H false n` for any `n : ℕ` — even numbers correspond to `Nat.bit false n`.

- Claim: `VTask.bitCasesOn (2 * n + 1) H = H true n` for any `n : ℕ` — odd numbers correspond to `Nat.bit true n`.

### Boundaries

- At `n = 0`: the decomposition gives `b = false` and `m = 0`, so `0 = Nat.bit false 0`; the `bit` function is called with `(false, 0)`.
- At `n = 1`: the decomposition gives `b = true` and `m = 0`, so `1 = Nat.bit true 0`; the `bit` function is called with `(true, 0)`.
- The function is total: it is defined for every `n : ℕ` with no preconditions.
- The mapping from `bit`-case functions to eliminators is injective: two case functions are equal if and only if the resulting eliminators (as functions of `n`) are equal.

### Not to be confused with

- `Nat.binaryRec`: a full binary recursion principle that recurses structurally on the binary representation, rather than just performing a single case split.
- `Nat.bit`: the constructor `Nat.bit : Bool → ℕ → ℕ` that builds a natural number from a bit and a tail; `VTask.bitCasesOn` is the corresponding eliminator.
- `Nat.casesOn`: the standard case split of `ℕ` into `0` and successors, which has no connection to the binary representation.