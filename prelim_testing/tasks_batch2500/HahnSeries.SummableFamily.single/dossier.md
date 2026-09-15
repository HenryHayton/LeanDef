## VTask.single

### Object

A `SummableFamily` over an index type `ι` that concentrates a single Hahn series `x` at a chosen index `i`. Every index other than `i` contributes the zero Hahn series, and only the index `i` contributes `x`. The construction packages the family together with the two structural conditions required of a summable family: that the union of the supports of all member series is partially well-ordered, and that for each group element `g`, only finitely many indices have `g` in the support of their series.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.single : {Γ : Type u_1} -> {R : Type u_3} -> [PartialOrder Γ] -> [AddCommMonoid R] -> {ι : Type u_7} -> [DecidableEq ι] -> (i : ι) -> (x : HahnSeries Γ R) -> HahnSeries.SummableFamily Γ R ι
<!-- PINNED-SIGNATURE:END -->


```
VTask.single : {Γ : Type u_1} -> {R : Type u_3} -> [PartialOrder Γ] -> [AddCommMonoid R] -> {ι : Type u_7} -> [DecidableEq ι] -> (i : ι) -> (x : HahnSeries Γ R) -> HahnSeries.SummableFamily Γ R ι
```

`Γ` is the totally ordered (in practice, partially well-ordered) group of exponents; `R` is the coefficient ring (additive commutative monoid); `ι` is the index type over which the family is indexed; `i` is the distinguished index at which the series is placed; `x` is the Hahn series that occupies the slot at index `i`.

### Conventions

At every index `j ≠ i`, the family evaluates to the zero Hahn series; equality on `ι` is decided by the `DecidableEq ι` instance. When `x` itself is the zero Hahn series, the family is identically zero at every index, including `i`.

### Worked examples

- Claim: The Hahn sum of `VTask.single i x` equals `x` — summing the single-element family recovers exactly the series placed at `i`.

- Claim: For `j ≠ i`, evaluating the family `VTask.single i x` at `j` gives the zero Hahn series — all other slots are zero.

- Claim: The support of `VTask.single i x` as a function `ι → HahnSeries Γ R` is contained in the singleton `{i}` — at most one index contributes a nonzero series.

- Claim: `(VTask.single (0 : ℕ) (1 : HahnSeries ℕ ℤ)).hsum = 1` — the hsum of the family consisting solely of the Hahn series `1` at index `0` is `1`.

### Boundaries

- When `x = 0`, the resulting `SummableFamily` is the all-zeros family; every structural condition is trivially satisfied and the hsum is `0`.
- When `ι` is the empty type, no valid `i` can be supplied, so the construction is vacuously inapplicable; the type signature enforces this by requiring `i : ι`.
- The `DecidableEq ι` instance is essential to define which indices carry `x` versus zero; the construction is parametric in this instance.
- The partial order on `Γ` (together with the PWO hypothesis carried by `x`) is used to verify the union-of-supports PWO condition; no stronger order assumption is required beyond what `x` itself already satisfies.

### Not to be confused with

- `HahnSeries.single` — places a single coefficient at a single exponent to form one Hahn series, rather than placing one Hahn series at a single index within a family.
- `HahnSeries.SummableFamily.powers` — the summable family consisting of all non-negative powers of a given Hahn series, indexed by `ℕ`; an infinite family rather than a singleton.
- `Finsupp.single` — a finitely-supported function on an index type taking a single nonzero value, which is the underlying combinatorial idea but lives in a different type and context.