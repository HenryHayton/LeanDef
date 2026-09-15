## VTask.twoCochain

### Object

The Lie algebra 2-cochains over a Lie algebra `L` with coefficients in a representation module `M` form a distinguished subspace of all `R`-bilinear maps `L × L → M` (presented as `R`-linear maps `L →ₗ[R] L →ₗ[R] M`). Specifically, a bilinear map `c : L → L → M` is a 2-cochain if and only if it is **alternating**: `c(x, x) = 0` for every `x ∈ L`. Equivalently (over any ring where `2` is a unit, and more generally as a consequence of alternating), such cochains satisfy `c(x, y) = −c(y, x)`. The collection of all such alternating bilinear maps is an `R`-submodule of the full space of `R`-bilinear maps `L → L → M`, and `VTask.twoCochain` is precisely that submodule.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.twoCochain : (R : Type u_1) -> [CommRing R] -> (L : Type u_2) -> [LieRing L] -> [LieAlgebra R L] -> (M : Type u_3) -> [AddCommGroup M] -> [Module R M] -> Submodule R (L →ₗ[R] L →ₗ[R] M)
<!-- PINNED-SIGNATURE:END -->


`VTask.twoCochain : (R : Type u_1) -> [CommRing R] -> (L : Type u_2) -> [LieRing L] -> [LieAlgebra R L] -> (M : Type u_3) -> [AddCommGroup M] -> [Module R M] -> Submodule R (L →ₗ[R] L →ₗ[R] M)`

The first argument `R` is the commutative ring of scalars over which everything is linear. The second argument `L` is the Lie algebra whose elements serve as the inputs to the cochains. The third argument `M` is the coefficient module — the target abelian group (an `R`-module) in which cochain values live. All algebraic structure arguments (`CommRing`, `LieRing`, `LieAlgebra`, `AddCommGroup`, `Module`) are instance parameters supplying the required operations and axioms.

### Conventions

There are no declared junk-value or boundary conventions: the submodule is defined for all valid combinations of `R`, `L`, and `M` satisfying the typeclass constraints, and the alternating condition `c x x = 0` is stated uniformly for all `x ∈ L` with no special cases.

### Worked examples

- Claim: The zero map `(0 : L →ₗ[R] L →ₗ[R] M)` belongs to `VTask.twoCochain R L M`, since `0(x)(x) = 0` for all `x`.

- Claim: If `c` and `d` are both elements of `VTask.twoCochain R L M` (i.e., both alternating), then their sum `c + d` is also in `VTask.twoCochain R L M`, because `(c + d)(x)(x) = c(x)(x) + d(x)(x) = 0 + 0 = 0`.

- Claim: If `c ∈ VTask.twoCochain R L M` and `r : R`, then `r • c ∈ VTask.twoCochain R L M`, since `(r • c)(x)(x) = r • c(x)(x) = r • 0 = 0`.

- Claim: A map `c : L →ₗ[R] L →ₗ[R] M` that satisfies `c x x ≠ 0` for some `x` does **not** belong to `VTask.twoCochain R L M`.

### Boundaries

- When `L` is the trivial (zero) Lie algebra, every bilinear map is trivially alternating, so `VTask.twoCochain R L M` equals the entire space `L →ₗ[R] L →ₗ[R] M`.
- When `M` is the trivial module (i.e., `M = 0`), every bilinear map takes value `0`, so every map is alternating and `VTask.twoCochain R L M` is again the whole (trivial) space.
- The condition `c x x = 0` is required for **all** `x ∈ L`; it is not sufficient to check it on a generating set unless one additionally uses bilinearity arguments.
- Over a ring where `2` is not invertible (e.g., a ring of characteristic 2), alternating (`c x x = 0`) is strictly stronger than antisymmetric (`c x y = −c y x`), and the submodule correctly uses the alternating condition.

### Not to be confused with

- **All bilinear maps `L →ₗ[R] L →ₗ[R] M`**: the full ambient module, without the alternating restriction; `VTask.twoCochain R L M` is a proper submodule whenever there exist non-alternating maps.
- **Lie algebra 1-cochains**: linear maps `L →ₗ[R] M`, which form the analogous submodule one degree lower in the cochain complex.
- **Antisymmetric bilinear maps (`c x y = −c y x`)**: over rings of characteristic 2 these differ from alternating maps; the 2-cochains here use the strictly alternating condition.
