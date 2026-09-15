## VTask.comap

### Object

Given a function `m : α → β` and a filter `f` on `β`, `VTask.comap m f` is the **pullback** (or inverse-image filter) of `f` along `m`. It is the coarsest filter on `α` that makes `m` a filter-morphism from that filter to `f`. Concretely, a subset `s ⊆ α` belongs to `VTask.comap m f` if and only if there exists some `t ∈ f` whose preimage under `m` is contained in `s`, i.e., `m ⁻¹' t ⊆ s`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comap : {α : Type u_1} -> {β : Type u_2} -> (m : α → β) -> (f : Filter β) -> Filter α
<!-- PINNED-SIGNATURE:END -->


`VTask.comap : {α : Type u_1} -> {β : Type u_2} -> (m : α → β) -> (f : Filter β) -> Filter α`

The first explicit argument `m` is the function along which the filter is pulled back; it maps from the domain type `α` to the codomain type `β`. The second explicit argument `f` is the filter on `β` being pulled back. The implicit arguments `α` and `β` are the types of the domain and codomain, inferred from `m`.

### Conventions

There are no declared junk-value or boundary conventions for this definition: the construction is total and well-defined for every function `m` and every filter `f` — no degenerate input produces a conventionally assigned output.

### Worked examples

- Claim: For the identity function `id : α → α`, `VTask.comap id f = f` for any filter `f` on `α` — the pullback along the identity recovers the original filter.

- Claim: For the constant function `fun _ => b₀`, `VTask.comap (fun _ => b₀) f` is the top (discrete) filter `⊤` on `α` if `b₀ ∈`-every set in `f`, and equals `⊤` whenever `f` is a principal filter at `b₀` — in general, it is at least as coarse as `⊤`, i.e., `VTask.comap (fun _ => b₀) ⊥ = ⊥`.

- Claim: The product filter `f ×ˢ g` on `α × β` equals `VTask.comap Prod.fst f ⊓ VTask.comap Prod.snd g`, showing that the product is built from two comaps.

- Claim: For composable functions `m : α → β` and `n : β → γ`, `VTask.comap (n ∘ m) f = VTask.comap m (VTask.comap n f)` — pulling back along a composition equals successive pullbacks.

### Boundaries

- When `f = ⊥` (the bottom filter, containing every subset of `β`), `VTask.comap m ⊥ = ⊥` — the pullback of the bottom filter is the bottom filter.
- When `f = ⊤` (the top/trivial filter on `β`, whose only member is `univ`), `VTask.comap m ⊤ = ⊤` — the pullback of the indiscrete filter is the indiscrete filter.
- When `m` is not surjective, the comap filter may fail to be a proper (non-bottom) filter even if `f` is a proper filter; specifically, if the range of `m` is disjoint from some set in `f`, then `VTask.comap m f = ⊥`.
- `VTask.comap m f` is always well-defined as a filter (closed under supersets and finite intersections) regardless of properties of `m` or `f`.

### Not to be confused with

- `Filter.map m f`: the **pushforward** (direct image) filter along `m`; `map` and `comap` are adjoint, not the same.
- `Filter.tendsto m f g`: a proposition asserting that `f` maps into `g` under `m`, i.e., `Filter.map m f ≤ g`, which uses comap dually but is a Prop, not a filter.
- `Set.preimage` (`m ⁻¹' t`): the preimage of a single set, not the comap of a whole filter; comap is the filter built from all such preimages.