## VTask.addVal

### Object

This is the canonical additive valuation on the ring of Hahn series `R⟦Γ⟧` (power series with coefficients in a domain `R` and exponents in an ordered cancellative commutative monoid `Γ`). It maps each nonzero Hahn series to its *order* — the smallest exponent at which the series has a nonzero coefficient — and maps the zero series to `⊤` (the formal top element adjoined to `Γ`). The result lives in `WithTop Γ`, which is `Γ` together with an extra element `⊤ > γ` for all `γ ∈ Γ`. The map satisfies all axioms of an additive valuation: it sends `0` to `⊤`, `1` to `0`, respects addition via `v(x + y) ≥ min(v(x), v(y))`, and is additive on multiplication `v(x · y) = v(x) + v(y)`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.addVal : (Γ : Type u_1) -> (R : Type u_2) -> [AddCancelCommMonoid Γ] -> [LinearOrder Γ] -> [IsOrderedCancelAddMonoid Γ] -> [Ring R] -> [IsDomain R] -> AddValuation (HahnSeries Γ R) (WithTop Γ)
<!-- PINNED-SIGNATURE:END -->


The first argument `Γ` is the *exponent type* — the ordered, cancellative, commutative monoid that indexes the coefficients of the Hahn series (e.g., `ℤ`, `ℝ`, or `ℕ`). The second argument `R` is the *coefficient ring*, which must be an integral domain. The remaining arguments are typeclass witnesses supplying the algebraic and order structure on `Γ` (an `AddCancelCommMonoid`, a `LinearOrder`, and an `IsOrderedCancelAddMonoid`) and on `R` (a `Ring` and an `IsDomain`). No value arguments beyond the types and instances are needed; the construction is entirely canonical.

### Conventions

The zero Hahn series is assigned the value `⊤ ∈ WithTop Γ`, which is strictly greater than every element of `Γ`; this follows the usual additive-valuation convention that `v(0) = +∞`.

### Worked examples

- Claim: `VTask.addVal Γ R` evaluated at the zero series equals `⊤` for any valid `Γ` and `R`.

- Claim: `VTask.addVal Γ R` evaluated at the series `1` (the multiplicative identity of `HahnSeries Γ R`) equals `(0 : WithTop Γ)`, i.e., the image of the additive identity of `Γ` in `WithTop Γ`.

- Claim: For nonzero Hahn series `x` and `y`, `VTask.addVal Γ R (x * y) = VTask.addVal Γ R x + VTask.addVal Γ R y`; the valuation is additive on products.

- Claim: For any Hahn series `x` and `y`, `VTask.addVal Γ R (x + y) ≥ min (VTask.addVal Γ R x) (VTask.addVal Γ R y)`; the valuation is ultrametric (non-Archimedean triangle inequality in additive form).

### Boundaries

- **Zero series**: `VTask.addVal Γ R 0 = ⊤`. This is the defining junk/edge convention for additive valuations: zero is sent to the top element.
- **Identity series**: `VTask.addVal Γ R 1 = 0`, where `0` here is the zero of `Γ` embedded in `WithTop Γ`. The identity Hahn series has its sole nonzero coefficient at the additive identity of `Γ`.
- **Product of nonzero series**: Because `R` is a domain, the product of two nonzero Hahn series is nonzero, and `VTask.addVal Γ R (x * y) = VTask.addVal Γ R x + VTask.addVal Γ R y` holds exactly (equality, not just inequality).
- **Sum**: `VTask.addVal Γ R (x + y)` may be strictly greater than `min(v(x), v(y))` when leading terms cancel; it equals `min(v(x), v(y))` when the two leading orders are distinct.

### Not to be confused with

- **`HahnSeries.order`**: The bare function `Γ → ...` returning the smallest exponent of a nonzero series; `VTask.addVal` packages this into a full `AddValuation` structure, adding the `⊤`-valued extension and the valuation axioms.
- **`Valuation` (multiplicative)**: The multiplicative counterpart, where the monoid law is multiplication and zero maps to `0`; `VTask.addVal` is the *additive* version where `0` maps to `⊤` and multiplication of series corresponds to addition of values.
- **`HahnSeries.orderTop`**: The auxiliary `WithTop Γ`-valued function used internally to define the valuation; it agrees with `VTask.addVal` as a plain function but is not itself an `AddValuation` structure.
