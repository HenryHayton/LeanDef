## VTask.Shatters

### Object

Given a family `𝒜` of finite sets (each a `Finset α`) and a finite set `s`, we say that `𝒜` **shatters** `s` — written `𝒜.Shatters s` — when every subset of `s` is "cut out" from `s` by some member of `𝒜`. More precisely, for every `t ⊆ s` there exists some `u ∈ 𝒜` such that `s ∩ u = t`. Equivalently, the collection of traces `{ s ∩ u | u ∈ 𝒜 }` is exactly the full power set of `s`. This is the central notion in VC theory (Vapnik–Chervonenkis theory), where shattering captures the idea that the family is expressive enough to realise all possible binary labellings on the points of `s`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Shatters : {α : Type u_1} -> [DecidableEq α] -> (𝒜 : Finset (Finset α)) -> (s : Finset α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Shatters : {α : Type u_1} -> [DecidableEq α] -> (𝒜 : Finset (Finset α)) -> (s : Finset α) -> Prop`

The implicit type argument `α` is the ambient type whose elements form the ground set. The `DecidableEq α` instance is needed to compute intersections and membership tests on `Finset α`. The first explicit argument `𝒜` is the **set family** — a finite collection of finite subsets of `α` — whose tracing power is being interrogated. The second explicit argument `s` is the **target set** — the finite subset of `α` that the family is claimed to shatter.

### Conventions

There are no special junk-value or boundary conventions declared for this predicate: it is a universally quantified `Prop` that is well-formed for every choice of `𝒜` and `s`, including the empty family and the empty set, so no special sentinel values are needed.

### Worked examples

- Claim: The family `𝒜 = { {}, {1}, {2}, {1,2} }` (the full power set of `{1,2}`) shatters `s = {1,2}`, because for every subset `t ⊆ {1,2}` we can find a `u ∈ 𝒜` with `{1,2} ∩ u = t`.

- Claim: The empty family `𝒜 = ∅` does **not** shatter the empty set `s = ∅`, because `∅.Shatters ∅` requires the existence of some `u ∈ ∅` with `∅ ∩ u = ∅`, yet `∅` has no members — so `(∅ : Finset (Finset ℕ)).Shatters ∅` is false.

- Claim: Any singleton family `𝒜 = {u}` shatters `s` if and only if `s ∩ u = s` (i.e., `s ⊆ u`), because then the only required trace `s` is achieved by `u`, and the only subset needing to be traced is... wait, one member can only produce one trace `s ∩ u`, so `𝒜` shatters `s` via a singleton only when `s = ∅` (the power set of `∅` has exactly one element, namely `∅` itself, which is `s ∩ u` for any `u`).

- Claim: If `𝒜` shatters `s` and `t ⊆ s`, then `𝒜` shatters `t` as well (`Shatters.mono_right`).

- Claim: If `𝒜 ⊆ ℬ` and `𝒜` shatters `s`, then `ℬ` shatters `s` as well (`Shatters.mono_left`).

### Boundaries

- **Empty set as target**: The empty set `∅` is shattered by any non-empty family (since its only subset is `∅` itself, and `s ∩ u = ∅ ∩ u = ∅` for any `u`). It is **not** shattered by the empty family, because no witness `u ∈ ∅` can exist.
- **Empty family**: `∅.Shatters s` is false for every `s`, including `s = ∅`, because no element `u ∈ ∅` exists to witness the intersection condition.
- **The family shatters s implies it is nonempty**: If `𝒜.Shatters s` holds then `𝒜` must be non-empty (there must be at least one member serving as witness for the empty subset of `s`).
- **Shattering implies a superset exists**: If `𝒜` shatters `s`, then some member of `𝒜` contains `s` as a subset (obtained by choosing `t = s` in the definition).
- **The VC dimension connection**: The size of any set shattered by `𝒜` is bounded above by the VC dimension `𝒜.vcDim`.

### Not to be confused with

- **`Finset.powerset`**: The powerset of `s` is the collection of all subsets of `s`; shattering says the *traces* of `𝒜` on `s` equal this powerset, but the powerset itself is not the shattering predicate.
- **`Finset.vcDim`**: The VC dimension is the supremum of sizes of sets that `𝒜` shatters; it is a derived numerical quantity, not the shattering predicate itself.
- **Set-theoretic covering / hitting**: A family can *cover* or *hit* a set (every point is in some member) without shattering it; shattering is a strictly stronger condition requiring all subsets, not merely points, to appear as traces.
