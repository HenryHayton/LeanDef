## VTask.toDual

### Object

Given a module `M` over a commutative semiring `R` with a chosen basis `b` indexed by a type `ι`, `VTask.toDual b` is the canonical linear map `M →ₗ[R] Dual R M` that sends each basis element `b i` to the corresponding dual basis functional `b.coord i` — that is, the linear functional which evaluates to `1` on `b i` and to `0` on every other basis element `b j` (with `j ≠ i`). On a general element of `M`, the map is extended by linearity. This construction generalises the classical notion of a dual basis from finite-dimensional linear algebra to the full generality of free modules over commutative semirings.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toDual : {R : Type uR} -> {M : Type uM} -> {ι : Type uι} -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> [DecidableEq ι] -> (b : Module.Basis ι R M) -> M →ₗ[R] Module.Dual R M
<!-- PINNED-SIGNATURE:END -->


The implicit arguments fix the universe levels and algebraic context: `R` is the coefficient commutative semiring, `M` is the module being dualised, and `ι` is the index type for the basis. The instances provide the required algebraic structures (`CommSemiring R`, `AddCommMonoid M`, `Module R M`) and decidable equality on the index type (needed to compare basis indices). The explicit argument `b : Module.Basis ι R M` is the chosen basis of `M`; different bases yield different linear maps.

### Conventions

No special junk-value or edge conventions are declared for this definition: it is a total construction valid for any basis of any free module over any commutative semiring, with no edge inputs requiring separate treatment.

### Worked examples

- Claim: For the standard basis of `R` over itself (viewed as a rank-1 free module), `VTask.toDual b` sends the unique basis element to the identity functional, which evaluates to `1` on that element.

- Claim: For the standard basis `b` of `Fin 2 → R` over `R`, applying `VTask.toDual b` to the basis vector `b 0` and then evaluating the resulting functional at `b 1` gives `0`, while evaluating at `b 0` gives `1`.

- Claim: For the standard basis `b` of `Fin 2 → R`, applying `VTask.toDual b` to `b 1` and evaluating at `b 1` gives `1`, and evaluating at `b 0` gives `0`.

- Claim: The map `VTask.toDual b` is `R`-linear (i.e., it respects addition and scalar multiplication), as it is constructed as a linear map `M →ₗ[R] Module.Dual R M`.

### Boundaries

- When `ι` is empty (the trivial zero module), `VTask.toDual b` is the unique linear map from the zero module to its dual, which is also zero; there are no basis elements to specify values on.
- When `R` is a field, `VTask.toDual b` recovers exactly the classical dual basis construction from linear algebra.
- The map is in general not surjective when `M` is infinite-dimensional (i.e., when `ι` is infinite): the image consists of those functionals that are zero on all but finitely many basis elements (i.e., finite linear combinations of dual basis elements), not all linear functionals.
- The map is always injective: distinct elements of `M` are distinguished by some dual basis functional in the image.
- The definition requires `DecidableEq ι` to compare basis indices; this is used internally to define the Kronecker-delta values.

### Not to be confused with

- `Module.Basis.dualBasis`: the indexed family of individual dual basis elements (the *functionals* themselves), rather than the single linear map packaging them together.
- `Module.Dual.eval`: the canonical map going in the *opposite* direction, from `M` into the double dual `Dual R (Dual R M)`, evaluating at a functional.
- `LinearMap.dualMap`: given a linear map `f : M →ₗ[R] N`, its dual/transpose `Dual R N →ₗ[R] Dual R M`; this is post-composition with `f`, not a basis-dependent construction.