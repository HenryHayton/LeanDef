## VTask.fourier

### Object

`VTask.fourier n` is the **n-th Fourier character** (or exponential monomial) on the additive circle `ℝ / (ℤ · T)`. Concretely, it is the function
$$x \mapsto \exp\!\left(\frac{2\pi i\, n\, x}{T}\right)$$
regarded as a bundled continuous map from the circle `AddCircle T` to the complex numbers `ℂ`. The family, indexed by the integer `n`, forms the classical Fourier basis for functions on a circle of period `T`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.fourier : {T : ℝ} -> (n : ℤ) -> C(AddCircle T, ℂ)
<!-- PINNED-SIGNATURE:END -->


`{T : ℝ}` is an implicit real parameter fixing the **period** of the circle; the circle itself is `ℝ / (ℤ · T)` and the exponential oscillates with that period. `n : ℤ` is the **frequency index** (winding number), an arbitrary integer selecting which Fourier character is returned. The result is a bundled continuous map in `C(AddCircle T, ℂ)`, packaging both the function and a proof of its continuity.

### Conventions

The period `T` is a real number and is left entirely unrestricted; the definition is stated for all `T : ℝ`, including `T = 0` and `T < 0`, even though the circle `AddCircle T` degenerates when `T = 0`. No junk-value convention is separately declared for any specific value of `T` or `n`; the definition simply applies the circle map in all cases.

### Worked examples

- Claim: For any period `T` and any integer `n`, `VTask.fourier n` is a continuous map from `AddCircle T` to `ℂ` (it is well-typed as a term of `C(AddCircle T, ℂ)`).

- Claim: Evaluating `VTask.fourier 0` at any point `x : AddCircle T` yields `1 : ℂ`, because `exp(0) = 1`.

- Claim: The pointwise product `(VTask.fourier m) * (VTask.fourier n)` evaluated at a point `x` equals `VTask.fourier (m + n)` evaluated at `x`, reflecting the group homomorphism property `exp(2πimx/T) · exp(2πinx/T) = exp(2πi(m+n)x/T)`.

- Claim: The complex conjugate of `VTask.fourier n` at any point `x` equals `VTask.fourier (-n)` at `x`, since `\overline{\exp(2\pi i n x/T)} = \exp(-2\pi i n x/T)`.

### Boundaries

- **`T = 0`**: The circle `AddCircle 0` is isomorphic to `ℝ` (the subgroup is trivial), and the definition still type-checks; `0 • x = 0` for all `x`, so `VTask.fourier n` in this degenerate case maps every equivalence class to `exp(0) = 1` regardless of `n`. This is a degenerate/junk regime.
- **`n = 0`**: The character `VTask.fourier 0` is the constant function `1` on `AddCircle T` for any period `T`.
- **`n < 0`**: Negative frequency indices give the conjugate characters `exp(-2π i |n| x / T)`; the definition handles all integers uniformly.
- **`T < 0`**: The circle is still well-formed as an additive quotient, and the definition applies; the resulting oscillation period is `|T|` but with reversed orientation.

### Not to be confused with

- **`fourierCoeff f n`**: The Fourier *coefficient* of a function `f`, a scalar computed by integrating `f` against `VTask.fourier (-n)`, not the basis character itself.
- **`Complex.exp` applied to a plain real or complex number**: That is the bare exponential function, not packaged as a continuous map on the circle or parametrized by a period.
- **`toCircle`**: The map from `AddCircle 1` (unit circle) to `circle ⊆ ℂ` used internally; `VTask.fourier` wraps this with scaling by `n` and works for arbitrary period `T`.
