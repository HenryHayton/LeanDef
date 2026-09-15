## VTask.inv

### Object

`VTask.inv n` is the inversion map on the ring `ZMod n`, the integers modulo `n`. It assigns to each element `a : ZMod n` a "pseudo-inverse" `a⁻¹ : ZMod n` with the defining property that `a * a⁻¹ = gcd(val(a), n)` (where `val(a)` is the canonical natural-number representative of `a`). In particular, when `a` is coprime to `n` — equivalently, when `a` is a unit in `ZMod n` — the product `a * a⁻¹` equals `1`, making this a genuine multiplicative inverse. When `a` is not coprime to `n`, the product lands at the gcd rather than at `1`, so this is not a group-theoretic inverse for non-units.

The special case `n = 0` identifies `ZMod 0` with `ℤ`, and the inversion map on integers is the sign function: it sends positive integers to `1`, negative integers to `-1`, and `0` to `0`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inv : (n : ℕ) -> ZMod n → ZMod n
<!-- PINNED-SIGNATURE:END -->


```
VTask.inv : (n : ℕ) -> ZMod n → ZMod n
```

The first argument `n : ℕ` is the modulus determining which ring `ZMod n` is being considered. The second argument is the element of `ZMod n` whose pseudo-inverse is to be computed.

### Conventions

When `n = 0`, the ring `ZMod 0` is identified with `ℤ`, and the inversion map is the integer sign function (`Int.sign`): it maps positive integers to `1`, negative integers to `-1`, and `0` to `0`. When `n ≥ 1`, the inverse of the element `a` is the Bézout coefficient produced by the extended Euclidean algorithm applied to `val(a)` and `n`, reduced modulo `n`. The inverse of `0 : ZMod n` is `0` for every `n`.

### Worked examples

- Claim: In `ZMod 7`, the inverse of `3` is `5`, because `3 * 5 = 15 ≡ 1 (mod 7)`.

- Claim: In `ZMod 6`, the inverse of `2` is `0`, because `gcd(2, 6) = 2 ≠ 1`, so `2 * (2⁻¹) = 2` in `ZMod 6` (not `1`).

- Claim: In `ZMod 5`, the inverse of `4` is `4`, because `4 * 4 = 16 ≡ 1 (mod 5)`.

- Claim: In `ZMod 0` (i.e., `ℤ`), the inverse of `(-3 : ZMod 0)` is `-1`, because `Int.sign (-3) = -1`.

- Claim: `(0 : ZMod n)⁻¹ = 0` for any `n : ℕ`.

### Boundaries

- **`a = 0`**: For every `n`, `(0 : ZMod n)⁻¹ = 0`. The product `0 * 0⁻¹ = 0 = gcd(0, n)`, consistent with the general identity.
- **`n = 0`**: The ring `ZMod 0 ≅ ℤ`, and the inversion map is `Int.sign`. Positive integers invert to `1`, negative integers to `-1`, and `0` to `0`. This does not satisfy `a * a⁻¹ = gcd(|a|, 0) = |a|` in the usual sense of gcd, so the `mul_inv_eq_gcd` identity should be understood in `ZMod 0 = ℤ`.
- **`n = 1`**: `ZMod 1` is the trivial ring with one element `0`, and inversion sends that element to itself.
- **`-1 : ZMod n`**: For all `n`, `(-1)⁻¹ = -1`, since `(-1) * (-1) = 1`.
- **Non-units**: When `gcd(val(a), n) > 1`, `a * a⁻¹ ≠ 1`; the pseudo-inverse exists as an element of `ZMod n` but does not provide a two-sided multiplicative inverse.

### Not to be confused with

- **`ZMod.unitOfCoprime` or `(ZMod n)ˣ`**: The type of actual units (invertible elements) in `ZMod n`; `VTask.inv` is defined for *all* elements, including non-units, while the units type only contains the coprime-to-`n` elements.
- **`Int.sign`**: The integer sign function, which equals `VTask.inv` only in the special case `n = 0`; for positive `n`, inversion uses the extended Euclidean algorithm, not sign.
- **`ZMod.invDFT` / `𝓕⁻`**: The inverse discrete Fourier transform on `ZMod N`-indexed functions, a completely different operation that happens to use the word "inverse" in a Fourier-analytic context.
