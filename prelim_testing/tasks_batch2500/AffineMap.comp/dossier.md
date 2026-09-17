## VTask.comp

### Object

`VTask.comp` is the composition of two affine maps. Given an affine map `f` from affine space `P2` to `P3` and an affine map `g` from `P1` to `P2` (all over a common ring `k`), it produces the affine map from `P1` to `P3` that first applies `g` and then applies `f`. The result is itself an affine map: its underlying function is the ordinary function composition `f ∘ g`, and its linear part is the composition of the respective linear parts of `f` and `g`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {k : Type u_1} -> {V1 : Type u_2} -> {P1 : Type u_3} -> {V2 : Type u_4} -> {P2 : Type u_5} -> {V3 : Type u_6} -> {P3 : Type u_7} -> [Ring k] -> [AddCommGroup V1] -> [Module k V1] -> [AddTorsor V1 P1] -> [AddCommGroup V2] -> [Module k V2] -> [AddTorsor V2 P2] -> [AddCommGroup V3] -> [Module k V3] -> [AddTorsor V3 P3] -> (f : P2 →ᵃ[k] P3) -> (g : P1 →ᵃ[k] P2) -> P1 →ᵃ[k] P3
<!-- PINNED-SIGNATURE:END -->


The implicit type arguments `k`, `V1`, `P1`, `V2`, `P2`, `V3`, `P3` fix, respectively, the scalar ring and the three pairs of translation vector spaces and their corresponding affine spaces. The typeclass arguments supply the necessary algebraic structures (ring, module, and torsor instances). The explicit argument `f` is the outer affine map (applied second), going from `P2` to `P3`. The explicit argument `g` is the inner affine map (applied first), going from `P1` to `P2`.

### Conventions

The argument order follows the usual mathematical convention for composition: `VTask.comp f g` denotes the composite `f ∘ g`, i.e., `g` is applied first and `f` second — matching the order used for ordinary function composition and for `LinearMap.comp`.

### Worked examples

- Claim: For any affine map `g : P1 →ᵃ[k] P2`, composing with the identity on `P2` gives a map whose underlying function equals `g`'s underlying function.

- Claim: If `f : P2 →ᵃ[k] P3` and `g : P1 →ᵃ[k] P2`, then `(VTask.comp f g).linear = f.linear.comp g.linear`.

- Claim: If `f : P2 →ᵃ[k] P3`, `g : P1 →ᵃ[k] P2`, and `h : P0 →ᵃ[k] P1`, then `VTask.comp (VTask.comp f g) h` and `VTask.comp f (VTask.comp g h)` have the same underlying function (associativity of composition).

- Claim: For `f : P2 →ᵃ[k] P3` and `g : P1 →ᵃ[k] P2`, `(VTask.comp f g) p = f (g p)` for every point `p : P1`.

### Boundaries

- `VTask.comp` is defined for any two composable affine maps; there are no domain restrictions beyond the typeclass requirements.
- When either `f` or `g` is a constant affine map (sending every point to a fixed point), the composition is also constant, specifically constant at `f` applied to the constant value of `g`.
- When `g` is the identity affine map on `P2` (i.e., `g = AffineMap.id k P2`), the composition `VTask.comp f g` behaves identically to `f`; symmetrically, `VTask.comp (AffineMap.id k P2) g` behaves identically to `g`.
- The linear part of the composition is always `f.linear ∘ g.linear`; if either linear part is zero, the composition's linear part is also zero.

### Not to be confused with

- `AffineMap.id`: the identity affine map — a special case, not a composition.
- `LinearMap.comp`: composition of linear (not affine) maps — ignores translation components entirely.
- Function composition `f ∘ g` applied directly to affine maps: yields a bare function, not a bundled `AffineMap` with a verified linear part and `map_vadd` property.