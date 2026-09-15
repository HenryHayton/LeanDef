## Object

`VTask.comp g f` is the composition of two bundled monotone functions: given a monotone map `f : α →o β` and a monotone map `g : β →o γ`, their composite is the monotone map `α →o γ` that sends each element `a : α` to `g(f(a))`. The bundling means that the proof of monotonicity is carried along automatically — the composite of two monotone functions is itself monotone.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [Preorder α] -> [Preorder β] -> [Preorder γ] -> (g : β →o γ) -> (f : α →o β) -> α →o γ
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [Preorder α] -> [Preorder β] -> [Preorder γ] -> (g : β →o γ) -> (f : α →o β) -> α →o γ`

The three type parameters `α`, `β`, and `γ` are the source, intermediate, and target types, respectively. Each carries an implicit `Preorder` instance that gives the ordering needed to speak of monotonicity. The explicit argument `g` is the outer (post-composition) monotone map from `β` to `γ`. The explicit argument `f` is the inner (pre-composition) monotone map from `α` to `β`. Note the order: `g` appears before `f` in the argument list, matching the conventional mathematical notation for composition.

## Conventions

No special junk-value or boundary conventions are declared: the operation is total and well-defined for any two composable bundled monotone maps, and no inputs produce a degenerate or overridden output.

## Worked examples

- Claim: Composing the identity monotone map on the left with any `f : α →o β` yields `f` itself (identity law `id_comp`).

- Claim: Composing any `f : α →o β` on the right with the identity monotone map yields `f` itself (identity law `comp_id`).

- Claim: For three composable monotone maps `h : α →o β`, `g : β →o γ`, `f : γ →o δ`, we have `(f.comp g).comp h = f.comp (g.comp h)` (associativity `comp_assoc`).

- Claim: If `g₁ ≤ g₂` and `f₁ ≤ f₂` (pointwise), then `VTask.comp g₁ f₁ ≤ VTask.comp g₂ f₂` (monotonicity of composition in both arguments).

- Claim: For a constant monotone map `const β c` and any `f : α →o β`, `VTask.comp (const β c) f = const α c` (composing after a constant yields a constant).

## Boundaries

- When either `α`, `β`, or `γ` is an empty type, the composition exists as a valid (vacuously monotone) bundled map; no special case is needed.
- When `f` and `g` are both the identity map, `VTask.comp id id` is again the identity map.
- The underlying function of `VTask.comp g f` is exactly the ordinary function composition `g ∘ f`; evaluating at any point `a` gives `g(f(a))`.
- The pointwise order on `α →o γ` makes `VTask.comp` monotone in both of its arguments simultaneously: if `g` is replaced by a pointwise-larger map and `f` by a pointwise-larger map, the composite is pointwise larger.

## Not to be confused with

- `OrderHom.id`: the identity monotone map, which is the unit for `VTask.comp` on both sides.
- `OrderHom.prod`: pairs two monotone maps into a single map into a product type, rather than sequentially composing them.
- Ordinary function composition `Function.comp` (or `∘`): composes bare functions with no bundled monotonicity proof, so it does not live in the `α →o γ` type.