## Object

The **order** of a Hahn series `x` over an ordered abelian group (or more generally, a partially ordered type with zero) is defined as follows: if `x` is the zero series, the order is `0`; otherwise, it is the **least element** of the support of `x` — that is, the smallest `γ : Γ` for which the coefficient `x.coeff γ` is nonzero. The support of a nonzero Hahn series is well-founded (by definition of Hahn series), so this minimum always exists.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.order : {Γ : Type u_1} -> {R : Type u_3} -> [PartialOrder Γ] -> [Zero R] -> [Zero Γ] -> (x : HahnSeries Γ R) -> Γ
<!-- PINNED-SIGNATURE:END -->


`VTask.order : {Γ : Type u_1} -> {R : Type u_3} -> [PartialOrder Γ] -> [Zero R] -> [Zero Γ] -> (x : HahnSeries Γ R) -> Γ`

The implicit type `Γ` is the **exponent group** (index type), which carries a partial order and a zero element. The implicit type `R` is the **coefficient type**, which also carries a zero element. The instance `[PartialOrder Γ]` supplies the ordering used to speak of a minimum. The instances `[Zero R]` and `[Zero Γ]` provide the zero elements of coefficients and exponents respectively. The explicit argument `x` is the **Hahn series** whose order is being computed.

## Conventions

The order of the zero Hahn series is defined to be `0 : Γ`, not some distinguished "negative infinity" or undefined value. This is a junk-value convention: since the zero series has empty support and no well-defined minimum, the value `0` is assigned purely for convenience.

## Worked examples

- Claim: `VTask.order (0 : HahnSeries ℤ ℚ) = 0` — the order of the zero series is `0 : ℤ`.

- Claim: For a Hahn series `x : HahnSeries ℤ ℚ` whose only nonzero coefficient is at `γ = 3`, `VTask.order x = 3`. The order picks out `3` as the unique (and hence minimal) element of the support.

- Claim: If `x : HahnSeries ℤ ℚ` has nonzero coefficients at `2` and `5` (and zero elsewhere), then `VTask.order x = 2`, since `2` is the minimum of `{2, 5}`.

- Claim: For any nonzero `x : HahnSeries Γ R`, the coefficient of `x` at `VTask.order x` is nonzero — i.e., `VTask.order x` lies in the support of `x`.

## Boundaries

- **Zero series**: `VTask.order 0 = 0` by the junk-value convention; the empty support has no natural minimum, so `0 : Γ` is returned.
- **Single-term series**: If `x` has exactly one nonzero coefficient at position `γ`, then `VTask.order x = γ`.
- **Minimum of support**: For any nonzero `x`, `VTask.order x` is the *least* element (in the partial order on `Γ`) of the support of `x`. All other elements of the support are `≥ VTask.order x`.
- **Well-foundedness requirement**: The result is well-defined for nonzero series precisely because the support of a Hahn series is required to be well-founded (a defining property of Hahn series), guaranteeing that the minimum exists.

## Not to be confused with

- **`HahnSeries.leadingCoeff`**: the *value* of the coefficient at the order, not the order (exponent) itself.
- **`PowerSeries.order`**: the analogous notion for formal power series over `ℕ`, where the exponent type is `ℕ` and the order is the index of the first nonzero coefficient; the Hahn series version generalises this to arbitrary well-ordered exponent types.
- **`multiplicity` / `emultiplicity`**: valuations or multiplicities of ring elements, which may coincide with `order` in special cases but are conceptually distinct and defined differently.