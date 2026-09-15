## VTask.IsMinFilter

### Object

`VTask.IsMinFilter f l a` is the predicate asserting that `a` is a **local minimum of `f` along the filter `l`**: there exists a set belonging to `l` that contains `a` in its "shadow" (i.e., the predicate holds on an `l`-large set) such that `f a ≤ f x` for every `x` in that set. In classical analysis terms, if `l` is the neighbourhood filter of `a` in a topological space, this says `a` is a local minimum of `f`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsMinFilter : {α : Type u} -> {β : Type v} -> [Preorder β] -> (f : α → β) -> (l : Filter α) -> (a : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


VTask.IsMinFilter : {α : Type u} -> {β : Type v} -> [Preorder β] -> (f : α → β) -> (l : Filter α) -> (a : α) -> Prop

- `α` is the domain type of the function (implicit).
- `β` is the codomain type, which is required to carry a preorder so that `≤` is available (implicit, with the preorder as an instance argument).
- `f` is the function whose local minimum behaviour is being studied.
- `l` is the filter on `α` encoding the notion of "neighbourhood" or "largeness" used to define locality.
- `a` is the point at which the local minimum is being tested.

### Conventions

No junk-value or edge-case conventions are declared for this predicate: it is a universally quantified `eventually` statement and is well-formed for any valid arguments, including degenerate filters such as `⊥` (in which case the predicate is vacuously true since every statement holds eventually in the bottom filter).

### Worked examples

- Claim: The constant function `fun _ : ℝ => (0 : ℝ)` satisfies `VTask.IsMinFilter` at every point for every filter, since `0 ≤ 0` everywhere.

- Claim: For `f : ℝ → ℝ` defined by `f x = x^2`, the point `a = 0` satisfies `VTask.IsMinFilter f (nhds 0) 0`, because `0^2 = 0 ≤ x^2` for all `x` in a neighbourhood of `0`.

- Claim: If `VTask.IsMinFilter f l a` holds and `g : β → γ` is a monotone function (with `γ` a preorder), then `VTask.IsMinFilter (g ∘ f) l a` also holds — composing with a monotone map preserves local minima.

- Claim: If `VTask.IsMinFilter f l a` holds and `l' ≤ l` (i.e., `l'` is a finer filter), then `VTask.IsMinFilter f l' a` also holds — local minima are preserved when passing to finer filters.

### Boundaries

- **Bottom filter (`l = ⊥`):** Every `eventually` statement is true with respect to the bottom filter (it contains every set), so `VTask.IsMinFilter f ⊥ a` holds trivially for any `f` and `a`.
- **Top filter / principal filter on a singleton:** If `l` is the principal filter of `{a}`, then the condition reduces to `f a ≤ f a`, which is reflexivity and therefore always true.
- **Non-strict inequality:** The condition is `f a ≤ f x`, not `f a < f x`, so a point where `f` is constant in a neighbourhood qualifies as a local minimum.
- **Preorder (not necessarily partial order):** The codomain need only be a preorder; in particular, antisymmetry is not required, so there can be points `x` near `a` with `f x ≤ f a` as well, and `a` can still be a minimum.
- **Negation duality:** `VTask.IsMinFilter f l a` implies `IsMaxFilter (fun x => -f x) l a` when the codomain supports negation, and conversely.

### Not to be confused with

- **`IsMinOn f s a`**: the global (or set-restricted) minimum of `f` on a set `s`, defined without any filter; `VTask.IsMinFilter` with `l = 𝓟 s` corresponds to `IsMinOn`.
- **`IsExtrFilter f l a`**: the predicate that `a` is either a local minimum or a local maximum of `f` along `l`; every `VTask.IsMinFilter` implies `IsExtrFilter` but not vice versa.
- **`IsMaxFilter f l a`**: the dual predicate asserting `f x ≤ f a` for `l`-almost all `x`; easily confused with `VTask.IsMinFilter` since they differ only in the direction of the inequality.
