## Object

`VTask.inl` is the canonical inclusion homomorphism that embeds the normal factor `N` into the semidirect product `N ⋊[φ] G` by sending each element `n ∈ N` to the pair `(n, 1)`, where `1` is the identity of `G`. It is a group homomorphism (a `MonoidHom`) that identifies `N` with the "left slot" of the semidirect product, keeping the `G`-component trivial.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inl : {N : Type u_1} -> {G : Type u_2} -> [Group N] -> [Group G] -> {φ : G →* MulAut N} -> N →* N ⋊[φ] G
<!-- PINNED-SIGNATURE:END -->


`VTask.inl : {N : Type u_1} -> {G : Type u_2} -> [Group N] -> [Group G] -> {φ : G →* MulAut N} -> N →* N ⋊[φ] G`

- `N` is the type of the normal subgroup factor, required to carry a `Group` structure.
- `G` is the type of the complement (acting) subgroup factor, also required to carry a `Group` structure.
- `φ` is the action homomorphism from `G` into the automorphism group of `N` that twists the semidirect product multiplication; it determines which semidirect product is being formed.
- The result is a `MonoidHom` (group homomorphism) from `N` into the semidirect product `N ⋊[φ] G`.

## Conventions

No special junk-value or boundary conventions are declared: the map is defined for every element of `N` and every valid semidirect product `N ⋊[φ] G`; there are no degenerate inputs requiring special treatment.

## Worked examples

- Claim: For any element `n : N`, the image `VTask.inl n` equals the pair `⟨n, 1⟩` in `N ⋊[φ] G`.

- Claim: `VTask.inl` maps the identity `1 : N` to the identity `(1, 1)` of `N ⋊[φ] G`, as required for a group homomorphism.

- Claim: `VTask.inl` is injective: if `VTask.inl n₁ = VTask.inl n₂` then `n₁ = n₂`, since the `N`-components of the two pairs must agree.

- Claim: The image of `VTask.inl` consists precisely of those elements `(n, g) ∈ N ⋊[φ] G` for which `g = 1`.

## Boundaries

- When `φ` is the trivial action (every `g` acts as the identity on `N`), the semidirect product `N ⋊[φ] G` is the direct product `N × G`, and `VTask.inl` becomes the standard left-factor inclusion `n ↦ (n, 1)` in the direct product.
- The map is always injective regardless of the action `φ`, because the first component of `⟨n, 1⟩` uniquely determines `n`.
- When `N` is the trivial group, `VTask.inl` is the unique homomorphism from the trivial group and lands at the identity of `N ⋊[φ] G`.

## Not to be confused with

- The complementary inclusion `VTask.inr : G →* N ⋊[φ] G`, which embeds the acting factor `G` via `g ↦ (1, g)` instead of `n ↦ (n, 1)`.
- The projection `N ⋊[φ] G →* G` that reads off the `G`-component; this is a left inverse of `VTask.inr`, not of `VTask.inl`.
- The canonical left projection `N ⋊[φ] G → N` (if it existed as a homomorphism); note that such a projection is generally not a group homomorphism when the action is nontrivial, so it is not simply the inverse of `VTask.inl`.
