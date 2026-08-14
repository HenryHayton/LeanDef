## Object

`VTask.EventuallyEq l f g` is the proposition that two functions `f` and `g` from a type `α` to a type `β` agree *eventually* along the filter `l`: the set of points `x ∈ α` at which `f x = g x` holds is a member of (i.e., is "large" with respect to) the filter `l`. This formalises the idea that `f` and `g` differ only on a "negligible" set as determined by `l`.

The notation `f =ᶠ[l] g` is standard shorthand for this proposition in Mathlib.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.EventuallyEq : {α : Type u_1} -> {β : Type u_2} -> (l : Filter α) -> (f g : α → β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.EventuallyEq (l : Filter α) (f g : α → β) : Prop`

The first argument `l` is the filter on `α` that determines what "eventually" means — it specifies which subsets of `α` are considered "large" or "almost everywhere". The second argument `f` and the third argument `g` are the two functions being compared; the proposition asserts they agree on a set belonging to `l`.

## Conventions

There are no special junk-value or out-of-domain conventions for this definition: it is a total predicate on all filters and all pairs of functions, and each choice of filter gives a well-defined equivalence relation on functions.

## Worked examples

- Claim: Every function is eventually equal to itself along any filter, i.e., `VTask.EventuallyEq l f f` holds for any `l` and `f`.

- Claim: If `f` and `g` are literally equal as functions (`f = g`), then `VTask.EventuallyEq l f g` holds for every filter `l`.

- Claim: For the principal filter `Filter.principal s`, `VTask.EventuallyEq (Filter.principal s) f g` holds if and only if `∀ x ∈ s, f x = g x`.

- Claim: For the cofinite filter on `ℕ`, two functions `f g : ℕ → ℤ` satisfy `VTask.EventuallyEq Filter.cofinite f g` if and only if `{n : ℕ | f n ≠ g n}` is finite.

## Boundaries

- When `l = ⊥` (the bottom filter, whose filter sets are all subsets of `α`, including `∅`): every set belongs to `⊥`, so `VTask.EventuallyEq ⊥ f g` holds for *all* pairs `f, g` regardless of their values.
- When `l = ⊤` (the top filter, i.e., the filter whose only member is the whole set `α`): `VTask.EventuallyEq ⊤ f g` requires that `f x = g x` for *every* `x`, i.e., `f = g` pointwise.
- `VTask.EventuallyEq` is an equivalence relation for any fixed `l`: it is reflexive (every function is eventually equal to itself), symmetric, and transitive.
- If `f =ᶠ[l] g` and `l' ≤ l` (i.e., `l'` is finer than `l`), then `f =ᶠ[l'] g` as well, since every `l`-large set is also `l'`-large.

## Not to be confused with

- `Filter.Eventually (fun x => f x = g x) l` — this is literally the same proposition unfolded; `VTask.EventuallyEq l f g` is definitionally equal to it, but `EventuallyEq` packages the two-function form with dedicated API and notation.
- `Filter.EventuallyLE l f g` (`f ≤ᶠ[l] g`) — the analogous *eventual inequality* (order) relation, which only requires `f x ≤ g x` on a filter-large set, not equality.
- Pointwise equality `f = g` (as functions) — this is the special case corresponding to `VTask.EventuallyEq ⊤ f g` and is strictly stronger than eventual equality along any proper filter.