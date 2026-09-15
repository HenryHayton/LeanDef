## Object

`VTask.prodPrimeFactors f` is the arithmetic function that sends a positive natural number $n$ to the product $\prod_{p \mid n} f(p)$, where the product runs over the distinct prime factors of $n$. It is an element of the type of arithmetic functions $\mathbb{N} \to R$; at $n = 0$ the value is defined to be $0$ (the junk/sentinel value required by the `ArithmeticFunction` type).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prodPrimeFactors : {R : Type u_1} -> [CommMonoidWithZero R] -> (f : ℕ → R) -> ArithmeticFunction R
<!-- PINNED-SIGNATURE:END -->


`VTask.prodPrimeFactors : {R : Type u_1} -> [CommMonoidWithZero R] -> (f : ℕ → R) -> ArithmeticFunction R`

The implicit type argument `R` is the codomain, which must carry a commutative monoid structure compatible with zero. The instance argument supplies this algebraic structure. The explicit argument `f : ℕ → R` is the weight function evaluated at each prime; it is the ingredient being multiplied together, one factor per distinct prime divisor.

## Conventions

At the input $n = 0$ the function returns $0 \in R$, regardless of `f`. This is a junk value required by the `ArithmeticFunction` interface (which demands that the zero of the natural numbers maps to the zero of $R$) and carries no number-theoretic meaning.

## Worked examples

- Claim: `VTask.prodPrimeFactors id 12 = 6`, because the distinct prime factors of 12 are {2, 3} and $2 \times 3 = 6$.
  ```lean
  example : VTask.prodPrimeFactors id 12 = 6 := by native_decide
  ```

- Claim: `VTask.prodPrimeFactors id 1 = 1`, because 1 has no prime factors, so the empty product is 1.
  ```lean
  example : VTask.prodPrimeFactors id 1 = 1 := by native_decide
  ```

- Claim: `VTask.prodPrimeFactors id 8 = 2`, because 8 = 2³ has only one distinct prime factor, namely 2.
  ```lean
  example : VTask.prodPrimeFactors id 8 = 2 := by native_decide
  ```

- Claim: `VTask.prodPrimeFactors (fun _ => (2 : ℤ)) 30 = 8`, because 30 = 2·3·5 has three distinct prime factors and $2^3 = 8$.
  ```lean
  example : VTask.prodPrimeFactors (fun _ => (2 : ℤ)) 30 = 8 := by native_decide
  ```

- Claim: `VTask.prodPrimeFactors id 0 = 0` (junk/sentinel value).
  ```lean
  example : VTask.prodPrimeFactors id 0 = 0 := by native_decide
  ```

## Boundaries

- **At $n = 0$**: the value is $0 \in R$ by definition (junk value; the product formula is not applied).
- **At $n = 1$**: the set of prime factors is empty, so the product is the empty product, which equals $1 \in R$ (the identity of the monoid). Hence `VTask.prodPrimeFactors f 1 = 1` for any `f`.
- **Prime powers $n = p^k$ with $k \geq 1$**: the set of distinct prime factors is the singleton $\{p\}$, so the value is simply $f(p)$, independent of the exponent $k$.
- **Squarefree $n$**: for squarefree $n$, each prime appears with multiplicity exactly 1 and the product coincides with the product of $f$ over all prime divisors in the usual sense. In this regime a range of Möbius-inversion identities connect `VTask.prodPrimeFactors f` to divisor sums.
- **The function `f` at non-primes**: values of `f` at composite or zero arguments are never used; only $f(p)$ for primes $p$ dividing $n$ contribute.

## Not to be confused with

- `ArithmeticFunction.moebius`: the Möbius function, which is defined via prime factorization but outputs $\pm 1$ or $0$ based on squarefreeness, not a general product of $f$-values.
- A product over prime factors *with multiplicity* (i.e., $\prod_{p^k \| n} f(p)^k$ or $\prod_{p \mid n, \text{ counted with mult.}} f(p)$): `VTask.prodPrimeFactors` uses each prime exactly once regardless of its exponent.
- `ArithmeticFunction.pmul` or pointwise multiplication of two arithmetic functions: that is a product over *functions*, not over the prime factors of the argument.
