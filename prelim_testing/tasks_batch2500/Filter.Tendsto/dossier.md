## Object

`VTask.Tendsto f l₁ l₂` is the classical "limit of a function" predicate in the language of filters. It asserts that the function `f : α → β` is *eventually* well-behaved with respect to the pair of filters `l₁` on `α` and `l₂` on `β`: every set that belongs to `l₂` (every "neighbourhood of the limit") has its `f`-preimage belonging to `l₁` (is a "neighbourhood of the point being approached"). In classical analysis this specialises to statements such as "`f(x) → L` as `x → a`", "a sequence converges", "a function tends to infinity", and so on, depending on which concrete filters are chosen for `l₁` and `l₂`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Tendsto : {α : Type u_1} -> {β : Type u_2} -> (f : α → β) -> (l₁ : Filter α) -> (l₂ : Filter β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> {β : Type u_2} -> (f : α → β) -> (l₁ : Filter α) -> (l₂ : Filter β) -> Prop`

The type parameters `α` and `β` are the domain and codomain types, inferred automatically. `f` is the function whose limit behaviour is being described. `l₁` is the filter on the domain, encoding the "direction of approach" or "input regime" (e.g. neighbourhoods of a point, the Fréchet filter on ℕ for sequences, `atTop` for `x → +∞`). `l₂` is the filter on the codomain, encoding the "target" or "output regime" (e.g. neighbourhoods of a limit value `L`, `atTop` for divergence to `+∞`).

## Conventions

There are no junk-value conventions to declare: `VTask.Tendsto` is a total predicate defined for every function and every pair of filters, and no special convention is needed for degenerate inputs — the definition is well-formed and meaningful in all cases including the trivial filter `⊥` and the whole filter `⊤`.

## Worked examples

- Claim: The constant function `fun _ : ℕ => (0 : ℝ)` satisfies `VTask.Tendsto (fun _ => 0) Filter.atTop (nhds 0)`, i.e. the constant zero sequence converges to zero.

- Claim: The identity function on any type satisfies `VTask.Tendsto id l l` for any filter `l`, since the identity sends every neighbourhood to itself.

- Claim: If `VTask.Tendsto f l₁ l₂` and `VTask.Tendsto g l₂ l₃` then `VTask.Tendsto (g ∘ f) l₁ l₃`, reflecting that limit relations compose (transitivity of `Tendsto` along filter maps).

- Claim: For the sequence `f : ℕ → ℕ` defined by `f n = n`, we have `VTask.Tendsto f Filter.atTop Filter.atTop`, i.e. `n → ∞` as `n → ∞`.

## Boundaries

- When `l₁ = ⊥` (the bottom filter, containing every set), `VTask.Tendsto f ⊥ l₂` holds for *every* `f` and `l₂`, because the image of `⊥` under `map f` is `⊥`, which is below every filter.
- When `l₂ = ⊤` (the top filter, whose only member is the whole space), `VTask.Tendsto f l₁ ⊤` holds for *every* `f` and `l₁`, because every filter is below `⊤`.
- The predicate is monotone in `l₂` (weakening the target makes it easier to satisfy) and antimonotone in `l₁` (strengthening the source makes it easier to satisfy).
- `VTask.Tendsto f l₁ l₂` does **not** require `f` to be continuous, injective, or have any algebraic structure; it is a purely order-theoretic statement about filters.

## Not to be confused with

- `Filter.Eventually`: asserts that a predicate holds on an `l`-large set, used to say something holds "near" a filter point, but does not involve a function mapping between two filter spaces.
- `ContinuousAt f x`: continuity of `f` at a point `x`, which is the special case `VTask.Tendsto f (nhds x) (nhds (f x))` — a particular choice of filters, not the general predicate.
- `Filter.map f l`: the direct image filter of `l` along `f`; `VTask.Tendsto f l₁ l₂` is the statement that this image filter is finer than (i.e. contained in) `l₂`, so `map` is a component of `Tendsto` but is not the same object.