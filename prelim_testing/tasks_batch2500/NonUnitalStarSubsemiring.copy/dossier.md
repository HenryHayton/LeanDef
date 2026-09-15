## Object

Given a non-unital star subsemiring `S` of a ring `R` and a set `s` that is definitionally equal to the carrier of `S` (witnessed by a proof `hs : s = ↑S`), `VTask.copy S s hs` is a new non-unital star subsemiring of `R` whose carrier is literally `s` rather than `↑S`. The resulting subsemiring is mathematically identical to `S`; the point is that the two carriers, though equal by proof, may differ in their definitional normal form, and having a subsemiring whose carrier is literally `s` can resolve definitional-equality issues in downstream proofs.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {R : Type v} -> [NonUnitalNonAssocSemiring R] -> [StarRing R] -> (S : NonUnitalStarSubsemiring R) -> (s : Set R) -> (hs : s = ↑S) -> NonUnitalStarSubsemiring R
<!-- PINNED-SIGNATURE:END -->


The first argument `S` is the non-unital star subsemiring being copied. The second argument `s` is the new carrier set, which must be a subset of `R`. The third argument `hs` is a proof that `s` equals the coercion of `S` to a set; it witnesses that the new carrier coincides with the old one.

## Conventions

No special junk-value or out-of-domain conventions are declared for this definition: it is a total, well-typed constructor whose only constraint is the proof `hs`, which is part of the explicit input.

## Worked examples

- Claim: For any non-unital star subsemiring `S`, `VTask.copy S ↑S rfl` has the same carrier as `S`.

- Claim: An element `x` belongs to `VTask.copy S s hs` if and only if `x ∈ s` (equivalently, `x ∈ S`, since `s = ↑S`).

- Claim: `VTask.copy S s hs` satisfies the `star_mem'` axiom: if `x ∈ s` then `star x ∈ s`, inherited from `S`.

## Boundaries

- The definition is only well-formed when `hs : s = ↑S` holds; there is no notion of a "junk" output because `hs` is a required proof argument.
- When `s` is definitionally equal (not merely propositionally equal) to `↑S`, `VTask.copy S s hs` is defeq to `S` itself; the whole purpose of the construction is the case where `s` is merely propositionally (not definitionally) equal to `↑S`.
- All algebraic operations (addition, multiplication, star, zero) on `VTask.copy S s hs` behave identically to those on `S`.

## Not to be confused with

- `NonUnitalStarSubsemiring.mk` — directly constructs a non-unital star subsemiring from raw data, without reference to an existing one; `VTask.copy` is specifically for cloning an existing subsemiring with a replaced carrier.
- `NonUnitalSubsemiring.copy` — the analogous copy operation for non-unital subsemirings that forgets the star structure; `VTask.copy` additionally preserves and re-checks the `star_mem'` axiom.
- Subtype coercion `(S : Set R)` — simply extracts the carrier as a set, without producing any algebraic structure.