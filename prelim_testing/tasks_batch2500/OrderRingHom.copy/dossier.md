## Object

`VTask.copy` constructs a new ordered ring homomorphism from an existing one, replacing its underlying function with a definitionally equal copy. The result is extensionally identical to the original morphism but carries a potentially different (though provably equal) function at the term level. This is a standard bookkeeping device used to enforce definitional equalities in situations where Lean's kernel-level reduction does not automatically identify two equal functions.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [NonAssocSemiring α] -> [Preorder α] -> [NonAssocSemiring β] -> [Preorder β] -> (f : α →+*o β) -> (f' : α → β) -> (h : f' = ⇑f) -> α →+*o β
<!-- PINNED-SIGNATURE:END -->


The first two type-universe arguments `α` and `β` are the source and target ordered semirings, each equipped with a `NonAssocSemiring` algebraic structure and a `Preorder`. The argument `f` is the original ordered ring homomorphism (a map `α →+*o β`) to be copied. The argument `f'` is the new underlying function, which must be a bare function `α → β`. The argument `h` is a proof that `f'` is equal to the coercion of `f` to a function; this equality is what guarantees the copy retains all the homomorphism properties of `f`.

## Conventions

No junk-value or edge conventions apply to this definition: it is a total constructor whose output is always a well-formed ordered ring homomorphism, and no boundary inputs produce degenerate or default outputs.

## Worked examples

- Claim: For any ordered ring homomorphism `f : α →+*o β`, `VTask.copy f (⇑f) rfl` has the same coercion as `f`, namely `⇑(VTask.copy f (⇑f) rfl) = ⇑f`.

- Claim: For any ordered ring homomorphism `f : α →+*o β`, `VTask.copy f (⇑f) rfl` is equal to `f` as an ordered ring homomorphism, i.e., `VTask.copy f (⇑f) rfl = f`.

- Claim: If `f : α →+*o β` and `g : α → β` satisfies `h : g = ⇑f`, then `⇑(VTask.copy f g h) = g`.

## Boundaries

- The proof `h` must witness `f' = ⇑f` (not merely propositional equality of values pointwise); the definition requires this exact form of equality so that all ring homomorphism and order homomorphism axioms are inherited without re-verification.
- The most common use case is `f' = ⇑f` and `h = rfl`, in which case the copy is trivially equal to the original both extensionally and (by `copy_eq`) as structured morphisms.
- There is no meaningful sense in which passing "unusual" arguments produces a surprising result: the constraint `h : f' = ⇑f` ensures the copy always has the same underlying function up to definitional equality.

## Not to be confused with

- `OrderRingHom.mk`: constructs an ordered ring homomorphism from scratch by supplying all fields, rather than copying from an existing one.
- `RingHom.copy`: the analogous copy operation for plain (unordered) ring homomorphisms, which does not carry order structure.
- `OrderAddMonoidHom.copy`: the analogous copy for ordered additive monoid homomorphisms, which lacks the multiplicative ring structure.