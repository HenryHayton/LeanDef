## VTask.prodMap

### Object

Given two partial functions `f : α →. γ` and `g : β →. δ`, `VTask.prodMap f g` is the partial function from pairs `α × β` to pairs `γ × δ` that maps a pair `(a, b)` to `(f(a), g(b))`, defined precisely when both `f` is defined at `a` and `g` is defined at `b`. It is the categorical product of two partial functions, generalising the ordinary product of total functions to the partial setting.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prodMap : {α : Type u_1} -> {β : Type u_2} -> {γ : Type u_3} -> {δ : Type u_4} -> (f : α →. γ) -> (g : β →. δ) -> α × β →. γ × δ
<!-- PINNED-SIGNATURE:END -->


VTask.prodMap : {α : Type u_1} -> {β : Type u_2} -> {γ : Type u_3} -> {δ : Type u_4} -> (f : α →. γ) -> (g : β →. δ) -> α × β →. γ × δ

The four type arguments `α`, `β`, `γ`, `δ` are the source and target types of the two component partial functions, inferred implicitly. The explicit argument `f` is the partial function applied to the first component of an input pair; `g` is the partial function applied to the second component. The result is the partial function on product types that applies `f` and `g` component-wise.

### Conventions

There are no junk-value or edge-case conventions to declare for this definition: `VTask.prodMap` is a total constructor — it accepts any two partial functions and produces a well-defined partial function on products. There are no distinguished inputs that require special treatment.

### Worked examples

- Claim: The domain of `VTask.prodMap f g` at a pair `(a, b)` is exactly the conjunction of `f` being defined at `a` and `g` being defined at `b`. That is, `(VTask.prodMap f g).Dom = { x | (f x.1).Dom ∧ (g x.2).Dom }`.

- Claim: A pair `(c, d)` is a member of `(VTask.prodMap f g) (a, b)` if and only if `c ∈ f a` and `d ∈ g b`. In other words, membership in the output pair decomposes as independent membership in each component.

- Claim: Applying `VTask.prodMap` to the identity partial functions on `α` and `β` yields the identity partial function on `α × β`, i.e., `(PFun.id α).prodMap (PFun.id β) = PFun.id _`.

- Claim: The product-map operation distributes over composition: `(f₂.comp f₁).prodMap (g₂.comp g₁) = (f₂.prodMap g₂).comp (f₁.prodMap g₁)`, reflecting the bifunctor law for the product construction.

### Boundaries

- If one of the two partial functions is the totally undefined partial function (i.e., its domain is empty), then `VTask.prodMap f g` is also totally undefined, since both components must be defined for the result to be defined.
- If both `f` and `g` are total (their domains are all of `α` and `β` respectively), then `VTask.prodMap f g` is also total, with domain all of `α × β`.
- When applied to a pair `(a, b)` where exactly one of `f a` or `g b` is defined, the result is still undefined (the domain condition requires both to hold simultaneously).
- The retrieved value, when the domain condition holds, is exactly the pair `((f a).get h.1, (g b).get h.2)` where `h` witnesses both components' definedness.

### Not to be confused with

- `PFun.prodLift`: lifts two partial functions `f : α →. γ` and `g : α →. δ` sharing the *same* domain type into a single partial function `α →. γ × δ`, rather than combining functions over a product source.
- The ordinary `Prod.map` for total functions: `VTask.prodMap` generalises this to partial functions, adding the requirement that both components must be simultaneously defined.
- `PFun.comp`: sequential composition of partial functions, which threads a single value through two functions rather than applying two functions independently to two components of a pair.