## VTask.IsPell

### Object
`VTask.IsPell z` is the proposition that the element `z = x + y√d` of the ring `ℤ√d` is a solution to the *Pell equation*, i.e., that its norm equals 1. Concretely, for `z = ⟨x, y⟩` this means `x² − d·y² = 1`. Solutions to this equation are precisely the elements of `ℤ√d` whose multiplicative norm (in the sense of the quadratic integer norm map) is equal to 1.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsPell : {d : ℤ} -> ℤ√d → Prop
<!-- PINNED-SIGNATURE:END -->


The implicit argument `d : ℤ` is the *radicand*, the integer under the square root that determines which quadratic integer ring `ℤ√d` is being considered. The explicit argument is an element of `ℤ√d`, given as a pair of integers `⟨x, y⟩` (the rational part and the coefficient of `√d`), and the predicate asserts that this specific element satisfies the Pell equation for the chosen `d`.

### Conventions

The predicate is meaningful for any integer `d`, including negative values (in which case `ℤ√d` consists of Gaussian-integer–style elements and solutions are those with complex norm 1), zero (where solutions must have `x = ±1`), and positive perfect squares. No domain restriction is imposed; the definition is total.

### Worked examples

- Claim: `VTask.IsPell (⟨1, 0⟩ : ℤ√2)` holds (the trivial solution `x = 1, y = 0`).

- Claim: `VTask.IsPell (⟨3, 2⟩ : ℤ√2)` holds, since `3² − 2·2² = 9 − 8 = 1`.

- Claim: `¬ VTask.IsPell (⟨2, 1⟩ : ℤ√2)`, since `2² − 2·1² = 4 − 2 = 2 ≠ 1`.

- Claim: `VTask.IsPell (⟨2, 1⟩ : ℤ√3)` holds, since `2² − 3·1² = 4 − 3 = 1`.

- Claim: For `d = −1` (Gaussian integers), `VTask.IsPell (⟨0, 1⟩ : ℤ√(-1))` holds, since `0² − (−1)·1² = 0 + 1 = 1`.

### Boundaries

- **Trivial solution**: For any `d`, the element `⟨1, 0⟩` satisfies the predicate, as `1 − d·0 = 1`; similarly `⟨−1, 0⟩` also satisfies it.
- **`d = 0`**: The equation becomes `x² = 1`, so the only solutions are `⟨1, 0⟩` and `⟨−1, 0⟩`; the `y`-component is unconstrained as a formal parameter but contributes 0 to the norm.
- **`d` a perfect square**: Solutions still exist (they include `⟨1, 0⟩`) but the equation factors over `ℤ` and there are typically only finitely many solution families.
- **Negative `d`**: The equation `x² + |d|·y² = 1` has only finitely many integer solutions (bounded by 1), so the predicate is satisfied only for small specific pairs.
- **`y = 0`**: The predicate reduces to `x² = 1`, i.e., `x = ±1` regardless of `d`.

### Not to be confused with

- **The norm map `ℤ√d → ℤ`**: The predicate `VTask.IsPell` is the *unit-norm condition* (norm = 1), not the norm function itself.
- **`Zsqrtd.normSq`**: The squared-norm function on `ℤ√d`; `VTask.IsPell z` is equivalent to `normSq z = 1`, but `normSq` is a function returning an integer, not a proposition.
- **The Pell equation over `ℕ`**: Sometimes Pell equations are stated with natural-number or positive-integer solutions only; here `x` and `y` range over all of `ℤ`, allowing negative values and the trivial solution.