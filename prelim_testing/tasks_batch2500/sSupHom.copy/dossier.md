## Object

`VTask.copy` produces a copy of a complete-supremum homomorphism (`sSupHom`) where the underlying function has been replaced by a definitionally equal one. The resulting homomorphism is equal to the original as a mathematical object, but carries `f'` as its literal underlying function. This is a purely technical device used to repair or enforce definitional equality between the coercion of a homomorphism and some other term.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [SupSet α] -> [SupSet β] -> (f : sSupHom α β) -> (f' : α → β) -> (h : f' = ⇑f) -> sSupHom α β
<!-- PINNED-SIGNATURE:END -->


The first two implicit arguments are the source and target types, which must each be equipped with a supremum operation (`SupSet`). The argument `f` is the original complete-supremum homomorphism being copied. The argument `f'` is the new underlying function that will replace `f`'s coercion in the resulting structure. The argument `h` is a proof that `f'` is equal to the coercion of `f`, certifying that the replacement is definitionally safe.

## Conventions

No special junk-value or out-of-range conventions apply: the function is total and every argument is constrained by the type system. There are no edge cases that produce an undefined or degenerate result.

## Worked examples

- Claim: For any `sSupHom f`, `VTask.copy f (⇑f) rfl` has the same underlying function as `f`.
  The coercion of `VTask.copy f (⇑f) rfl` is exactly `⇑f` (by `coe_copy`).

- Claim: For any `sSupHom f`, `VTask.copy f (⇑f) rfl` is equal to `f` as an `sSupHom`.
  This follows from `copy_eq`: the copied hom and the original are identical as `sSupHom` values.

- Claim: If `g : α → β` satisfies `g = ⇑f`, then `VTask.copy f g h` coerces to `g`, not merely to something equal to `g`.
  This is the defining purpose: the copy carries `g` as its literal `toFun`, making `⇑(VTask.copy f g h) = g` hold definitionally.

## Boundaries

- The proof `h` must be an equality `f' = ⇑f` (pointing from the new function to the old coercion). Reversing the direction would require `h.symm`.
- When `f' = ⇑f` is supplied as `rfl` (when they are definitionally equal), the result is literally the same homomorphism with the same coercion.
- The operation never changes the mathematical content: the image of every set under `VTask.copy f f' h` is the same as under `f`.
- There is no restriction on `α` or `β` beyond having a `SupSet` instance; in particular, no completeness or lattice axioms beyond `SupSet` are required by the signature.

## Not to be confused with

- `sInfHom.copy`: the analogous constructor for complete-infimum homomorphisms, which preserves `sInf` rather than `sSup`.
- The identity morphism on `sSupHom`: that produces a canonical element, whereas `VTask.copy` adjusts the definitional representation of a given element.
- Bundled homomorphism coercion `⇑f`: that extracts the underlying function from an `sSupHom`, while `VTask.copy` wraps a function back into an `sSupHom`.