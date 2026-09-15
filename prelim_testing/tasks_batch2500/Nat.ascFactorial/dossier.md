## Object

`VTask.ascFactorial n k` computes the **ascending factorial** (also called the **rising factorial** or **Pochhammer symbol** over ℕ) of a natural number `n` taken `k` steps upward. Concretely, it is the product of `k` consecutive natural numbers starting at `n`:

$$n^{\overline{k}} = n\,(n+1)\,(n+2)\cdots(n+k-1)$$

with the empty product convention giving value 1 when `k = 0`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ascFactorial : (n : ℕ) -> ℕ → ℕ
<!-- PINNED-SIGNATURE:END -->


The first argument `n : ℕ` is the **starting value** of the ascending run — the smallest factor in the product. The second argument `k : ℕ` is the **length** of the run — how many consecutive integers are multiplied together.

## Conventions

When the length `k` is zero, the product is empty and the result is defined to be 1 (the standard empty-product convention). When the starting value `n` is zero and the length `k` is at least 1, the product includes the factor 0, so the result is 0.

## Worked examples

- Claim: `VTask.ascFactorial 3 4 = 3 * 4 * 5 * 6 = 360`
  ```lean
  example : VTask.ascFactorial 3 4 = 360 := by decide
  ```

- Claim: `VTask.ascFactorial n 0 = 1` for every `n` (empty product)
  ```lean
  example (n : ℕ) : VTask.ascFactorial n 0 = 1 := Nat.ascFactorial_zero n
  ```

- Claim: `VTask.ascFactorial 1 k = k !` — starting at 1, the ascending factorial equals the ordinary factorial
  ```lean
  example (k : ℕ) : VTask.ascFactorial 1 k = k.factorial := Nat.one_ascFactorial k
  ```

- Claim: `VTask.ascFactorial 0 3 = 0` — starting at 0 with positive length gives 0
  ```lean
  example : VTask.ascFactorial 0 3 = 0 := by decide
  ```

- Claim: `n ! * VTask.ascFactorial (n+1) k = (n+k)!` — connecting ascending factorial to ordinary factorial

## Boundaries

- **`k = 0`**: The result is 1 regardless of `n` (empty product).
- **`n = 0`, `k ≥ 1`**: The factor `0` appears in the product, so the result is 0.
- **`n = 1`**: The ascending factorial coincides with the ordinary factorial: `VTask.ascFactorial 1 k = k!`.
- **Lower bound**: `n ^ k ≤ VTask.ascFactorial n k` for all `n, k`.
- **Upper bound**: `VTask.ascFactorial (n+1) k ≤ (n+k) ^ k` for all `n, k`.
- **Divisibility**: `k!` divides `VTask.ascFactorial n k` for all `n, k` (the ratio is a generalised binomial coefficient).

## Not to be confused with

- **`Nat.descFactorial n k`** (`n.descFactorial k = n * (n-1) * … * (n-k+1)`): the *descending* factorial, which counts downward from `n` rather than upward.
- **`ascPochhammer R k`** (`ascPochhammer`): the polynomial version of the same product defined over a general semiring `R`; evaluating it at a natural number `n` recovers `VTask.ascFactorial n k`.
- **`Nat.factorial n`** (`n!`): the special case `VTask.ascFactorial 1 n`, i.e., the ascending factorial starting from 1; not the same for general starting points.
