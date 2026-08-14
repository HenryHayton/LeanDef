## Object

`VTask.seq f g` is the *applicative sequencing* filter: given a filter `f` of functions `α → β` and a filter `g` of inputs `α`, it produces the filter of outputs `β` that arises when a function "close to" `f` is applied to a point "close to" `g`. Concretely, a set `s ⊆ β` belongs to `VTask.seq f g` if and only if there exist a set `u` in `f` (a set of functions) and a set `t` in `g` (a set of inputs) such that every value `m x` with `m ∈ u` and `x ∈ t` lies in `s`. This is the filter-theoretic analogue of the applicative `<*>` operation on sets, lifted to the filter lattice.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.seq : {α : Type u_1} -> {β : Type u_2} -> (f : Filter (α → β)) -> (g : Filter α) -> Filter β
<!-- PINNED-SIGNATURE:END -->


`(f : Filter (α → β)) -> (g : Filter α) -> Filter β`

The first argument `f` is a filter on the type of functions `α → β`; it represents a notion of "nearness" or "eventual behaviour" among functions. The second argument `g` is a filter on the domain type `α`; it represents a corresponding notion for inputs. The result is a filter on the codomain type `β`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total operation defined uniformly for all filters `f` and `g`, with no edge inputs that require special-cased output.

## Worked examples

- Claim: A set `s` belongs to `VTask.seq f g` if and only if there exist `u ∈ f` and `t ∈ g` such that for all `m ∈ u` and all `x ∈ t`, `m x ∈ s` (membership characterisation via `mem_seq_iff`).

- Claim: `VTask.seq (Filter.pure h) g = Filter.map h g` for any function `h : α → β` and filter `g` on `α`; applying a pure/principal function filter to `g` is the same as mapping `h` over `g`.

- Claim: `VTask.seq f (Filter.pure a) = Filter.map (fun m => m a) f` for any `a : α` and filter `f` on `α → β`; sequencing with a pure input evaluates every function in `f` at the fixed point `a`.

- Claim: `VTask.seq` is monotone in both arguments: if `f₁ ≤ f₂` and `g₁ ≤ g₂` then `VTask.seq f₁ g₁ ≤ VTask.seq f₂ g₂`.

- Claim: The filter product `f ×ˢ g` equals `VTask.seq (Filter.map Prod.mk f) g`, so `VTask.seq` subsumes the product filter construction.

## Boundaries

- When `f = Filter.pure h` for a single function `h`, `VTask.seq f g` coincides with `Filter.map h g`, collapsing to ordinary pushforward.
- When `g = Filter.pure a` for a single point `a`, `VTask.seq f g` coincides with `Filter.map (· a) f`, evaluating every function in `f` at `a`.
- When either `f` or `g` is `⊥` (the trivial filter containing every set, i.e., the "bot" filter), `VTask.seq f g` is also `⊥`, because every set `s` trivially has witnesses `u = ∅ ∈ f` or `t = ∅ ∈ g`.
- The operation is **not** the one induced by the monadic bind on filters; it is a distinct applicative structure and may differ from `f >>= fun m => g >>= fun x => pure (m x)` in general.

## Not to be confused with

- `Filter.map`: maps a single ordinary function over a filter; `VTask.seq` generalises this to a *filter-valued* family of functions.
- The monadic bind-derived `ap` (i.e., `f >>= fun m => g.map m`): that construction uses the bind of filters and can produce a strictly larger filter than `VTask.seq f g`; the two do not coincide in general.
- `Set.seq u t`: the set-level applicative sequencing, applying every function in a set `u : Set (α → β)` to every point in `t : Set α`; `VTask.seq` lifts this to filters by quantifying over members of the respective filters.