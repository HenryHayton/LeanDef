## VTask.fastGrowing

### Object

The fast-growing hierarchy is a classical sequence of rapidly increasing functions `ℕ → ℕ` indexed by ordinal notations below ε₀. The hierarchy is defined recursively on the ordinal index:

- At the zero ordinal (and any ordinal whose fundamental sequence terminates immediately): `f_0(n) = n + 1` (the successor function).
- At a successor ordinal `α + 1`: `f_{α+1}(n) = f_α^[n](n)`, i.e., the function `f_α` iterated `n` times and applied to `n`.
- At a limit ordinal `α`: `f_α(n) = f_{α[n]}(n)`, where `α[n]` is the `n`-th term of the canonical fundamental sequence converging to `α`.

This hierarchy grows extremely rapidly: `f_0` is linear, `f_1` is roughly `2n`, `f_2` is roughly `n · 2^n`, and so on, with the growth rate becoming non-primitive-recursive for ordinals ≥ ω.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.fastGrowing : ONote → ℕ → ℕ
<!-- PINNED-SIGNATURE:END -->


`VTask.fastGrowing : ONote → ℕ → ℕ`

The first argument is the ordinal notation (an element of `ONote`, representing an ordinal below ε₀) that indexes which level of the hierarchy is being computed. The second argument is the natural number input to that level's function.

### Conventions

The function is defined by structural recursion on the ordinal notation using its fundamental sequence. When the fundamental sequence of the ordinal notation identifies it as zero (or any notation with no predecessor or limit approximants), the function is taken to be the successor function `n ↦ n + 1`. There is no separate junk value or out-of-domain convention: every `ONote` input yields a well-defined `ℕ → ℕ` function.

### Worked Examples

- Claim: `VTask.fastGrowing 0 n = n + 1` for any `n` (level 0 is the successor function).

- Claim: `VTask.fastGrowing 1 = fun n => 2 * n` (level 1 doubles its input).

- Claim: `VTask.fastGrowing 2 = fun n => (2 ^ n) * n` (level 2 produces roughly `n · 2^n`).

- Claim: At the ordinal ω (the first limit ordinal), `VTask.fastGrowing ω n = VTask.fastGrowing n n`, because the fundamental sequence of ω is `0, 1, 2, 3, …` so `f_ω(n) = f_n(n)`.

- Claim: The value of the fast-growing hierarchy at ε₀ applied to 2 equals 2048 (matching `fastGrowingε₀_two`: `fastGrowingε₀ 2 = 2048`, where `fastGrowingε₀` is `VTask.fastGrowing` evaluated at the notation for ε₀).

### Boundaries

- **At ordinal 0**: The function is exactly `Nat.succ`, i.e., `n ↦ n + 1`. This is confirmed by `fastGrowing_zero`.
- **At successor ordinals**: The function iterates the previous level's function `n` times and applies it to `n`, producing rapid growth even from small inputs.
- **At limit ordinals**: The function diagonalises over the fundamental sequence; at ω this gives `f_ω(n) = f_n(n)`, which already grows faster than any fixed level.
- **Any `ONote` is a valid input**: The function is total; there is no undefined case. Every ordinal notation in `ONote` (which represents ordinals strictly below ε₀) is handled.
- **At small natural number inputs** such as `n = 0` or `n = 1`: the iterated and diagonalised definitions often produce modest values (e.g., `f_1(1) = 2`, `f_2(2) = 8`) even though they grow very fast for large `n`.

### Not to be confused with

- **`ONote.fundamentalSequence`**: This is the auxiliary function supplying the canonical fundamental sequence `α[n]` used in the limit case; it is an ingredient of `VTask.fastGrowing`, not the hierarchy itself.
- **`Nat.rec` / primitive recursion**: Ordinary primitive recursion grows much more slowly; the fast-growing hierarchy for ordinals ≥ ω is not primitive recursive.
- **The Ackermann function**: The Ackermann function is closely related in growth rate to `f_ω`, but is a different two-argument function defined without ordinal indices.
