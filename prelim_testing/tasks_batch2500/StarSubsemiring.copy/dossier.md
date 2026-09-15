## Object

A "copy" of a star sub-semiring: given a star sub-semiring `S` of a star ring `R` and a set `s` that is definitionally equal (via a proof `hs`) to the carrier of `S`, this produces a new `StarSubsemiring R` whose carrier is literally `s` rather than `↑S`. The mathematical content is identical to `S`; the construction exists solely to adjust definitional equality of the carrier set without changing the mathematical object.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {R : Type v} -> [NonAssocSemiring R] -> [StarRing R] -> (S : StarSubsemiring R) -> (s : Set R) -> (hs : s = ↑S) -> StarSubsemiring R
<!-- PINNED-SIGNATURE:END -->


The first argument `S` is the star sub-semiring being copied. The second argument `s` is the new set to use as the carrier of the copy. The third argument `hs` is a proof that `s` equals the coercion of `S` to a set (i.e., the carrier of `S`); this equality is what justifies that the copy is a valid star sub-semiring with carrier `s`.

## Conventions

The copy operation is only defined when `s` is provably equal to the carrier of `S`; there are no junk values because the function is total over its stated domain (the proof `hs` is required as an explicit argument).

## Worked examples

- Claim: For any `StarSubsemiring R` named `S`, the carrier of `VTask.copy S ↑S rfl` equals `↑S`.

- Claim: For any `StarSubsemiring R` named `S` and any element `x`, `x ∈ VTask.copy S ↑S rfl` if and only if `x ∈ S`.

- Claim: If `s = ↑S` (with proof `hs`), then `↑(VTask.copy S s hs) = s`.

## Boundaries

- The only admissible input for `s` is a set provably equal to `↑S`; the type system enforces this by requiring `hs : s = ↑S` as an explicit argument.
- When `s` is literally `↑S` and `hs` is `rfl`, the copy is structurally identical to `S` but may be definitionally distinct.
- The construction preserves all star sub-semiring axioms (closure under addition, multiplication, zero, and the star operation) since membership in the copy is equivalent to membership in the original.
- There is no mathematical difference between the copy and the original: every element of `S` is in the copy, and vice versa.

## Not to be confused with

- `StarSubsemiring.subtype`: the inclusion map from a star sub-semiring into the ambient ring — a morphism, not a copy operation.
- `StarSubsemiring.map`: transports a star sub-semiring along a star ring homomorphism, genuinely producing a potentially different sub-semiring.
- `Subsemiring.copy`: the analogous copy operation for sub-semirings without the star structure; `VTask.copy` additionally preserves the `star_mem` axiom.