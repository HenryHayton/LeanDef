## VTask.lift

### Object

Given a commutative ring `R`, an `R`-algebra `S`, an ideal `I` of `S`, and an `R`-module `M`, the **cotangent space** of `I` is the quotient `I / I²`. `VTask.lift` produces an `R`-linear map from this cotangent space to `M`, given a linear map `f : I →ₗ[R] M` whose value on any product of two elements of `I` is zero. The condition `f(xy) = 0` for all `x, y ∈ I` is exactly what is needed for `f` to factor through the quotient by `I²`, so the lift is the unique `R`-linear map making the obvious triangle commute.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : {R : Type u} -> [CommRing R] -> {S : Type u_3} -> [CommRing S] -> [Algebra R S] -> {I : Ideal S} -> {M : Type u_4} -> [AddCommGroup M] -> [Module R M] -> (f : ↥I →ₗ[R] M) -> (hf : ∀ (x y : ↥I), f (x * y) = 0) -> I.Cotangent →ₗ[R] M
<!-- PINNED-SIGNATURE:END -->


The implicit argument `R` is the base commutative ring over which everything is linear; it carries a `CommRing` instance. The implicit argument `S` is the ambient commutative ring (an `R`-algebra) containing the ideal. The implicit argument `I` is the ideal of `S` whose cotangent space is being mapped out of. The implicit argument `M` is the target `R`-module. The explicit argument `f` is an `R`-linear map from `I` (regarded as a submodule of `S`) to `M`. The explicit argument `hf` is the vanishing condition: `f` sends every product `x * y`, for `x, y ∈ I`, to zero; this is the precise algebraic condition ensuring `f` factors through `I / I²`.

### Conventions

The construction is well-defined precisely because the vanishing condition `hf` ensures that `f` kills the submodule `I²` inside `I`; without this condition the quotient map would not be well-defined. No junk-value conventions arise: the arguments are constrained by the hypothesis `hf`, so the map is always the canonical factorization.

### Worked examples

- Claim: When `f : I →ₗ[R] M` satisfies the vanishing condition, composing `VTask.lift f hf` with the canonical projection `I.toCotangent : I →ₗ[R] I.Cotangent` recovers `f` exactly, i.e., `VTask.lift f hf ∘ₗ I.toCotangent = f`.

- Claim: `VTask.lift f hf` is surjective if and only if the original map `f : I →ₗ[R] M` is surjective, because every element of `I.Cotangent` is the image of some element of `I` under `toCotangent`.

- Claim: For any element `x : I`, evaluating the lifted map at the cotangent class of `x` gives `VTask.lift f hf (I.toCotangent x) = f x`.

### Boundaries

- If `I = 0`, the cotangent space is trivial and the lift is the zero map regardless of `f`.
- If `I² = I` (e.g., `I` is the unit ideal in a suitable ring), then the cotangent space is zero, and again the lift must be the zero map; in this case any `f` satisfying `hf` is forced to be zero on `I` as well.
- The vanishing condition `hf` is stated for all pairs `(x, y) : I × I`; there is no commutativity assumption exploited — both orders must conceptually vanish (though for commutative `S` they are equivalent).
- The lift is unique: any `R`-linear map `g : I.Cotangent →ₗ[R] M` satisfying `g ∘ₗ I.toCotangent = f` must equal `VTask.lift f hf`, since `toCotangent` is surjective.

### Not to be confused with

- `Ideal.Cotangent` (the type itself, `I / I²` as an `R`-module): `VTask.lift` maps *out of* this type, it does not construct it.
- `Ideal.toCotangent` (the canonical surjection `I →ₗ[R] I.Cotangent`): this maps *into* the cotangent space; `VTask.lift` maps out of it, and the two compose to give back `f`.
- An arbitrary quotient lift (e.g., `Submodule.liftQ`): `VTask.lift` is specifically tailored to the cotangent space construction and includes the vanishing-on-products hypothesis rather than a general kernel condition.
