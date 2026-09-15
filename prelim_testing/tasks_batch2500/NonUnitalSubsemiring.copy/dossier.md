## Object

`VTask.copy` produces a new non-unital subsemiring that is definitionally identical to a given one, but whose underlying carrier set is replaced by a provably equal set. Its purpose is to resolve definitional equality mismatches: when two descriptions of the same set of elements are definitionally (not merely propositionally) distinct in Lean's type theory, wrapping the subsemiring with `copy` forces the carrier to be whichever presentation is needed, without changing any mathematical content.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {R : Type u} -> [NonUnitalNonAssocSemiring R] -> (S : NonUnitalSubsemiring R) -> (s : Set R) -> (hs : s = ↑S) -> NonUnitalSubsemiring R
<!-- PINNED-SIGNATURE:END -->


`{R : Type u} -> [NonUnitalNonAssocSemiring R] -> (S : NonUnitalSubsemiring R) -> (s : Set R) -> (hs : s = ↑S) -> NonUnitalSubsemiring R`

The ambient type `R` is a non-unital, non-associative semiring (it supports addition and multiplication satisfying the semiring axioms, but need not have a multiplicative unit or associative multiplication). `S` is the source non-unital subsemiring being copied. `s` is the new carrier set that will replace `S`'s carrier in the result. `hs` is the proof that `s` is propositionally equal to the coercion of `S` to a set; this guarantees no elements are added or removed.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total function whose only precondition is the proof `hs`, which is part of the explicit input rather than an implicit constraint.

## Worked examples

- Claim: For any non-unital subsemiring `S` and any set `s` with `hs : s = ↑S`, the carrier of `VTask.copy S s hs` equals `s` as a set.

- Claim: For any non-unital subsemiring `S` and proof `hs : (↑S : Set R) = ↑S`, the element membership in `VTask.copy S (↑S) hs` coincides exactly with membership in `S`; that is, `x ∈ VTask.copy S (↑S) hs ↔ x ∈ S`.

- Claim: If `s` and `t` are both equal to `↑S` (as sets), then `VTask.copy S s hs` and `VTask.copy S t ht` have the same elements.

## Boundaries

- The proof `hs` must be a proof of propositional (not merely definitional) equality; Lean requires an explicit term here.
- When `s` is definitionally equal to `↑S` but not syntactically so, `copy` is the standard way to obtain a subsemiring with carrier literally `s` rather than `↑S`.
- The result is mathematically the same subsemiring as `S`; no new elements are introduced and no elements are removed. The only change is definitional/syntactic.
- If `s = ↑S` holds, all subsemiring axioms (closure under addition, zero, and multiplication) are automatically inherited because the proof obligation is discharged by `hs`.

## Not to be confused with

- `NonUnitalSubsemiring.mk` — the raw constructor that builds a non-unital subsemiring from scratch by providing a carrier and all closure proofs explicitly, rather than copying an existing one.
- Set-theoretic operations such as `NonUnitalSubsemiring.map` or `NonUnitalSubsemiring.comap` — those genuinely change which elements belong to the subsemiring by applying a ring homomorphism, unlike `copy` which preserves the element set.
- Subtype or coercion casting — one might be tempted to cast `S` along an equality of types, but `copy` is preferred because it produces an actual `NonUnitalSubsemiring R` with the desired carrier, rather than a term obtained by transport.