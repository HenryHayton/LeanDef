## Object

`VTask.mk'` constructs an affine equivalence (a bijective affine map together with its inverse) between two affine spaces `P₁` and `P₂` over a ring `k`, given only: a set-theoretic map `e`, a linear equivalence `e'` serving as the underlying linear part, a single base point `p`, and a proof that the affine-translation formula holds at that base point for all other points. In other words, it packages an affine bijection from first principles, checking the affine linearity condition via the formula `e p' = e'(p' -ᵥ p) +ᵥ e p` rather than requiring it to be separately verified for the inverse.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mk' : {k : Type u_1} -> {P₁ : Type u_2} -> {P₂ : Type u_3} -> {V₁ : Type u_6} -> {V₂ : Type u_7} -> [Ring k] -> [AddCommGroup V₁] -> [AddCommGroup V₂] -> [Module k V₁] -> [Module k V₂] -> [AddTorsor V₁ P₁] -> [AddTorsor V₂ P₂] -> (e : P₁ → P₂) -> (e' : V₁ ≃ₗ[k] V₂) -> (p : P₁) -> (h : ∀ (p' : P₁), e p' = e' (p' -ᵥ p) +ᵥ e p) -> P₁ ≃ᵃ[k] P₂
<!-- PINNED-SIGNATURE:END -->


The implicit type arguments `k`, `P₁`, `P₂`, `V₁`, `V₂` are, respectively, the scalar ring, the two affine spaces (source and target), and their associated translation vector spaces. The typeclass arguments supply the ring structure on `k`, the additive group and module structures on `V₁` and `V₂`, and the torsor structures linking each vector space to its affine space.

- `e` is the underlying set-theoretic map from `P₁` to `P₂` that will become the forward direction of the equivalence.
- `e'` is a linear equivalence from `V₁` to `V₂` that serves as the linear part (direction-space action) of the affine equivalence.
- `p` is a chosen base point in `P₁` at which the affine-translation compatibility is anchored.
- `h` is the proof that for every point `p'` in `P₁`, the image `e p'` equals `e'` applied to the displacement `p' -ᵥ p`, then translated by `e p`; this is the defining condition of an affine map witnessed at the base point `p`.

## Conventions

There are no junk-value or edge-case conventions declared for this constructor: it is a total function whose output is fully determined by well-typed inputs, and all relevant structure is enforced by the type system and the supplied proof `h`.

## Worked examples

- Claim: For the identity map on a real affine space, `VTask.mk'` with the identity linear equivalence, any base point, and the trivially-satisfied condition produces an affine equivalence whose underlying function is the identity.

- Claim: The coercion of `VTask.mk' e e' p h` as a function equals `e`, i.e., `⇑(VTask.mk' e e' p h) = e`.

- Claim: The linear part of `VTask.mk' e e' p h` is exactly `e'`, i.e., `(VTask.mk' e e' p h).linear = e'`.

- Claim: The affine equivalence built by `VTask.mk' e e' p h` satisfies, for every `p'`, the equation `(VTask.mk' e e' p h) p' = e' (p' -ᵥ p) +ᵥ e p` (unfolding `h`).

## Boundaries

- The condition `h` only needs to be verified at one base point `p`; the constructor derives the full affine map behaviour everywhere from this single-point check.
- If the map `e` is not actually a bijection consistent with `e'` being its linear part, the types still accept the construction, but the proof `h` will be unprovable; there is no additional runtime check beyond what `h` enforces.
- The base point `p` is not stored in the resulting affine equivalence; it serves only as a witness in the construction. The output is an `AffineEquiv` that is independent of which base point was chosen (as long as `h` holds).
- When `k` is a field and the affine spaces are affine subspaces or finite-dimensional, all the usual affine-equivalence theorems apply to the output without further hypotheses.

## Not to be confused with

- `AffineEquiv.mk` (the raw record constructor): requires specifying the inverse function and all structural axioms directly, rather than deriving them from a single-point affine formula.
- `AffineMap.mk'`: constructs only a (non-invertible) affine map, not an equivalence; there is no inverse or bijectivity guarantee.
- `AffineEquiv.ofEq`: builds an affine equivalence from an equality of affine subspaces, a completely different construction with no linear-equivalence input.