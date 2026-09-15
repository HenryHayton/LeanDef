## Object

`VTask.mk'` constructs a subring of a non-associative ring `R` from three compatible pieces of data: an underlying set `s`, a submonoid `sm`, and an additive subgroup `sa`, provided that both `sm` and `sa` have exactly `s` as their carrier set. The result is the unique `Subring R` whose underlying set is `s`, whose multiplicative structure is recorded by `sm`, and whose additive structure is recorded by `sa`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mk' : {R : Type u} -> [NonAssocRing R] -> (s : Set R) -> (sm : Submonoid R) -> (sa : AddSubgroup R) -> (hm : ↑sm = s) -> (ha : ↑sa = s) -> Subring R
<!-- PINNED-SIGNATURE:END -->


The implicit type argument `R` is the ambient ring, which must carry a `NonAssocRing` instance. The argument `s` is the carrier set that the resulting subring will have. The argument `sm` is a submonoid of `R` (closed under multiplication and containing 1) that is required to live on exactly `s`. The argument `sa` is an additive subgroup of `R` (closed under addition, negation, and containing 0) also required to live on exactly `s`. The proof `hm` witnesses that the coercion of `sm` to a set equals `s`, and the proof `ha` witnesses that the coercion of `sa` to a set equals `s`.

## Conventions

No special junk-value or edge conventions are declared: the constructor is total and well-defined whenever the two compatibility proofs `hm` and `ha` are supplied; there are no inputs for which an arbitrary or degenerate output is chosen by convention.

## Worked examples

- Claim: For any `Subring R`, one can recover it via `VTask.mk'` by taking `s = T.carrier`, `sm = T.toSubmonoid`, `sa = T.toAddSubgroup`, with the canonical proofs, and the result equals the original subring.

- Claim: An element `x` belongs to `VTask.mk' s sm sa hm ha` if and only if it belongs to `s`.

- Claim: The `toSubmonoid` of `VTask.mk' s sm sa hm ha` is definitionally equal to `sm`, and the `toAddSubgroup` is definitionally equal to `sa`.

## Boundaries

- If `sm` and `sa` happen to be the submonoid and additive subgroup of an existing subring but the proofs `hm` and `ha` are provided for a different equal set `s`, the result is still a well-formed subring on `s`.
- The constructor requires a `NonAssocRing` instance rather than a full `Ring`; in particular, multiplication need not be associative.
- Because both `hm` and `ha` must certify the same set `s`, the construction is consistent: there is no possibility of the multiplicative and additive pieces referring to different underlying sets.
- The constructor produces a value of type `Subring R`, not merely a `Set R`; in particular, all subring axioms are guaranteed by the types of `sm` and `sa` together.

## Not to be confused with

- `Subring.mk` (the basic structure constructor): takes raw closure-under-operations data rather than pre-packaged submonoid/additive-subgroup witnesses.
- `NonUnitalSubring.mk'`: the analogous constructor for non-unital subrings, where the multiplicative piece is only a subsemigroup (no identity required).
- `Subring.toSubmonoid` / `Subring.toAddSubgroup`: these are projections *out of* an existing subring, not a way to build one.