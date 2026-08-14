## Object

`VTask.withBot f` takes a supremum-preserving map `f : α → β` between semilattice-sup types and lifts it to a supremum-and-bottom-preserving map between the "bottom-adjoined" extensions `WithBot α → WithBot β`. The construction adds a new least element `⊥` to both the domain and codomain and extends `f` by sending the new `⊥` to the new `⊥`, making the lifted map a `SupBotHom`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.withBot : {α : Type u_1} -> {β : Type u_2} -> [SemilatticeSup α] -> [SemilatticeSup β] -> (f : SupHom α β) -> SupBotHom (WithBot α) (WithBot β)
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> {β : Type u_2} -> [SemilatticeSup α] -> [SemilatticeSup β] -> (f : SupHom α β) -> SupBotHom (WithBot α) (WithBot β)`

The implicit type arguments `α` and `β` are the source and target types. The two instance arguments supply the semilattice-sup structures on `α` and `β` respectively. The explicit argument `f` is the supremum-preserving map (a `SupHom`) being lifted; it is the only piece of data actually provided by the user.

## Conventions

The new bottom element `⊥` in `WithBot α` (the one that was adjoined, not any pre-existing bottom) is mapped to the new bottom element `⊥` in `WithBot β` — junk values do not arise because `⊥` is always defined and its image is fixed.

## Worked examples

- Claim: For the identity `SupHom`, `VTask.withBot (SupHom.id α)` equals the identity `SupBotHom` on `WithBot α`.

- Claim: For composable `SupHom`s `f : SupHom β γ` and `g : SupHom α β`, lifting their composition equals composing their individual lifts: `VTask.withBot (f.comp g) = (VTask.withBot f).comp (VTask.withBot g)`.

- Claim: `VTask.withBot f` maps `⊥` to `⊥` — that is, the `map_bot` condition holds by definition, so the `⊥` of `WithBot α` is preserved.

- Claim: For any `a b : α` (viewed as elements of `WithBot α` via the canonical inclusion), `VTask.withBot f (↑a ⊔ ↑b) = ↑(f a) ⊔ ↑(f b)`, reflecting that `f` preserves finite suprema on the non-bottom part.

## Boundaries

- When one or both inputs to the lifted map are `⊥`, the supremum involves `⊥` as an absorbing-identity element in a `WithBot` lattice, and the map handles these cases correctly: `⊥ ⊔ x = x` is respected by sending the `⊥` summand to `⊥` in the codomain.
- When both inputs are coerced elements `(a : α)` and `(b : α)`, the output is the coercion of `f (a ⊔ b)`, using `f`'s sup-preservation on the underlying type.
- The construction is functorial: it respects composition and identities, so it defines a functor from the category of semilattice-sup homomorphisms to the category of `SupBotHom`s.

## Not to be confused with

- `SupBotHom.withTop`: the dual construction that adjoins a top element `⊤` to domain and codomain of a `SupHom`, not a bottom.
- `InfHom.withTop` / `InfTopHom`: the analogous construction for infimum-preserving maps with an adjoined top, which is the order-dual situation.
- `SupHom.withTop`: a version that adjoins `⊤` rather than `⊥`; do not confuse the direction of the adjunction.