## Object

`VTask.SeparatingLeft B` is the property that a (semilinear) bilinear map `B : M₁ →ₛₗ[I₁] M₂ →ₛₗ[I₂] M` is *left-separating* (also called *left non-degenerate*): the only element of `M₁` that pairs to zero with every element of `M₂` is the zero vector itself. Equivalently, `B` has a trivial *left radical*: no nonzero `x ∈ M₁` is left-orthogonal to all of `M₂`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SeparatingLeft : {R : Type u_1} -> {R₁ : Type u_2} -> {R₂ : Type u_3} -> {M : Type u_5} -> {M₁ : Type u_6} -> {M₂ : Type u_7} -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> [CommSemiring R₁] -> [AddCommMonoid M₁] -> [Module R₁ M₁] -> [CommSemiring R₂] -> [AddCommMonoid M₂] -> [Module R₂ M₂] -> {I₁ : R₁ →+* R} -> {I₂ : R₂ →+* R} -> (B : M₁ →ₛₗ[I₁] M₂ →ₛₗ[I₂] M) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.SeparatingLeft : {R : Type u_1} -> {R₁ : Type u_2} -> {R₂ : Type u_3} -> {M : Type u_5} -> {M₁ : Type u_6} -> {M₂ : Type u_7} -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> [CommSemiring R₁] -> [AddCommMonoid M₁] -> [Module R₁ M₁] -> [CommSemiring R₂] -> [AddCommMonoid M₂] -> [Module R₂ M₂] -> {I₁ : R₁ →+* R} -> {I₂ : R₂ →+* R} -> (B : M₁ →ₛₗ[I₁] M₂ →ₛₗ[I₂] M) -> Prop`

The ring `R` is the common target semiring of the two scalar rings `R₁` and `R₂`, via ring homomorphisms `I₁` and `I₂` respectively, making `B` a semilinear-bilinear map. The module `M` is the codomain of the bilinear map, while `M₁` and `M₂` are its two input modules. The principal explicit argument `B` is the semilinear bilinear map whose left-separation is being asserted.

## Conventions

No junk-value or edge-case conventions are declared for this predicate: it is a straightforwardly total `Prop`-valued predicate on bilinear maps, well-defined for all inputs without any distinguished junk-value convention.

## Worked examples

- Claim: For a field `K` and a vector space `V`, the evaluation map `Dual.eval K V` (viewed as a bilinear map from `V` to its double dual) is left-separating.

- Claim: If `B : M₁ →ₛₗ[I₁] M₂ →ₛₗ[I₂] M` is left-separating, then the flipped map `B.flip` is right-separating.

- Claim: For a finite-dimensional space over a field, `B.SeparatingLeft` holds if and only if the matrix of `B` with respect to any pair of bases has nonzero determinant.

- Claim: For the zero bilinear map on a nontrivial module, `VTask.SeparatingLeft` does **not** hold, since every element of `M₁` maps everything to `0`, yet there exist nonzero elements in `M₁`.

## Boundaries

- On the zero module `M₁` (i.e., when `M₁` is the trivial module), `VTask.SeparatingLeft B` holds vacuously: the only element of `M₁` is `0`, which trivially satisfies `x = 0`.
- On a trivial (zero) bilinear map `B = 0` and a nontrivial `M₁`, the predicate fails, since every nonzero `x` satisfies `B x y = 0` for all `y` but `x ≠ 0`.
- Left-separation is strictly a one-sided condition: it says nothing about elements of `M₂` being separated by `B(x, -)`. The analogous right-sided condition is `SeparatingRight`.
- When `B` is reflexive (i.e., `B x y = 0 ↔ B y x = 0`), left-separation is equivalent to full non-degeneracy.
- The kernel characterization: `VTask.SeparatingLeft B` is equivalent to the kernel of the linear map `x ↦ B x` (from `M₁` to `M₂ →ₛₗ M`) being the zero submodule.

## Not to be confused with

- `LinearMap.SeparatingRight`: the analogous condition on the *right* argument; `B.SeparatingRight` means no nonzero `y ∈ M₂` is right-orthogonal to all of `M₁`. Related via `B.flip.SeparatingRight ↔ B.SeparatingLeft`.
- `LinearMap.Nondegenerate`: a stronger two-sided condition (both left and right separating); it coincides with `SeparatingLeft` only when `B` is reflexive.
- `LinearMap.ker B = ⊥`: the equivalent kernel formulation, which is a statement about submodules rather than directly a separation property.