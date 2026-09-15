## VTask.PTendsto

### Object

`VTask.PTendsto f l₁ l₂` is a predicate asserting that the partial function `f : α →. β` tends to the filter `l₂` along the filter `l₁`. Concretely, it says that for every set `s` that belongs to `l₂` (every "output neighbourhood"), the *core* of `s` under `f` — that is, the set of all inputs `a` in the domain of `f` such that every value `f` might assign to `a` lies in `s` — belongs to `l₁`. This generalises the usual notion of convergence for total functions to the setting of partial functions, using the core (rather than the preimage) of output sets.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.PTendsto : {α : Type u} -> {β : Type v} -> (f : α →. β) -> (l₁ : Filter α) -> (l₂ : Filter β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`{α : Type u} -> {β : Type v} -> (f : α →. β) -> (l₁ : Filter α) -> (l₂ : Filter β) -> Prop`

The implicit type arguments fix the source and target types. The first explicit argument `f` is the partial function whose limiting behaviour is being described. The second argument `l₁` is the filter on the source type, representing the "direction" or "regime" in which inputs are approaching something (e.g. a point, infinity, or a set). The third argument `l₂` is the filter on the target type, representing the "target neighbourhood system" that the values of `f` are required to approach.

### Conventions

There are no special junk-value or boundary conventions for this predicate: it is a universally-defined proposition whose meaning is determined entirely by the filter-inequality condition, with no inputs excluded or assigned sentinel behaviour.

### Worked examples

- Claim: For a total function `f : α → β` viewed as a partial function defined on all of `α`, `VTask.PTendsto (PFun.res f Set.univ) l₁ l₂` holds if and only if `Filter.Tendsto f l₁ l₂` holds, showing that `VTask.PTendsto` strictly generalises ordinary `Tendsto`.

- Claim: For the partial function `f : ℕ →. ℕ` defined only on even numbers sending each even `n` to `n / 2`, `VTask.PTendsto f (Filter.atTop) (Filter.atTop)` holds: every cofinite output neighbourhood has a core that is a cofinite set of inputs (within the domain), so eventually-large outputs are witnessed by eventually-large inputs.

- Claim: If `VTask.PTendsto f l₁ l₂` holds, then for every `s ∈ l₂`, the set `PFun.core f s` belongs to `l₁`; this is the unfolded characterisation given by `ptendsto_def`.

- Claim: The strictly stronger variant `PTendsto'` (which uses preimage rather than core) implies `VTask.PTendsto`, since the preimage of any set is always a subset of its core when the partial function is involved.

### Boundaries

- If `l₁` or `l₂` is the bottom filter (`⊥`), the predicate holds trivially: `⊥ ≤ l₂` is always true, and a filter pushing forward through `pmap` cannot produce anything larger than the codomain filter when the source filter is `⊥`.
- If `f` has empty domain (no inputs are defined), then for every set `s`, the core `f.core s` is the whole type `α`, so the core of every `l₂`-set is `Set.univ ∈ l₁`, meaning the predicate holds vacuously for any `l₁` and `l₂`.
- When `f` is a total function (its domain is all of `α`), `VTask.PTendsto f l₁ l₂` coincides with `Filter.Tendsto` of the underlying function, witnessed by `tendsto_iff_ptendsto_univ`.
- The predicate is monotone in `l₁` (larger `l₁` makes the condition easier to satisfy) and antitone in `l₂` (larger `l₂` imposes more membership requirements).

### Not to be confused with

- `PTendsto'`: a strictly stronger variant that replaces the core of output sets by their preimage; it implies `VTask.PTendsto` but is not equivalent unless the domain of `f` belongs to `l₁`.
- `Filter.Tendsto`: the ordinary limit predicate for total functions `f : α → β`; `VTask.PTendsto` reduces to it when `f` has full domain, but is genuinely more general.
- `RTendsto`: a relational limit predicate for relations `r : α → β → Prop`; `VTask.PTendsto f l₁ l₂` is equivalent to `RTendsto f.graph' l₁ l₂`, but the two are conceptually presented differently (partial function vs. relation).
