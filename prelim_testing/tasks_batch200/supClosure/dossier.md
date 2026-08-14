## Object

`VTask.supClosure` is the closure operator on the power set of a join-semilattice `α` (a type equipped with a binary join/supremum operation `⊔`) that maps each set `s ⊆ α` to the smallest sup-closed superset of `s`. A set is *sup-closed* if it is closed under finite non-empty suprema: whenever a finite non-empty collection of elements all belong to the set, their join also belongs to the set. The resulting object is a `ClosureOperator` on `Set α`, meaning it packages together the monotone, extensive, and idempotent maps `Set α → Set α` in a single bundled structure.

Concretely, an element `a ∈ α` belongs to `VTask.supClosure s` exactly when `a` can be expressed as the supremum `t.sup' ht id` of some finite non-empty subset `t` of `s`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.supClosure : {α : Type u_3} -> [SemilatticeSup α] -> ClosureOperator (Set α)
<!-- PINNED-SIGNATURE:END -->


VTask.supClosure : {α : Type u_3} -> [SemilatticeSup α] -> ClosureOperator (Set α)

The implicit type argument `α` is the carrier type whose elements are being organised into sets. The typeclass argument `[SemilatticeSup α]` equips `α` with a binary join/supremum operation `⊔` satisfying the usual semilattice axioms (associativity, commutativity, idempotence, and the absorption order), which is the structure needed to take finite non-empty suprema. No explicit set argument appears in the operator itself; the resulting `ClosureOperator` is a function-valued object that one applies to a set to obtain its sup-closure.

## Conventions

Only **non-empty** finite subsets are used when characterising membership in the closure: the empty supremum is excluded. Consequently, every element of `s` already belongs to `VTask.supClosure s` (it is the sup of the singleton containing itself), but the empty set is **not** adjoined unless `s` happens to contain a bottom element expressible as a non-empty sup from `s`.

## Worked examples

- Claim: For any set `s` in a `SemilatticeSup`, `s ⊆ VTask.supClosure s` (the closure is extensive).

- Claim: For any set `s` in a `SemilatticeSup`, `VTask.supClosure (VTask.supClosure s) = VTask.supClosure s` (the closure operator is idempotent).

- Claim: The set `VTask.supClosure s` is sup-closed for any `s`; that is, whenever `a` and `b` belong to `VTask.supClosure s`, so does `a ⊔ b`.

- Claim: `VTask.supClosure Set.univ = Set.univ` — the closure of the full set is the full set.

- Claim: If `s ⊆ t` then `VTask.supClosure s ⊆ VTask.supClosure t` (monotonicity).

- Claim: `VTask.supClosure s = s` if and only if `s` is already sup-closed.

## Boundaries

- **Empty input set**: `VTask.supClosure ∅` consists of all elements of `α` that can be expressed as a non-empty finite sup of members of `∅`. Since no element belongs to `∅`, no non-empty finite subset exists, so `VTask.supClosure ∅ = ∅`.
- **Already sup-closed set**: If `s` is sup-closed, then `VTask.supClosure s = s`; the operator is the identity on its fixed points.
- **Singleton set `{a}`**: `VTask.supClosure {a} = {a}`, because the only finite non-empty subset is `{a}` itself, and its sup is `a`.
- **Finite input set**: If `s` is finite, then `VTask.supClosure s` is also finite, since it consists only of sups of finsets drawn from a finite set.
- **Universal set**: `VTask.supClosure Set.univ = Set.univ`, since every element is (trivially) the sup of the singleton containing itself.
- **Least upper bounds are preserved**: `IsLUB (VTask.supClosure s) a ↔ IsLUB s a`, so the sup-closure does not change which element is the least upper bound of the set.

## Not to be confused with

- `infClosure` / `meetClosure`: The analogous closure operator for a meet-semilattice, closing a set under finite non-empty infima; `VTask.supClosure` closes under *joins*, not meets.
- `SupClosed` (the predicate): This is merely the property that a set is already closed under binary joins; `VTask.supClosure` is the *operator* that produces the smallest set satisfying that property.
- `closure` or `convexHull`-style closure operators: General closure operators on lattices may close under other operations or infinitary suprema; `VTask.supClosure` specifically uses only *finite non-empty* suprema and lives on `Set α` ordered by inclusion.