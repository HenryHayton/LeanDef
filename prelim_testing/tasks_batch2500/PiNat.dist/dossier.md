## Object

`VTask.dist` equips the countably-infinite product space `Π n, E n` (sequences whose `n`-th term lives in the type `E n`) with a canonical metric. The distance between two sequences `x` and `y` is `(1/2)^n` where `n` is the smallest index at which the sequences first disagree, and it is `0` when the sequences are identical. This turns the product into an ultrametric space (in fact a compact metrizable space when each `E n` is finite and nonempty).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.dist : {E : ℕ → Type u_1} -> Dist ((n : ℕ) → E n)
<!-- PINNED-SIGNATURE:END -->


`VTask.dist : {E : ℕ → Type u_1} -> Dist ((n : ℕ) → E n)`

The implicit argument `E` is the type family — it assigns to each natural number `n` the set of possible values at position `n`. The result is a `Dist` instance on the dependent-function type `(n : ℕ) → E n`, i.e., it produces the distance structure on sequences valued in `E`.

## Conventions

When two sequences are equal, the distance is defined to be `0`, even though the formula `(1/2)^n` with a first-difference index is undefined for equal sequences; this case is handled by a direct assignment of `0`.

## Worked examples

- Claim: For any sequence `x : (n : ℕ) → E n`, the distance from `x` to itself is `0` (the equal-sequences case).

- Claim: If `x` and `y` differ for the first time at index `3`, then `VTask.dist` assigns them the value `(1/2)^3 = 1/8`.

- Claim: The distance between any two sequences is at most `1`, since `(1/2)^n ≤ (1/2)^0 = 1` for all `n ≥ 0`.

- Claim: If `dist x y < (1/2)^n` then `x` and `y` agree on all indices `i ≤ n`, i.e., small distance implies long common prefix.

- Claim: The distance satisfies the strong (ultrametric) triangle inequality: `dist x z ≤ max (dist x y) (dist y z)` for all sequences `x`, `y`, `z`.

## Boundaries

- **Equal sequences**: When `x = y` the distance is exactly `0`, regardless of the type family `E`.
- **Sequences differing at index 0**: When `x 0 ≠ y 0`, the first-difference index is `0`, so the distance is `(1/2)^0 = 1`, which is the maximum possible value.
- **Distance is always in `[0, 1]`**: Non-negativity holds because `(1/2)^n > 0` and the zero branch is non-negative; the upper bound `1` is attained when sequences disagree at index `0`.
- **Ultrametric inequality**: The metric is non-Archimedean; the ordinary triangle inequality `dist x z ≤ dist x y + dist y z` follows from the stronger ultrametric inequality.
- **Symmetry**: The first index of disagreement does not depend on the order of comparison, so `dist x y = dist y x`.

## Not to be confused with

- The product of individual metrics on each `E n` (e.g., a weighted `ℓ¹` or `ℓ∞` sum): that approach requires each `E n` to already carry a metric, whereas `VTask.dist` only requires the types `E n` with equality and assigns distance based purely on the first differing coordinate.
- `PiNat.cylinder`: a cylinder set `cylinder x n` is the set of sequences agreeing with `x` on the first `n` indices; this is the open ball of radius `(1/2)^n` around `x`, closely related to but not the same as the distance function itself.
- The Baire space metric on `ℕ^ℕ` with distance `1/(n+1)` for first difference at `n`: that is a different (topologically equivalent) formula, not the same numerical values as `VTask.dist`.