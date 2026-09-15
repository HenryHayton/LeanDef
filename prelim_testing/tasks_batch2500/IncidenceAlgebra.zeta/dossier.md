## Object

The zeta function of the incidence algebra over a linearly (or partially) ordered type `α` with coefficients in a type `𝕜` is the element of the incidence algebra that assigns the value `1` to every pair `(a, b)` with `a ≤ b`, and `0` to every pair with `a > b` (equivalently, every pair outside a valid interval). Because the incidence algebra's multiplication is convolution over intervals, left- or right-multiplying any function by the zeta function sums it over the relevant interval. The zeta function is a two-sided inverse of the Möbius function in the incidence algebra, making Möbius inversion available algebraically.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.zeta : (𝕜 : Type u_2) -> {α : Type u_5} -> [Zero 𝕜] -> [One 𝕜] -> [LE α] -> [DecidableLE α] -> IncidenceAlgebra 𝕜 α
<!-- PINNED-SIGNATURE:END -->


VTask.zeta : (𝕜 : Type u_2) -> {α : Type u_5} -> [Zero 𝕜] -> [One 𝕜] -> [LE α] -> [DecidableLE α] -> IncidenceAlgebra 𝕜 α

The first explicit argument `𝕜` is the coefficient type, which must carry both a zero element and a one element; the values of the zeta function are drawn from `𝕜`. The implicit argument `α` is the underlying poset type whose elements serve as the row and column indices of the incidence algebra; it must be equipped with a `≤` relation and a decision procedure for that relation so that the two-branch definition (1 if `a ≤ b`, else 0) can be evaluated.

## Conventions

For any pair `(a, b)` with `¬(a ≤ b)` (i.e., `b < a` or the two elements are incomparable), the zeta function returns `0`; this is the junk value used to ensure the function is a well-typed element of the incidence algebra, which requires every function to return `0` outside valid intervals.

## Worked examples

- Claim: For natural numbers with their usual order, `VTask.zeta ℕ 3 5 = 1` (since `3 ≤ 5`).

- Claim: For natural numbers with their usual order, `VTask.zeta ℕ 5 3 = 0` (since `¬(5 ≤ 3)`).

- Claim: Multiplying the Möbius function on the left by `VTask.zeta 𝕜` yields the multiplicative identity `1` in the incidence algebra, i.e., `mu 𝕜 * VTask.zeta 𝕜 = 1`.

- Claim: On a product poset `α × β`, the value of `VTask.zeta 𝕜` at a pair `((a₁, b₁), (a₂, b₂))` factors as the product of the values on each coordinate: `VTask.zeta 𝕜 (a₁, b₁) (a₂, b₂) = VTask.zeta 𝕜 a₁ a₂ * VTask.zeta 𝕜 b₁ b₂`.

## Boundaries

- When `a = b`, the condition `a ≤ b` holds (by reflexivity of `≤`), so the zeta function returns `1` on the diagonal.
- When `a` and `b` are incomparable (neither `a ≤ b` nor `b ≤ a`), the zeta function returns `0`, since the condition `a ≤ b` fails.
- The self-convolution `VTask.zeta 𝕜 * VTask.zeta 𝕜` evaluated at `(a, b)` equals the cardinality of the closed interval `[a, b]` (when the order is locally finite and `𝕜` is a semiring), reflecting how repeated summation over intervals counts paths through the interval.
- The definition is total over all pairs `(a, b) : α × α`; there is no domain restriction.

## Not to be confused with

- **The Möbius function** (`mu`): this is the two-sided inverse of the zeta function in the incidence algebra, not the zeta function itself; it assigns non-trivial inclusion-exclusion coefficients rather than simply `0` or `1`.
- **The identity element `1` of the incidence algebra**: the identity assigns `1` when `a = b` and `0` otherwise (only the diagonal), whereas the zeta function assigns `1` to all of `a ≤ b`.
- **The Riemann zeta function**: a completely unrelated analytic object; the incidence-algebra zeta function is a combinatorial/algebraic construction on posets.