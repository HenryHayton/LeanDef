## VTask.skewAdjoint

### Object

Given a type `R` equipped with an additive group structure and a star operation (an involution compatible with addition), the **skew-adjoint elements** are those elements `x` of `R` satisfying `star x = -x`. This construction packages all such elements together as an additive subgroup of `R`, meaning the collection is closed under addition, negation, and contains zero, and inherits the ambient group structure.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.skewAdjoint : (R : Type u_1) -> [AddCommGroup R] -> [StarAddMonoid R] -> AddSubgroup R
<!-- PINNED-SIGNATURE:END -->


The sole explicit argument is the ambient type `R`, which carries the elements being classified. The two implicit typeclass arguments supply the necessary algebraic infrastructure: `AddCommGroup R` provides the additive group structure (so that negation and addition are available), and `StarAddMonoid R` equips `R` with a star operation that is compatible with addition (i.e., `star (x + y) = star x + star y` and `star 0 = 0`). The output is the additive subgroup of `R` consisting exactly of the skew-adjoint elements.

### Conventions

There are no declared junk-value or edge conventions for this definition: `VTask.skewAdjoint` is total on its type-theoretic domain and has no inputs that could be "out of range" — every choice of `R` with the required typeclasses yields a well-defined additive subgroup.

### Worked examples

- Claim: The imaginary unit `I` in the complex numbers `ℂ` belongs to `VTask.skewAdjoint ℂ` (since `star I = -I` under complex conjugation).

- Claim: The zero element `0` always belongs to `VTask.skewAdjoint R` for any `R`, because `star 0 = 0 = -0`.

- Claim: An element `x` belongs to `VTask.skewAdjoint R` if and only if `star x = -x`.

- Claim: The sum of two skew-adjoint elements is again skew-adjoint, i.e., if `x` and `y` are in `VTask.skewAdjoint R` then so is `x + y`.

### Boundaries

- **Zero**: The zero element `0 ∈ R` always belongs to `VTask.skewAdjoint R`, since `star 0 = 0` and `-0 = 0`.
- **Negation**: If `x ∈ VTask.skewAdjoint R` then `-x ∈ VTask.skewAdjoint R`; the subgroup is closed under negation.
- **Addition**: If `x, y ∈ VTask.skewAdjoint R` then `x + y ∈ VTask.skewAdjoint R`.
- **Self-adjoint overlap**: In a type where `char R = 2` (so `-x = x`), the self-adjoint and skew-adjoint subgroups coincide.
- **In `ℝ`**: The only real number satisfying `x = -x` is `0`, so `VTask.skewAdjoint ℝ` consists of `{0}` alone (since `star` on `ℝ` is the identity).

### Not to be confused with

- **`selfAdjoint R`**: The additive subgroup of *self-adjoint* elements, where `star x = x` (not `star x = -x`).
- **`LinearMap.BilinForm.skewAdjointSubmodule`**: A related but distinct notion for linear maps relative to a bilinear form, tracking skew-adjointness in the sense `B(f v, w) = -B(v, f w)`.
- **`IsSelfAdjoint`**: A predicate (not a subgroup) asserting `star x = x` for a single element; the skew-adjoint analogue would be `star x = -x` without the subgroup packaging.