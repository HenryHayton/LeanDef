## Object

`VTask.inl` is the canonical group homomorphism from `Q` into the (restricted) wreath product `D ≀ᵣ Q`, which sends each element `q ∈ Q` to the pair `(1, q)` — i.e., the element whose first component is the identity function (the trivial element of the direct sum of copies of `D`) and whose second component is `q` itself. It embeds `Q` as the "bottom" or "base" factor of the wreath product.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inl : {D : Type u_1} -> {Q : Type u_2} -> [Group D] -> [Group Q] -> Q →* D ≀ᵣ Q
<!-- PINNED-SIGNATURE:END -->


`VTask.inl : {D : Type u_1} -> {Q : Type u_2} -> [Group D] -> [Group Q] -> Q →* D ≀ᵣ Q`

The type `D` is the fiber group — the group whose copies are permuted. The type `Q` is the acting group — the group that does the permuting. Both `D` and `Q` must carry `Group` instances. The result is a group homomorphism `Q →* D ≀ᵣ Q` encoding the canonical inclusion of `Q` into the wreath product.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total group homomorphism defined for every element of `Q`, including the identity and every product, with no domain restrictions.

## Worked examples

- Claim: For any `q : Q`, `VTask.inl q` equals `⟨1, q⟩` in `D ≀ᵣ Q` — the pair of the trivial fiber element and `q`.

- Claim: `VTask.inl` maps the identity of `Q` to the identity of `D ≀ᵣ Q`, because the first component is the identity of the fiber (the trivial function) and the second is the identity of `Q`.

- Claim: For `q₁ q₂ : Q`, `VTask.inl (q₁ * q₂) = VTask.inl q₁ * VTask.inl q₂`, reflecting that `VTask.inl` is a group homomorphism.

- Claim: `VTask.inl` is injective: if `VTask.inl q₁ = VTask.inl q₂`, then `q₁ = q₂`, since the `Q`-component of `⟨1, q⟩` determines `q` uniquely.

## Boundaries

- When `Q` is the trivial group, `VTask.inl` maps the single element `1` to the identity of `D ≀ᵣ Q`, giving a trivial (but valid) embedding.
- When `D` is the trivial group, the wreath product `D ≀ᵣ Q` reduces essentially to `Q` itself, and `VTask.inl` is an isomorphism in that degenerate case.
- The map is always a split injection: its image is a subgroup of `D ≀ᵣ Q` isomorphic to `Q`, complemented by the normal subgroup of fiber elements.

## Not to be confused with

- The companion map `inr` (or analogous fiber inclusion), which would embed individual fiber elements `D` into `D ≀ᵣ Q` rather than the acting group `Q`.
- The full wreath product element `⟨f, q⟩` for an arbitrary fiber function `f`: `VTask.inl` is specifically the special case where `f = 1` (the identity/trivial fiber element).
- Direct-product or semidirect-product canonical inclusions: the wreath product `D ≀ᵣ Q` is a semidirect product, and `VTask.inl` plays the role of the inclusion of the complement subgroup `Q`, not the normal subgroup.