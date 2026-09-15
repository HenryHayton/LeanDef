## Object

`VTask.ppow f k` is the **pointwise k-th power** of an arithmetic function `f : ℕ → R`. For each positive natural number `k`, it is the arithmetic function sending every natural number `n` to `f(n)^k`. The edge case `k = 0` is handled by convention: regardless of `f`, the zeroth pointwise power is defined to be the arithmetic zeta function `ζ` (which sends every positive natural number to 1, and 0 to 0).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ppow : {R : Type u_1} -> [Semiring R] -> (f : ArithmeticFunction R) -> (k : ℕ) -> ArithmeticFunction R
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `R` is the codomain semiring. The typeclass argument supplies the semiring structure on `R`. The first explicit argument `f` is the arithmetic function being raised to a power — a function `ℕ → R` satisfying `f(0) = 0`. The second explicit argument `k` is the (natural number) exponent.

## Conventions

When the exponent `k` is zero, `VTask.ppow f 0` returns the arithmetic zeta function `ζ` for every choice of `f`; this is the standard junk-value/edge convention adopted to keep the pointwise-power operation total on natural-number exponents.

## Worked examples

- Claim: For any arithmetic function `f`, `VTask.ppow f 0 = ζ` (the zeta function).

- Claim: `VTask.ppow f 1 = f` for any arithmetic function `f`.

- Claim: For `k > 0`, `VTask.ppow f k` evaluated at `n` equals `f n ^ k`; for example, if `f` is the identity arithmetic function `id` (sending `n` to `n`), then `VTask.ppow id 3` sends each `n` to `n ^ 3`.

- Claim: `VTask.ppow f (k + 1) = VTask.ppow f k |>.pmul f` for `k > 0`, expressing the pointwise-power recurrence via pointwise multiplication.

## Boundaries

- At `k = 0`: The result is always `ζ`, independent of `f`. This is a deliberate definitional choice, not derived from the general formula `f(n)^0`, since `f(0)^0` in a semiring could differ from the zeta convention at 0.
- At `k = 1`: The result equals `f` itself.
- At `n = 0` (the input to the resulting arithmetic function): For positive `k`, the output is `f(0)^k = 0^k = 0`, consistent with the requirement that arithmetic functions in Mathlib satisfy `f(0) = 0`.
- The recurrence `ppow (k+1) = ppow k |>.pmul f` holds for all `k ≥ 0` (with the convention that `ppow 0 = ζ`).

## Not to be confused with

- `ArithmeticFunction.pmul`: The pointwise *product* of two arithmetic functions (a single multiplication), whereas `ppow` raises one function to a repeated pointwise power.
- Dirichlet convolution power: Repeated Dirichlet convolution of an arithmetic function with itself, an entirely different operation from pointwise exponentiation.
- `HPow` on the function type: Generic function-level power, which may not respect the arithmetic-function zero convention at 0.