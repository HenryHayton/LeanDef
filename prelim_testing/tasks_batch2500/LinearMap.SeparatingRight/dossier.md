## VTask.SeparatingRight

### Object

A sesquilinear (in particular, bilinear) map `B : M₁ →ₛₗ[I₁] M₂ →ₛₗ[I₂] M` is called **right-separating** if the only element of `M₂` that is orthogonal to every element of `M₁` (under `B`) is zero. Concretely, whenever `B x y = 0` for every `x ∈ M₁`, one must have `y = 0`. In other words, the map has no nonzero right-null vectors: the right radical of `B` is trivial.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SeparatingRight : {R : Type u_1} -> {R₁ : Type u_2} -> {R₂ : Type u_3} -> {M : Type u_5} -> {M₁ : Type u_6} -> {M₂ : Type u_7} -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> [CommSemiring R₁] -> [AddCommMonoid M₁] -> [Module R₁ M₁] -> [CommSemiring R₂] -> [AddCommMonoid M₂] -> [Module R₂ M₂] -> {I₁ : R₁ →+* R} -> {I₂ : R₂ →+* R} -> (B : M₁ →ₛₗ[I₁] M₂ →ₛₗ[I₂] M) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit arguments `R`, `R₁`, `R₂` are the scalar rings, and `M`, `M₁`, `M₂` are the corresponding modules. The ring homomorphisms `I₁ : R₁ →+* R` and `I₂ : R₂ →+* R` specify how scalars act in each argument (making `B` semilinear rather than strictly linear in each variable). The principal argument `B` is the sesquilinear map being tested for the right-separating property.

### Conventions

No special junk-value or out-of-domain conventions are declared: the predicate is a universally quantified `Prop` that is well-defined for every sesquilinear map `B`, with no edge cases requiring separate treatment.

### Worked Examples

- Claim: The canonical evaluation pairing `Dual.eval K V : V →ₗ[K] (V →ₗ[K] K) →ₗ[K] K` (viewed as a bilinear map) is right-separating, because a linear functional annihilated by every vector must be zero.

- Claim: If `B : M₁ →ₛₗ[I₁] M₂ →ₛₗ[I₂] M` satisfies `VTask.SeparatingRight B`, then the flipped map `B.flip : M₂ →ₛₗ[I₂] M₁ →ₛₗ[I₁] M` is left-separating (i.e., `B.flip.SeparatingLeft` holds).

- Claim: For a reflexive bilinear form `B : M →ₗ[R] M →ₗ[R] M₁`, `B` is nondegenerate if and only if it is right-separating.

- Claim: `VTask.SeparatingRight B` is equivalent to the kernel of the flipped map `B.flip` being the zero submodule (i.e., `LinearMap.ker B.flip = ⊥`).

### Boundaries

- The zero map is **not** right-separating when `M₂` is nontrivial, since every element of `M₂` is mapped to zero by every `x`, yet nonzero elements exist.
- When `M₂` is the zero module, every map is vacuously right-separating (there is no nonzero `y` to witness a failure).
- The property is purely about right null-vectors; a map can be right-separating without being left-separating, and vice versa, unless additional symmetry hypotheses (e.g., reflexivity) are assumed.
- For a finite-dimensional bilinear form represented by a matrix, right-separating is equivalent to the matrix having nonzero determinant.

### Not to be confused with

- `LinearMap.SeparatingLeft`: the analogous condition on the *left* argument — the only `x ∈ M₁` killed by every `y` is zero; left- and right-separating are generally independent conditions.
- `LinearMap.Nondegenerate`: requires *both* left- and right-separation simultaneously; coincides with right-separating only under reflexivity hypotheses.
- `LinearMap.IsOrtho`: a relation between two specific elements, not a global property of the map.