## Object

Given an arithmetic function `f : ℕ → R` whose value at 1 is invertible in a ring `R`, `VTask.dirichletInverseFun f hf` is the **Dirichlet inverse** of `f`: the unique arithmetic function `g : ℕ → R` such that the Dirichlet convolution `f * g` equals the arithmetic identity function (the function sending 1 to 1 and all other positive integers to 0). The Dirichlet inverse exists precisely when `f(1)` is invertible in `R`, which is encoded by the `Invertible` witness.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.dirichletInverseFun : {R : Type u_1} -> [Ring R] -> (f : ℕ → R) -> (hf : Invertible (f 1)) -> (n : ℕ) -> R
<!-- PINNED-SIGNATURE:END -->


`VTask.dirichletInverseFun : {R : Type u_1} -> [Ring R] -> (f : ℕ → R) -> (hf : Invertible (f 1)) -> (n : ℕ) -> R`

The implicit type argument `R` is the codomain ring. The ring instance `[Ring R]` provides the algebraic structure needed for addition, subtraction, and multiplication. The argument `f` is the arithmetic function whose Dirichlet inverse is being computed. The argument `hf` is a witness that `f 1` is invertible in `R` (providing a two-sided inverse `⅟(f 1)`); this witness is used to make the construction computable when `f` is computable. The final argument `n` is the natural number at which the Dirichlet inverse is evaluated.

## Conventions

At `n = 0`, the Dirichlet inverse returns `0`; this is a junk value since Dirichlet series are indexed by positive integers and the value at 0 carries no number-theoretic meaning. At `n = 1`, the Dirichlet inverse returns `⅟(f 1)`, the chosen inverse of `f(1)` in `R`. For `n ≥ 2`, the value is defined by the recursive formula `-(⅟(f 1)) * ∑_{d | n, d < n} f(n/d) * g(d)`, where the sum runs over proper divisors of `n`; this recursion is well-founded because proper divisors are strictly smaller than `n`.

## Worked examples

- Claim: `VTask.dirichletInverseFun f hf 0 = 0` for any `f` and `hf` — the value at zero is always 0.

- Claim: `VTask.dirichletInverseFun f hf 1 = ⅟(f 1)` — the value at 1 is the chosen inverse of `f(1)`.

- Claim: For `n = 6` (which has proper divisors {1, 2, 3}), `VTask.dirichletInverseFun f hf 6 = -(⅟(f 1)) * (f 6 * ⅟(f 1) + f 3 * VTask.dirichletInverseFun f hf 2 + f 2 * VTask.dirichletInverseFun f hf 3)`, illustrating the recursive unfolding with the sum over proper divisors 1, 2, 3 of 6.

- Claim: When `f` is the constant function `1` (sending every `n` to `1 : ℤ`) with the natural invertibility of `1` in `ℤ`, the Dirichlet inverse of `f` evaluated at a prime `p` equals `-1`, since `-(⅟1) * (f(p) * g(1)) = -(1) * (1 * 1) = -1`.

## Boundaries

- **At `n = 0`**: Returns `0` by convention; this is a junk value since Dirichlet series are normally indexed by positive integers.
- **At `n = 1`**: Returns `⅟(f 1)`, the multiplicative inverse of `f(1)` supplied via the `Invertible` instance.
- **When `f(1)` is not invertible**: The function cannot be constructed — the `Invertible (f 1)` hypothesis is required, and there is no junk fallback for this condition.
- **For `n ≥ 2`**: The recursive formula involves a finite sum over proper divisors; since every proper divisor is strictly less than `n`, the recursion terminates.
- **When the ring `R` is non-commutative**: The formula still makes sense but the Dirichlet convolution theory may behave differently; the definition itself is well-typed for any ring.

## Not to be confused with

- **`ArithmeticFunction.pmul`** (pointwise multiplication of arithmetic functions): this is ordinary pointwise product, not Dirichlet convolution or inversion.
- **`ArithmeticFunction.MoebiusFun`** (the Möbius function `μ`)**: the Möbius function is the Dirichlet inverse of the constant-1 arithmetic function over `ℤ`, so it is a special case of `VTask.dirichletInverseFun`, not the same general construction.
- **Multiplicative inverses in the ring `R`**: `⅟(f 1)` is the ring-level inverse of the element `f(1)`, whereas `VTask.dirichletInverseFun f hf` is the Dirichlet-convolution-level inverse of the entire function `f`.