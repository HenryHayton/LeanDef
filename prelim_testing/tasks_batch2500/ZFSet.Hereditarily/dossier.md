## VTask.Hereditarily

### Object

Given a predicate `p` on ZFC sets, `Hereditarily p x` is the proposition that the set `x` satisfies `p`, and moreover every member of `x` satisfies `p` hereditarily — that is, every member of every member of `x`, and so on, recursively through the entire membership tree of `x`. Informally, `x` is "hereditarily `p`" if `p` holds at every node of the transitive closure of membership in `x`, including `x` itself.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Hereditarily : (p : ZFSet.{u_1} → Prop) -> (x : ZFSet.{u_1}) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Hereditarily : (p : ZFSet.{u_1} → Prop) -> (x : ZFSet.{u_1}) -> Prop`

The first argument is the predicate on ZFC sets whose hereditary satisfaction is being checked. The second argument is the ZFC set whose entire membership hierarchy is being tested against that predicate.

### Conventions

The empty set vacuously satisfies the "all members are hereditarily `p`" clause for any `p`, so `Hereditarily p ∅` reduces to `p ∅`; in particular, if `p` holds of the empty set then the empty set is hereditarily `p`.

### Worked examples

- Claim: If `Hereditarily p x` holds, then `p x` holds (the predicate applies to the set itself).

- Claim: If `Hereditarily p x` holds and `y ∈ x`, then `Hereditarily p y` holds (the predicate propagates to every member).

- Claim: If `Hereditarily p x` holds, then `p ∅` holds, because the empty set is a member of the transitive closure of any set (transitivity eventually reaches the empty set at the bottom of the membership hierarchy).

- Claim: `Hereditarily p x` is equivalent to `p x ∧ ∀ y ∈ x, Hereditarily p y`, giving a direct unfolding of the recursive definition.

### Boundaries

- At the empty set `∅`: `Hereditarily p ∅` is equivalent to `p ∅` alone, since the universal quantifier over members of `∅` is vacuously true. There are no members to recurse into.
- For a singleton `{a}`: `Hereditarily p {a}` requires `p {a}` and `Hereditarily p a`, which in turn requires `p a` and hereditary satisfaction for every member of `a`.
- If `p` is the constantly-true predicate, then `Hereditarily p x` holds for every ZFC set `x`.
- If `p` fails at the empty set, then `Hereditarily p x` fails for every ZFC set `x` (since every set eventually has the empty set in its transitive closure, as guaranteed by the axiom of foundation).

### Not to be confused with

- `ZFSet.mem_transitiveClosure`: captures reachability through iterated membership but is a set-membership relation, not a predicate-satisfaction assertion.
- A predicate `p x ∧ ∀ y ∈ x, p y` (only one level deep): `Hereditarily p x` requires `p` at *all* depths, not merely at `x` and its immediate members.
- `ZFSet.IsTransitive`: asserts that all members of members are again members of the set (a property of the set's structure), rather than asserting a predicate holds throughout the membership hierarchy.