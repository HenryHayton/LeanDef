## Object

`VTask.mk'` constructs an affine map `P1 →ᵃ[k] P2` between two affine spaces over a ring `k`. An affine map consists of an underlying set-function together with a compatible linear map on the associated translation vector spaces; `VTask.mk'` packages these two pieces together after verifying compatibility at a single chosen base point, rather than requiring the compatibility condition to be checked in full generality up front.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mk' : {k : Type u_1} -> {V1 : Type u_2} -> {P1 : Type u_3} -> {V2 : Type u_4} -> {P2 : Type u_5} -> [Ring k] -> [AddCommGroup V1] -> [Module k V1] -> [AddTorsor V1 P1] -> [AddCommGroup V2] -> [Module k V2] -> [AddTorsor V2 P2] -> (f : P1 → P2) -> (f' : V1 →ₗ[k] V2) -> (p : P1) -> (h : ∀ (p' : P1), f p' = f' (p' -ᵥ p) +ᵥ f p) -> P1 →ᵃ[k] P2
<!-- PINNED-SIGNATURE:END -->


`VTask.mk' : {k : Type u_1} -> {V1 : Type u_2} -> {P1 : Type u_3} -> {V2 : Type u_4} -> {P2 : Type u_5} -> [Ring k] -> [AddCommGroup V1] -> [Module k V1] -> [AddTorsor V1 P1] -> [AddCommGroup V2] -> [Module k V2] -> [AddTorsor V2 P2] -> (f : P1 → P2) -> (f' : V1 →ₗ[k] V2) -> (p : P1) -> (h : ∀ (p' : P1), f p' = f' (p' -ᵥ p) +ᵥ f p) -> P1 →ᵃ[k] P2`

The implicit type arguments `k`, `V1`, `P1`, `V2`, `P2` are the scalar ring, the first translation vector space, the first affine space (a torsor over `V1`), the second translation vector space, and the second affine space respectively. The typeclass arguments supply the algebraic structures. The explicit argument `f` is the underlying set-function from `P1` to `P2`. The argument `f'` is the proposed linear part of the affine map, a `k`-linear map from `V1` to `V2`. The argument `p` is a chosen base point in `P1` at which the affine compatibility is checked. The argument `h` is the proof that for every point `p'` in `P1`, the value of `f` at `p'` equals translating `f p` by the image under `f'` of the displacement vector from `p` to `p'`; this single-basepoint condition is sufficient to determine the full affine structure.

## Conventions

There are no junk-value or edge conventions: `VTask.mk'` is a total constructor and every well-typed input produces a valid affine map.

## Worked examples

- Claim: The underlying function of `VTask.mk' f f' p h` is exactly `f`.
  (That is, coercing the resulting affine map to a bare function recovers `f` definitionally.)

- Claim: The linear part of `VTask.mk' f f' p h` is exactly `f'`.
  (That is, the `.linear` field of the resulting affine map is definitionally equal to `f'`.)

- Claim: Given the identity linear map on a vector space `V` viewed as an affine space over itself, and the base point `0`, the affine map produced by `VTask.mk'` for the identity function with the identity linear part satisfies the affine map identity law for all displacements.

- Claim: Given affine spaces `P1 = P2 = ℝ` (real affine line), setting `f = fun x => 2 * x + 1`, `f' = (2 : ℝ →ₗ[ℝ] ℝ)` (scaling by 2), and base point `p = 0`, with `h` the proof that `f p' = f' (p' - 0) + f 0` for all `p'`, the resulting affine map acts as the affine function `x ↦ 2x + 1`.

## Boundaries

- The verification hypothesis `h` only needs to hold at the single base point `p`; the full affine compatibility `f (v +ᵥ p') = f' v +ᵥ f p'` for all `p'` and `v` is derived from `h` automatically.
- The base point `p` does not appear in the output affine map in any observable way: different choices of `p` (with correspondingly different proofs `h`) produce the same affine map as long as `f` and `f'` agree.
- If `h` is provided for some `p` but `f` and `f'` are not actually compatible as an affine map, the hypothesis `h` simply cannot be proved, so the constructor cannot be abused to produce an invalid affine map.
- There is no restriction on the ring `k`; in particular, it need not be a field or commutative.

## Not to be confused with

- `AffineMap.mk` (the raw record constructor): requires the full compatibility condition `∀ p v, f (v +ᵥ p) = f' v +ᵥ f p` rather than the single-basepoint form.
- `AffineMap.linear`: the projection that extracts the linear part from an already-constructed affine map, as opposed to providing one during construction.
- `LinearMap.mk`: constructs a purely linear map between modules, with no affine (torsor) structure involved.