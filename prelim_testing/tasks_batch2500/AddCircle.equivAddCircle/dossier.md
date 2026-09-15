## Object

A canonical isomorphism of additive abelian groups between two additive circles (quotient groups of a field by a cyclic subgroup) with possibly different non-zero periods. Concretely, it is the group isomorphism `AddCircle p ≃+ AddCircle q` given by rescaling by the ratio `p⁻¹ * q`: it sends a coset representative `x` (in the period-`p` circle) to the coset of `x * (p⁻¹ * q)` in the period-`q` circle, and its inverse does the reverse rescaling by `q⁻¹ * p`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.equivAddCircle : {𝕜 : Type u_1} -> [Field 𝕜] -> (p q : 𝕜) -> (hp : p ≠ 0) -> (hq : q ≠ 0) -> AddCircle p ≃+ AddCircle q
<!-- PINNED-SIGNATURE:END -->


`{𝕜 : Type u_1} -> [Field 𝕜] -> (p q : 𝕜) -> (hp : p ≠ 0) -> (hq : q ≠ 0) -> AddCircle p ≃+ AddCircle q`

The type variable `𝕜` is the ambient field whose additive structure is being quotiented. The argument `p` is the period of the source additive circle, and `q` is the period of the target additive circle. The argument `hp` is the proof that `p` is non-zero (ensuring `AddCircle p` is a non-degenerate quotient and that rescaling by `p⁻¹` is well-defined), and `hq` is the corresponding non-zero proof for `q`.

## Conventions

The non-zero hypotheses `hp` and `hq` are strictly required; the definition is not extended to the zero-period case by any junk-value convention. No sentinel or default value is provided when either period is zero.

## Worked examples

- Claim: For any non-zero `p` and `q` in a field, the coset of `x` in `AddCircle p` maps under `VTask.equivAddCircle p q hp hq` to the coset of `x * (p⁻¹ * q)` in `AddCircle q`.

- Claim: The inverse of `VTask.equivAddCircle p q hp hq` equals `VTask.equivAddCircle q p hq hp`; in particular, `(VTask.equivAddCircle p q hp hq).symm` sends the coset of `x` in `AddCircle q` to the coset of `x * (q⁻¹ * p)` in `AddCircle p`.

- Claim: When `p = q`, the map `VTask.equivAddCircle p p hp hp` acts as multiplication by `p⁻¹ * p = 1`, hence sends every coset representative `x` to the coset of `x` itself, i.e., it is (equal to) the identity on `AddCircle p`.

## Boundaries

- When `p = q`, the equivalence is the identity automorphism of `AddCircle p` (rescaling by `p⁻¹ * p = 1`).
- The non-zero conditions `hp` and `hq` are necessary: if either period were zero, the additive circle degenerates (it would coincide with `𝕜` itself as a quotient by the trivial subgroup), and the rescaling factor `p⁻¹` would be undefined.
- The construction is symmetric in the sense that `(VTask.equivAddCircle p q hp hq).symm = VTask.equivAddCircle q p hq hp` as group equivalences.
- The equivalence is purely algebraic (a group isomorphism); it does not carry topological or smooth structure in this definition.

## Not to be confused with

- `AddCircle p` itself: that is the type (the quotient group `𝕜 ⧸ zmultiples p`), not the isomorphism between two such types.
- `AddAut.mulRight`: the underlying automorphism of `𝕜` used internally to implement the rescaling; this is an automorphism of the field as an additive group, not a map between circles with different periods.
- The real-analytic or topological equivalence between circles: `VTask.equivAddCircle` is purely an additive group equivalence and does not assert continuity or smoothness.