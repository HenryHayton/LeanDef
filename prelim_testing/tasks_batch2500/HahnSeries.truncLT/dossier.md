## Object

`VTask.truncLT c` is the truncation-below-`c` operator on Hahn series: given a Hahn series `x` over an ordered index type `Γ` with coefficients in a type `R` carrying a zero, it returns a new Hahn series whose coefficient at index `i` equals that of `x` when `i < c`, and equals zero otherwise. In other words, it keeps only the "lower" part of the series—the terms whose index is strictly less than `c`—and kills everything at or above `c`. The construction is natural with respect to zero: the zero series maps to the zero series, so the whole thing packages as a zero-preserving map (a `ZeroHom`) from Hahn series to Hahn series.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.truncLT : {Γ : Type u_1} -> {R : Type u_3} -> [Zero R] -> [PartialOrder Γ] -> [DecidableLT Γ] -> (c : Γ) -> ZeroHom (HahnSeries Γ R) (HahnSeries Γ R)
<!-- PINNED-SIGNATURE:END -->


`VTask.truncLT : {Γ : Type u_1} -> {R : Type u_3} -> [Zero R] -> [PartialOrder Γ] -> [DecidableLT Γ] -> (c : Γ) -> ZeroHom (HahnSeries Γ R) (HahnSeries Γ R)`

The index type `Γ` is the ordered set from which the exponents (indices) of the Hahn series are drawn; it must carry a partial order and a decidable strict-less-than relation so that the truncation threshold can be tested computably. The coefficient type `R` need only carry a zero element (no ring or additive structure is required). The explicit argument `c` is the cutoff index: coefficients at indices strictly below `c` are retained, while those at `c` and above are replaced by zero. The result is a `ZeroHom`, i.e., a bundled zero-preserving map between Hahn series.

## Conventions

The strict inequality `i < c` is used as the retention condition, so the coefficient at the cutoff index `c` itself is zeroed out (not retained). There are no junk-value conventions specific to this definition beyond the standard behavior of `if … then … else 0`: the only "edge" is the behavior at the boundary, and that boundary is strict.

## Worked examples

- Claim: For any Hahn series `x : HahnSeries ℤ ℚ` and any index `i : ℤ` with `i < 3`, `(VTask.truncLT 3 x).coeff i = x.coeff i`.

- Claim: For any Hahn series `x : HahnSeries ℤ ℚ`, `(VTask.truncLT 3 x).coeff 3 = 0` (the coefficient exactly at the cutoff is zeroed out).

- Claim: For any Hahn series `x : HahnSeries ℤ ℚ` and any index `i : ℤ` with `i ≥ 3`, `(VTask.truncLT 3 x).coeff i = 0`.

- Claim: `VTask.truncLT c (0 : HahnSeries Γ R) = 0` for any cutoff `c` (the zero series maps to the zero series, as required by the `ZeroHom` structure).

## Boundaries

- **At the cutoff `i = c`:** The coefficient is zeroed out. The retention condition is *strict* (`i < c`), so `c` itself lies on the "killed" side.
- **Indices far below `c`:** Coefficients are copied verbatim from the input series.
- **Indices far above `c`:** All coefficients are zero in the output.
- **Zero series input:** The output is the zero series, consistent with the `ZeroHom` requirement.
- **Partial order (not total order):** For indices `i` that are incomparable to `c` (neither `i < c` nor `c ≤ i` holds in a partial order), the `<` test fails, so the coefficient at such an incomparable index is zeroed out.
- **Support preservation:** The support of the truncated series is a subset of the support of the original series, so well-partial-orderedness of the support is inherited automatically.

## Not to be confused with

- **`HahnSeries.truncLE` or a `≤`-based truncation:** A hypothetical variant that retains coefficients at indices `i ≤ c` (i.e., keeps the coefficient at the cutoff); `VTask.truncLT` uses strict `<` and kills the coefficient at `c` itself.
- **`HahnSeries.order` or leading-term operations:** Those extract a single distinguished index (the minimum of the support), whereas `VTask.truncLT` modifies an entire series by zeroing a tail.
- **Restriction to a sub-series or submodule:** `VTask.truncLT` returns a full Hahn series (with the same index and coefficient types) rather than a series indexed by a sub-poset; it achieves truncation purely by setting unwanted coefficients to zero.