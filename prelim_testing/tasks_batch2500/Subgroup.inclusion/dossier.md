## Object

Given a group `G` and two subgroups `H` and `K` of `G` with `H ≤ K` (i.e., every element of `H` is also an element of `K`), `VTask.inclusion h` is the canonical inclusion group homomorphism from `H` to `K`. It sends every element of `H` to the same element viewed as an element of `K`, preserving the group structure. This is the natural embedding that witnesses the containment `H ≤ K` as a morphism in the category of groups.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inclusion : {G : Type u_1} -> [Group G] -> {H K : Subgroup G} -> (h : H ≤ K) -> ↥H →* ↥K
<!-- PINNED-SIGNATURE:END -->


`VTask.inclusion : {G : Type u_1} -> [Group G] -> {H K : Subgroup G} -> (h : H ≤ K) -> ↥H →* ↥K`

The implicit argument `G` is the ambient group. The instance argument supplies the group structure on `G`. The implicit arguments `H` and `K` are subgroups of `G`. The explicit argument `h` is a proof that `H` is contained in `K` (i.e., every element belonging to `H` also belongs to `K`). The result is a group homomorphism from `H` to `K`.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is total on its domain and the behavior is uniformly determined by the containment proof `h`.

## Worked examples

- Claim: For any group `G` and any subgroup `H`, applying `VTask.inclusion (le_refl H)` to an element `x : H` yields an element of `H` with the same underlying value as `x`.

- Claim: For subgroups `H ≤ K ≤ G`, the composite of two inclusion maps `VTask.inclusion h₁₂` and `VTask.inclusion h₂₃` equals `VTask.inclusion (le_trans h₁₂ h₂₃)` as group homomorphisms from `H` to the ambient supergroup.

- Claim: `VTask.inclusion h` is injective for any containment `h : H ≤ K`, since distinct elements of `H` have distinct underlying group elements and the map does not change values.

- Claim: The kernel of `VTask.inclusion h` is the trivial subgroup of `H` for any `h : H ≤ K`.

## Boundaries

- When `H = K` and `h` is the reflexivity proof `le_refl H`, the map `VTask.inclusion h` is the identity homomorphism on `H` (up to the trivial coercion between equal subgroup types).
- The map is always injective (it is an embedding), since it acts as the identity on underlying group elements.
- When `H` is the trivial subgroup `⊥` of `K`, the inclusion is the unique homomorphism from the trivial group into `K`, sending the identity to the identity.
- The map is surjective if and only if `H = K`; in general it need not be surjective.

## Not to be confused with

- `Subgroup.subtype H`: the canonical homomorphism from a subgroup `H` into the ambient group `G` itself, rather than into another subgroup `K`.
- `MonoidHom.id H`: the identity endomorphism on `H`, which is only the same as `VTask.inclusion h` when `H = K` and the proof `h` is reflexivity.
- The set-theoretic inclusion `Set.inclusion h`: a function between the underlying sets (without group homomorphism structure), which is a different object even though it performs the same underlying map.