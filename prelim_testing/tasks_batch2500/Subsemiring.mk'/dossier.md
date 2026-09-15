## Object

`VTask.mk'` assembles a subsemiring of a non-associative semiring `R` from three pieces of data that are already known to coincide as subsets of `R`: a multiplicative submonoid, an additive submonoid, and the underlying set they share. The result is a `Subsemiring R` whose carrier is exactly `s`, whose multiplicative structure comes from `sm`, and whose additive structure comes from `sa`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mk' : {R : Type u} -> [NonAssocSemiring R] -> (s : Set R) -> (sm : Submonoid R) -> (hm : ↑sm = s) -> (sa : AddSubmonoid R) -> (ha : ↑sa = s) -> Subsemiring R
<!-- PINNED-SIGNATURE:END -->


`VTask.mk' : {R : Type u} -> [NonAssocSemiring R] -> (s : Set R) -> (sm : Submonoid R) -> (hm : ↑sm = s) -> (sa : AddSubmonoid R) -> (ha : ↑sa = s) -> Subsemiring R`

The ambient type `R` is a non-associative semiring (carrying both `+` and `·` with the usual unit and distribution laws, but not necessarily associativity of `·`). The argument `s` is the intended carrier set of the new subsemiring. The argument `sm` is a multiplicative submonoid of `R` that will supply closure under `·` and the identity `1`; `hm` is a proof that the underlying set of `sm` equals `s`. The argument `sa` is an additive submonoid of `R` that will supply closure under `+` and the identity `0`; `ha` is a proof that the underlying set of `sa` equals `s`.

## Conventions

No special junk-value or default conventions are declared for this constructor: it is a total function and every argument carries a proof obligation (`hm` and `ha`) ensuring the inputs are consistent, so there are no degenerate input regimes to document.

## Worked examples

- Claim: For any `sm : Submonoid R` and `sa : AddSubmonoid R` with `↑sm = s` and `↑sa = s`, an element `x` belongs to `VTask.mk' s sm hm sa ha` if and only if it belongs to `s`.

- Claim: The `toSubmonoid` projection of `VTask.mk' s sm hm sa ha` recovers exactly `sm`.

- Claim: The `toAddSubmonoid` projection of `VTask.mk' s sm hm sa ha` recovers exactly `sa`.

- Claim: The coercion of `VTask.mk' s sm hm sa ha` to `Set R` equals `s`.

## Boundaries

- The constructor requires that both `↑sm` and `↑sa` are **equal** (not merely in bijection) to `s` as sets. Providing proofs `hm` and `ha` that refer to different sets is a type error; the equalities must both target the same `s`.
- Because `R` is only assumed to be a `NonAssocSemiring`, multiplication need not be associative; nevertheless the subsemiring produced still tracks multiplicative closure under `·` and the presence of `1`.
- If `sm` and `sa` are structurally distinct subobjects that happen to have the same carrier, `VTask.mk'` produces a single `Subsemiring R` that is definitionally equal to neither `sm` nor `sa` on its own, but its projections recover each input exactly.

## Not to be confused with

- `Subsemiring.mk` (the raw structure constructor): that constructor takes the carrier and all closure proofs directly, without accepting pre-built submonoid/additive-submonoid witnesses.
- `NonUnitalSubsemiring.mk'`: analogous constructor for non-unital subsemirings; it uses a `Subsemigroup` (no identity requirement) instead of a `Submonoid`, so it does not enforce `1 ∈ s`.
- `Subring.mk'`: the ring-theoretic analogue; it additionally requires an additive subgroup (not merely an additive submonoid), enforcing closure under negation.