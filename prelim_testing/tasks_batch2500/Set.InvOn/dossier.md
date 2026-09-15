## VTask.InvOn

### Object

`VTask.InvOn g f s t` is the proposition that `g` is a two-sided inverse to `f` when `f` is regarded as a function from the set `s` to the set `t`. Concretely, it asserts two things simultaneously: (1) for every `x` in `s`, applying `f` first and then `g` returns `x` (i.e., `g` is a left inverse of `f` on `s`), and (2) for every `y` in `t`, applying `g` first and then `f` returns `y` (i.e., `g` is a right inverse of `f` on `t`). Together these say that `f` and `g` are mutual set-theoretic inverses between `s` and `t`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.InvOn : {α : Type u} -> {β : Type v} -> (g : β → α) -> (f : α → β) -> (s : Set α) -> (t : Set β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.InvOn : {α : Type u} -> {β : Type v} -> (g : β → α) -> (f : α → β) -> (s : Set α) -> (t : Set β) -> Prop`

The first explicit argument `g` is the candidate inverse function, mapping from `β` back to `α`. The second argument `f` is the forward function, mapping from `α` to `β`. The third argument `s` is the subset of the domain type `α` on which the left-inverse condition `g(f(x)) = x` must hold. The fourth argument `t` is the subset of the codomain type `β` on which the right-inverse condition `f(g(y)) = y` must hold.

### Conventions

No junk-value or out-of-domain conventions are declared: `VTask.InvOn` is a `Prop`-valued predicate that is meaningful for all choices of `g`, `f`, `s`, and `t`; it simply holds or fails to hold according to whether both component conditions are satisfied.

### Worked examples

- Claim: `VTask.InvOn id id (Set.univ : Set ℕ) (Set.univ : Set ℕ)` holds, because the identity function is its own two-sided inverse on any set.

- Claim: For `f x = x + 1` and `g y = y - 1` on natural numbers, `VTask.InvOn g f (Set.univ : Set ℕ) (Set.range f)` holds, since `g(f(x)) = x` for all `x` (left inverse on `Set.univ`) and `f(g(y)) = y` for all `y` in the image of `f` (right inverse on `Set.range f`).

- Claim: `VTask.InvOn (fun s => s.erase a) (fun s => insert a s) {s : Finset α | a ∉ s} {s : Finset α | a ∈ s}` expresses that inserting and erasing an element are mutual inverses on the appropriate halves of the power set (the roles of `f` and `g` are swapped compared to `Finset.insert_erase_invOn`).

- Claim: If `f : α → β` is a bijection from `s` to `t`, then `VTask.InvOn (invFunOn f s) f s t` holds, expressing that the set-theoretic inverse function is indeed a two-sided inverse for `f` between `s` and `t`.

### Boundaries

- When `s` or `t` is the empty set, the corresponding component condition holds vacuously. In particular, `VTask.InvOn g f ∅ ∅` is always true regardless of what `g` and `f` are.
- The left-inverse condition only constrains the behaviour of `g ∘ f` at points in `s`; the right-inverse condition only constrains `f ∘ g` at points in `t`. Behaviour of `f` outside `s`, or of `g` outside `t`, is completely unconstrained.
- `VTask.InvOn g f s t` does **not** by itself require that `f` maps `s` into `t` or that `g` maps `t` into `s`; those are additional hypotheses (e.g., `MapsTo`) that must be supplied separately when needed for theorems about bijectivity.
- The relation is not symmetric in `f` and `g` without also swapping `s` and `t`: `VTask.InvOn g f s t` is equivalent to `VTask.InvOn f g t s`.

### Not to be confused with

- `Set.LeftInvOn g f s`: only the left-inverse half — `g(f(x)) = x` for `x ∈ s` — without any condition on a target set `t`.
- `Set.RightInvOn g f t`: only the right-inverse half — `f(g(y)) = y` for `y ∈ t` — without any condition on a source set `s`.
- `Function.Involutive f`: a global statement that `f` is its own inverse everywhere, with no restriction to subsets.
