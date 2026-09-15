## Object

`VTask.inclusion h` is the canonical inclusion map from a Lie submodule `N` into a larger Lie submodule `N'`, expressed as a morphism of Lie modules (a map that is simultaneously `R`-linear and compatible with the Lie bracket action of `L`). Concretely, it sends each element of `N` to the same element viewed inside `N'`, exploiting the fact that `N ⊆ N'`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inclusion : {R : Type u} -> {L : Type v} -> {M : Type w} -> [CommRing R] -> [LieRing L] -> [AddCommGroup M] -> [Module R M] -> [LieRingModule L M] -> {N N' : LieSubmodule R L M} -> (h : N ≤ N') -> ↥N →ₗ⁅R,L⁆ ↥N'
<!-- PINNED-SIGNATURE:END -->


`VTask.inclusion : {R : Type u} -> {L : Type v} -> {M : Type w} -> [CommRing R] -> [LieRing L] -> [AddCommGroup M] -> [Module R M] -> [LieRingModule L M] -> {N N' : LieSubmodule R L M} -> (h : N ≤ N') -> ↥N →ₗ⁅R,L⁆ ↥N'`

The ambient commutative ring `R` provides the scalar structure; `L` is the Lie ring acting on the module; `M` is the ambient additive commutative group equipped with an `R`-module structure and a compatible `L`-action. The two Lie submodules `N` and `N'` of `M` are the source and target, respectively. The proof `h` witnesses that `N` is contained in `N'` (i.e., `N ≤ N'` in the lattice of Lie submodules), and this containment is precisely what allows the inclusion to be well-defined.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a total function whose output is fully determined whenever a valid proof `h : N ≤ N'` is supplied, and the only meaningful edge case (equality `N = N'`) is handled naturally—the inclusion is then the identity morphism on the coerced type.

## Worked examples

- Claim: For any Lie submodule `N` and proof `h : N ≤ N`, applying `VTask.inclusion h` to an element `⟨x, hx⟩ : ↥N` yields the element `⟨x, hx⟩ : ↥N` (viewed in `N` itself), i.e., the map acts as the identity on underlying elements.

- Claim: If `N ≤ N'` and `x : ↥N`, then `(VTask.inclusion h x : M) = (x : M)` — the inclusion map does not change the underlying element of `M`.

- Claim: `VTask.inclusion h` is injective for any `h : N ≤ N'`, since distinct elements of `N` map to distinct elements of `N'`.

## Boundaries

- When `N = N'`, `h` is the reflexivity proof `le_refl N`, and `VTask.inclusion h` becomes the identity Lie module morphism on `↥N`.
- The map is always injective: if two elements of `N` have the same image in `N'`, they are equal as elements of `M` and hence equal in `N`.
- The morphism is *not* generally surjective unless `N = N'`.
- Although `h` is a proof (hence unique by proof irrelevance), different proofs `h h' : N ≤ N'` yield definitionally equal morphisms.

## Not to be confused with

- `Submodule.inclusion`: the analogous inclusion for plain `R`-submodules, which is only `R`-linear and does not carry the Lie-bracket compatibility that `VTask.inclusion` provides.
- `LieSubmodule.subtype`: the Lie module morphism from `↥N` into the ambient module `M`, rather than into a containing submodule `N'`.
- `LieSubalgebra.inclusion`: a similar construction for Lie subalgebras (subsystems closed under the bracket), not for submodules of a Lie module action.