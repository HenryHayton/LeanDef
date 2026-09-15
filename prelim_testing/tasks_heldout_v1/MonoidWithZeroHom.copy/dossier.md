## Object

`VTask.copy` produces a `MonoidHom` (a monoid homomorphism, without the zero-preservation requirement) from a `MonoidWithZeroHom` `f : α →*₀ β`, by replacing its underlying function with a new function `f'` that is required to be definitionally equal to (i.e., provably the same as) the coercion of `f`. The result carries exactly the same mathematical behaviour as `f` but is packaged as a plain `MonoidHom`. The primary purpose is to fix or massage definitional equalities without changing any mathematical content.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [MulZeroOneClass α] -> [MulZeroOneClass β] -> (f : α →*₀ β) -> (f' : α → β) -> (h : f' = ⇑f) -> α →* β
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [MulZeroOneClass α] -> [MulZeroOneClass β] -> (f : α →*₀ β) -> (f' : α → β) -> (h : f' = ⇑f) -> α →* β`

The type parameters `α` and `β` are the source and target types, each required to carry a `MulZeroOneClass` structure (a type equipped with multiplication, zero, and one). The instance arguments supply those algebraic structures. The argument `f` is the original monoid-with-zero homomorphism being copied. The argument `f'` is the new underlying function that will appear as the `toFun` of the resulting `MonoidHom`. The argument `h` is a proof that `f'` equals the coercion of `f` to a bare function, establishing that the two functions are the same map.

## Conventions

There are no junk-value or out-of-domain conventions for this definition: it is total and well-defined for any valid inputs satisfying the stated types and typeclass constraints.

## Worked examples

- Claim: For any `MonoidWithZeroHom` `f`, calling `VTask.copy f (⇑f) rfl` yields a `MonoidHom` whose underlying function equals `⇑f`.

- Claim: For any `MonoidWithZeroHom` `f : α →*₀ β` and proof `h : f' = ⇑f`, the `MonoidHom` produced by `VTask.copy f f' h`, when viewed as a function, equals `f'`.

- Claim: For any `MonoidWithZeroHom` `f : α →*₀ β` and proof `h : f' = ⇑f`, the result `VTask.copy f f' h` is equal (as a `MonoidHom`) to `f.toMonoidHom`.

## Boundaries

- The proof `h` must have type `f' = ⇑f`; the equality goes in this direction (new function equals old coercion), not the reverse.
- The output type is `α →* β` (a `MonoidHom`), not `α →*₀ β` (a `MonoidWithZeroHom`); the zero-preservation data is intentionally dropped from the packaging.
- When `f' = ⇑f` is `rfl` (the functions are definitionally identical), the copy is indistinguishable from `f.toMonoidHom` by the `copy_eq` lemma.
- Because `h` is a propositional equality, the construction works even when `f'` and `⇑f` are only propositionally, not definitionally, equal, but typically the point is to introduce a definitionally distinct but propositionally equal function.

## Not to be confused with

- `MonoidWithZeroHom.toMonoidHom`: simply forgets the zero-preservation component of `f` without replacing the underlying function, whereas `VTask.copy` additionally substitutes a new function `f'`.
- `ZeroHom.copy` / `MonoidHom.copy`: analogous copy operations for `ZeroHom` and plain `MonoidHom`, which do not start from a `MonoidWithZeroHom`.
- The identity function on `MonoidHom`: `VTask.copy` does not produce a copy of a `MonoidHom`; it produces a `MonoidHom` from a `MonoidWithZeroHom`, changing the packaging rather than the underlying algebra.