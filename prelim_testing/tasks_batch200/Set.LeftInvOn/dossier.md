## VTask.LeftInvOn

### Object

`VTask.LeftInvOn g f s` is the proposition that `g` is a **left inverse** to `f` on the set `s`: for every element `x` belonging to `s`, applying `f` first and then `g` returns `x` unchanged, i.e., `g(f(x)) = x` for all `x ∈ s`. It is a restricted form of the identity equation, imposed only on points inside `s` rather than on the whole type.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.LeftInvOn : {α : Type u} -> {β : Type v} -> (g : β → α) -> (f : α → β) -> (s : Set α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.LeftInvOn : {α : Type u} -> {β : Type v} -> (g : β → α) -> (f : α → β) -> (s : Set α) -> Prop`

The universe levels `u` and `v` are implicit. The first explicit argument `g` is the **candidate left inverse**, a function from `β` back to `α`. The second explicit argument `f` is the **forward function**, mapping `α` to `β`. The third explicit argument `s` is the **domain of interest**, the subset of `α` on which the left-inverse identity is required to hold.

### Conventions

There are no junk-value or default conventions to declare: the predicate is a universally quantified proposition over a set, with no distinguished behaviour at degenerate inputs beyond what the quantification itself delivers — over the empty set the statement is vacuously true, which is just the standard interpretation of universal quantification.

### Worked examples

- Claim: `VTask.LeftInvOn id id (Set.univ : Set ℕ)` holds, since `id(id(x)) = x` for every natural number `x`.

- Claim: `VTask.LeftInvOn (fun _ => 0) (fun _ => 0) (∅ : Set ℕ)` holds vacuously, because the domain is empty and there are no obligations to satisfy.

- Claim: Let `f : ℝ → ℝ` be `fun x => x + 1` and `g : ℝ → ℝ` be `fun y => y - 1`; then `VTask.LeftInvOn g f Set.univ` holds because `(f(x)) - 1 = (x + 1) - 1 = x` for all real `x`.

- Claim: If `f : ℝ → ℝ` is `fun x => x * x` (squaring) and `g` is `Real.sqrt`, then `VTask.LeftInvOn g f {x : ℝ | 0 ≤ x}` holds, since `√(x²) = x` for non-negative reals `x`.

### Boundaries

- **Empty set**: When `s = ∅`, `VTask.LeftInvOn g f ∅` is vacuously true for any `g` and `f`, because there are no points `x ∈ ∅` to check.
- **Full type (universal set)**: When `s = Set.univ`, the condition reduces to the global statement that `g` is a left inverse of `f` everywhere on `α`.
- **Non-injective `f`**: `VTask.LeftInvOn g f s` forces `f` to be injective on `s` (as a consequence), since if `f(x₁) = f(x₂)` for `x₁, x₂ ∈ s` then `x₁ = g(f(x₁)) = g(f(x₂)) = x₂`.
- **`g` need not be a right inverse**: The predicate says nothing about `f(g(y))` for `y` in the image of `f`; that is the separate notion of `RightInvOn`.
- **Behaviour of `g` outside `f '' s`**: `g` is unconstrained on values of `β` that are not in the image of `s` under `f`; the condition only restricts `g` at points of the form `f(x)` with `x ∈ s`.

### Not to be confused with

- **`Set.RightInvOn g f t`**: asserts `f(g(y)) = y` for `y ∈ t`, i.e., `g` is a *right* inverse to `f` on `t` — the roles of left and right are swapped.
- **`Function.LeftInverse g f`**: the *global* (non-set-restricted) statement that `g(f(x)) = x` for *all* `x : α`, with no set parameter.
- **`Set.InvOn g f s t`**: simultaneously asserts both `LeftInvOn g f s` and `RightInvOn g f t`, encoding a two-sided partial inverse on matching domain and codomain sets.
