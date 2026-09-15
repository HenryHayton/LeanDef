## VTask.delta

### Object

`VTask.delta` is the Dirac delta function on the natural numbers centred at 1: it assigns the complex number 1 to the input 1, and 0 to every other natural number. Equivalently, it is the indicator function of the singleton set {1} inside ℕ, viewed as a ℂ-valued arithmetic function.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.delta : (n : ℕ) -> ℂ
<!-- PINNED-SIGNATURE:END -->


```
VTask.delta : (n : ℕ) -> ℂ
```

The single argument `n` is the natural number at which the function is evaluated.

### Conventions

The function is total on all of ℕ. There are no junk-value conventions to declare: every natural number is a legitimate input, and the function returns the unambiguous value 0 for any input other than 1.

### Worked examples

- Claim: `VTask.delta 1 = 1` (the unique non-zero value; the function returns 1 at its distinguished point)

- Claim: `VTask.delta 0 = 0` (zero is not equal to 1, so the function returns 0)

- Claim: `VTask.delta 7 = 0` (any natural number other than 1 gives 0)

- Claim: For every `n : ℕ` with `n ≠ 1`, `VTask.delta n = 0`

### Boundaries

- At `n = 1`: the function returns `(1 : ℂ)`, the multiplicative identity.
- At `n = 0`: returns `(0 : ℂ)`. Despite 0 being the additive identity of ℕ, it receives the same treatment as all non-1 inputs.
- For all `n ≥ 2`: returns `(0 : ℂ)`.
- The function is bounded: its range is exactly {0, 1} ⊆ ℂ.

### Not to be confused with

- The Kronecker delta `δ_{m,n}` (a two-variable function testing equality of two inputs, rather than membership in a fixed singleton).
- The Dirac delta distribution on ℝ (a distribution/measure on a continuous space, not a pointwise ℕ → ℂ function).
- The constant function 1 on ℕ (which assigns 1 to every natural number, not just to 1).