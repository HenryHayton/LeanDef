## VTask.map

### Object

Given a star monoid homomorphism `f : R →⋆* S` between two star monoids, `VTask.map f` is the induced star monoid homomorphism from the unitary subgroup of `R` to the unitary subgroup of `S`. Concretely, it sends each unitary element `u ∈ unitary R` to `f u`, and this lands in `unitary S` because star monoid homomorphisms preserve the unitary condition.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {R : Type u_2} -> {S : Type u_3} -> [Monoid R] -> [StarMul R] -> [Monoid S] -> [StarMul S] -> (f : R →⋆* S) -> ↥(unitary R) →⋆* ↥(unitary S)
<!-- PINNED-SIGNATURE:END -->


The universe-polymorphic types `R` and `S` are the source and target star monoids, equipped with monoid and star-multiplication structures supplied via instance arguments. The explicit argument `f` is the star monoid homomorphism `R →⋆* S` that drives the construction. The result is a star monoid homomorphism `unitary R →⋆* unitary S`, i.e. a homomorphism between the unitary subgroups regarded as star monoids in their own right.

### Conventions

There are no junk-value or edge-case conventions declared for this definition: it is a total construction whose output is always a well-formed star monoid homomorphism, and no inputs fall outside the domain.

### Worked examples

- Claim: For the identity star monoid homomorphism `StarMulHom.id R`, `VTask.map (.id R)` equals the identity star monoid homomorphism on `unitary R`.

- Claim: For composable star monoid homomorphisms `f : R →⋆* S` and `g : S →⋆* T`, `VTask.map (g.comp f)` equals `(VTask.map g).comp (VTask.map f)` — i.e. the construction is functorial.

- Claim: For any `f : R →⋆* S` and any `u : unitary R`, the underlying element of `S` obtained from `VTask.map f u` equals `f u` (the coercion commutes with the map).

- Claim: If `f : R →⋆* S` is injective, then `VTask.map f : unitary R → unitary S` is also injective.

### Boundaries

- When `f` is the identity star monoid homomorphism, `VTask.map f` is the identity on `unitary R`.
- When `f` is a star monoid isomorphism (promoted to a star monoid homomorphism), the result agrees with the equivalence-level construction `mapEquiv` applied to `f`.
- The unitary subgroup is closed under star, so the map respects star: `VTask.map f (star u) = star (VTask.map f u)` for every `u`.
- If `f` is the zero map on a trivial monoid, the construction still produces a well-typed star monoid homomorphism (sending the single unitary element to the single unitary element of the target).

### Not to be confused with

- `Unitary.mapEquiv` — the variant of this construction for star monoid *isomorphisms* `R ≃⋆* S`, which produces an equivalence `unitary R ≃⋆* unitary S` rather than just a homomorphism.
- `Unitary.map_mem` — the bare membership lemma stating that `f r ∈ unitary S` whenever `r ∈ unitary R`; this is a building block used inside `VTask.map`, not the homomorphism itself.
- `Units.map` — the analogous construction for the group of units rather than the subgroup of unitary elements; units and unitary elements coincide in some settings but differ in general.
