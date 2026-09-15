## Object

`VTask.PTendsto'` is a predicate asserting that a partial function `f : α →. β` is *convergent from filter `l₁` to filter `l₂`* in the following sense: for every set `s` belonging to `l₂` (i.e., every `l₂`-neighbourhood), the **preimage** of `s` under `f` — meaning the set of points `x : α` such that `f x` is defined and its value lies in `s` — belongs to `l₁`. This is one way to generalise the classical notion of a filter limit (`Filter.Tendsto`) to partial functions, using the *full* preimage (not the domain-restricted one).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.PTendsto' : {α : Type u} -> {β : Type v} -> (f : α →. β) -> (l₁ : Filter α) -> (l₂ : Filter β) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.PTendsto' : {α : Type u} -> {β : Type v} -> (f : α →. β) -> (l₁ : Filter α) -> (l₂ : Filter β) -> Prop
```

`f` is the partial function whose convergence behaviour is being studied. `l₁` is the filter on the domain type `α` representing the "direction from which" the function is evaluated (e.g. a neighbourhood filter of a limit point). `l₂` is the filter on the codomain type `β` representing the "target" of convergence (e.g. a neighbourhood filter of the purported limit value).

## Conventions

There are no special junk-value or boundary conventions for this predicate: it is a well-defined `Prop` for every partial function and every pair of filters, with no undefined or degenerate cases requiring special treatment.

## Worked examples

- Claim: If `f` is a total function and its underlying function satisfies `Filter.Tendsto g l₁ l₂`, then `VTask.PTendsto'` holds for the partial function `PFun.lift g` with the same filters.

- Claim: `VTask.PTendsto' f l₁ l₂` holds if and only if for every `s ∈ l₂` the preimage `f.preimage s` belongs to `l₁` (unfolding via `ptendsto'_def`).

- Claim: If `VTask.PTendsto' f l₁ l₂` holds, then `PTendsto f l₁ l₂` also holds (the `'` version implies the plain version, by `ptendsto_of_ptendsto'`).

- Claim: Conversely, if `PTendsto f l₁ l₂` holds *and* the domain `f.Dom` belongs to `l₁`, then `VTask.PTendsto' f l₁ l₂` holds (by `ptendsto'_of_ptendsto`).

## Boundaries

- When `f` is everywhere undefined (domain is empty), its preimage of any set is empty. The predicate `VTask.PTendsto' f l₁ l₂` then says that `∅ ∈ l₁` for every `s ∈ l₂` — this fails for any proper filter `l₁`, since proper filters do not contain the empty set. Hence convergence of the totally-undefined partial function to any filter fails whenever `l₁` is a proper filter.
- When `l₂` is the trivial (top) filter `⊤` on `β` (whose only member is `Set.univ`), the condition reduces to requiring that `f.preimage Set.univ = f.Dom ∈ l₁`.
- When `l₁` is the bottom filter `⊥` on `α`, the condition is trivially satisfied for any `f` and `l₂`, since every set belongs to `⊥`.
- `VTask.PTendsto'` implies `PTendsto` unconditionally, but the reverse implication requires `f.Dom ∈ l₁` as an extra hypothesis. This means `VTask.PTendsto'` is the *stronger* of the two notions.

## Not to be confused with

- `Filter.PTendsto` (the weaker, plain version): uses the domain-restricted preimage; `PTendsto` does *not* require the domain to be large in `l₁`, while `VTask.PTendsto'` effectively does.
- `Filter.Tendsto`: the standard limit predicate for total functions `f : α → β`; `VTask.PTendsto'` reduces to this when `f` is everywhere defined.
- `Filter.rcomap'`: the right comap along a relation used internally in the definition; it is a filter operation, not the convergence predicate itself.