## Object

`VTask.withTop f` is the canonical extension of a sup-homomorphism `f : α →sup β` to a sup-homomorphism `WithTop α →sup WithTop β`. It lifts `f` to the larger ordered type obtained by freely adjoining a greatest element `⊤` to both the domain and codomain: elements that were already in `α` (resp. `β`) are mapped by `f` as before, while the new top element of `WithTop α` is sent to the new top element of `WithTop β`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.withTop : {α : Type u_1} -> {β : Type u_2} -> [SemilatticeSup α] -> [SemilatticeSup β] -> (f : SupHom α β) -> SupHom (WithTop α) (WithTop β)
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> {β : Type u_2} -> [SemilatticeSup α] -> [SemilatticeSup β] -> (f : SupHom α β) -> SupHom (WithTop α) (WithTop β)`

The first two arguments are the source and target types of the original homomorphism, inferred implicitly. The next two arguments are the semilattice-sup structures on those types, supplied by instance search. The final explicit argument `f` is the sup-homomorphism being extended.

## Conventions

The new top element `⊤` in `WithTop α` is mapped to the new top element `⊤` in `WithTop β`; there is no junk value — the construction is total and canonical on all of `WithTop α`.

## Worked examples

- Claim: Applying `VTask.withTop (SupHom.id α)` to a `WithTop`-coerced element `a : α` returns the coercion of `a` back into `WithTop α`, i.e., `VTask.withTop (SupHom.id α) = SupHom.id (WithTop α)`.

- Claim: For composable sup-homomorphisms `f : SupHom β γ` and `g : SupHom α β`, extending each separately and then composing equals extending their composite: `(f.comp g).withTop = f.withTop.comp g.withTop` (functoriality of `VTask.withTop`).

- Claim: For any `a b : WithTop α`, `VTask.withTop f (a ⊔ b) = VTask.withTop f a ⊔ VTask.withTop f b`; in particular, when both are `⊤`, both sides equal `⊤`.

## Boundaries

- When `a = ⊤` in `WithTop α`, the extended map sends it to `⊤` in `WithTop β`, regardless of `f`.
- When `a` is a coercion of a proper element of `α`, the extended map acts exactly as `f` (then recoerces the result into `WithTop β`).
- The construction correctly handles the binary sup in all four cases: `⊤ ⊔ ⊤`, `⊤ ⊔ b↑`, `a↑ ⊔ ⊤`, and `a↑ ⊔ b↑`.
- The function is total; every element of `WithTop α` (including the newly adjoined `⊤`) has a well-defined image.

## Not to be confused with

- `SupHom.withBot`: the analogous construction adjoining a bottom element `⊥` rather than a top element.
- `WithTop.map` (the bare function): this is just the underlying function on `WithTop`, not packaged as a `SupHom`; `VTask.withTop f` provides the proof that the map preserves `⊔`.
- `OrderHom` extensions to `WithTop`: those extend order-preserving maps, not necessarily sup-preserving ones, and lack the algebraic `SupHom` structure.