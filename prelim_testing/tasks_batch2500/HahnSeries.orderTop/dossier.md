## VTask.orderTop

### Object

Given a Hahn series `x` with exponents in a partially ordered type `Γ` and coefficients in a type `R` with a distinguished zero, `VTask.orderTop x` returns an element of `WithTop Γ` that records the *smallest exponent* at which `x` has a nonzero coefficient — or `⊤` when `x` is the zero series. Informally, it is the "order" or "valuation" of the series, lifted to include a top element to handle the zero series gracefully.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.orderTop : {Γ : Type u_1} -> {R : Type u_3} -> [PartialOrder Γ] -> [Zero R] -> (x : HahnSeries Γ R) -> WithTop Γ
<!-- PINNED-SIGNATURE:END -->


`VTask.orderTop : {Γ : Type u_1} -> {R : Type u_3} -> [PartialOrder Γ] -> [Zero R] -> (x : HahnSeries Γ R) -> WithTop Γ`

The implicit type `Γ` is the ordered index type for exponents; it must carry a partial order. The implicit type `R` is the coefficient type, which need only carry a zero element (no ring structure is required). The explicit argument `x` is the Hahn series whose minimal nonzero exponent is being measured.

### Conventions

When `x` is the zero Hahn series (all coefficients are zero), `VTask.orderTop x` is defined to be `⊤`, the distinguished top element of `WithTop Γ`, rather than being left undefined or raising an error.

### Worked examples

- Claim: For the zero Hahn series over any coefficient type and exponent type, `VTask.orderTop 0 = ⊤`.

- Claim: For a single-term Hahn series `single a r` with nonzero coefficient `r`, `VTask.orderTop (single a r) = a` (coerced into `WithTop Γ`).

- Claim: Negating a Hahn series does not change its orderTop: `VTask.orderTop (-x) = VTask.orderTop x` for any `x`.

- Claim: The orderTop of a series with a known nonzero coefficient at exponent `a` satisfies `a ≤ VTask.orderTop (single a r)` (with the inequality in `WithTop Γ`).

### Boundaries

- **Zero series**: `VTask.orderTop` returns `⊤` for the zero series. This is the unique case where the result equals `⊤`; equivalently, `VTask.orderTop x ≠ ⊤` if and only if `x ≠ 0`.
- **Single-term series with nonzero coefficient**: `VTask.orderTop (single a r) = ↑a` exactly when `r ≠ 0`; when `r = 0`, the single-term series is actually the zero series, so `VTask.orderTop` returns `⊤`.
- **Partial vs linear order**: The definition requires only a partial order on `Γ`, but the minimum of the support is well-defined because Hahn series supports are well-founded (well-ordered sets), so the minimum always exists for nonzero series.
- **Embedding of exponents**: Under an order embedding `f : Γ ↪o Γ'`, the orderTop of a pushed-forward series equals `WithTop.map f` applied to the original orderTop.

### Not to be confused with

- `HahnSeries.order`: A version that returns an element of `Γ` (without a `WithTop` wrapper) and requires additional hypotheses to avoid the zero case; `VTask.orderTop` is the `WithTop`-valued variant that handles the zero series uniformly.
- `HahnSeries.addVal`: The additive valuation on Hahn series; by a known theorem it coincides with `VTask.orderTop`, but it is packaged as a valuation morphism rather than a bare function.
- `HahnSeries.leadingCoeff`: The coefficient of the series at the minimal exponent; this is the *value* at the index that `VTask.orderTop` identifies, not the index itself.