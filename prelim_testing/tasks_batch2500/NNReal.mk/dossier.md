## Object

`VTask.mk` constructs a nonnegative real number — an element of the type `ℝ≥0` (written `NNReal`) — by bundling together an ordinary real number with a proof that it is nonnegative. The result behaves exactly like the real number `x`, but lives in the type-theoretically distinct world of nonnegative reals, where all values are guaranteed to be `≥ 0`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mk : (x : ℝ) -> (hx : 0 ≤ x) -> NNReal
<!-- PINNED-SIGNATURE:END -->


VTask.mk : (x : ℝ) -> (hx : 0 ≤ x) -> NNReal

The first argument `x` is the underlying real number being wrapped. The second argument `hx` is the proof that `x` is nonnegative; it is the evidence that entitles `x` to be promoted into `ℝ≥0`.

## Conventions

There are no declared junk-value or edge conventions: the constructor is total on its stated domain (any real `x` together with a proof `0 ≤ x`), so no out-of-domain inputs exist and no special fallback values are assigned.

## Worked examples

- Claim: `VTask.mk 3 (by norm_num)` has underlying real value `3`.
  ```lean
  example : (VTask.mk 3 (by norm_num) : NNReal).val = 3 := by norm_num
  ```

- Claim: `VTask.mk 0 (le_refl 0)` is the zero element of `ℝ≥0`.
  ```lean
  example : VTask.mk 0 (le_refl 0) = 0 := by
    ext; simp [VTask.mk]
  ```

- Claim: For a natural number `n`, `VTask.mk (n : ℝ) (Nat.cast_nonneg n)` equals the canonical coercion of `n` to `ℝ≥0`.

- Claim: For `r : ℝ` with `0 ≤ r`, `Real.toNNReal r = VTask.mk r hr`.

## Boundaries

- When `x = 0` and `hx` is the proof `0 ≤ 0`, the result is the zero element `(0 : ℝ≥0)`, which is a valid, ordinary member of the type.
- The nonnegativity proof `hx` is proof-irrelevant: two calls `VTask.mk x h1` and `VTask.mk x h2` with different proofs of the same inequality produce definitionally equal terms.
- There is no upper bound on `x`; any nonnegative real, no matter how large, is accepted.
- The underlying real value is preserved exactly: coercing the result back to `ℝ` recovers `x` definitionally.

## Not to be confused with

- `Real.toNNReal`: converts any real to `ℝ≥0` by clamping negative values to zero; no proof is required but negative inputs silently become `0`, whereas `VTask.mk` requires an explicit nonnegativity proof and never alters the value.
- `ENNReal.ofReal`: lifts a real to the extended nonnegative reals `ℝ≥0∞` (which includes `∞`); unlike `VTask.mk`, the target type admits infinity.
- The anonymous constructor `⟨x, hx⟩` for `{r : ℝ // 0 ≤ r}`: structurally identical but discouraged in favour of `VTask.mk` to avoid unintended reliance on the definitional equality between `ℝ≥0` and its subtype representation.