## Object

`VTask.atom W a b` is the **elliptic atom** `Wₐ(a, b)` associated with a weight function `W : ℤ → R` on a commutative ring `R`. It is the product of `W` evaluated at two derived integer arguments: one obtained from the half-sum of `a` and `b`, and another from the half-difference. This atom serves as the fundamental building block in the theory of elliptic nets, encoding how the weight function interacts with pairs of integers.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.atom : {R : Type u_1} -> [CommRing R] -> (W : ℤ → R) -> (a b : ℤ) -> R
<!-- PINNED-SIGNATURE:END -->


VTask.atom : {R : Type u_1} -> [CommRing R] -> (W : ℤ → R) -> (a b : ℤ) -> R

- `R` is the underlying commutative ring (inferred implicitly).
- The `CommRing R` instance supplies the ring structure needed for the product.
- `W` is a weight function assigning a ring element to each integer, playing the role of the elliptic net's term sequence.
- `a` and `b` are the two integer indices whose sum and difference (halved via truncated integer division) determine the arguments at which `W` is evaluated.

## Conventions

The definition uses **truncated integer division** (`tdiv`) to compute `(a + b) / 2` and `(a - b) / 2`. This means the result is mathematically meaningful (i.e., yields the intended half-sum and half-difference) only when `a` and `b` have the **same parity** (both even or both odd). When `a` and `b` have different parity, the truncated divisions introduce rounding, and the atom value does not carry the intended geometric meaning; the definition is still total but its output in the mixed-parity case is a junk value.

## Worked examples

- Claim: For `W = id` (the identity function `W n = n` as integers in `ℤ`), `VTask.atom W 3 1 = W 2 * W 1`, i.e., `2 * 1 = 2`.

- Claim: For `W = id` over `ℤ`, `VTask.atom W 4 2 = W 3 * W 1`, i.e., the atom at `(4, 2)` equals `3 * 1 = 3`.

- Claim: For `W = id` over `ℤ`, `VTask.atom W 0 0 = W 0 * W 0 = 0`.

- Claim: `VTask.atom W a b = VTask.atom W b a` whenever `W` is arbitrary, since `(a+b)/2 = (b+a)/2` and `|a-b|/2` appears symmetrically (up to sign, when `W` is even).

## Boundaries

- **Same parity (valid regime):** When `a ≡ b (mod 2)`, both `(a + b)` and `(a - b)` are even, so truncated division by 2 is exact. The atom equals `W((a+b)/2) * W((a-b)/2)` in the usual sense.
- **Different parity (junk-value regime):** When `a` and `b` have different parity, `(a+b)` and `(a-b)` are both odd. Truncated integer division rounds toward zero, so the arguments passed to `W` are off by 1/2 in an integer sense. The result is a well-defined ring element but does not represent a meaningful elliptic atom.
- **`a = b`:** The atom becomes `W(a) * W(0)`, which is zero whenever `W(0) = 0`.
- **`a = 0, b = 0`:** The atom is `W(0) * W(0) = W(0)²`.
- The function is total for all `a, b : ℤ` and all weight functions `W`; no domain restriction is enforced in the type.

## Not to be confused with

- **The elliptic net term `W n` itself:** `VTask.atom` is a *product* of two evaluations of `W`, not a single evaluation.
- **Exact integer division:** The use of truncated (`tdiv`) division means `VTask.atom` does *not* silently assume divisibility; callers must ensure same parity for meaningful results.
- **Symmetric bilinear forms:** Although the atom resembles a quadratic form expression, it is a product in the ring `R`, not an inner product or bilinear pairing.