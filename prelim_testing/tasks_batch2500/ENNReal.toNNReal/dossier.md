## Object

`VTask.toNNReal` is the canonical projection from the extended non-negative reals `ℝ≥0∞` (which includes a formal point at infinity, written `⊤`) down to the ordinary non-negative reals `ℝ≥0`. When the input is a genuine finite non-negative real value it returns that value; when the input is `⊤` (infinity), it returns the junk value `0`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toNNReal : ENNReal → NNReal
<!-- PINNED-SIGNATURE:END -->


The single argument is an element of the extended non-negative reals `ℝ≥0∞`, i.e. either a finite non-negative real or the symbol `⊤` representing positive infinity.

## Conventions

When the input is `⊤` (positive infinity), which has no counterpart in `ℝ≥0`, the function returns `0 : ℝ≥0` as a conventional junk value.

## Worked examples

- Claim: `VTask.toNNReal ⊤ = 0` — infinity maps to the junk value `0`.

- Claim: For any finite value `r : ℝ≥0`, `VTask.toNNReal (r : ℝ≥0∞) = r` — a finite non-negative real is returned unchanged.

- Claim: `VTask.toNNReal 0 = 0` — zero (a finite value) maps to `0 : ℝ≥0`.

- Claim: `VTask.toNNReal 5 = 5` — the finite value `5` is returned unchanged as an element of `ℝ≥0`.

## Boundaries

- **Input `⊤`:** There is no finite non-negative real that represents infinity, so `⊤` is sent to `0` by convention. This is the only point where information is lost.
- **Input `0`:** The finite value `0 : ℝ≥0∞` maps to `0 : ℝ≥0`; there is no ambiguity with the junk value since the junk value also happens to be `0`, but this case is genuinely finite.
- **Injectivity:** The function is injective on finite values but not globally injective, since both `⊤` and `(0 : ℝ≥0∞)` produce `0 : ℝ≥0`.
- **Range:** Every element of `ℝ≥0` is in the range (each `r : ℝ≥0` is the image of the coercion `(r : ℝ≥0∞)`).

## Not to be confused with

- **`ENNReal.toReal`**: Projects `ℝ≥0∞` to `ℝ` (not `ℝ≥0`), also sending `⊤` to `0`.
- **`ENNReal.ofNNReal` / the coercion `ℝ≥0 → ℝ≥0∞`**: The reverse direction, embedding `ℝ≥0` into `ℝ≥0∞`; this is a left inverse of `VTask.toNNReal` on finite inputs.
- **`NNReal.toReal`**: Projects `ℝ≥0` to `ℝ`, a different (injective) map that does not involve `⊤` at all.
