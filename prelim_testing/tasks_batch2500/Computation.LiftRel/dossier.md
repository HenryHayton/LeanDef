## Object

`VTask.LiftRel R ca cb` is a relational lifting of a binary relation `R : α → β → Prop` from values to possibly-nonterminating computations. It asserts a two-sided correspondence: every value that `ca` might produce is `R`-related to some value that `cb` produces, and conversely every value that `cb` might produce is `R`-related to some value that `ca` produces. In this sense it generalises computation equivalence (the special case where `R` is equality) to arbitrary relations.

Concretely, `VTask.LiftRel R ca cb` holds if and only if:
- For every `a` such that `ca` terminates with output `a`, there exists `b` such that `cb` terminates with output `b` and `R a b` holds.
- For every `b` such that `cb` terminates with output `b`, there exists `a` such that `ca` terminates with output `a` and `R a b` holds.

If either computation diverges (never terminates), the vacuous side of each implication is satisfied automatically: a diverging `ca` makes the first clause trivially true, and a diverging `cb` makes the second clause trivially true.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.LiftRel : {α : Type u} -> {β : Type v} -> (R : α → β → Prop) -> (ca : Computation α) -> (cb : Computation β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.LiftRel : {α : Type u} -> {β : Type v} -> (R : α → β → Prop) -> (ca : Computation α) -> (cb : Computation β) -> Prop`

The implicit arguments `α` and `β` are the value types of the two computations. `R` is the relation between those value types that the lifting is built from. `ca` is the computation over `α` (the left-hand side). `cb` is the computation over `β` (the right-hand side). The result is a `Prop` asserting the bilateral correspondence described above.

## Conventions

If `ca` diverges (produces no output), both directions of the correspondence hold vacuously regardless of `cb` and `R`, because there are no values of `ca` to check. Similarly if `cb` diverges, both implications are vacuously true. This means two diverging computations always satisfy `VTask.LiftRel R` for any `R`.

## Worked examples

- Claim: If `R` is a reflexive relation on `α`, then `VTask.LiftRel R (Computation.pure a) (Computation.pure a)` holds for any `a : α` and reflexive `R`.

- Claim: `VTask.LiftRel (fun a b => a ≤ b) (Computation.pure 3) (Computation.pure 5)` holds, since `3 ≤ 5`.

- Claim: `VTask.LiftRel R` is symmetric (up to swapping `R`) in the sense that `VTask.LiftRel (Function.swap R) cb ca ↔ VTask.LiftRel R ca cb`.

- Claim: Two divergent computations `ca : Computation α` and `cb : Computation β` satisfy `VTask.LiftRel R ca cb` whenever both diverge, for any `R`.

## Boundaries

- **Both diverge**: `VTask.LiftRel R ca cb` holds vacuously because neither computation ever produces a value to check.
- **Left diverges, right terminates**: The first clause (left → right) is vacuously true; the second clause (right → left) requires every output `b` of `cb` to be matched by some output of `ca`, which fails since `ca` produces nothing. Hence `VTask.LiftRel R ca cb` is **false** in this case (assuming `cb` actually terminates with some value).
- **Left terminates, right diverges**: Symmetrically, `VTask.LiftRel R ca cb` is **false** when `ca` terminates with some value but `cb` diverges.
- **R is always false**: If `R a b` is false for all `a`, `b`, then `VTask.LiftRel R ca cb` holds only if both `ca` and `cb` diverge.
- **R is always true**: `VTask.LiftRel R ca cb` reduces to: `ca` terminates iff `cb` terminates (i.e., they agree on termination, regardless of output values).
- Since computations in this setting are deterministic (each produces at most one value), the existential witnesses `b` and `a` in the two clauses are unique when they exist.

## Not to be confused with

- **`Computation.Equiv` (computation bisimilarity / equality)**: The special case of `VTask.LiftRel` where `R` is `Eq`; `VTask.LiftRel Eq ca cb` coincides with `ca ~ cb`.
- **`VTask.LiftRelAux`**: A single-step auxiliary relation used in the coinductive unfolding of `VTask.LiftRel`; it operates on `destruct` outputs rather than full computations.
- **`Stream'.WSeq.LiftRel`**: A similarly-named lifting relation on *weak sequences* rather than computations; it asserts element-wise relatedness of the sequence values, not termination correspondence.