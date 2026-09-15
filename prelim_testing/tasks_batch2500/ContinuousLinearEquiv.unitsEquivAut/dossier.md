## VTask.unitsEquivAut

### Object

This is a canonical equivalence (a bijection with explicit inverse) between the group of units of a topological semiring `R` and the group of continuous linear automorphisms of `R` viewed as a module over itself. Concretely, every invertible element `u : Rˣ` gives rise to the continuous `R`-linear automorphism "multiply by `u`", and conversely every continuous `R`-linear automorphism of `R` is determined by the image of `1`, which must be a unit. This equivalence makes precise the classical algebraic fact that `GL₁(R) ≅ Rˣ` in the continuous setting.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.unitsEquivAut : (R : Type u_1) -> [Semiring R] -> [TopologicalSpace R] -> [ContinuousMul R] -> Rˣ ≃ R ≃L[R] R
<!-- PINNED-SIGNATURE:END -->


`VTask.unitsEquivAut : (R : Type u_1) -> [Semiring R] -> [TopologicalSpace R] -> [ContinuousMul R] -> Rˣ ≃ R ≃L[R] R`

The first argument `R` is the topological semiring whose units and continuous self-automorphisms are being compared. The `Semiring R` instance endows `R` with its ring-theoretic structure. The `TopologicalSpace R` instance equips `R` with its topology. The `ContinuousMul R` instance ensures multiplication in `R` is jointly continuous, which is needed so that the map "multiply by `u`" is indeed a continuous linear map. The output is a type-level equivalence (`≃`) whose forward direction sends a unit to its associated continuous linear automorphism, and whose backward direction recovers a unit from a continuous linear automorphism.

### Conventions

No junk-value or boundary conventions are declared: the equivalence is total and every inhabitant of `Rˣ` (respectively `R ≃L[R] R`) maps to a well-defined element on the other side; there are no edge cases that produce canonical defaults or silent identifications.

### Worked examples

- Claim: Applying `VTask.unitsEquivAut R` to the multiplicative identity unit `(1 : Rˣ)` yields the identity continuous linear equivalence on `R`.

- Claim: Applying `VTask.unitsEquivAut R` to a unit `u` and then evaluating at `1 : R` returns the underlying element `↑u : R` (i.e., the automorphism is "multiply by `u`").

- Claim: The inverse direction of `VTask.unitsEquivAut R`, applied to the identity automorphism `ContinuousLinearEquiv.refl R R`, returns the unit `(1 : Rˣ)`.

- Claim: For any two units `u v : Rˣ`, `VTask.unitsEquivAut R (u * v)` equals `(VTask.unitsEquivAut R u).trans (VTask.unitsEquivAut R v)` as continuous linear equivalences (the equivalence is a group homomorphism).

### Boundaries

- The definition requires `R` to be a semiring with a topological space structure and continuous multiplication; it does not require `R` to be commutative or to be a field.
- When `R` is the zero ring (where `0 = 1`), the unit group is trivial and `R ≃L[R] R` likewise has only one element; the equivalence holds trivially.
- The `ContinuousMul` hypothesis is essential: without it, multiplication by a unit need not be a continuous map, so the forward direction of the equivalence would not be well-typed.
- Both directions of the equivalence are explicit and constructive; in particular the inverse of the constructed continuous linear equivalence corresponds to the inverse unit.

### Not to be confused with

- `ContinuousLinearEquiv.refl R R`: this is a single specific element of `R ≃L[R] R` (the identity automorphism), whereas `VTask.unitsEquivAut` is the entire equivalence between `Rˣ` and `R ≃L[R] R`.
- The analogous equivalence for bare (non-topological) linear automorphisms `R ≃ₗ[R] R`: that version ignores continuity and yields a different, coarser bijection.
- `Units.map` applied to the inclusion of continuous linear maps: that gives a group homomorphism into units of an endomorphism monoid, not the equivalence with `R ≃L[R] R`.
