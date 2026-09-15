## VTask.prod

### Object

Given two affine maps `f : P1 →ᵃ[k] P2` and `g : P1 →ᵃ[k] P3` sharing the same source affine space `P1` (over a ring `k`), `VTask.prod f g` is the affine map `P1 →ᵃ[k] P2 × P3` that sends each point `p : P1` to the pair `(f p, g p)`. It is the canonical pairing of two affine maps into a product affine space.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {k : Type u_1} -> {V1 : Type u_2} -> {P1 : Type u_3} -> {V2 : Type u_4} -> {P2 : Type u_5} -> {V3 : Type u_6} -> {P3 : Type u_7} -> [Ring k] -> [AddCommGroup V1] -> [Module k V1] -> [AddTorsor V1 P1] -> [AddCommGroup V2] -> [Module k V2] -> [AddTorsor V2 P2] -> [AddCommGroup V3] -> [Module k V3] -> [AddTorsor V3 P3] -> (f : P1 →ᵃ[k] P2) -> (g : P1 →ᵃ[k] P3) -> P1 →ᵃ[k] P2 × P3
<!-- PINNED-SIGNATURE:END -->


The implicit type arguments `k`, `V1`, `P1`, `V2`, `P2`, `V3`, `P3` fix the scalar ring, the three translation vector spaces, and the three affine spaces involved, together with the required algebraic structure instances. The explicit argument `f` is the first component map, taking a point of `P1` to a point of `P2`. The explicit argument `g` is the second component map, taking a point of `P1` to a point of `P3`.

### Conventions

No junk-value or edge-case conventions are declared for this definition: it is a total constructor on well-typed affine maps and every input produces a well-defined affine map with no degenerate regime.

### Worked examples

- Claim: For any two affine maps `f : P1 →ᵃ[k] P2` and `g : P1 →ᵃ[k] P3` and any point `p : P1`, the value of `VTask.prod f g` at `p` equals `(f p, g p)`.

- Claim: The linear part of `VTask.prod f g` is the product of the linear parts of `f` and `g`, i.e., `(VTask.prod f g).linear = f.linear.prod g.linear`.

- Claim: If `f` and `g` are both constant affine maps (sending every point to a fixed point), then `VTask.prod f g` is also a constant map into the product space.

- Claim: `VTask.prod f g` is injective if and only if `f` and `g` together separate points of `P1` (i.e., for each pair of distinct points at least one of `f`, `g` distinguishes them).

### Boundaries

- When `P2` or `P3` is a trivial (one-point) affine space, `VTask.prod f g` reduces essentially to the other component map (up to the trivial factor).
- The definition is well-formed for any ring `k`, including non-commutative rings, as long as the appropriate module and torsor instances exist.
- There is no restriction on the dimensions or cardinalities of the affine spaces involved.

### Not to be confused with

- The affine map `P1 × P2 →ᵃ[k] P3` formed from maps on a *product* source (the "uncurried" direction), which is a distinct construction.
- The linear map analogue `LinearMap.prod`, which pairs two linear maps on a common module; `VTask.prod` is its affine counterpart but operates on affine spaces with basepoints rather than modules.
- The projection maps `AffineMap.fst` and `AffineMap.snd` out of a product affine space, which are the left/right inverses to `VTask.prod` in the appropriate sense.