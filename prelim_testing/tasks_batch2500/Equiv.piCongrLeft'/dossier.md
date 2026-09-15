## VTask.piCongrLeft'

### Object

Given a type family `P` indexed over a type `α`, and an equivalence `e` between `α` and another type `β`, `VTask.piCongrLeft'` produces an equivalence of dependent function types: the type of sections `(a : α) → P a` is equivalent to the type of sections `(b : β) → P (e.symm b)`. Concretely, any function `f` out of `α` into the fibers of `P` can be reindexed along `e` to produce a function out of `β` into the same fibers, and this reindexing is invertible. This is the "change of base" or "transport" operation on dependent pi-types.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piCongrLeft' : {α : Sort u_1} -> {β : Sort u_4} -> (P : α → Sort u_9) -> (e : α ≃ β) -> ((a : α) → P a) ≃ ((b : β) → P (e.symm b))
<!-- PINNED-SIGNATURE:END -->


`VTask.piCongrLeft' : {α : Sort u_1} -> {β : Sort u_4} -> (P : α → Sort u_9) -> (e : α ≃ β) -> ((a : α) → P a) ≃ ((b : β) → P (e.symm b))`

The first implicit argument `α` is the source index type; the second implicit argument `β` is the target index type. The argument `P` is the type family (fibration) indexed over `α` that is being transported. The argument `e` is the equivalence from `α` to `β` whose inverse (`e.symm`) is used to reindex the fiber.

### Conventions

No junk-value or edge-case conventions are declared: the construction is total and well-defined for all choices of `α`, `β`, `P`, and `e`, including degenerate choices such as empty types or the identity equivalence.

### Worked examples

- Claim: Applying `VTask.piCongrLeft' P (.refl α)` to any section `f` of `P` returns the same section (up to the reflexivity equivalence being trivial).

- Claim: For the constant family `P := fun _ => R` and any equivalence `e : α ≃ β`, the forward direction of `VTask.piCongrLeft' (fun _ => R) e` sends `f : α → R` to the function `fun b => f (e.symm b)`.

- Claim: The symmetry of `VTask.piCongrLeft' (fun _ => P) e` equals `VTask.piCongrLeft' (fun _ => P) e.symm`, reflecting the law that inverting the equivalence of base spaces corresponds to using the inverse equivalence.

- Claim: For `e = Equiv.refl α`, `VTask.piCongrLeft' P (Equiv.refl α)` is the identity equivalence on `(a : α) → P a`.

### Boundaries

- When `α` and `β` are both empty types and `e` is the unique equivalence between them, both `(a : α) → P a` and `(b : β) → P (e.symm b)` are the unit type (there is exactly one dependent function out of an empty type), and the equivalence maps the unique element to the unique element.
- When `e = Equiv.refl α`, the equivalence `VTask.piCongrLeft' P e` reduces to the reflexivity (identity) equivalence on `∀ a, P a`, as stated by `piCongrLeft'_refl`.
- When `P` is a constant family `fun _ => T`, the result is an equivalence `(α → T) ≃ (β → T)`, i.e., the non-dependent function-type version of base-change.
- The forward function applies `e.symm` to each index; the inverse undoes this using the fact that `e.symm` followed by `e` is the identity.

### Not to be confused with

- `Equiv.piCongrLeft`: the "opposite direction" variant where the result type is `(b : β) → P b` and the source type uses the forward map, rather than composing with `e.symm`.
- `Equiv.piCongrRight`: transports the *fibers* (codomain) of dependent functions rather than the *base* (index type).
- `Equiv.piCongr`: simultaneously transports both the base and the fibers of dependent pi-types.