## VTask.IsMultiplicative

### Object

A predicate on arithmetic functions (functions from the natural numbers to a monoid-with-zero `R`) asserting that the function is *multiplicative* in the classical number-theoretic sense: it sends 1 to 1, and it respects multiplication over pairs of coprime natural numbers. Concretely, `f` is multiplicative if (i) `f(1) = 1` and (ii) whenever `gcd(m, n) = 1` one has `f(m·n) = f(m)·f(n)`. This is the standard definition used throughout analytic and algebraic number theory for functions such as Euler's totient, the Möbius function, the divisor-sum functions, and so on.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsMultiplicative : {R : Type u_1} -> [MonoidWithZero R] -> (f : ArithmeticFunction R) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsMultiplicative : {R : Type u_1} -> [MonoidWithZero R] -> (f : ArithmeticFunction R) -> Prop`

The implicit type argument `R` is the codomain ring or monoid-with-zero into which the arithmetic function takes values. The instance argument supplies the multiplicative-monoid-with-zero structure on `R` needed to state the multiplicativity condition and the normalisation `f(1) = 1`. The explicit argument `f` is the arithmetic function being tested; it is a function `ℕ → R` (packaged as an `ArithmeticFunction`) whose multiplicativity is being asserted.

### Conventions

There are no junk-value conventions for this predicate: it is a `Prop` applied uniformly to every arithmetic function, and no special meaning is assigned to boundary inputs such as `f 0`.

### Worked examples

- Claim: The constant-1 arithmetic function `(1 : ArithmeticFunction R)` (the Dirichlet identity with value 1 at 1 and 0 elsewhere) satisfies `VTask.IsMultiplicative`.

- Claim: The Möbius function `μ` satisfies `VTask.IsMultiplicative`.

- Claim: The divisor-power-sum function `σ k` satisfies `VTask.IsMultiplicative` for every `k : ℕ`.

- Claim: The identity arithmetic function `ArithmeticFunction.id` satisfies `VTask.IsMultiplicative`.

- Claim: If `f` satisfies `VTask.IsMultiplicative` then so does `f ^ k` for any `k : ℕ` (in a `CommSemiring`).

- Claim: If `f` satisfies `VTask.IsMultiplicative` and `t` is a finite set of primes, then `f(∏ p ∈ t, p) = ∏ p ∈ t, f p`.

### Boundaries

- The normalisation condition `f 1 = 1` is an independent conjunct; it cannot be dropped. A function satisfying only the coprimality-multiplicativity clause but with `f 1 ≠ 1` (e.g., the zero function on coprime pairs) would **not** be considered multiplicative under this definition.
- Arithmetic functions are defined on all of `ℕ`, including `0`. The predicate places no constraint on `f 0`, so multiplicative functions may freely take any value at `0`. In particular, `f 0 = 0` is common but not required by this predicate.
- The coprimality hypothesis is essential: the multiplicativity clause only fires when `Nat.Coprime m n` holds, so no constraint is imposed on `f` at non-coprime pairs.
- The predicate is meaningful for any `MonoidWithZero R`; stronger results (e.g., closure under Dirichlet convolution) require additional structure such as `CommSemiring` or `CommRing`.

### Not to be confused with

- **Completely multiplicative functions**: a strictly stronger notion requiring `f(m·n) = f(m)·f(n)` for *all* pairs `m, n`, not just coprime ones; every completely multiplicative function is multiplicative, but not conversely (e.g., σ is multiplicative but not completely multiplicative).
- **`ArithmeticFunction.pmul` (pointwise multiplication)**: the pointwise product of two arithmetic functions, which is distinct from the Dirichlet convolution; multiplicativity is preserved under Dirichlet convolution and `pmul` of multiplicative functions, but these are different operations.
- **Multiplicative maps between monoids** (`MonoidHom`): a general algebraic notion of structure-preserving map between any two monoids, unrelated to the number-theoretic coprimality condition that defines multiplicativity of arithmetic functions.