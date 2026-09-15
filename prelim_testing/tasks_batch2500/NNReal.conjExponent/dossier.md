## VTask.conjExponent

### Object

Given a non-negative real number `p`, its *conjugate exponent* is the non-negative real number `q = p / (p − 1)`. This is the unique value satisfying the Hölder conjugacy relation `p⁻¹ + q⁻¹ = 1`, which arises in Hölder's inequality and the theory of Lp spaces. For example, the conjugate of `p = 2` is `q = 2` (the self-conjugate case), the conjugate of `p = 3` is `q = 3/2`, and in general larger `p` gives a conjugate closer to `1`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.conjExponent : (p : NNReal) -> NNReal
<!-- PINNED-SIGNATURE:END -->


The single argument `p : NNReal` is the exponent whose Hölder conjugate is to be computed. It is a non-negative real number (an element of `ℝ≥0`).

### Conventions

The function is defined for all `p : NNReal` without restriction. When `p = 0`, subtraction in `NNReal` is truncated (saturating at 0), so `p − 1 = 0`, and therefore `VTask.conjExponent 0 = 0 / 0 = 0`. When `p = 1`, similarly `p − 1 = 0`, so `VTask.conjExponent 1 = 1 / 0 = 0` (division by zero in `NNReal` yields 0). These junk values do not satisfy the Hölder relation; the meaningful range is `1 < p < ∞`, where the conjugacy identity `p⁻¹ + q⁻¹ = 1` holds.

### Worked examples

- Claim: `VTask.conjExponent 2 = 2` (the self-conjugate case: 1/2 + 1/2 = 1)

- Claim: `VTask.conjExponent 3 = 3/2` (since 1/3 + 2/3 = 1)

- Claim: `VTask.conjExponent 4 = 4/3` (since 1/4 + 3/4 = 1)

- Claim: For any `p : NNReal` with `1 < p`, the pair `(p, VTask.conjExponent p)` satisfies the Hölder conjugate relation, i.e., `p.HolderConjugate (VTask.conjExponent p)`.

### Boundaries

- At `p = 0`: `NNReal` subtraction truncates `0 − 1` to `0`, so `VTask.conjExponent 0 = 0 / 0 = 0`. This is a junk value with no Hölder meaning.
- At `p = 1`: `1 − 1 = 0`, so `VTask.conjExponent 1 = 1 / 0 = 0`. Again a junk value; `1` has no finite Hölder conjugate (the conjugate would be `+∞`).
- For `0 < p ≤ 1` (excluding the meaningful regime): the formula returns a value in `[0, ∞)` via truncated arithmetic, but the Hölder relation does not hold.
- For `p > 1`: the formula is genuine, giving `q = p/(p−1) > 1`, with `q` strictly decreasing from `+∞` (as `p → 1⁺`) to `1` (as `p → ∞`).
- As `p → ∞` in `NNReal`, `q → 1` from above.

### Not to be confused with

- `NNReal.HolderConjugate`: the *predicate* asserting that two exponents `p` and `q` are Hölder conjugates; `VTask.conjExponent` computes the conjugate value, while `HolderConjugate` checks the relation.
- The real-valued version of the conjugate exponent defined on `ℝ` (rather than `ℝ≥0`): that variant may handle edge cases differently.
- The *Lebesgue conjugate* in the extended sense including `p = 1 ↔ q = ∞` and `p = ∞ ↔ q = 1`, which requires working in the extended non-negative reals `ℝ≥0∞`.