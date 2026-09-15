## Object

`VTask.toRingAut` is a group homomorphism from a group `G` to the group of ring automorphisms of a semiring `R`, built from the data of a multiplicative semiring action of `G` on `R`. Concretely, every element `g : G` determines an invertible ring map `R → R` (multiplication by `g` via the action), and this assignment is compatible with the group structure of `G`: it sends the identity of `G` to the identity automorphism of `R`, and it sends a product `g * h` to the composition of the corresponding automorphisms.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toRingAut : (G : Type u_1) -> (R : Type u_2) -> [Group G] -> [Semiring R] -> [MulSemiringAction G R] -> G →* RingAut R
<!-- PINNED-SIGNATURE:END -->


`VTask.toRingAut : (G : Type u_1) -> (R : Type u_2) -> [Group G] -> [Semiring R] -> [MulSemiringAction G R] -> G →* RingAut R`

The first explicit argument `G` is the group that acts. The second explicit argument `R` is the semiring being acted upon. The instance arguments supply: the group structure on `G`, the semiring structure on `R`, and the multiplicative semiring action of `G` on `R` (which simultaneously packages the scalar-multiplication law, additivity, and multiplicativity of each `g • –` map).

## Conventions

There are no declared junk-value conventions for this definition: it is total on its domain (every group element and every semiring with a `MulSemiringAction` gives a well-defined ring automorphism), and no special edge-case outputs are assigned.

## Worked examples

- Claim: For the trivial group acting on any semiring `R`, `VTask.toRingAut` sends the unique element to the identity ring automorphism of `R`.

- Claim: The map `VTask.toRingAut G R` sends a product `g * h` (in `G`) to the ring automorphism corresponding to `g` composed with the ring automorphism corresponding to `h`, i.e., it is a group homomorphism.

- Claim: For a commutative ring `R` with a `MulSemiringAction` of a group `G`, the underlying ring equivalence of `(VTask.toRingAut G R) g` equals `MulSemiringAction.toRingEquiv G R g` for every `g : G`.

## Boundaries

- When `G` is the trivial group, the homomorphism maps the single element to the identity automorphism; the image is trivial in `RingAut R`.
- When the action is trivial (every `g` acts as the identity), every group element is sent to the identity automorphism of `R`, so the homomorphism is the trivial one regardless of the group structure of `G`.
- When the `MulSemiringAction` is faithful (distinct group elements induce distinct automorphisms), the homomorphism is injective, and `G` embeds into `RingAut R`.
- The homomorphism lands in `RingAut R` (the full automorphism group), not merely in ring endomorphisms; invertibility of each automorphism is guaranteed by the group-action axioms.

## Not to be confused with

- `DistribMulAction.toAddAut`: the weaker version that only produces an additive automorphism (ignores multiplicative structure of `R`).
- `MulDistribMulAction.toMulAut`: the weaker version that only produces a multiplicative automorphism (ignores additive structure of `R`).
- `MulSemiringAction.toRingEquiv`: the underlying per-element function (for a fixed `g : G`, produces one `RingEquiv`) rather than the group homomorphism packaging all elements together.