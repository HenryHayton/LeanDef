## Object

`VTask.codRestrict` takes a function `f : ι → α` whose values are known to all lie inside a set `s ⊆ α`, and produces a new function `ι → ↑s` that sends each input to the same output, but now typed as an element of the subtype `↑s` (i.e., paired with its membership proof). In other words, it "cuts down" the codomain of `f` from `α` to the subtype `s`, making the containment explicit in the type.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.codRestrict : {α : Type u_1} -> {ι : Sort u_5} -> (f : ι → α) -> (s : Set α) -> (h : ∀ (x : ι), f x ∈ s) -> ι → ↑s
<!-- PINNED-SIGNATURE:END -->


`VTask.codRestrict : {α : Type u_1} -> {ι : Sort u_5} -> (f : ι → α) -> (s : Set α) -> (h : ∀ (x : ι), f x ∈ s) -> ι → ↑s`

The first implicit argument is the ambient type `α` in which the set `s` lives. The second implicit argument `ι` is the index type (the domain of `f`). The argument `f` is the original function whose codomain one wishes to restrict. The argument `s` is the target subset of `α` to which the codomain is being cut down. The argument `h` is the proof obligation that every value `f x` is indeed a member of `s`, so the restriction is valid. The result is a function from `ι` to the subtype `↑s`.

## Conventions

There are no junk-value or edge conventions to declare: the definition is total and has no degenerate inputs — it is well-defined for any `f`, `s`, and membership proof `h`.

## Worked examples

- Claim: For `f : Fin 3 → ℕ` defined by `f i = i.val`, and `s = Set.univ`, `VTask.codRestrict f Set.univ (fun x => Set.mem_univ _)` produces a function whose underlying value at each index equals `f` applied to that index.

- Claim: The coercion back to `α` of `VTask.codRestrict f s h x` equals `f x` for all `x`.

- Claim: `VTask.codRestrict (fun n : ℕ => n) (Set.univ : Set ℕ) (fun x => Set.mem_univ x)` is a well-typed function `ℕ → ↑(Set.univ : Set ℕ)`.

- Claim: `VTask.codRestrict` to the range of `f` is always surjective onto that range (i.e., `(VTask.codRestrict f (Set.range f) Set.mem_range_self).Surjective` holds).

## Boundaries

- If `s = ∅` and `h` provides a proof that all `f x ∈ ∅`, then the proof `h` is absurd (since no element is in the empty set), but this can only happen when `ι` itself is empty. In that case, the function is vacuously well-defined and the resulting function is the unique function from an empty type.
- There is no restriction on `ι` being a type as opposed to a general `Sort`, so `ι` can be a `Prop` (a proof type), and the function still makes sense.
- The set `s` need not be a subspace, subgroup, or have any additional structure; `VTask.codRestrict` works for arbitrary sets.
- When `f` is injective, the restricted function is also injective; when the range of `f` equals `s`, the restricted function is surjective.

## Not to be confused with

- `Set.restrict` (domain restriction): that operation restricts the *domain* of a function to a set `s`, yielding `↑s → α`, whereas `VTask.codRestrict` restricts the *codomain*.
- `MapsTo.restrict`: this combines both a domain restriction and a codomain restriction given a maps-to hypothesis, producing `↑s → ↑t`; `VTask.codRestrict` only restricts the codomain and leaves the domain unchanged.
- `Subtype.coind`: essentially the same construction, but conventionally described as building a function into `Subtype s` via coinduction; `VTask.codRestrict` is the `Set`-namespace version with codomain written as `↥s`.