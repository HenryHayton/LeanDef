## Object

Given two relation homomorphisms — one from a relation `r` on `α` to a relation `s` on `β`, and one from `s` on `β` to a relation `t` on `γ` — their composition is the relation homomorphism from `r` to `t` obtained by composing the underlying functions pointwise. That is, if `f` maps `r`-related pairs to `s`-related pairs, and `g` maps `s`-related pairs to `t`-related pairs, then `g ∘ f` maps `r`-related pairs to `t`-related pairs.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {α : Type u_1} -> {β : Type u_2} -> {γ : Type u_3} -> {r : α → α → Prop} -> {s : β → β → Prop} -> {t : γ → γ → Prop} -> (g : s →r t) -> (f : r →r s) -> r →r t
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> {β : Type u_2} -> {γ : Type u_3} -> {r : α → α → Prop} -> {s : β → β → Prop} -> {t : γ → γ → Prop} -> (g : s →r t) -> (f : r →r s) -> r →r t`

The type parameters `α`, `β`, `γ` are the carrier types, inferred implicitly. The relations `r`, `s`, `t` are binary relations on those types, also inferred implicitly. The first explicit argument `g` is a relation homomorphism from `s` to `t` (the "outer" map). The second explicit argument `f` is a relation homomorphism from `r` to `s` (the "inner" map). The result is a relation homomorphism from `r` to `t`, obtained by applying `f` first and then `g`.

## Conventions

No special junk-value or edge conventions are declared: the operation is total and well-defined for any two composable relation homomorphisms; there are no degenerate inputs requiring special treatment.

## Worked examples

- Claim: Composing the identity homomorphism on `r` with any `f : r →r s` on the left with the identity on `s` yields a homomorphism whose underlying function sends `x` to `f x`.

- Claim: For any `f : r →r s`, `VTask.comp (RelHom.id s) f = f` (left identity law).
  ```lean
  example {α β : Type*} {r : α → α → Prop} {s : β → β → Prop} (f : r →r s) :
      VTask.comp (RelHom.id s) f = f := RelHom.id_comp f
  ```

- Claim: For any `f : r →r s`, `VTask.comp f (RelHom.id r) = f` (right identity law).
  ```lean
  example {α β : Type*} {r : α → α → Prop} {s : β → β → Prop} (f : r →r s) :
      VTask.comp f (RelHom.id r) = f := RelHom.comp_id f
  ```

- Claim: Composition is associative: for `h : r →r s`, `g : s →r t`, `f : t →r u`, `VTask.comp (VTask.comp f g) h = VTask.comp f (VTask.comp g h)`.
  ```lean
  example {α β γ δ : Type*} {r : α → α → Prop} {s : β → β → Prop}
      {t : γ → γ → Prop} {u : δ → δ → Prop}
      (h : r →r s) (g : s →r t) (f : t →r u) :
      VTask.comp (VTask.comp f g) h = VTask.comp f (VTask.comp g h) :=
    RelHom.comp_assoc h g f
  ```

## Boundaries

- When either `f` or `g` is the identity relation homomorphism, the composition returns a homomorphism equal to the other argument (the left and right identity laws).
- The operation is defined for any composable pair: as long as the codomain relation of `f` matches the domain relation of `g`, the composition is valid.
- The underlying function of the composition is exactly function composition of the underlying functions of `g` and `f`.
- There are no inputs for which the operation is undefined or produces a junk value.

## Not to be confused with

- `RelHom.id`: the *identity* relation homomorphism on a single relation, not a composition of two.
- `RelIso.trans`: composition for relation *isomorphisms* (which are invertible), a strictly stronger structure than homomorphisms.
- Function composition `Function.comp`: operates on bare functions without preserving any relational structure, whereas `VTask.comp` additionally guarantees the relation-preservation property.