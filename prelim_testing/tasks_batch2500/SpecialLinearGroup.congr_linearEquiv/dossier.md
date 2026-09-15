## VTask.congr_linearEquiv

### Object

Given a linear isomorphism `e : V ≃ₗ[R] W` between two `R`-modules, `VTask.congr_linearEquiv e` is the multiplicative isomorphism (group isomorphism) between the special linear groups `SL(R, V)` and `SL(R, W)`. It transports the group of determinant-one automorphisms of `V` to the corresponding group for `W` by conjugation: an element `f ∈ SL(R, V)` is sent to `e ∘ f ∘ e⁻¹` (viewed as an automorphism of `W`), and the inverse direction conjugates by `e⁻¹`. The construction is functorial: it respects composition of linear equivalences and sends the identity equivalence to the identity group isomorphism.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.congr_linearEquiv : {R : Type u_1} -> {V : Type u_2} -> [CommRing R] -> [AddCommGroup V] -> [Module R V] -> {W : Type u_3} -> [AddCommGroup W] -> [Module R W] -> (e : V ≃ₗ[R] W) -> SpecialLinearGroup R V ≃* SpecialLinearGroup R W
<!-- PINNED-SIGNATURE:END -->


The implicit arguments `R`, `V`, `W` are the commutative ring of scalars and the two `R`-modules, respectively, together with their required typeclass instances (`CommRing`, `AddCommGroup`, `Module`). The explicit argument `e` is the linear isomorphism from `V` to `W` along which the conjugation is performed.

### Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total construction well-defined for any linear isomorphism `e`, with no degenerate inputs.

### Worked examples

- Claim: When `e` is the identity linear equivalence on `V`, `VTask.congr_linearEquiv e` equals the identity multiplicative isomorphism on `SpecialLinearGroup R V`.

- Claim: The inverse of `VTask.congr_linearEquiv e` equals `VTask.congr_linearEquiv e.symm`, so the construction respects taking inverses of the underlying linear isomorphism.

- Claim: For composable linear isomorphisms `e : V ≃ₗ[R] W` and `f : W ≃ₗ[R] X`, the composition `(VTask.congr_linearEquiv e).trans (VTask.congr_linearEquiv f)` equals `VTask.congr_linearEquiv (e.trans f)`, establishing functoriality.

- Claim: For `e : V ≃ₗ[R] W`, `f : SpecialLinearGroup R V`, and `x : W`, the value `VTask.congr_linearEquiv e f` applied to `x` equals `e (f (e.symm x))`.

### Boundaries

- When `V = W` and `e` is the identity linear equivalence, `VTask.congr_linearEquiv e` reduces to the trivial automorphism of `SpecialLinearGroup R V`.
- The construction is always an isomorphism (never merely a homomorphism), since a linear equivalence is always invertible; there is no regime in which `e` could be a non-invertible map.
- Membership in the special linear group (determinant equal to 1) is preserved under conjugation by any linear automorphism, so the codomain is correctly `SpecialLinearGroup R W` without additional hypotheses.
- The construction is contravariantly symmetric: `(VTask.congr_linearEquiv e).symm = VTask.congr_linearEquiv e.symm`.

### Not to be confused with

- `Matrix.SpecialLinearGroup.map`: a related construction that transports the special linear group along a ring homomorphism rather than a module isomorphism.
- `MulEquiv.conj`: conjugation isomorphism inside a single group, not between two different special linear groups.
- `LinearEquiv.conj`: the analogous conjugation for the full general linear group (all invertible linear maps), without the determinant-one constraint.