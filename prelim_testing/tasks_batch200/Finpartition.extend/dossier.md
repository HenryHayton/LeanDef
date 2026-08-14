## Object

`VTask.extend` constructs a new finite partition of an element `c` in a modular lattice by adjoining a fresh atom `b` to an existing finite partition `P` of `a`, provided that `b` is nonzero, `a` and `b` are disjoint, and `a ⊔ b = c`. The result is a `Finpartition c` whose parts are exactly the parts of `P` together with the single new part `b`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.extend : {α : Type u_1} -> [Lattice α] -> [OrderBot α] -> [IsModularLattice α] -> [DecidableEq α] -> {a b c : α} -> (P : Finpartition a) -> (hb : b ≠ ⊥) -> (hab : Disjoint a b) -> (hc : a ⊔ b = c) -> Finpartition c
<!-- PINNED-SIGNATURE:END -->


VTask.extend : {α : Type u_1} -> [Lattice α] -> [OrderBot α] -> [IsModularLattice α] -> [DecidableEq α] -> {a b c : α} -> (P : Finpartition a) -> (hb : b ≠ ⊥) -> (hab : Disjoint a b) -> (hc : a ⊔ b = c) -> Finpartition c

The implicit type `α` is a modular lattice with a bottom element and decidable equality. The implicit elements `a`, `b`, `c` are elements of this lattice. `P` is a finite partition of `a`, the element being extended. `hb` is the proof that `b` is not the bottom element (ensuring the new part is nondegenerate). `hab` is the proof that `a` and `b` are disjoint (ensuring no overlap between old and new parts). `hc` is the proof that the join of `a` and `b` equals `c`, identifying the element that the resulting partition covers.

## Conventions

The parts of the resulting `Finpartition c` are exactly `insert b P.parts`; the new element `b` is inserted as a single additional part alongside all existing parts of `P`. The cardinality of the resulting partition's parts is exactly one more than the cardinality of `P`'s parts.

## Worked examples

- Claim: If `P` is a finpartition of `a` and `b` is disjoint from `a` with `a ⊔ b = c`, then `(VTask.extend P hb hab hc).parts = insert b P.parts`.

- Claim: The number of parts in `VTask.extend P hb hab hc` equals `P.parts.card + 1`.

- Claim: `b` is a member of `(VTask.extend P hb hab hc).parts`.

## Boundaries

- The condition `b ≠ ⊥` is strictly required; if `b` were the bottom element it would not be a valid part of any finpartition (finpartitions never contain `⊥`).
- The disjointness condition `Disjoint a b` ensures that inserting `b` does not cause two parts of the new partition to overlap, which would violate the independent-sup condition.
- When `a = ⊥` (the partition is the empty partition of the bottom element) and `a ⊔ b = b`, `extend` produces a finpartition of `b` with a single part `{b}`.
- The proof `hc : a ⊔ b = c` is used purely to identify the target element; the construction otherwise only depends on `a`, `b`, and `P`.

## Not to be confused with

- `Finpartition.extendOfLE`: extends a finpartition along a lattice inequality `a ≤ b` by adjoining the difference `b \ a`, rather than an arbitrary disjoint element with an explicit proof.
- `Finpartition.bind`: refines a finpartition by replacing each part with a sub-partition of that part, which grows the number of parts multiplicatively rather than additively.
- `Finpartition.indiscrete`: produces a one-part finpartition of a nonzero element, rather than extending an existing partition.