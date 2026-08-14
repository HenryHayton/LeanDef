## Object

`VTask.pi s t` is the finite set of all *partially-defined dependent functions* that live exactly over the index set `s`: given a finite set `s` of indices of type `α` and, for each index `a : α`, a finite set `t a` of possible values of type `β a`, the construction produces the finite set of all functions `f` such that, for every `a` that belongs to `s`, `f a` is an element of `t a`. Because membership in `s` is carried as an explicit proof argument, each such function is only required to be defined (and to land in `t a`) for indices `a` lying in `s`; the function has no obligation on indices outside `s`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {α : Type u_1} -> {β : α → Type u} -> [DecidableEq α] -> (s : Finset α) -> (t : (a : α) → Finset (β a)) -> Finset ((a : α) → a ∈ s → β a)
<!-- PINNED-SIGNATURE:END -->


`VTask.pi : {α : Type u_1} -> {β : α → Type u} -> [DecidableEq α] -> (s : Finset α) -> (t : (a : α) → Finset (β a)) -> Finset ((a : α) → a ∈ s → β a)`

The implicit type `α` is the index type; the implicit dependent type family `β` assigns a value type to each index. The `DecidableEq α` instance is required to decide index equality during membership tests. The argument `s` is the finite set of indices over which the functions are defined. The argument `t` assigns, to each index `a : α`, a finite set `t a` of admissible values of type `β a`; elements of the result must pick their value for `a` from `t a` whenever `a ∈ s`.

## Conventions

When `s` is the empty finset, `VTask.pi s t` is the singleton containing the unique empty function (the one with no obligations), regardless of `t`. This is the standard convention for a product over an empty index set being a one-element set.

## Worked examples

- Claim: `VTask.pi ∅ t` is a singleton set containing the unique function on the empty domain, for any `t`.

- Claim: A function `f : (a : α) → a ∈ s → β a` belongs to `VTask.pi s t` if and only if, for every `a ∈ s`, `f a ‹a ∈ s›` belongs to `t a`.

- Claim: If `s = {a₀}` is a one-element finset and `t a₀ = {v₀, v₁}`, then `VTask.pi s t` has exactly two elements, one sending `a₀` to `v₀` and one sending `a₀` to `v₁`.

- Claim: The cardinality of `VTask.pi s t` equals the product `∏ a ∈ s, (t a).card`.

## Boundaries

- When `s = ∅`, the result is the singleton `{Pi.empty β}` — the unique function of type `(a : α) → a ∈ (∅ : Finset α) → β a`. This holds unconditionally, regardless of the values of `t`.
- When any `t a` is empty for some `a ∈ s`, the result is the empty finset, because no function can pick a value for that index.
- The functions in `VTask.pi s t` are only partially defined: their type carries the membership proof `a ∈ s` as an explicit argument, so they have no specified behaviour for indices outside `s`.
- The choice of `t a` for `a ∉ s` is entirely irrelevant: since no function in the result is ever evaluated at an index outside `s`, varying `t` on indices not in `s` does not change the result.

## Not to be confused with

- `Fintype.piFinset`: constructs a finset of *total* functions `(a : α) → β a` when `α` is a `Fintype`, requiring every index to have a value; elements are fully defined everywhere, not just on a chosen sub-finset.
- `Set.pi`: the set-theoretic (not necessarily finite) analogue, which is a `Set` rather than a `Finset` and involves ordinary total functions restricted to a set of indices.
- `Finset.piAntidiag`: a finset of functions `α → ℕ` whose values over a given finset sum to a fixed natural number — related in structure but concerned with a specific numerical constraint, not with drawing values from prescribed fibers.