## Object

`VTask.copy` produces a new co-Heyting algebra homomorphism that is judgmentally equal to a given one on its underlying function, except that the underlying function is replaced by a (provably equal) substitute. The resulting homomorphism carries the same structural properties (preservation of binary suprema, binary infima, top, and set-difference/co-implication) as the original, but its `toFun` field is definitionally the supplied substitute. The primary use case is resolving definitional equality mismatches that arise in formal proofs.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [CoheytingAlgebra α] -> [CoheytingAlgebra β] -> (f : CoheytingHom α β) -> (f' : α → β) -> (h : f' = ⇑f) -> CoheytingHom α β
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [CoheytingAlgebra α] -> [CoheytingAlgebra β] -> (f : CoheytingHom α β) -> (f' : α → β) -> (h : f' = ⇑f) -> CoheytingHom α β`

The two implicit type arguments are the source and target co-Heyting algebras. The two instance arguments supply the co-Heyting algebra structures on those types. The argument `f` is the original co-Heyting homomorphism being copied. The argument `f'` is the new underlying function that will serve as `toFun` of the result. The argument `h` is a proof that `f'` is propositionally equal to the coercion of `f` to a bare function; this equality is what allows all the homomorphism axioms to be transferred.

## Conventions

There are no junk-value or out-of-domain conventions for this definition: every combination of valid inputs yields a well-formed co-Heyting homomorphism, and the definition is total over its stated domain.

## Worked examples

- Claim: The coercion of `VTask.copy f f' h` to a bare function is exactly `f'`.
  (By `CoheytingHom.coe_copy`, `⇑(f.copy f' h) = f'` holds for any admissible `f`, `f'`, `h`.)

- Claim: `VTask.copy f f' h` equals `f` as a co-Heyting homomorphism.
  (By `CoheytingHom.copy_eq`, `f.copy f' h = f` holds whenever `h : f' = ⇑f`; the copy is propositionally equal to the original even though it may differ definitionally on `toFun`.)

- Claim: If `f' = ⇑f` and `a : α`, then `(VTask.copy f f' h) a = f a`.
  (Follows from `coe_copy` and the fact that `f' = ⇑f`, so evaluation agrees pointwise.)

## Boundaries

- The proof `h` must go in the direction `f' = ⇑f` (not the reverse); swapping would require a separate `h.symm`.
- If `f'` is chosen to be definitionally equal to `⇑f` without any propositional proof, the copy is trivially equal to `f`; the definition still type-checks and produces a valid homomorphism.
- When `f' = ⇑f` is given, the result is always propositionally equal to `f` (by `copy_eq`), so `copy` never introduces genuinely new homomorphisms — its value lies entirely in controlling definitional equality of the underlying function.
- The definition is fully polymorphic: it works for any co-Heyting algebras `α` and `β`, with no size or structure restrictions beyond those imposed by the `CoheytingAlgebra` typeclass.

## Not to be confused with

- `HeytingHom.copy` — the analogous copy constructor for Heyting algebra homomorphisms (the dual notion), which preserves Heyting rather than co-Heyting structure.
- `BoundedLatticeHom.copy` — the copy constructor for bounded lattice homomorphisms, which does not require preservation of the set-difference/co-implication operation.
- The identity homomorphism `CoheytingHom.id` — constructs a canonical homomorphism rather than copying an existing one with a modified underlying function.