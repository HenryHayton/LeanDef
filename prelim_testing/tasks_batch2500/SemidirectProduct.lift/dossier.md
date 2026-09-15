## Object

`VTask.lift` constructs a group homomorphism out of a semidirect product `N ⋊[φ] G → H`. Given a group `H` and compatible homomorphisms `fn : N → H` and `fg : G → H` — compatible in the sense that `fn` intertwines the twisting action of `G` on `N` (via `φ`) with the conjugation action of the image of `fg` inside `H` — the lift is the unique group homomorphism whose restriction to the `N`-factor recovers `fn` and whose restriction to the `G`-factor recovers `fg`.

Informally, every element of `N ⋊[φ] G` can be written as a pair `(n, g)`, and the lift sends it to `fn(n) · fg(g)` in `H`. The compatibility condition is exactly what is needed to make this assignment multiplicative.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : {N : Type u_1} -> {G : Type u_2} -> {H : Type u_3} -> [Group N] -> [Group G] -> [Group H] -> {φ : G →* MulAut N} -> (fn : N →* H) -> (fg : G →* H) -> (h : ∀ (g : G), fn.comp (MulEquiv.toMonoidHom (φ g)) = (MulEquiv.toMonoidHom (MulAut.conj (fg g))).comp fn) -> N ⋊[φ] G →* H
<!-- PINNED-SIGNATURE:END -->


`VTask.lift : {N : Type u_1} -> {G : Type u_2} -> {H : Type u_3} -> [Group N] -> [Group G] -> [Group H] -> {φ : G →* MulAut N} -> (fn : N →* H) -> (fg : G →* H) -> (h : ∀ (g : G), fn.comp (MulEquiv.toMonoidHom (φ g)) = (MulEquiv.toMonoidHom (MulAut.conj (fg g))).comp fn) -> N ⋊[φ] G →* H`

- `N`, `G`, `H` are the three underlying groups: `N` is the normal factor, `G` is the complement, and `H` is the target group. All three carry `Group` instances.
- `φ` is the twisting homomorphism from `G` into the automorphism group of `N` that defines which semidirect product `N ⋊[φ] G` is being considered.
- `fn` is the group homomorphism from the normal factor `N` into `H`; it determines where the `N`-component of each semidirect-product element is sent.
- `fg` is the group homomorphism from the complement `G` into `H`; it determines where the `G`-component of each semidirect-product element is sent.
- `h` is the compatibility proof: for every element `g : G`, the homomorphism `fn` composed with the automorphism `φ g` equals conjugation-by-`fg(g)` composed with `fn`. This is the precise condition ensuring that the formula `(n, g) ↦ fn(n) · fg(g)` respects the twisted multiplication of the semidirect product.

## Conventions

There are no junk-value or edge conventions to declare: the definition is a total construction whose output is fully determined by the three inputs `fn`, `fg`, and `h`, with no special treatment of degenerate cases.

## Worked examples

- Claim: When `fn` and `fg` are the canonical inclusions of `N` and `G` into `N ⋊[φ] G` itself (i.e., `inl` and `inr`), the lift is the identity homomorphism on `N ⋊[φ] G`.

- Claim: For any group homomorphism `F : N ⋊[φ] G →* H`, the lift of `F ∘ inl` and `F ∘ inr` equals `F`; that is, every homomorphism out of a semidirect product arises uniquely via `VTask.lift` from its restrictions to the two factors. (This is `lift_unique`.)

- Claim: The composite of `VTask.lift fn fg h` with the canonical inclusion `inl : N →* N ⋊[φ] G` equals `fn`.

- Claim: The composite of `VTask.lift fn fg h` with the canonical inclusion `inr : G →* N ⋊[φ] G` equals `fg`.

## Boundaries

- When `G` is the trivial group, `N ⋊[φ] G` is isomorphic to `N`, and `VTask.lift` reduces to `fn` (the `fg` component is vacuous).
- When `N` is the trivial group, `N ⋊[φ] G` is isomorphic to `G`, and `VTask.lift` reduces to `fg`.
- When `φ` is the trivial action (every `φ g` is the identity automorphism), the semidirect product is a direct product, and the compatibility condition `h` reduces to saying that `fn` and `fg` have commuting images in `H` — which is the standard universal property of a direct product.
- The compatibility condition `h` is not optional: without it, the formula `(n, g) ↦ fn(n) · fg(g)` need not be multiplicative.

## Not to be confused with

- `SemidirectProduct.inl` / `SemidirectProduct.inr`: these are the canonical *inclusions* into `N ⋊[φ] G`, going in the opposite direction (from a factor into the semidirect product, not out of it).
- The direct product universal property (`MonoidHom.prod`): that construction maps out of `N × G` and requires the images of `N` and `G` to commute in `H`; `VTask.lift` handles the twisted case where they need only satisfy the weaker conjugation compatibility.
- `SemidirectProduct.toMul`: a related map that forgets the semidirect product structure entirely, not a homomorphism constructed from given maps on the factors.