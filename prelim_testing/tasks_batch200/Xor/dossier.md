## Object

`VTask.Xor a b` is the proposition asserting that exactly one of `a` and `b` holds — the logical exclusive-or (XOR) of two propositions. It is true when `a` is true and `b` is false, or when `b` is true and `a` is false, and false when both hold or neither holds.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Xor : (a b : Prop) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Xor : (a b : Prop) -> Prop`

The first argument `a` is the left proposition; the second argument `b` is the right proposition. Both are arbitrary propositions, and the result expresses that precisely one of them is true.

## Conventions

There are no special junk-value or edge conventions for this definition: it is a total, purely logical connective defined uniformly for all propositions, with no degenerate inputs or boundary cases that require a separate convention.

## Worked examples

- Claim: `VTask.Xor (Even 3) (Odd 3)` holds, since 3 is odd but not even.

- Claim: `VTask.Xor a b` is equivalent to `a ↔ ¬b` for any propositions `a` and `b` (i.e., XOR captures exactly the situation where the two propositions have opposite truth values).

- Claim: `VTask.Xor a b` implies `a ∨ b` — if exactly one of two propositions holds, then at least one holds.

- Claim: `VTask.Xor a b` is symmetric: `VTask.Xor a b = VTask.Xor b a` for all propositions `a` and `b`.

- Claim: `VTask.Xor (Even n) (Odd n)` holds for every natural number `n`, capturing that every natural number is either even or odd but not both.

## Boundaries

- When both `a` and `b` are true, `VTask.Xor a b` is false — exclusive-or differs from inclusive-or precisely in this case.
- When both `a` and `b` are false, `VTask.Xor a b` is also false — it requires exactly one true proposition.
- `VTask.Xor a a` is always false for any proposition `a`, since a proposition and itself cannot satisfy the "exactly one" condition.
- `VTask.Xor a (¬a)` is always true by the law of excluded middle, since `a` and `¬a` are mutually exclusive and exhaustive.

## Not to be confused with

- `Or a b` (inclusive or): true when at least one of `a`, `b` holds, including when both are true — unlike XOR which requires exactly one.
- `p ∆ q` (symmetric difference `symmDiff`): for propositions, this is propositionally equal to `VTask.Xor p q`, but `symmDiff` is a more general lattice-theoretic operation defined for arbitrary lattices.
- `Bool.xor`: the boolean exclusive-or on `Bool` values, not on `Prop`; analogous in spirit but operates in a decidable boolean setting rather than the general propositional setting.