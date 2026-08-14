## Object

Given an arithmetic function `f : ℕ → R` (where `R` is a ring) whose value at 1 is invertible, `VTask.dirichletInverseFun f hf` is the **Dirichlet inverse** of `f`. That is, it is the unique arithmetic function `g : ℕ → R` satisfying `(f * g)(n) = ε(n)` under Dirichlet convolution, where `ε` is the arithmetic identity (1 at n = 1, 0 elsewhere). The function is constructed by an explicit recursive formula: it is 0 at 0, the ring-inverse of `f(1)` at 1, and for `n ≥ 2` it is determined by the requirement that the Dirichlet convolution `(f * g)(n) = 0`, solved for `g(n)` using the proper divisors of `n`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.dirichletInverseFun : {R : Type u_1} -> [Ring R] -> (f : ℕ → R) -> (hf : Invertible (f 1)) -> (n : ℕ) -> R
<!-- PINNED-SIGNATURE:END -->


VTask.dirichletInverseFun : {R : Type u_1} -> [Ring R] -> (f : ℕ → R) -> (hf : Invertible (f 1)) -> (n : ℕ) -> R

- `R` is the target ring (implicit, inferred from context).
- The `Ring R` instance provides the ring structure on `R` (addition, multiplication, negation).
- `f` is the arithmetic function whose Dirichlet inverse is being computed; it is a function from natural numbers to `R`.
- `hf` is an `Invertible` witness for `f 1`, providing both the inverse element `⅟(f 1)` and the proofs that it is a two-sided inverse in `R`. This witness makes the construction computable when `f` is computable.
- `n` is the natural number at which the Dirichlet inverse is evaluated.

## Conventions

At `n = 0`, the Dirichlet inverse is defined to be `0` (junk value, since Dirichlet convolution is conventionally indexed over positive integers and the value at 0 carries no arithmetic meaning). At `n = 1`, the value is `⅟(f 1)`, the ring-inverse of `f(1)` supplied by the `Invertible` instance.

## Worked examples

- Claim: `VTask.dirichletInverseFun f hf 0 = 0` for any `f` and `hf` — the value at zero is always the zero element of `R`.

- Claim: `VTask.dirichletInverseFun f hf 1 = ⅟(f 1)` — the value at one is the ring-inverse of `f(1)`.

- Claim: For `n = 6` (which has proper divisors `{1, 2, 3}`), `VTask.dirichletInverseFun f hf 6 = -⅟(f 1) * ∑ d ∈ Nat.properDivisors 6, f (6 / d) * VTask.dirichletInverseFun f hf d`, expressing the recursive computation in terms of values at 1, 2, and 3.

- Claim: If `f` is the constant function `f(n) = 1` with `R = ℤ` (so `f 1 = 1` and `⅟(f 1) = 1`), then the Dirichlet inverse of `f` is the Möbius function — each value `VTask.dirichletInverseFun f hf n` equals `μ(n)` for positive `n`.

## Boundaries

- At `n = 0`: returns `0` unconditionally, regardless of `f` or `hf`. This is a junk value; the Dirichlet inverse has no natural definition at 0.
- At `n = 1`: returns `⅟(f 1)`, the multiplicative inverse of `f(1)`. The existence of this inverse is precisely the condition encoded by `hf : Invertible (f 1)`.
- For `n ≥ 2`: the recursion bottoms out because proper divisors of `n` are strictly less than `n`, so the recursion is well-founded. The sum ranges over all proper divisors of `n` (positive divisors strictly less than `n`).
- The `Invertible` typeclass rather than an explicit inverse function is used so that computability is preserved when `f` is a computable function and `R` has a computable `Invertible` instance.
- If `f 1` is not invertible in `R`, the function cannot be formed (the `hf` argument would be unavailable), which correctly reflects the classical fact that a Dirichlet inverse exists if and only if `f(1)` is a unit.

## Not to be confused with

- **The Möbius function** `ArithmeticFunction.moebius`: the Dirichlet inverse of the constant-1 function; `VTask.dirichletInverseFun` generalises this to an arbitrary invertible arithmetic function.
- **Dirichlet convolution** `ArithmeticFunction.pmul` or the `*` on arithmetic functions: `VTask.dirichletInverseFun` produces the *inverse* under convolution, not the convolution product itself.
- **`Ring.inverse`** or **`Units.inv`**: these compute the ring-inverse of a single element, whereas `VTask.dirichletInverseFun` computes an entire function (the Dirichlet inverse) whose definition involves a recursive sum over divisors, not just pointwise inversion.