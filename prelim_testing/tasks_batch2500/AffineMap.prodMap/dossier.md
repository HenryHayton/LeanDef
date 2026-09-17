## Object

`VTask.prodMap` constructs the product of two affine maps. Given an affine map `f : P1 →ᵃ[k] P2` and an affine map `g : P3 →ᵃ[k] P4`, it produces a single affine map on product spaces `P1 × P3 →ᵃ[k] P2 × P4` that acts component-wise: a pair `(p, q)` is sent to `(f(p), g(q))`.

In classical terms: if `f` and `g` are affine maps between affine spaces over a common ring `k`, then `VTask.prodMap f g` is the affine map whose underlying set-theoretic function is `Prod.map f g`, and whose associated linear map is the product of the linear parts of `f` and `g`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prodMap : {k : Type u_1} -> {V1 : Type u_2} -> {P1 : Type u_3} -> {V2 : Type u_4} -> {P2 : Type u_5} -> {V3 : Type u_6} -> {P3 : Type u_7} -> {V4 : Type u_8} -> {P4 : Type u_9} -> [Ring k] -> [AddCommGroup V1] -> [Module k V1] -> [AddTorsor V1 P1] -> [AddCommGroup V2] -> [Module k V2] -> [AddTorsor V2 P2] -> [AddCommGroup V3] -> [Module k V3] -> [AddTorsor V3 P3] -> [AddCommGroup V4] -> [Module k V4] -> [AddTorsor V4 P4] -> (f : P1 →ᵃ[k] P2) -> (g : P3 →ᵃ[k] P4) -> P1 × P3 →ᵃ[k] P2 × P4
<!-- PINNED-SIGNATURE:END -->



The universe-polymorphic type parameters `k`, `V1`/`P1`, `V2`/`P2`, `V3`/`P3`, `V4`/`P4` are inferred automatically; each `Vi` is a vector space (direction space) and `Pi` is the corresponding affine space (a torsor over `Vi`), all over the ring `k`. The instance arguments supply the ring structure on `k`, the module structures on the `Vi`, and the torsor structures linking each `Vi` to its `Pi`. The explicit argument `f` is the first affine map, acting between the affine spaces `P1` and `P2`. The explicit argument `g` is the second affine map, acting between the affine spaces `P3` and `P4`.

## Conventions

No junk-value or edge conventions are declared for this definition: it is a total constructor whose output is well-defined for every valid pair of affine maps, and there are no degenerate input regimes that require a special convention.

## Worked examples

- Claim: Applying `VTask.prodMap f g` to a pair `(p, q)` yields `(f p, g q)` — the map acts coordinate-wise, so the first component of the output depends only on `f` and `p`, and the second only on `g` and `q`.

- Claim: The linear part of `VTask.prodMap f g` is the product linear map of the linear parts of `f` and `g`; concretely, for any vector `(v, w)` in `V1 × V3`, the linear part sends it to `(f.linear v, g.linear w)`.

- Claim: When both `f` and `g` are the identity affine map on their respective spaces, `VTask.prodMap f g` is the identity affine map on the product space.

- Claim: `VTask.prodMap (f₂.comp f₁) (g₂.comp g₁)` equals `(VTask.prodMap f₂ g₂).comp (VTask.prodMap f₁ g₁)` — product distributes over composition of affine maps.

## Boundaries

- The definition is total: it is valid for any pair of affine maps `f` and `g` over the same ring `k`, with no restriction on the spaces or maps involved.
- There is no edge case when the affine spaces are trivial (zero-dimensional): the construction still yields a well-formed affine map on the product of trivial spaces.
- The two affine maps `f` and `g` need not share domain or codomain spaces; the only compatibility requirement is that they share the base ring `k`.

## Not to be confused with

- `AffineMap.comp`: composition of two affine maps in sequence (one after the other), rather than in parallel on a product.
- `LinearMap.prodMap`: the analogous construction for linear maps (not affine maps); lacks the basepoint/torsor structure.
- `AffineMap.fst` / `AffineMap.snd`: the projection affine maps from a product space onto a factor, which are the "inverses" of the pairing rather than a parallel combination.