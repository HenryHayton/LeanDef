## Object

`VTask.removeBot P indep sSup_eq` constructs a `Partition s` — a way of expressing `s` as the supremum of a family of pairwise-independent, non-bottom parts — from the set `P`, provided that `P` is already supremum-independent and that its supremum equals `s`. The construction simply strips out the bottom element `⊥` from `P` so that the resulting partition satisfies the required convention that no part equals `⊥`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.removeBot : {α : Type u_1} -> {s : α} -> [CompleteLattice α] -> (P : Set α) -> (indep : sSupIndep P) -> (sSup_eq : sSup P = s) -> Partition s
<!-- PINNED-SIGNATURE:END -->


`VTask.removeBot : {α : Type u_1} -> {s : α} -> [CompleteLattice α] -> (P : Set α) -> (indep : sSupIndep P) -> (sSup_eq : sSup P = s) -> Partition s`

- `α` is the ambient complete-lattice type whose elements are the parts of the partition.
- `s` is the element of `α` being partitioned (i.e., the element that `P` covers as a supremum).
- The `CompleteLattice` instance supplies the lattice structure (suprema, infima, `⊥`, etc.).
- `P` is the set of proposed parts before the removal of `⊥`.
- `indep` is a proof that `P` is supremum-independent: the supremum of any sub-family of `P` is independent from the remaining elements.
- `sSup_eq` is a proof that the supremum of `P` equals `s`, confirming that `P` does cover exactly `s`.

## Conventions

The bottom element `⊥` is always removed from `P` even if it was not present; the resulting partition's `parts` field is exactly `P \ {⊥}`, so any element of `P` equal to `⊥` is silently discarded and does not appear as a part.

## Worked examples

- Claim: For the singleton set `{s}` in a complete lattice, `VTask.removeBot {s} (sSupIndep_singleton s) sSup_singleton` is the top partition of `s` (i.e., the unique partition into a single non-bottom part, when `s ≠ ⊥`).

- Claim: An element `x` belongs to the parts of `VTask.removeBot P indep h` if and only if `x ∈ P` and `x ≠ ⊥`, by `Partition.mem_removeBot`.

- Claim: If `P` contains `⊥`, then `⊥` is not a member of the parts of `VTask.removeBot P indep h`.

## Boundaries

- If `P` is empty, then `sSup_eq` forces `sSup ∅ = s`, meaning `s = ⊥`. In this case `P \ {⊥}` is still empty, and the resulting partition is a valid (degenerate) partition of `⊥` into no parts.
- If `P` already contains no `⊥`, the construction is the identity on the underlying set: no element is removed.
- If `P` contains `⊥` among other elements, only `⊥` is removed; the supremum is unaffected because `⊥` contributes nothing to a supremum.
- The independence condition `indep` is inherited by monotonicity of `sSupIndep` under subset inclusion, so removing `⊥` preserves it automatically.

## Not to be confused with

- `Partition.mk` (the raw constructor): requires the `bot_notMem` condition to be supplied manually, whereas `VTask.removeBot` enforces it by construction.
- `sSupIndep` itself: a property of a set, not a `Partition`; `VTask.removeBot` consumes a proof of `sSupIndep` rather than producing one.
- `Partition.top` (the top element of the partition lattice): equals `VTask.removeBot {s} _ _` only when `s` is the top element of the lattice; for general `s` it is a different object.