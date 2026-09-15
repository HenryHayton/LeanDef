## Object

`VTask.prod f g` is the **pairing** (or diagonal product) of two order-preserving maps with a common domain: given monotone maps `f : α →o β` and `g : α →o γ`, it is the monotone map `α →o β × γ` sending every element `x` of `α` to the pair `(f x, g x)`. The product order on `β × γ` is used, where a pair is ≤ another pair if and only if both components are ≤ component-wise.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [Preorder α] -> [Preorder β] -> [Preorder γ] -> (f : α →o β) -> (g : α →o γ) -> α →o β × γ
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_2} -> {β : Type u_3} -> {γ : Type u_4} -> [Preorder α] -> [Preorder β] -> [Preorder γ] -> (f : α →o β) -> (g : α →o γ) -> α →o β × γ`

The three implicit type arguments are the shared domain type `α`, the codomain type `β` for the first map, and the codomain type `γ` for the second map. The three typeclass arguments supply the preorder structures needed on each of those types. The argument `f` is the first bundled monotone map, determining the left component of each output pair. The argument `g` is the second bundled monotone map, determining the right component of each output pair.

## Conventions

No special junk-value or edge conventions are declared: the construction is total and well-defined for any two order homomorphisms sharing a common domain; there are no boundary inputs requiring a conventionally assigned output.

## Worked examples

- Claim: For the natural number ordering, `VTask.prod id id` sends every `n : ℕ` to `(n, n)`.

- Claim: Projecting the first component of `VTask.prod f g` via the bundled `fst` map recovers `f`, i.e., `OrderHom.fst.comp (VTask.prod f g) = f` for any `f : α →o β` and `g : α →o γ`.

- Claim: Projecting the second component of `VTask.prod f g` via the bundled `snd` map recovers `g`, i.e., `OrderHom.snd.comp (VTask.prod f g) = g` for any `f : α →o β` and `g : α →o γ`.

- Claim: `VTask.prod` is monotone in both arguments: if `f₁ ≤ f₂` and `g₁ ≤ g₂` pointwise as order homomorphisms, then `VTask.prod f₁ g₁ ≤ VTask.prod f₂ g₂` pointwise.

## Boundaries

- When both `f` and `g` are the identity on the same type `α = β = γ`, the result is the diagonal map `x ↦ (x, x)`, which is indeed monotone.
- When `α` is a one-element (unit) preorder, `VTask.prod f g` simply returns the single pair `(f ⋆, g ⋆)` as a constant monotone map.
- When `β` or `γ` carries a discrete (equality-only) preorder, monotonicity of `VTask.prod f g` forces `f` or `g` respectively to be a constant map.
- The pairing satisfies the universal property of products in the category of preorders and monotone maps: composing with the two projection homomorphisms `fst` and `snd` recovers the original maps.

## Not to be confused with

- `OrderHom.comp`: composes two monotone maps sequentially (output of one feeds input of the other), rather than running two maps in parallel on the same input.
- `Prod.map` (or `OrderHom.prodMap`): lifts a pair of maps `f : α →o β`, `g : γ →o δ` to a map `α × γ →o β × δ` on a product domain, acting component-wise — distinct from pairing two maps on a *common* domain.
- `Pi.orderHom` or `OrderHom.pi`: the analogous construction for an arbitrary (possibly infinite) family of codomains indexed by a type, generalizing the binary pairing.
