## VTask.inclusion

### Object

Given two Lie ideals `I₁` and `I₂` of a Lie algebra `L` over a commutative ring `R`, with `I₁` contained in `I₂`, this is the canonical inclusion map from `I₁` into `I₂` viewed as a morphism of Lie algebras (a Lie algebra homomorphism over `R`). It sends each element of `I₁` to the same element regarded as a member of the larger ideal `I₂`, and it is compatible with both the `R`-module structure and the Lie bracket.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inclusion : {R : Type u} -> {L : Type v} -> [CommRing R] -> [LieRing L] -> [LieAlgebra R L] -> {I₁ I₂ : LieIdeal R L} -> (h : I₁ ≤ I₂) -> ↥I₁ →ₗ⁅R⁆ ↥I₂
<!-- PINNED-SIGNATURE:END -->


`VTask.inclusion : {R : Type u} -> {L : Type v} -> [CommRing R] -> [LieRing L] -> [LieAlgebra R L] -> {I₁ I₂ : LieIdeal R L} -> (h : I₁ ≤ I₂) -> ↥I₁ →ₗ⁅R⁆ ↥I₂`

`R` is the commutative ring of scalars. `L` is the ambient Lie algebra over `R`. `I₁` and `I₂` are Lie ideals of `L`. The argument `h` is the proof (or witness) that `I₁` is a sub-ideal of `I₂`, i.e., every element of `I₁` belongs to `I₂`. The result is the Lie algebra morphism from `I₁` (as a Lie algebra in its own right) to `I₂` (as a Lie algebra in its own right) that performs this inclusion.

### Conventions

There are no junk-value or boundary conventions to declare for this definition: it is defined for every pair of Lie ideals `I₁ ≤ I₂` and always produces a legitimate, injective Lie algebra morphism.

### Worked examples

- Claim: For any Lie ideals `I₁ ≤ I₂`, applying `VTask.inclusion h` to an element `x : I₁` gives an element of `I₂` whose underlying value in `L` equals that of `x`.

- Claim: For Lie ideals `I₁ ≤ I₂`, the morphism `VTask.inclusion h` is injective: distinct elements of `I₁` map to distinct elements of `I₂`.

- Claim: For Lie ideals `I₁ ≤ I₂`, applying `VTask.inclusion h` to `x : I₁` yields `⟨x.1, h x.2⟩ : I₂`, i.e., the same underlying element of `L` with the membership proof promoted by `h`.

- Claim: For Lie ideals `I₁ ≤ I₂` and elements `x y : I₁`, the inclusion respects the Lie bracket: `VTask.inclusion h ⁅x, y⁆ = ⁅VTask.inclusion h x, VTask.inclusion h y⁆`.

### Boundaries

- When `I₁ = I₂` (and `h` is the reflexivity proof), `VTask.inclusion h` is the identity Lie algebra morphism on `I₁`.
- The morphism is always injective regardless of which ideals are chosen, as long as `I₁ ≤ I₂`.
- The coercion of `VTask.inclusion h x` back to `L` always equals the coercion of `x` itself to `L`; no information about the element is changed, only the type-level membership witness.
- There is no non-trivial behavior at any boundary: the map is total and well-behaved for all inputs satisfying `I₁ ≤ I₂`.

### Not to be confused with

- `Submodule.inclusion`: The analogous inclusion for submodules (as an `R`-linear map, not a Lie algebra morphism); `VTask.inclusion` additionally preserves the Lie bracket.
- `LieIdeal.incl`: A possible alternative name or a morphism from a Lie ideal into the full ambient Lie algebra `L`; `VTask.inclusion` maps between two ideals, not from an ideal to `L` itself.
- `LieAlgebra.ofEq`: A re-indexing isomorphism for Lie algebras when two types are propositionally equal, which is conceptually different from the inclusion between two ideals related by `≤`.
