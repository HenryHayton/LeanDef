## Object

`VTask.lift` is the canonical equivalence expressing the **universal property of the free product (coproduct) of monoids**. Given an indexed family of monoids `M i` and a target monoid `N`, it establishes a bijection between:
- families of monoid homomorphisms `(i : ι) → M i →* N` (one homomorphism out of each summand), and
- single monoid homomorphisms `Monoid.CoprodI M →* N` out of the free product.

This bijection witnesses that `Monoid.CoprodI M` is the categorical coproduct in the category of monoids: a map out of the coproduct is the same data as a compatible family of maps out of each summand.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : {ι : Type u_1} -> {M : ι → Type u_2} -> [(i : ι) → Monoid (M i)] -> {N : Type u_3} -> [Monoid N] -> ((i : ι) → M i →* N) ≃ (Monoid.CoprodI M →* N)
<!-- PINNED-SIGNATURE:END -->


`VTask.lift : {ι : Type u_1} -> {M : ι → Type u_2} -> [(i : ι) → Monoid (M i)] -> {N : Type u_3} -> [Monoid N] -> ((i : ι) → M i →* N) ≃ (Monoid.CoprodI M →* N)`

The index type `ι` parametrises the family of summands. `M` is the indexed family of monoids being freely combined into their coproduct. The instance argument supplies a monoid structure on each `M i`. `N` is the target monoid into which homomorphisms land, equipped with its own monoid instance. The equivalence itself takes no further explicit arguments: it is a value of type `Equiv` between the two homomorphism types.

## Conventions

The forward direction `VTask.lift.toFun` sends a family `fi : (i : ι) → M i →* N` to the unique monoid homomorphism `Monoid.CoprodI M →* N` that extends each `fi i` via the canonical inclusion `of : M i →* Monoid.CoprodI M`. The inverse direction `VTask.lift.invFun` recovers the family by pre-composing a given homomorphism with each inclusion `of`.

## Worked examples

- Claim: Applying the forward direction of `VTask.lift` to a family `fi` and then evaluating at an element `of m` (the image of `m : M i` under the canonical inclusion) returns `fi i m`.

- Claim: The forward direction of `VTask.lift` applied to the family of canonical inclusions `of` is the identity homomorphism on `Monoid.CoprodI M`; that is, `VTask.lift (fun i => of) = MonoidHom.id (Monoid.CoprodI M)`.

- Claim: Pre-composing the result of `VTask.lift fi` with the canonical inclusion `of` for index `i` recovers exactly `fi i`; formally, `(VTask.lift fi).comp of = fi i`.

- Claim: The image (mrange) of `VTask.lift fi` in `N` equals the supremum over all `i` of the images of `fi i`.

## Boundaries

- When `ι` is empty, `Monoid.CoprodI M` is the trivial monoid (the initial object), so the only homomorphism out of it is the trivial one, and the only family of maps is the empty family. The equivalence handles this degenerate case correctly without special casing.
- When `ι` has exactly one element, `Monoid.CoprodI M` is isomorphic to `M` itself, and the equivalence reduces to the identity: a single homomorphism `M →* N` corresponds to itself.
- The equivalence is definitionally natural: the round-trip identities `left_inv` and `right_inv` hold by reflexivity of the monoid homomorphism evaluations on generators.
- Injectivity of the resulting homomorphism is not automatic; it depends on additional properties of the family `fi` (e.g., a ping-pong argument).

## Not to be confused with

- `Monoid.CoprodI.of`: the canonical inclusion `M i →* Monoid.CoprodI M` for a single summand, which is an input ingredient to `VTask.lift`, not the universal map itself.
- `FreeMonoid.lift`: the analogous universal property for the *free monoid* on a single set, not for a coproduct of multiple monoids.
- `MulEquiv` (a monoid isomorphism): `VTask.lift` produces an `Equiv` between hom-sets, not an isomorphism of monoids.
