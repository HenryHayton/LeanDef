## Object

A function `f : R → ℝ` is **power-multiplicative** if it commutes with taking positive natural-number powers: for every element `r` of `R` and every positive natural number `n`, the value of `f` at `r^n` equals `(f r)^n`. This is a standard condition on norms and seminorms appearing in non-Archimedean analysis and spectral theory.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsPowMul : {R : Type u_1} -> [Pow R ℕ] -> (f : R → ℝ) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsPowMul : {R : Type u_1} -> [Pow R ℕ] -> (f : R → ℝ) -> Prop`

The implicit type argument `R` is the domain type whose elements are being raised to natural-number powers. The instance argument supplies the operation of raising an element of `R` to a natural-number exponent. The explicit argument `f` is the real-valued function being tested for power-multiplicativity.

## Conventions

The condition is stated only for exponents `n` satisfying `1 ≤ n` (i.e., positive natural numbers). There is no requirement imposed at `n = 0`; in particular, `f(r^0) = (f r)^0` need not hold. This means the behaviour of `f` at the identity element (if one exists) is unconstrained by the predicate.

## Worked examples

- Claim: The spectral norm on a normed field extension satisfies `VTask.IsPowMul`.
  *(This follows from `isPowMul_spectralNorm` in Mathlib: the spectral norm is the canonical example of a power-multiplicative algebra norm.)*

- Claim: Any multiplicative ring norm `f : MulRingNorm A` on a ring `A`, viewed as a function `A → ℝ`, satisfies `VTask.IsPowMul f`.
  *(Every multiplicative ring norm satisfies `f(r^n) = f(r)^n` for all `n ≥ 1` by multiplicativity.)*

- Claim: If `f : S → ℝ` satisfies `VTask.IsPowMul f` on a ring `S`, and `A` is a subalgebra of `S`, then the restriction of `f` to `A` also satisfies `VTask.IsPowMul`.
  *(This is the restriction theorem: power-multiplicativity is inherited by subalgebras.)*

- Claim: If `R` is a monoid and `f` satisfies `VTask.IsPowMul f`, then `f 1 ≤ 1`.
  *(Applying the condition at `r = 1` and `n ≥ 1` forces `f(1) = f(1)^n` for all positive `n`, which together with `f(1) ∈ ℝ` implies `f(1) ≤ 1`.)*

## Boundaries

- **Exponent `n = 0`:** The predicate makes no assertion about `n = 0`. A function may fail `f(r^0) = (f r)^0` and still be power-multiplicative in this sense.
- **No algebraic structure required beyond `Pow R ℕ`:** The definition is stated for any type equipped with a natural-number power operation; no ring, monoid, or norm axioms are assumed at the level of the predicate itself.
- **No continuity or positivity requirement:** Power-multiplicativity alone does not force `f` to be non-negative, continuous, or a norm; those are separate conditions.
- **Restriction to subalgebras:** Power-multiplicativity passes to subalgebras (and more generally to sub-types where the power operation agrees with the ambient one).

## Not to be confused with

- **Multiplicativity (`f(ab) = f(a)f(b)`):** A function can be power-multiplicative without being fully multiplicative (the equation only involves powers of a single element, not products of two distinct elements).
- **Submultiplicativity (`f(ab) ≤ f(a)f(b)`):** A seminorm is submultiplicative but need not be power-multiplicative; a power-multiplicative seminorm is a strictly stronger condition.
- **`IsAlgNorm` / algebra norm predicates:** Those predicates bundle power-multiplicativity with additional norm and algebra-compatibility conditions; `VTask.IsPowMul` is the isolated functional-equation component.