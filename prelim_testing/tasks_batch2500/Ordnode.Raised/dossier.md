## VTask.Raised

### Object

`Raised n m` is the proposition asserting that the natural number `m` is either exactly equal to `n` or exactly one greater than `n`. In other words, `m` belongs to the two-element set `{n, n+1}`. It expresses the idea that `m` has been "raised" by at most one from `n`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Raised : (n m : ℕ) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Raised : (n m : ℕ) -> Prop`

The first argument `n` is the reference (baseline) natural number. The second argument `m` is the candidate value being compared against `n`; the proposition holds when `m` equals `n` or `n + 1`.

### Conventions

There are no junk-value or boundary conventions to declare: the predicate is a total, two-case disjunction defined for all pairs of natural numbers without any special treatment of edge inputs.

### Worked examples

- Claim: `VTask.Raised 5 5` holds (the equal case, where `m = n`).

- Claim: `VTask.Raised 5 6` holds (the successor case, where `m = n + 1`).

- Claim: `VTask.Raised 5 7` does not hold (7 is strictly more than one above 5).

- Claim: `VTask.Raised n m` is equivalent to `n ≤ m ∧ m ≤ n + 1` for all natural numbers `n` and `m`.

- Claim: If `VTask.Raised n m` holds, then `Nat.dist n m ≤ 1`.

### Boundaries

- At `n = 0`: `Raised 0 m` holds exactly when `m = 0` or `m = 1`; there is no wrap-around or special treatment since natural number subtraction is not involved.
- The predicate is asymmetric: `Raised n m` does **not** imply `Raised m n` in general (e.g., `Raised 5 6` holds but `Raised 6 5` does not, since 5 ≠ 6 and 5 ≠ 6 + 1).
- When `m < n`, the proposition is always false, because neither `m = n` nor `m = n + 1` can hold.

### Not to be confused with

- `Nat.succ_le` / `n + 1 ≤ m`: that asserts `m` is **at least** one above `n`, whereas `Raised n m` requires `m` to be **at most** one above `n`.
- `Nat.dist n m ≤ 1`: this is a symmetric condition (distance in either direction), while `Raised n m` is directional (only `m = n` or `m = n + 1`, not `m = n - 1`).
- `BalancedSz`: a separate size-balance predicate for ordnode trees; it is related to `Raised` in tree-rebalancing lemmas but has a different meaning and quantitative bound.