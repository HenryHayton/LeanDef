## VTask.LiftRel

### Object

Given a relation `r : β → γ → Prop` between two types, `VTask.LiftRel r f g` is the predicate on filter germs that holds when `r (f x) (g x)` is true for **almost every** point `x` — that is, on a set belonging to the filter `l`. It is the canonical way to promote a pointwise relation between functions to a relation between their equivalence classes in the germ quotient, and it is well-defined precisely because the "eventually" quantifier is compatible with the germ equivalence relation.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.LiftRel : {α : Type u_1} -> {β : Type u_2} -> {γ : Type u_3} -> {l : Filter α} -> (r : β → γ → Prop) -> (f : l.Germ β) -> (g : l.Germ γ) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.LiftRel : {α : Type u_1} -> {β : Type u_2} -> {γ : Type u_3} ->
  {l : Filter α} -> (r : β → γ → Prop) -> (f : l.Germ β) -> (g : l.Germ γ) -> Prop
```

The implicit type parameters `α`, `β`, `γ` are the index type and the two value types respectively. The implicit `l : Filter α` is the filter over which the germ quotient is formed; it determines what "almost every" means. The explicit argument `r : β → γ → Prop` is the pointwise relation to be lifted. The arguments `f : l.Germ β` and `g : l.Germ γ` are the two germs (equivalence classes of functions `α → β` and `α → γ` under eventual equality) to be compared.

### Conventions

The definition is total: it is defined for every filter `l`, including the trivial filter. When `l` is the trivial (bottom) filter — in which every set is "large" — the eventual condition `∀ᶠ x in l, r (f x) (g x)` is vacuously true, so `VTask.LiftRel r f g` holds for any `f`, `g`, and `r` in that degenerate case.

### Worked examples

- Claim: For constant germs `↑x` and `↑y`, if `r x y` holds, then `VTask.LiftRel r (↑x : l.Germ β) (↑y : l.Germ γ)` holds.

- Claim: For a `NeBot` filter `l` and constant germs, `VTask.LiftRel r (↑x : l.Germ β) (↑y : l.Germ γ)` is equivalent to `r x y`. In particular, `VTask.LiftRel (· ≤ ·) (↑(3 : ℕ) : l.Germ ℕ) ↑5` holds when `l` is a `NeBot` filter, since `3 ≤ 5`.

- Claim: For representative functions `f : α → β` and `g : α → γ`, `VTask.LiftRel r (↑f : l.Germ β) (↑g : l.Germ γ)` is equivalent to `∀ᶠ x in l, r (f x) (g x)`. This is the fundamental unfolding lemma.

- Claim: The `≤` order on `l.Germ β` (for a `Preorder β`) equals `VTask.LiftRel (· ≤ ·)`. That is, `f ≤ g ↔ VTask.LiftRel (· ≤ ·) f g` for all germs `f g : l.Germ β`.

### Boundaries

- **Bottom filter (`l = ⊥`):** Every set belongs to `⊥`, so `∀ᶠ x in ⊥, P x` is vacuously true. Therefore `VTask.LiftRel r f g` holds for *all* `f`, `g`, `r` when `l = ⊥`, regardless of the values of `f` and `g`.
- **`NeBot` filter:** When `l` is `NeBot`, the constant-germ version is a genuine biconditional: `VTask.LiftRel r ↑x ↑y ↔ r x y`.
- **Non-constant representatives:** Two germs may be represented by different functions that agree eventually; `VTask.LiftRel` correctly treats such representatives as indistinguishable, since it depends only on the eventual behaviour.
- **Empty type `β` or `γ`:** The definition is still type-correct; there simply are no germs of inhabited type to instantiate.

### Not to be confused with

- **`Filter.Eventually` / `∀ᶠ x in l, P x`:** The underlying eventual quantifier used inside `VTask.LiftRel`; `VTask.LiftRel` is the quotient-level encapsulation of that notion.
- **`Filter.Germ.map₂`:** Lifts a *function* `β → γ → δ` to germs, whereas `VTask.LiftRel` lifts a *relation* and produces a `Prop`.
- **`Filter.EventuallyEq`:** The special case `VTask.LiftRel (· = ·)`, which is the germ equality/equivalence relation itself, not a general relation lift.