## Object

`VTask.nonunits` extracts, from a valuation subring `A` of a field `K`, the collection of its non-unit elements — that is, those elements of `K` whose valuation is strictly less than 1 — and packages that collection as a non-unital subring of `K`. These are precisely the elements that do not have a multiplicative inverse inside `A`; they form the unique maximal ideal of the valuation ring.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.nonunits : {K : Type u} -> [Field K] -> (A : ValuationSubring K) -> NonUnitalSubring K
<!-- PINNED-SIGNATURE:END -->


The implicit argument `K` is the ambient field. The instance `[Field K]` supplies the field structure. The explicit argument `A` is the valuation subring of `K` whose non-unit elements are to be extracted.

## Conventions

No special junk-value or boundary conventions are declared: the carrier is defined by a strict inequality on the valuation, so every element of `K` either satisfies it or not, and no sentinel values are involved.

## Worked examples

- Claim: For any valuation subring `A` of a field `K`, the zero element `0 : K` belongs to `VTask.nonunits A`.

- Claim: For any valuation subring `A` of a field `K`, if `x` and `y` are elements of `VTask.nonunits A`, then their sum `x + y` is also an element of `VTask.nonunits A`, because the valuation is non-archimedean and both have valuation strictly less than 1.

- Claim: For any valuation subring `A` of a field `K`, if `x` belongs to `VTask.nonunits A` and `y` belongs to `VTask.nonunits A`, then their product `x * y` also belongs to `VTask.nonunits A`, since the valuation is multiplicative and both factors have valuation strictly less than 1.

- Claim: The element `1 : K` does NOT belong to `VTask.nonunits A` for any valuation subring `A`, since the valuation of 1 equals 1, which is not strictly less than 1.

## Boundaries

- The carrier is an open condition (strict inequality `< 1`) on the valuation, so `1` is excluded and the result is not a (unital) subring — it lacks a multiplicative identity, which is why the return type is `NonUnitalSubring K` rather than `Subring K`.
- The zero element `0` always belongs, since valuations send 0 to 0, and `0 < 1`.
- Negation is closed: if `x` is a non-unit then so is `-x`, because the valuation satisfies `v(-x) = v(x)`.
- Units of `A` (elements with valuation exactly equal to 1) are precisely absent from this set.
- In the context of a discrete valuation ring, `VTask.nonunits A` coincides with the unique maximal ideal of `A`.

## Not to be confused with

- The maximal ideal of `A` as a `Ideal`: `VTask.nonunits` gives the same set but as a `NonUnitalSubring`, emphasising the ring-operation structure rather than the module structure over `A`.
- The units subgroup `Aˣ`: that consists of elements with valuation exactly 1, the complement of `VTask.nonunits` within the invertible elements of `K`.
- The subring `A` itself (the valuation subring): `A` consists of elements with valuation ≤ 1, strictly containing `VTask.nonunits A`.