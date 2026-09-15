## Object

`VTask.GrowsPolynomially f` is a predicate on a function `f : ℝ → ℝ` asserting that `f` has *polynomially controlled growth* in the following sense: for every ratio `b` strictly between 0 and 1, there exist positive constants `c₁` and `c₂` such that, for all sufficiently large `x`, every value `u` lying in the interval `[b·x, x]` satisfies `c₁·f(x) ≤ f(u) ≤ c₂·f(x)`. In plain terms, `f` does not oscillate wildly on sub-intervals that are a fixed fraction of `x`; its values at nearby points are controlled by a multiplicative constant relative to its value at `x`. This is precisely the growth regularity condition required to apply the Akra–Bazzi theorem for solving divide-and-conquer recurrences.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.GrowsPolynomially : (f : ℝ → ℝ) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.GrowsPolynomially : (f : ℝ → ℝ) -> Prop`

The single argument is the real-valued function whose growth behaviour is being classified. The predicate holds when `f` satisfies the uniform multiplicative sandwich condition described above, eventually and for every sub-proportional interval scale.

## Conventions

All quantifiers in the condition are eventually-true (in the filter sense): the constants `c₁`, `c₂` may depend on the ratio `b`, and the inequality is only required to hold for all sufficiently large `x`, not for every `x ∈ ℝ`. No sign restriction on `f` is built into the definition itself; both positive and sign-changing functions are in the domain.

## Worked examples

- Claim: The identity function `f(x) = x` satisfies `VTask.GrowsPolynomially (fun x => x)`, because for any `b ∈ (0,1)` and `u ∈ [b·x, x]` we have `b·x ≤ u ≤ x`, so `c₁ = b` and `c₂ = 1` work.

- Claim: The natural logarithm `Real.log` satisfies `VTask.GrowsPolynomially Real.log`; indeed for large `x` and `u ∈ [b·x, x]`, the ratio `log(u)/log(x)` is sandwiched between positive constants depending on `b`.

- Claim: A constant function `f(x) = c` (for any fixed `c : ℝ`) satisfies `VTask.GrowsPolynomially (fun _ => c)`, since `c₁ = c₂ = 1` trivially works (it is even asymptotically equivalent to a constant).

- Claim: If `VTask.GrowsPolynomially f` and `VTask.GrowsPolynomially g`, then `VTask.GrowsPolynomially (fun x => f x * g x)` — the class is closed under pointwise products.

- Claim: If `VTask.GrowsPolynomially f` and `f` is eventually non-negative, then for any `p : ℝ`, `VTask.GrowsPolynomially (fun x => (f x) ^ p)` — the class is closed under real powers of eventually non-negative members.

## Boundaries

- The condition is vacuously satisfiable by functions that are eventually constant or asymptotically equivalent to a constant.
- The predicate only speaks about eventual behaviour (via a filter), so the values of `f` on any bounded initial segment are irrelevant.
- If `f` oscillates so that values at nearby points differ by unbounded multiplicative factors, the predicate fails; e.g., rapidly oscillating or superexponentially growing functions generically fail.
- The constants `c₁` and `c₂` are permitted to depend on the ratio `b`, so the predicate does not require a single pair of constants to work uniformly for all `b`.
- There is no requirement that `f` be measurable, continuous, or monotone; the predicate is purely pointwise-asymptotic.

## Not to be confused with

- **Polynomial growth / `Asymptotics.IsBigO`**: `f = O(xⁿ)` means `f` is bounded by a polynomial; `GrowsPolynomially` says nothing about an absolute polynomial bound, only about relative stability of `f` on sub-proportional intervals.
- **`Asymptotics.IsTheta`**: `f =Θ g` compares two functions globally; `GrowsPolynomially` is an intrinsic self-comparison on scaled sub-intervals, not a comparison between two distinct functions.
- **Regularly varying functions**: regular variation (in the sense of Karamata) is a related but distinct notion; regular variation of index `ρ` implies `GrowsPolynomially`, but `GrowsPolynomially` does not require the existence of a definite index or a limit of `f(tx)/f(x)` as `x → ∞`.
