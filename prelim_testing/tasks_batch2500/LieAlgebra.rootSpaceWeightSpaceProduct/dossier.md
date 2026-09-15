## Object

Given a nilpotent Lie subalgebra `H` of a Lie algebra `L` over a commutative ring `R`, and a Lie module `M` for `L`, this construction produces a canonical `R`-bilinear pairing between the **root space** of `L` for a weight character `χ₁` and the **generalized weight space** of `M` for a character `χ₂`, landing in the generalized weight space of `M` for the sum character `χ₃ = χ₁ + χ₂`. The pairing is given on pure tensors by the Lie bracket action: a root vector `x` (an element of `L` in the root space for `χ₁`) acts on a weight vector `m` (in the weight space for `χ₂`) via `⁅x, m⁆`. This map is not merely `R`-linear but is a **morphism of Lie modules** over `H`, meaning it intertwines the adjoint action of `H` on the tensor product with the action of `H` on the target weight space.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.rootSpaceWeightSpaceProduct : (R : Type u_1) -> (L : Type u_2) -> [CommRing R] -> [LieRing L] -> [LieAlgebra R L] -> (H : LieSubalgebra R L) -> [LieRing.IsNilpotent ↥H] -> (M : Type u_3) -> [AddCommGroup M] -> [Module R M] -> [LieRingModule L M] -> [LieModule R L M] -> (χ₁ χ₂ χ₃ : ↥H → R) -> (hχ : χ₁ + χ₂ = χ₃) -> TensorProduct R ↥(LieAlgebra.rootSpace H χ₁) ↥(LieModule.genWeightSpace M χ₂) →ₗ⁅R,↥H⁆
    ↥(LieModule.genWeightSpace M χ₃)
<!-- PINNED-SIGNATURE:END -->


The type string is inserted automatically below this heading.

- `R` is the base commutative ring over which all structures are defined.
- `L` is the Lie algebra containing the subalgebra `H` and acting on `M`.
- `H` is a nilpotent Lie subalgebra of `L`; nilpotency is essential for the theory of weight spaces.
- `M` is a Lie module for `L` (and hence for `H`), in which the weight spaces live.
- `χ₁` is a linear functional (character) on `H` indexing the root space of `L` being used as the source of root vectors.
- `χ₂` is a linear functional on `H` indexing the generalized weight space of `M` being used as the source of weight vectors.
- `χ₃` is the target character for the generalized weight space in `M` where the products land.
- `hχ` is the proof that `χ₁ + χ₂ = χ₃`, witnessing that the source characters add to the target character.

## Conventions

The map is defined on the tensor product `rootSpace H χ₁ ⊗[R] genWeightSpace M χ₂`, so on pure tensors `x ⊗ₜ m` the output (coerced to `M`) equals the Lie bracket `⁅(x : L), (m : M)⁆`. No junk-value conventions are declared for this definition: it is a total construction and the only nontrivial hypothesis required is the additive compatibility `hχ : χ₁ + χ₂ = χ₃`.

## Worked examples

- Claim: For any root vector `x : rootSpace H χ₁` and weight vector `m : genWeightSpace M χ₂`, the image of `x ⊗ₜ m` under `VTask.rootSpaceWeightSpaceProduct R L H M χ₁ χ₂ (χ₁ + χ₂) rfl` coerces (as an element of `M`) to `⁅(x : L), (m : M)⁆`.

- Claim: When `χ₁ = 0` and `χ₂ = χ`, so `χ₃ = χ`, the map `VTask.rootSpaceWeightSpaceProduct R L H M 0 χ χ (zero_add χ)` takes the tensor product of the zero root space (i.e., `H` itself acting on `L` with eigenvalue `0`) with the `χ`-weight space of `M` into the `χ`-weight space of `M`, reflecting the fact that `H` preserves weight spaces.

- Claim: When `L` is itself the module `M` (so the Lie module action is the adjoint action), the map `VTask.rootSpaceWeightSpaceProduct R L H L χ₁ χ₂ (χ₁ + χ₂) rfl` agrees with the root space product `rootSpaceProduct R L H`, specialising the pairing to multiplication of root vectors within `L`.

## Boundaries

- If `χ₁ = 0` (the zero character), the root space `rootSpace H 0` is the **Cartan subalgebra centraliser** (contains `H`), and the map reduces to the natural action of these elements on weight vectors; the weight space for `χ₂` is preserved.
- If `χ₂ = 0`, the generalized weight space `genWeightSpace M 0` is the `0`-weight space of `M`, and the map carries root vectors to the `χ₁`-weight space.
- The map is defined for all `χ₁`, `χ₂`, `χ₃` with `χ₁ + χ₂ = χ₃`; if no such elements exist in the source spaces (e.g., the root space or weight space is trivial), the map is trivially the zero map.
- The hypothesis `hχ : χ₁ + χ₂ = χ₃` is necessary and cannot be dropped; without it, there is no reason the Lie bracket action lands in any particular weight space.

## Not to be confused with

- `rootSpaceProduct`: the special case of this construction where the module `M` is `L` itself (with the adjoint action), pairing two root spaces of `L` rather than a root space with a weight space of an external module.
- `genWeightSpace`: one of the *source* or *target* objects (a submodule of `M`), not the map itself.
- `LieModule.toEndomorphism`: the action of a single Lie algebra element on a module, which is a plain linear map, not a Lie module morphism on a tensor product of weight spaces.