## Object

`VTask.monoidOf S` is the canonical monoid homomorphism that embeds a commutative monoid `M` into its localization `Localization S` at a submonoid `S`. Concretely, it sends each element `x : M` to the equivalence class of the fraction `x/1` in the localization. The result is not merely a monoid homomorphism but a full *localization map* — a bundled structure that records both the homomorphism and the proof that it satisfies the universal property of localization (units of `S` become invertible, every element of the localization is in the image of the map's fraction-forming operation, and equality in the localization is controlled by the localization relation on `M × S`).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.monoidOf : {M : Type u_1} -> [CommMonoid M] -> (S : Submonoid M) -> S.LocalizationMap (Localization S)
<!-- PINNED-SIGNATURE:END -->


`VTask.monoidOf : {M : Type u_1} -> [CommMonoid M] -> (S : Submonoid M) -> S.LocalizationMap (Localization S)`

The implicit type argument `M` is the ambient commutative monoid being localized. The instance argument supplies the `CommMonoid` structure on `M`. The explicit argument `S` is the submonoid of `M` at which the localization is formed; it specifies which elements are to be inverted. The return value is a `Submonoid.LocalizationMap` — a bundled monoid homomorphism from `M` to `Localization S` together with proofs of the three axioms that characterize a localization map.

## Conventions

There are no declared junk-value or out-of-domain conventions for this definition: it is total and well-defined for any commutative monoid `M` and any submonoid `S` of `M`, including the trivial submonoid `{1}` and the full submonoid `M` itself.

## Worked examples

- Claim: For any commutative monoid `M` and submonoid `S`, applying `VTask.monoidOf S` to an element `x : M` yields `Localization.mk x 1` in `Localization S`.

- Claim: The underlying function of `VTask.monoidOf S` is a monoid homomorphism, so `(VTask.monoidOf S) (x * y) = (VTask.monoidOf S) x * (VTask.monoidOf S) y` for all `x y : M`.

- Claim: Every element `s : S` maps to a unit in `Localization S` via `VTask.monoidOf S`, i.e., `IsUnit ((VTask.monoidOf S) s)` holds for all `s : S`.

- Claim: The map `VTask.monoidOf S` is surjective in the localization sense: every element `z : Localization S` can be written as `(VTask.monoidOf S).mk' a b` for some `a : M` and `b : S`.

## Boundaries

- When `S` is the trivial submonoid `{1}`, no new elements are inverted, and `Localization S` is isomorphic to `M` itself; `VTask.monoidOf S` is in this case essentially the identity.
- When `S = M` (the whole monoid treated as a submonoid, if that is a submonoid), every element is inverted and the localization becomes a group; `VTask.monoidOf S` is then the canonical embedding of `M` into that group.
- The map always sends the identity `1 : M` to `1 : Localization S`, since `mk 1 1` is the identity of the localization.
- `VTask.monoidOf S` is injective if and only if `S` contains no zero-divisors (in the monoid-theoretic sense); otherwise distinct elements of `M` may become identified in the localization.

## Not to be confused with

- `Submonoid.LocalizationMap.mk'` — the fraction-forming operation `mk' a b = (monoidOf S a) * (unit b)⁻¹` built *from* a localization map; `VTask.monoidOf S` is the localization map itself, not the fraction map.
- `Localization.mk` — the bare quotient-type constructor `mk x s : Localization S`; `VTask.monoidOf S` wraps this into a bundled localization map and is equal to `mk x 1` on elements, but carries the full universal-property data.
- `algebraMap R (Localization M)` — in the commutative ring setting the canonical ring homomorphism into the localization; `VTask.monoidOf` is its multiplicative (monoid) analogue, and the two coincide when `M` is a submonoid of the multiplicative monoid of a ring.