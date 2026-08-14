## Object

Given a finpartition `P` of an element `a` in a generalized Boolean algebra, and a proof that `a ≤ b`, `VTask.extendOfLE P hab` produces a finpartition of `b`. If `a = b` the original partition is returned unchanged; if `a < b` the new part `b \ a` (the "leftover" piece) is adjoined to the existing parts, yielding a partition of the strictly larger element `b`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.extendOfLE : {α : Type u_1} -> [GeneralizedBooleanAlgebra α] -> [DecidableEq α] -> {a b : α} -> (P : Finpartition a) -> (hab : a ≤ b) -> Finpartition b
<!-- PINNED-SIGNATURE:END -->


`VTask.extendOfLE : {α : Type u_1} -> [GeneralizedBooleanAlgebra α] -> [DecidableEq α] -> {a b : α} -> (P : Finpartition a) -> (hab : a ≤ b) -> Finpartition b`

The type `α` is a generalized Boolean algebra (implicit), which supplies meet, join, and set-difference operations. `DecidableEq α` is the decidable-equality instance (implicit) needed to work with the underlying finsets. The implicit elements `a` and `b` are the elements of `α` involved: `a` is the element that `P` partitions, and `b` is the larger element to which the partition is extended. `P` is the existing finpartition of `a`. `hab` is the proof that `a ≤ b`, establishing that the extension is valid.

## Conventions

When `a = b` (equivalently, `b \ a = ⊥`), the result has exactly the same parts as `P`; no new part is introduced. When `a < b` (equivalently, `b \ a ≠ ⊥`), the element `b \ a` is inserted as an additional part, so the resulting partition has exactly the parts of `P` together with the single new part `b \ a`.

## Worked examples

- Claim: For any finpartition `P` of `a` and any `a ≤ b`, every part of `P` is also a part of `VTask.extendOfLE P hab`.

- Claim: If `a < b`, then the parts of `VTask.extendOfLE P (le_of_lt hab)` are exactly `insert (b \ a) P.parts`.

- Claim: If `a = b`, then the parts of `VTask.extendOfLE P hab.le` equal `P.parts` (no new part is added).

- Claim: For any part `p` of `VTask.extendOfLE P hab`, either `p` is a part of `P` or `p = b \ a`.

## Boundaries

- When `a = b`, `b \ a = ⊥` holds, so the "extension" is the identity: the returned finpartition has exactly the same parts as `P`. In particular, the empty difference does **not** get added as a spurious part.
- When `a < b`, `b \ a` is a nonzero element that is disjoint from `a` and whose join with `a` equals `b`; it is inserted as a genuine new part.
- The function is total on all `a ≤ b`; there is no case that is undefined or that produces a junk value.
- If `P` has parts `{p₁, …, pₙ}` summing to `a`, and `a < b`, the extended partition has parts `{b \ a, p₁, …, pₙ}` summing to `b`.

## Not to be confused with

- `Finpartition.extend`: the lower-level constructor that adjoins a single explicitly provided disjoint part; `VTask.extendOfLE` calls this internally but additionally handles the degenerate `a = b` case automatically.
- `Finpartition.bind`: combines a partition with a family of sub-partitions by refinement, a different operation that increases the number of parts multiplicatively rather than by one.
- `Finpartition.indiscrete`: the single-part partition of any nonzero element, which is not related to extending an existing partition.