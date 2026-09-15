## Object

A **cylinder set** (also called a cylinder of length `n` around `x`) in the product space `Π n, E n` is the set of all sequences `y` that agree with a fixed reference sequence `x` on their first `n` coordinates, i.e., `y i = x i` for every index `i` strictly less than `n`. Cylinder sets are the fundamental open-and-closed building blocks of the product topology on sequence spaces; they form a basis for the topology and play a central role in the metrization of such spaces.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cylinder : {E : ℕ → Type u_1} -> (x : (n : ℕ) → E n) -> (n : ℕ) -> Set ((n : ℕ) → E n)
<!-- PINNED-SIGNATURE:END -->


`VTask.cylinder : {E : ℕ → Type u_1} -> (x : (n : ℕ) → E n) -> (n : ℕ) -> Set ((n : ℕ) → E n)`

The implicit argument `E` is the family of types, one for each natural-number index, whose product forms the ambient sequence space. The first explicit argument `x` is the reference sequence (the centre of the cylinder), whose initial segment the cylinder tracks. The second explicit argument `n` is the length of the cylinder, specifying how many leading coordinates must match `x`; it is a natural number.

## Conventions

When the length `n` is zero, the cylinder imposes no constraints at all and therefore equals the entire space (the universal set). This is the natural junk-free convention: an empty matching requirement is satisfied by every sequence.

## Worked examples

- Claim: Every sequence `x` is itself a member of `VTask.cylinder x n` for any `n`, because it trivially agrees with itself on all coordinates.

- Claim: `VTask.cylinder x 0 = Set.univ` — the cylinder of length 0 around any sequence is the whole space, since there are no coordinates to match.

- Claim: Cylinder sets are anti-monotone in the length: if `m ≤ n` then `VTask.cylinder x n ⊆ VTask.cylinder x m`, because a sequence matching `x` on the first `n` coordinates certainly matches on the first `m ≤ n` coordinates.

- Claim: `VTask.cylinder x n` equals the product `Set.pi (Finset.range n : Set ℕ) (fun i => {x i})`, i.e., it is exactly the pi-set that fixes each coordinate `i < n` to the single value `x i` and is unrestricted elsewhere.

- Claim: Membership is symmetric — `y ∈ VTask.cylinder x n` if and only if `x ∈ VTask.cylinder y n` — since the condition `y i = x i` is symmetric in `x` and `y`.

## Boundaries

- **Length 0:** `VTask.cylinder x 0 = Set.univ`. No index satisfies `i < 0`, so the condition is vacuously true for every sequence, yielding the whole space.
- **Length 1:** Only coordinate `0` must match, so the cylinder is a large (cofinite in structure) set of sequences.
- **Monotonicity (anti):** Larger `n` gives a smaller (or equal) set; the cylinders form a nested decreasing family as `n` grows.
- **Updating coordinate `n`:** The sequence `update x n y` (which equals `x` everywhere except at index `n`) still lies in `VTask.cylinder x n`, because `n` itself is not in the range `{i | i < n}`.
- **Self-membership:** `x` always belongs to `VTask.cylinder x n` for any `n` and any `x`.
- **Union decomposition:** The union over all values `k : E n` of `VTask.cylinder (update x n k) (n+1)` equals `VTask.cylinder x n`, giving a disjoint partition of any cylinder into cylinders of the next length.

## Not to be confused with

- **`Set.pi` (general pi-sets):** A `Set.pi` fixes coordinates in an arbitrary set of indices to arbitrary sets of values; a cylinder specifically fixes the *initial segment* `{0, …, n−1}` to singleton sets `{x i}`.
- **`PiNat.firstDiff`:** The first index at which two sequences differ; related to cylinder membership (`y ∈ cylinder x n` iff `n ≤ firstDiff x y` when `x ≠ y`), but is a natural-number-valued function, not a set.
- **Balls in the product metric:** In the canonical metric on `Π n, E n`, a closed ball of radius `(1/2)^n` around `x` coincides with `VTask.cylinder x n`, but the ball notation `Metric.closedBall x r` obscures the coordinate-matching structure that the cylinder name makes explicit.