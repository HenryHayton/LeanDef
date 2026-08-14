## VTask.contractNth

### Object

Given a tuple `g = (g₀, g₁, …, gₙ)` of `n + 1` elements (indexed by `Fin (n + 1)`) and a position `j` in that tuple, `VTask.contractNth j op g` produces a shorter tuple of `n` elements (indexed by `Fin n`) obtained by **merging** the adjacent pair `(gⱼ, gⱼ₊₁)` into the single value `op gⱼ gⱼ₊₁`, while leaving all other entries in place. Concretely, the resulting tuple is

```
(g₀, …, gⱼ₋₁, op gⱼ gⱼ₊₁, gⱼ₊₂, …, gₙ)
```

This is a length-reducing operation that collapses two neighbouring slots into one by applying a binary operation to them.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.contractNth : {n : ℕ} -> {α : Sort u_1} -> (j : Fin (n + 1)) -> (op : α → α → α) -> (g : Fin (n + 1) → α) -> (k : Fin n) -> α
<!-- PINNED-SIGNATURE:END -->


```
VTask.contractNth : {n : ℕ} -> {α : Sort u_1} -> (j : Fin (n + 1)) -> (op : α → α → α) -> (g : Fin (n + 1) → α) -> (k : Fin n) -> α
```

The implicit argument `n` is one less than the length of the input tuple. The implicit argument `α` is the type of the elements. The argument `j` is the index (into the original length-`n + 1` tuple) of the **left** entry of the pair to be merged; the right entry is automatically `j + 1`. The argument `op` is the binary operation used to combine `gⱼ` and `gⱼ₊₁`. The argument `g` is the original tuple of `n + 1` elements, presented as a function `Fin (n + 1) → α`. The argument `k` is the output index (in `Fin n`) at which the result is being queried.

### Conventions

The function is total: every combination of `j`, `op`, `g`, and `k` yields a value. No junk-value or out-of-range convention is needed because the types enforce validity. The output at index `k` is determined by a three-way case split: when `k < j` the entry is the original entry at position `k`; when `k = j` the entry is `op gⱼ gⱼ₊₁`; and when `k > j` the entry is the original entry at position `k + 1` (i.e., shifted up by one).

### Worked examples

- Claim: For `g = (10, 20, 30)` and `j = 1` (the middle position) with `op = (· + ·)`, the result at output index `0` is `10` (the entry before the merge point, left unchanged).

- Claim: For `g = (10, 20, 30)` and `j = 1` with `op = (· + ·)`, the result at output index `1` is `50` (the merged pair `20 + 30`).

- Claim: For `g = (10, 20, 30, 40)` and `j = 0` (the first position) with `op = (· * ·)`, the result at output index `0` is `200` (i.e., `10 * 20`), and the result at output index `1` is `30`, and the result at output index `2` is `40`.

- Claim: For `g = (a, b, c)` and `j = 2` (the last valid merge position) with `op = (· + ·)`, the result at output index `0` is `a`, the result at output index `1` is `b + c`.

### Boundaries

- When `j = 0` (the leftmost merge), the first output slot contains `op g₀ g₁` and the remaining outputs are `g₂, g₃, …, gₙ`.
- When `j = n` (the rightmost merge, since `j : Fin (n + 1)`), all output slots `k < n` with `k < n` equal `gₖ` and the last output slot (index `n − 1`) equals `op gₙ gₙ₊₁`; since `j = n` and `k` ranges over `Fin n` (i.e., `0` through `n − 1`), the case `k = j` occurs exactly at `k = n − 1` only when `n` fits, and all earlier outputs are passed through unchanged.
- When `n = 0`, `j` must be `0 : Fin 1`, and `k : Fin 0` is vacuous, so the resulting function has an empty domain and `VTask.contractNth` is never actually applied to a concrete `k`.
- The operation `op` is not required to be associative, commutative, or have an identity; the definition works for any binary operation.

### Not to be confused with

- `Fin.insertNth`: the dual operation that *inserts* a new element into a tuple, increasing its length by one, rather than merging two adjacent elements and decreasing length.
- `Fin.removeNth` / `Fin.succAbove`-based removal: these drop a single entry entirely without combining it with its neighbour, whereas `VTask.contractNth` merges two adjacent entries via `op`.
- `Matrix.contractNth` or similar matrix contractions: in linear algebra, "contraction" typically refers to summing over a repeated index (a trace-like operation), which is unrelated to this tuple-merging construction.