## Object

A constructor that produces a new non-unital, non-associative semiring homomorphism (`NonUnitalNonAssocSemiring` homomorphism) from an existing one, but with its underlying function replaced by a definitionally equal alternative. The resulting morphism is mathematically identical to the original — same source, same target, same values — but Lean's kernel sees the new function as its `toFun`, which can resolve definitional-equality issues that would otherwise block type-checking or rewriting.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [NonUnitalNonAssocSemiring α] -> [NonUnitalNonAssocSemiring β] -> (f : α →ₙ+* β) -> (f' : α → β) -> (h : f' = ⇑f) -> α →ₙ+* β
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [NonUnitalNonAssocSemiring α] -> [NonUnitalNonAssocSemiring β] -> (f : α →ₙ+* β) -> (f' : α → β) -> (h : f' = ⇑f) -> α →ₙ+* β`

The first implicit argument is the source type; the second is the target type. The two instance arguments supply the `NonUnitalNonAssocSemiring` structures on those types. `f` is the original non-unital ring homomorphism being copied. `f'` is the new bare function to use as the underlying map. `h` is a proof that `f'` is propositionally (in fact, judgementally) equal to the coercion of `f` to a function; it certifies that the replacement carries exactly the same values.

## Conventions

The operation is total: no restriction on the inputs beyond what the types require. There are no junk-value conventions declared for this definition.

## Worked examples

- Claim: For any non-unital ring homomorphism `f`, `VTask.copy f (⇑f) rfl` has the same underlying function as `f` (i.e., `⇑(VTask.copy f (⇑f) rfl) = ⇑f`).

- Claim: For any non-unital ring homomorphism `f`, `VTask.copy f (⇑f) rfl` is equal to `f` as a non-unital ring homomorphism (i.e., `VTask.copy f (⇑f) rfl = f`).

- Claim: If `f' : α → β` satisfies `h : f' = ⇑f`, then the coercion of `VTask.copy f f' h` to a function equals `f'` (not merely `⇑f`), so `⇑(VTask.copy f f' h) = f'`.

## Boundaries

- The proof `h` must witness that `f'` equals the coercion of `f`; if `f'` and `⇑f` happen to be definitionally equal but `h` is non-trivial (e.g., a longer equality proof), the result is still the copy with `f'` as its `toFun`.
- When `f' = ⇑f` and `h = rfl`, the copy is trivially equal to `f` both as a function and as a structured morphism.
- The copy preserves all semiring-homomorphism axioms automatically, because `h` guarantees the underlying function is the same.
- This constructor is purely a bookkeeping device: it does not change any mathematical behaviour, only how Lean's kernel unfolds `toFun`.

## Not to be confused with

- `NonUnitalRingHom.mk`: constructs a non-unital ring homomorphism from scratch by supplying the function and all axiom proofs, rather than wrapping an existing one.
- `RingHom.copy`: the analogous construction for *unital* ring homomorphisms (`α →+* β`), which additionally requires the map to send `1` to `1`.
- `NonUnitalRingHom.comp`: composes two non-unital ring homomorphisms into a new one; unrelated to fixing definitional equalities.