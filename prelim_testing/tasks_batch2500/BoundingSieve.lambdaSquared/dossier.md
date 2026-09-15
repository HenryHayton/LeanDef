## VTask.lambdaSquared

### Object

The Λ² (lambda-squared) sieve weight function associated to a sequence of real-valued weights. Given a weight sequence `weights : ℕ → ℝ`, the value `VTask.lambdaSquared weights d` is the real number obtained by summing `weights d₁ · weights d₂` over all ordered pairs `(d₁, d₂)` of divisors of `d` whose least common multiple equals `d`. In other words, it is the "diagonal convolution" of the weight sequence with itself, twisted by the lcm condition: it keeps only those divisor pairs that reconstruct `d` as their lcm.

This construction is the cornerstone of Selberg's sieve method: any weight sequence satisfying `weights 1 = 1` gives an upper-bounding sieve (an upper Möbius function) via this formula, and the main sieve sum can be diagonalised into a sum of squares in terms of the so-called Selberg terms.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lambdaSquared : (weights : ℕ → ℝ) -> ℕ → ℝ
<!-- PINNED-SIGNATURE:END -->


`(weights : ℕ → ℝ) -> ℕ → ℝ`

The first argument is the underlying weight sequence — a function assigning a real number to every natural number; in sieve theory this sequence is typically supported on square-free integers dividing a fixed product of primes. The second argument (the argument of the returned function) is the natural number `d` at which the Λ²-sieve weight is evaluated.

### Conventions

The output at `d = 0` is 0, because `Nat.divisors 0` is the empty set, so the double sum is empty. The function is defined for all natural numbers without restriction, using the convention that `Nat.divisors 0 = ∅`.

### Worked examples

- Claim: For constant weights `weights = fun _ => 1`, `VTask.lambdaSquared weights 1 = 1`, because the only divisor of 1 is 1 itself, the only divisor pair is `(1, 1)`, `lcm(1,1) = 1 = d`, and the contribution is `1 · 1 = 1`.

- Claim: For constant weights `weights = fun _ => 1`, `VTask.lambdaSquared weights 6 = 4`, because the divisors of 6 are `{1, 2, 3, 6}` and the ordered pairs `(d₁, d₂)` from this set with `lcm(d₁, d₂) = 6` are exactly `(2, 3)`, `(3, 2)`, `(6, 1)`, `(1, 6)` — four pairs each contributing `1 · 1 = 1`, giving a total of 4.

- Claim: For the weight sequence `weights = fun n => if n = 1 then 1 else 0`, `VTask.lambdaSquared weights 4 = 0`, because the only nonzero-weight pair is `(1, 1)` but `lcm(1, 1) = 1 ≠ 4`, so every term in the double sum is 0.

- Claim: For `weights = fun n => if n = 1 then 1 else 0`, `VTask.lambdaSquared weights 1 = 1`, because the pair `(1,1)` satisfies `lcm(1,1) = 1` and contributes `1 · 1 = 1`.

### Boundaries

- At `d = 0`: the function returns 0, since `Nat.divisors 0` is empty and the double sum is vacuous.
- At `d = 1`: the only divisor pair is `(1, 1)` with `lcm(1, 1) = 1`, so `VTask.lambdaSquared weights 1 = weights 1 ^ 2`. In particular, when `weights 1 = 1` this equals 1, consistent with the sieve normalisation.
- For a prime `p`: the divisors are `{1, p}`, so the contributing pairs are those `(d₁, d₂)` from `{1, p}²` with `lcm = p`, namely `(1, p)`, `(p, 1)`, and `(p, p)`. The result is `2 · weights 1 · weights p + (weights p)²`.
- The function is defined on all of `ℕ` without any coprimality or squarefreeness restriction on the input, though in sieve applications the weight sequence is typically supported only on squarefree numbers dividing a fixed modulus.

### Not to be confused with

- The Selberg lambda weights themselves (`weights`): `VTask.lambdaSquared weights` is the *derived* sieve function formed from the squares/cross-products of the lambda weights, not the weights themselves.
- Möbius inversion or the Möbius function `μ`: while Λ² sieves produce upper Möbius functions, `VTask.lambdaSquared` is a specific quadratic construction, not the classical Möbius function.
- A pointwise square `(weights d)^2`: the value `VTask.lambdaSquared weights d` is a double sum over *all* divisor pairs of `d` with lcm equal to `d`, not just the square of `weights` at `d`.