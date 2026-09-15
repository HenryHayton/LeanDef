## Object

A **W-type** `WType β` is the initial algebra for the polynomial functor `α ↦ Σ a : α, β a → (−)`: its elements are well-founded trees where each node is labelled by some `a : α` and has one child for every element of the fibre `β a`. The elimination map `VTask.elim` is the *canonical fold* (catamorphism) that collapses such a tree into a value of any target type `γ`, given an algebra structure on `γ` expressed as a function `fγ` that knows how to combine a node label with the already-folded children.

Formally, given the algebra `fγ : (Σ a : α, β a → γ) → γ`, the fold assigns to every tree `⟨a, f⟩` the value `fγ ⟨a, λ b, fold(f b)⟩`, recursing into all children and then applying `fγ` at the root. This is well-defined because `WType β` is an *inductive* (well-founded) type.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.elim : {α : Type u_1} -> {β : α → Type u_2} -> (γ : Type u_3) -> (fγ : (a : α) × (β a → γ) → γ) -> WType β → γ
<!-- PINNED-SIGNATURE:END -->


VTask.elim : {α : Type u_1} -> {β : α → Type u_2} -> (γ : Type u_3) -> (fγ : (a : α) × (β a → γ) → γ) -> WType β → γ

- `α` is the type of **node labels** (shapes), an implicit universe-polymorphic type.
- `β` is the **arity family**: for each label `a : α`, `β a` is the type whose elements index the children of a node labelled `a`. This is also implicit.
- `γ` is the **target type** into which the tree is folded; it is an explicit argument.
- `fγ` is the **algebra map** on `γ`: given a pair of a node label `a` and a function `β a → γ` supplying the already-folded values of all children, it produces the folded value at the current node.
- The final argument is the **tree** of type `WType β` to be folded.

## Conventions

There are no junk-value or out-of-domain conventions to declare: the function is total, structurally recursive on a well-founded inductive type, and every argument is unrestricted within its type.

## Worked examples

- Claim: For the W-type of unary natural numbers (node type `Bool`, arities `tt ↦ Unit` for successor and `ff ↦ Empty` for zero), applying `VTask.elim` with the algebra `fγ ⟨tt, k⟩ = k () + 1`, `fγ ⟨ff, _⟩ = 0` to the tree representing `2` yields `2 : ℕ`.

- Claim: If every child of a node is mapped to the same value `c : γ` (i.e., `fγ` ignores its second component and always returns some constant), then `VTask.elim γ fγ` is a constant function on `WType β` returning that constant, provided `fγ` itself is constant.

- Claim: When `α = Unit` and `β () = Empty` (so every tree is a single leaf), `VTask.elim γ fγ (WType.mk () Empty.elim)` equals `fγ ⟨(), Empty.elim⟩`.

- Claim: The elimination map is the *unique* `WType β`-algebra homomorphism from the initial algebra `WType β` to any `γ`-algebra `fγ`; any other map satisfying the same recursion equation must agree with `VTask.elim γ fγ` on every tree.

## Boundaries

- **Leaf nodes** (nodes `⟨a, f⟩` where `β a` is uninhabited, so `f` is `Empty.elim` or equivalent): the fold still applies `fγ ⟨a, fun b => ...⟩` correctly; since there are no children, the function `β a → γ` is vacuously defined and `fγ` receives a pair whose second component has empty domain. The result is simply `fγ ⟨a, Empty.elim⟩` (or the appropriate vacuous function).
- **Branching nodes** (nodes where `β a` has many elements): each child subtree is recursively folded before `fγ` is invoked, ensuring well-founded recursion terminates.
- **Single-element `α`** (all nodes have the same label): the shape type collapses and only the arity `β ()` matters; the fold degenerates to a tree fold over a fixed branching type.
- **`γ = WType β`** with `fγ = WType.mk` as the algebra: the fold is the identity on `WType β` (by initiality), though Lean does not automatically reduce it to the identity without proof.

## Not to be confused with

- **`WType.rec` / `WType.recOn`**: the built-in recursor for `WType β`, which operates in `Sort` (including `Prop`) and is the primitive eliminator; `VTask.elim` is a derived, `Type`-valued version stated in terms of `Sigma`-type algebras.
- **`WType.mk`**: the sole *constructor* of `WType β`, building a tree from a node label and a child function; `VTask.elim` goes in the *opposite* direction, destructing trees.
- **`Sigma.elim`** or **`PSigma.elim`**: eliminators for sigma types, which are flat pairing types, not recursive tree types; they have a superficially similar signature but act on a single constructor with no recursion.
