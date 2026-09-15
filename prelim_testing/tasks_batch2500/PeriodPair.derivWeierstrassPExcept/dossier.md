## VTask.derivWeierstrassPExcept

### Object

This is a punctured or «term-deleted» version of the derivative of the Weierstrass ℘ function associated with a complex period lattice. The standard derivative of the Weierstrass ℘ function is the series ℘'(z) = −2 ∑_{l ∈ Λ} (z − l)^{−3}, summed over all lattice points l. The object defined here is exactly that series, but with one nominated lattice point l₀ silently replaced by 0, i.e., the term corresponding to l₀ is dropped. The result is a complex-valued function of z that equals ℘'(z) minus the single summand −2/(z − l₀)³ (when l₀ actually belongs to the lattice). The purpose is to isolate or study the divergence at a particular lattice point without carrying the singular term along.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.derivWeierstrassPExcept : (L : PeriodPair) -> (l₀ z : ℂ) -> ℂ
<!-- PINNED-SIGNATURE:END -->


The first argument `L` is a period pair, which encodes the two ℂ-linearly independent complex periods that generate the lattice Λ ⊂ ℂ over which the sum is taken. The second argument `l₀` is the distinguished lattice point (or any complex number) whose corresponding term is to be omitted from the sum; only the term indexed by the lattice element equal to l₀ is suppressed. The third argument `z` is the point in the complex plane at which the punctured sum is evaluated.

### Conventions

If `l₀` is not actually a member of the lattice Λ, then no term is ever suppressed — the condition `l.1 = l₀` is never true — and the function coincides with the full derivative series ℘'(z). If `z` itself equals a lattice point other than l₀, the series contains a divergent term (as in the full ℘'); the function is still formally defined as a tsum (which may take a junk value in Lean whenever the indexed family is not summable), but analytically it should be understood as having a pole there. If `z = l₀`, the term that would have been the most singular near l₀ has been removed, and the remaining sum may be better behaved at that point.

### Worked examples

- Claim: For any period pair `L` and any `l₀`, evaluating `VTask.derivWeierstrassPExcept L l₀ z` at `z = l₀` gives a value from which the −2/(z − l₀)³ pole has been removed, leaving a convergent (finite) contribution from all other lattice points.

- Claim: If `l₀ = 0` (the origin, which is always in the lattice), then `VTask.derivWeierstrassPExcept L 0 z` equals the sum of −2/(z − l)³ over all non-zero lattice points, which is the «reduced» or «punctured-at-0» derivative series familiar in the standard treatment of ℘'.

- Claim: If `l₀` is not in the lattice of `L`, then `VTask.derivWeierstrassPExcept L l₀ z` equals the full Weierstrass ℘' series ∑_{l ∈ Λ} −2/(z − l)³ (since no term is ever zeroed out).

### Boundaries

- When `l₀ ∉ Λ`, the function is identical to the full ℘' series; the exclusion mechanism has no effect.
- When `z` is a lattice point different from `l₀`, the sum contains a term −2/(z − z)³ = −2/0³ which is ∞ or a junk value in ℂ; the tsum is not summable in the analytic sense and Lean's tsum returns a junk value.
- When `z = l₀ ∈ Λ`, the offending term has been zeroed out, and the remaining series is the standard ℘'-without-l₀ sum; its convergence (absolute, locally uniform) follows from standard lattice-sum estimates for exponent 3.
- The function is doubly periodic (with the same periods as L) and meromorphic in z, with poles of order 3 at each lattice point except l₀ (assuming l₀ ∈ Λ).

### Not to be confused with

- The full Weierstrass ℘' derivative (without any term excluded): that includes the l₀ term and has a pole at every lattice point including l₀.
- `WeierstrassPExcept` (the ℘ function itself with the l₀-term missing), which omits one term from the ℘ series rather than from its derivative; the present object is the derivative version.
- The Weierstrass ℘ function (not its derivative), which has poles of order 2 rather than order 3 at lattice points.