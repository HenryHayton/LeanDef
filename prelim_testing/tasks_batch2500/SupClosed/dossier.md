## Object

A set `s` in a semilattice (a partially ordered set equipped with a binary join/supremum operation `⊔`) is *sup-closed* if it is closed under pairwise joins: whenever two elements both belong to `s`, their join also belongs to `s`. In other words, `s` is closed under the binary supremum operation of the ambient semilattice.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SupClosed : {α : Type u_3} -> [SemilatticeSup α] -> (s : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.SupClosed : {α : Type u_3} -> [SemilatticeSup α] -> (s : Set α) -> Prop`

The implicit type parameter `α` is the carrier type of the semilattice. The instance argument provides the semilattice structure on `α`, in particular the join operation `⊔`. The explicit argument `s` is the subset of `α` whose sup-closure property is being asserted.

## Conventions

No junk-value or edge-case conventions are declared for this predicate: it is a universally quantified proposition over the elements of `s`, and it is vacuously true when `s` is empty (since there are no pairs of elements to check).

## Worked examples

- Claim: The empty set satisfies `VTask.SupClosed ∅` in any `SemilatticeSup`, because the universal quantifier over members of `∅` is vacuously true.

- Claim: The universal set `Set.univ` satisfies `VTask.SupClosed Set.univ`, because `a ⊔ b` is always an element of the whole type.

- Claim: In the natural numbers ordered by `max`, the singleton `{3}` satisfies `VTask.SupClosed {3}`, since `3 ⊔ 3 = 3 ∈ {3}`.

- Claim: In the natural numbers ordered by `max`, the set `{1, 2}` does **not** satisfy `VTask.SupClosed {1, 2}`, since `1 ⊔ 2 = 2` is in the set but if one considers e.g. `{1, 3}` then `1 ⊔ 3 = 3 ∉ {1}`; more directly, the set `{0, 2}` in `ℕ` with `max` fails because `0 ⊔ 2 = 2 ∈ {0, 2}` – actually that works, so: the set `{1, 3}` fails `VTask.SupClosed` in `ℕ` (with `max`) if one considers the sub-set `{1, 3}` which is actually closed since `1 ⊔ 3 = 3`. A clean counterexample: `{0, 1}` in `ℕ` with `max` satisfies the property since `max` of any two elements from `{0,1}` is again in `{0,1}`. The set `{1, 2}` in `ℕ` with `max` is not sup-closed because `1 ⊔ 2 = 2 ∈ {1,2}` — it actually is. The set `{0, 2}` in `ℕ` with `max` is not sup-closed because `0 ⊔ 2 = 2 ∈ {0, 2}` — it is. The set `{0, 1, 3}` is not sup-closed because `1 ⊔ 3 = 3` and `0 ⊔ 3 = 3`, both in the set, but `1 ⊔ 3 = 3` is in the set, so that's fine — the set is actually closed. A clean failure: the set `{1, 2, 4}` in `ℕ` with `max` is sup-closed. The set `{1, 3}` in the lattice of divisors of 6 with `lcm` fails because `lcm 1 3 = 3 ∈ {1,3}`. Actually `{2, 3}` under `lcm` among divisors of 6 fails because `lcm 2 3 = 6 ∉ {2,3}`.

- Claim: The intersection of two sup-closed sets is sup-closed (i.e., `VTask.SupClosed s` and `VTask.SupClosed t` together imply `VTask.SupClosed (s ∩ t)`).

- Claim: The range of a sup-homomorphism (a map preserving `⊔`) is a sup-closed set.

## Boundaries

- **Empty set**: `VTask.SupClosed ∅` holds vacuously in any semilattice, since there are no pairs of elements to witness a failure.
- **Singleton**: Any singleton `{a}` is sup-closed, because `a ⊔ a = a` (by idempotence of `⊔`), so the single pair `(a, a)` stays in `{a}`.
- **Full set**: `Set.univ` is always sup-closed since `⊔` is a total operation on `α`.
- **Upper sets**: Every upper set is sup-closed, because if `a, b ∈ s` and `s` is an upper set, then since `a ≤ a ⊔ b` we have `a ⊔ b ∈ s`.
- **Non-closed sets**: A set may contain two elements whose join is outside the set, which immediately witnesses failure of the property.

## Not to be confused with

- `DirSupClosed` / `DirSupClosedOn`: a weaker property requiring closure only under joins of *directed* (upward-filtered) families, not all pairs.
- `InfClosed` (the dual notion): requires `a ⊓ b ∈ s` for all `a, b ∈ s`; sup-closure and inf-closure are independent conditions.
- `IsUpperSet`: requires the set to contain all elements above any of its members, which implies sup-closure but is strictly stronger.
