## Object

`VTask.inclusion` is the canonical ring homomorphism that witnesses the inclusion of one subring inside a larger one. Given two subrings `S` and `T` of a common ambient non-associative ring `R` with `S ≤ T` (meaning every element of `S` also belongs to `T`), this construction packages the identity-on-elements map into a genuine ring homomorphism `S →+* T`, where both domain and codomain carry their subring ring structures.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inclusion : {R : Type u} -> [NonAssocRing R] -> {S T : Subring R} -> (h : S ≤ T) -> ↥S →+* ↥T
<!-- PINNED-SIGNATURE:END -->


`VTask.inclusion : {R : Type u} -> [NonAssocRing R] -> {S T : Subring R} -> (h : S ≤ T) -> ↥S →+* ↥T`

The ambient type `R` is the ring in which both subrings live; it is inferred implicitly. The `NonAssocRing` instance supplies the ring structure on `R`. `S` and `T` are the two subrings of `R`, also inferred implicitly from context. The explicit argument `h` is the proof that `S` is a subring of `T` (i.e., every element of `S` belongs to `T`); it is precisely this proof that makes the codomain restriction to `↥T` valid. The result is a ring homomorphism from the subring type of `S` to the subring type of `T`.

## Conventions

No special junk-value or edge conventions are declared for this definition: when `h : S ≤ T` holds, the homomorphism is always well-defined and total, and there are no degenerate inputs requiring a special convention.

## Worked examples

- Claim: For any subring `S` of `R`, the inclusion `VTask.inclusion (le_refl S)` sends each element of `S` to the element with the same underlying value, viewed in `S` itself.

- Claim: For subrings `S ≤ T ≤ U` of a ring `R`, the composition of `VTask.inclusion (h₁ : S ≤ T)` followed by `VTask.inclusion (h₂ : T ≤ U)` equals `VTask.inclusion (le_trans h₁ h₂)` as ring homomorphisms.

- Claim: The underlying function of `VTask.inclusion h` maps an element `⟨x, hx⟩ : ↥S` to the element `⟨x, h hx⟩ : ↥T`; in particular, the coercion to `R` is unchanged by the inclusion.

- Claim: `VTask.inclusion h` is an injective ring homomorphism whenever `S ≤ T`.

## Boundaries

- When `S = T` and `h` is the reflexivity proof `le_refl S`, the resulting homomorphism is an isomorphism (in fact a ring automorphism of `S`), but `VTask.inclusion` still returns a value of type `↥S →+* ↥T` rather than an isomorphism type; no special casing occurs.
- The definition is total: it is valid for every pair of subrings satisfying `S ≤ T`, including the edge case where `S` or `T` is the bottom subring (containing only 0 and 1) or the top subring (all of `R`).
- Because the map acts as the identity on underlying elements of `R`, it is always injective; it need not be surjective unless `S = T`.

## Not to be confused with

- `Subring.subtype`: the ring homomorphism from a single subring `S` into the ambient ring `R` itself, rather than into a larger subring.
- `RingHom.inclusion` (for subalgebras or other sub-objects): analogous constructions for algebras or subsemirings that share the name but operate in different algebraic categories.
- Order-theoretic inclusion `S ≤ T` as a bare set-containment proof: `VTask.inclusion` is the ring-homomorphism package built from that proof, not the proof itself.