## VTask.IsCover

### Object

Given a binary relation `U` on a set `X` (called an *entourage*, playing the role of a notion of "closeness" or "proximity"), `VTask.IsCover U s N` is the proposition that the set `N` is a **`U`-cover** (or **`U`-net**) of the set `s`. Concretely, this means that every point of `s` is `U`-related to (i.e., `U`-close to) at least one point of `N`. In other words, the "balls" centred at points of `N`, defined by the relation `U`, collectively cover all of `s`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsCover : {X : Type u_1} -> (U : SetRel X X) -> (s N : Set X) -> Prop
<!-- PINNED-SIGNATURE:END -->


`(U : SetRel X X) -> (s N : Set X) -> Prop`

The implicit argument `X` is the ambient type (think: a metric space or uniform space). The first explicit argument `U` is the entourage — the binary relation on `X` encoding the notion of proximity or closeness. The second argument `s` is the set to be covered. The third argument `N` is the proposed cover (net): the finite or infinite collection of "centre" points whose `U`-neighbourhoods must reach every point of `s`.

### Conventions

There are no junk-value or boundary conventions to declare: the predicate is a universally quantified proposition that is well-defined for all inputs without restriction, including when `s` or `N` is empty or when `U` is an arbitrary (possibly non-reflexive, non-symmetric) relation.

### Worked examples

- Claim: If `U` is reflexive, then every set `s` is a `U`-cover of itself, i.e., `VTask.IsCover U s s` holds whenever `U.IsRefl`.

- Claim: If `N` is a `U`-cover of `t`, and `s ⊆ t`, then `N` is also a `U`-cover of `s` (anti-monotonicity in the covered set).

- Claim: If `N₁` is a `U`-cover of `s` and `N₂ ⊇ N₁`, then `N₂` is also a `U`-cover of `s` (monotonicity in the net).

- Claim: If `N₁` is a `U`-cover of `s` and `N₂` is a `U`-cover of `t`, then `N₁ ∪ N₂` is a `U`-cover of `s ∪ t`.

### Boundaries

- **Empty covered set**: If `s = ∅`, then `VTask.IsCover U ∅ N` holds vacuously for any `N` (including `N = ∅`), because there are no points of `s` to cover.
- **Empty net**: If `N = ∅`, then `VTask.IsCover U s ∅` holds if and only if `s = ∅`, since there are no candidate witnesses in `N`.
- **Non-reflexive or non-symmetric `U`**: The definition makes sense for arbitrary binary relations; no symmetry or reflexivity is assumed. In particular, `VTask.IsCover U s s` may fail if `U` is not reflexive.
- **Coarsening the entourage**: If `U ⊆ V` (i.e., `V` is at least as coarse/broad a relation as `U`) and `N` is a `U`-cover of `s`, then `N` is also a `V`-cover of `s`, since every `U`-witness is also a `V`-witness.

### Not to be confused with

- **`SetRel.IsSeparated`**: A set `N` is `U`-separated if no two distinct points of `N` are `U`-close to each other — the opposite flavor from covering; a maximal `U`-separated subset of `s` is always a `U`-cover of `s`.
- **`Set.IsCover` / topological covers**: In topology, a cover of `s` is a family of open sets whose union contains `s`; here instead, `N` is a set of centre points and coverage is determined by a relation, not by set union.
- **`Metric.IsSeparated` or metric ε-nets**: In a metric space, an ε-net is the special case where `U` is the relation `d(x, y) < ε`; `VTask.IsCover` generalises this to an arbitrary entourage.
