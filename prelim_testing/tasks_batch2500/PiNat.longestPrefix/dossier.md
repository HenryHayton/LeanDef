## VTask.longestPrefix

### Object

`VTask.longestPrefix x s` is a natural number measuring how deeply the point `x` in the product space `Π (n : ℕ), E n` shares a common initial segment with elements of the set `s`. Concretely, it is the largest `n` such that there exists some element `y ∈ s` whose first `n` coordinates all agree with those of `x` (i.e., `y` and `x` share a prefix of length `n`). When no such element exists (for instance because `s` is empty), the value is `0` by convention.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.longestPrefix : {E : ℕ → Type u_2} -> (x : (n : ℕ) → E n) -> (s : Set ((n : ℕ) → E n)) -> ℕ
<!-- PINNED-SIGNATURE:END -->


`{E : ℕ → Type u_2}` is the implicit type-family, assigning a type to each natural-number index. `x : (n : ℕ) → E n` is the reference point in the product space whose prefixes are being matched against elements of `s`. `s : Set ((n : ℕ) → E n)` is the subset of the same product space against which `x` is compared.

### Conventions

When `s` is empty, or more generally when no element of `s` agrees with `x` on even a single coordinate beyond the zeroth level, `VTask.longestPrefix x s` returns `0`.

### Worked examples

- Claim: If `s` consists of a single sequence `y` that agrees with `x` everywhere, then `VTask.longestPrefix x s` is very large (unbounded), but in finite approximations the cylinder intersection is always nonempty.

- Claim: If `s` is a nonempty closed set and `x ∉ s`, then `s ∩ cylinder x (VTask.longestPrefix x s)` is nonempty, meaning the longest-prefix cylinder still touches `s`.

- Claim: If `s` is a nonempty closed set and `x ∉ s`, and `n > VTask.longestPrefix x s`, then `s` and `cylinder x n` are disjoint — no element of `s` agrees with `x` on `n` initial coordinates.

- Claim: For the set `s = {x}` (a singleton containing `x` itself) and any closed nonempty `s`, the first-difference index `firstDiff x y` for any `y ∈ s` satisfies `firstDiff x y ≤ VTask.longestPrefix x s` when `x ∉ s`.

### Boundaries

- When `s` is empty, there is no element sharing any prefix with `x`, so the value is `0` by the junk-value convention (subtraction of natural numbers bottoms out at `0`).
- When `x ∈ s`, the set contains a sequence agreeing with `x` on every prefix, so `shortestPrefixDiff x s` would be zero or the supremum would be infinite; the definition may return `0` or an extremely large value depending on the closed-set structure, but the key theorems above assume `x ∉ s`.
- The value `0` does not mean "no coordinates agree"; it is the fallback when the computation bottoms out via truncated subtraction.
- For a nonempty closed set `s` with `x ∉ s`, the value is always a genuine positive integer giving the exact depth of agreement.

### Not to be confused with

- `PiNat.firstDiff x y`: measures the first index where two *specific* sequences `x` and `y` disagree, rather than optimising over all elements of a set.
- `PiNat.shortestPrefixDiff x s`: the companion quantity equal to `VTask.longestPrefix x s + 1`; it is the *shortest* prefix length that distinguishes `x` from every element of `s`, whereas `longestPrefix` is the longest prefix still shared with some element.
- `PiNat.cylinder x n`: the set of all sequences agreeing with `x` on the first `n` coordinates — the geometric object whose radius is controlled by `longestPrefix`, not the radius itself.
