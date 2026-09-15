## VTask.lift

### Object

Given a commutative `R`-algebra `A` equipped with divided powers on an ideal `I`, and a linear map `g : M →ₗ[R] A` whose image lands inside `I`, `VTask.lift` constructs the canonical `R`-algebra homomorphism from the divided power algebra `DividedPowerAlgebra R M` into `A`. It realises the (weak) universal property of the divided power algebra: any linear map from `M` into a divided-power ideal of an `R`-algebra extends uniquely (up to the divided-power structure) to an algebra map out of `DividedPowerAlgebra R M`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : {R : Type u_2} -> {M : Type u_3} -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> {A : Type u_4} -> [CommSemiring A] -> [Algebra R A] -> {I : Ideal A} -> (hI : DividedPowers I) -> (g : M →ₗ[R] A) -> (hg : ∀ (m : M), g m ∈ I) -> DividedPowerAlgebra R M →ₐ[R] A
<!-- PINNED-SIGNATURE:END -->


VTask.lift : {R : Type u_2} -> {M : Type u_3} -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> {A : Type u_4} -> [CommSemiring A] -> [Algebra R A] -> {I : Ideal A} -> (hI : DividedPowers I) -> (g : M →ₗ[R] A) -> (hg : ∀ (m : M), g m ∈ I) -> DividedPowerAlgebra R M →ₐ[R] A

- `R` is the base commutative semiring over which all modules and algebras are defined.
- `M` is the `R`-module whose divided power algebra is being mapped out of.
- `A` is the target commutative `R`-algebra.
- `I` is the ideal of `A` carrying divided powers.
- `hI` is the divided-power structure on `I`; it supplies the operations `dpow n a` for `a ∈ I`.
- `g` is the `R`-linear map from `M` into `A` that initiates the extension.
- `hg` is the proof that every element in the image of `g` belongs to `I`, making divided powers applicable to those elements.

### Conventions

There are no junk-value or out-of-domain conventions to declare: every argument is required and carries genuine mathematical content; the map is total on its stated domain.

### Worked examples

- Claim: When `A = DividedPowerAlgebra R M` itself, `I` is its augmentation ideal, and `g` is the canonical linear inclusion, `VTask.lift hI g hg` is an `R`-algebra endomorphism of `DividedPowerAlgebra R M` that acts as the identity on generators.

- Claim: For `R = ℤ`, `M = ℤ` (free rank-1 module), and `A` any divided-power `ℤ`-algebra with `g(1) ∈ I`, the morphism produced by `VTask.lift` sends the divided-power generator `dp n 1` of `DividedPowerAlgebra ℤ ℤ` to `hI.dpow n (g 1)` in `A`.

- Claim: The composite of `VTask.lift hI g hg` with the canonical `R`-linear map `M → DividedPowerAlgebra R M` (sending `m` to the degree-1 generator `dp 1 m`) equals `g` as `R`-linear maps.

### Boundaries

- If `g` is the zero map, then `hg` is satisfied trivially (since `0 ∈ I` for any ideal), and `VTask.lift` produces the algebra map that sends every divided-power generator `dp n m` to `hI.dpow n 0`, which by the divided-power axiom `dpow_zero` equals `1` for `n = 0` and `0` for `n ≥ 1`.
- The hypothesis `hg` is essential: without knowing `g m ∈ I`, the divided power `hI.dpow n (g m)` is not defined (or may be junk), so the resulting map would not be well-formed with respect to the divided-power axioms.
- The map is an `R`-algebra homomorphism (not merely an `R`-module map), meaning it preserves the ring multiplication and the unit, as well as commuting with the `R`-algebra structure maps.

### Not to be confused with

- `DividedPowerAlgebra.lift'` — an auxiliary or more general variant of the lifting map that may require more explicit data and is used internally to construct `VTask.lift`.
- The free algebra universal property (`MvPolynomial.aeval` or `FreeAlgebra.lift`) — those extend linear maps to algebra maps without any divided-power or ideal membership conditions.
- `DividedPowers.dpow` itself — that is merely the operation giving the `n`-th divided power of a single element in a fixed divided-power ring; `VTask.lift` constructs a global algebra morphism using that operation.
