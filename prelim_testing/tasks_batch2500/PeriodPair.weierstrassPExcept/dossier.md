## VTask.weierstrassPExcept

### Object

The *punctured Weierstrass ℘ sum* attached to a period lattice `L`, obtained by forming the usual Weierstrass ℘ series over `L` but replacing the single term indexed by the lattice point `l₀` with zero. In other words, it is the sum
$$\sum_{\substack{l \in L \\ l \neq l_0}} \left(\frac{1}{(z-l)^2} - \frac{1}{l^2}\right)$$
(where the `l = l_0` term contributes nothing). This auxiliary function is introduced so that computations can safely omit one potentially diverging summand — for instance when `z` coincides with `l₀`, making the `1/(z-l_0)^2` term blow up — while keeping the rest of the lattice sum intact.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.weierstrassPExcept : (L : PeriodPair) -> (l₀ z : ℂ) -> ℂ
<!-- PINNED-SIGNATURE:END -->


The first argument `L` is a period pair, encoding the two fundamental periods that generate the underlying complex lattice `L.lattice`. The second argument `l₀` is the distinguished lattice point whose contribution is suppressed (set to zero). The third argument `z` is the point in the complex plane at which the sum is evaluated.

### Conventions

When `l₀` is not actually a point of the lattice `L.lattice`, the condition `l = l₀` is never satisfied for any summand, so the function coincides exactly with the full Weierstrass ℘ series (minus its principal part at `z = 0`). In particular, the "exception" has no practical effect for non-lattice values of `l₀`.

The term at `l = 0` (when `l₀ ≠ 0`) retains its usual Eisenstein-style correction `1/(z-0)^2 - 1/0^2`; because `1/0^2` is taken to be `0` in Lean's division-by-zero convention for complex numbers, this term reduces to `1/z^2`, matching the standard Weierstrass normalisation for the zero lattice point.

### Worked examples

- Claim: For a period pair `L`, if `l₀` is not in `L.lattice`, then `VTask.weierstrassPExcept L l₀ z` equals the full Weierstrass ℘ sum over all lattice points (with the standard `1/(z-l)^2 - 1/l^2` summands).

- Claim: For a period pair `L`, `VTask.weierstrassPExcept L l₀ l₀` suppresses the otherwise-divergent term `1/(l₀ - l₀)^2 = 1/0^2`, leaving a finite complex-valued sum over all other lattice points.

- Claim: When `l₀ = 0`, the principal-part term `1/z^2` is removed from the sum, so `VTask.weierstrassPExcept L 0 z` equals `∑' l : L.lattice, if l = 0 then 0 else (1/(z-l)^2 - 1/l^2)`, which omits the `1/z^2` singularity entirely.

- Claim: Adding the missing term back, the full Weierstrass ℘ function satisfies `℘(L, z) = VTask.weierstrassPExcept L l₀ z + (1/(z-l₀)^2 - 1/l₀^2)` whenever `l₀` is a nonzero lattice point.

### Boundaries

- **`z` equals `l₀`**: The term that would diverge (`1/(z-l₀)^2`) is exactly the omitted one, so the sum remains finite (convergence depends on the remaining terms, but no explicit infinity is introduced by the missing term).
- **`z` equals some other lattice point `l₁ ≠ l₀`**: The term `1/(z-l₁)^2` is still present and diverges; the function is not finite at such points.
- **`l₀` not in the lattice**: The exception has no effect; the function equals the usual Weierstrass ℘ series.
- **`l₀ = 0`**: The term `1/z^2` is suppressed, removing the standard pole of ℘ at the origin.
- **`z = 0`, `l₀ ≠ 0`**: The `l = 0` summand contributes `1/z^2 - 1/0^2 = 1/z^2 - 0 = 1/z^2`, diverging as usual.

### Not to be confused with

- **The full Weierstrass ℘ function**: That includes every lattice-point summand without exception; `VTask.weierstrassPExcept` deliberately zeros out the `l₀` term.
- **The Weierstrass ζ-function**: A related but distinct lattice sum involving `1/(z-l)` rather than `1/(z-l)^2` terms.
- **A residue or principal-part subtraction**: This object does not subtract a Laurent-series principal part at `l₀`; it replaces the entire `l₀`-indexed summand with zero.