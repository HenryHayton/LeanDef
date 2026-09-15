## Object

`VTask.IsExtrFilter f l a` is the proposition that the point `a` is either a filter-local minimum or a filter-local maximum of the function `f` with respect to the filter `l`. Concretely, it asserts that in some `l`-neighbourhood of `a` (made precise by the filter), the value `f a` is either ≤ all nearby values or ≥ all nearby values.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsExtrFilter : {α : Type u} -> {β : Type v} -> [Preorder β] -> (f : α → β) -> (l : Filter α) -> (a : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsExtrFilter : {α : Type u} -> {β : Type v} -> [Preorder β] -> (f : α → β) -> (l : Filter α) -> (a : α) -> Prop`

The implicit type `α` is the domain of the function and the carrier of the filter. The implicit type `β` is the codomain, which must carry a preorder so that comparisons of function values make sense. The instance argument supplies that preorder on `β`. The explicit argument `f` is the function whose extremal behaviour is being studied. The explicit argument `l` is the filter on `α` that specifies the notion of "neighbourhood" or "locality" around `a`. The explicit argument `a` is the distinguished point that is being tested for extremality.

## Conventions

No junk-value or edge-case conventions are declared for this predicate: it is a pure disjunction of two well-formed propositions and is meaningful for every choice of inputs.

## Worked examples

- Claim: A constant function satisfies `VTask.IsExtrFilter (fun _ => b) l a` for any filter `l` and any point `a`, because a constant is simultaneously a minimum and a maximum.

- Claim: If `h : VTask.IsExtrFilter f l a` and `g : β → γ` is monotone, then `VTask.IsExtrFilter (g ∘ f) l a` — composing with a monotone function preserves the extremum at `a`.

- Claim: If `h : VTask.IsExtrFilter f l a` and `l' ≤ l`, then `VTask.IsExtrFilter f l' a` — restricting to a coarser (smaller) filter preserves the extremum.

- Claim: If `h : VTask.IsExtrFilter f l a` and `g : β → γ` is antitone, then `VTask.IsExtrFilter (g ∘ f) l a` — composing with an order-reversing function also preserves extremality (swapping min and max).

## Boundaries

- When `l` is the `⊤` filter (the principal filter of the whole space), `VTask.IsExtrFilter f l a` means `a` is a global minimum or global maximum of `f`.
- When `l` is the neighbourhood filter `𝓝 a` in a topological space, `VTask.IsExtrFilter f l a` specialises to the notion of a local extremum in the classical sense.
- The predicate is satisfied trivially by any constant function, regardless of the filter.
- Negating `f` swaps minima and maxima, so if `VTask.IsExtrFilter f l a` holds for a negation-enabled codomain, then `VTask.IsExtrFilter (fun x => -f x) l a` also holds.
- If the filter `l` is replaced by any filter that is smaller (i.e., `l' ≤ l`), the predicate is preserved: extremality over a larger neighbourhood implies extremality over a smaller one.

## Not to be confused with

- `IsMinFilter f l a` — the strictly one-sided version asserting only that `a` is a filter-local minimum; `VTask.IsExtrFilter` is the disjunction of this with the maximum version.
- `IsMaxFilter f l a` — the strictly one-sided version asserting only that `a` is a filter-local maximum; again, `VTask.IsExtrFilter` is weaker (it allows either).
- `IsLocalExtr f a` — the topological specialisation where the filter is implicitly `𝓝 a`; `VTask.IsExtrFilter` is the more general filter-parametrised form.