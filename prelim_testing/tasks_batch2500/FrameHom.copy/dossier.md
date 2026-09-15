## Object

A *copy* of a frame homomorphism is a new `FrameHom` record that carries a potentially different (but provably equal) underlying function in place of the original one. Because Lean's type theory distinguishes definitions by how they reduce, swapping in a definitionally friendlier function while keeping all the homomorphism data intact can resolve goals that are blocked by definitional mismatches. The result is a frame homomorphism that is propositionally equal to the original and has exactly the new function as its coercion.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [CompleteLattice α] -> [CompleteLattice β] -> (f : FrameHom α β) -> (f' : α → β) -> (h : f' = ⇑f) -> FrameHom α β
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [CompleteLattice α] -> [CompleteLattice β] -> (f : FrameHom α β) -> (f' : α → β) -> (h : f' = ⇑f) -> FrameHom α β`

The implicit type arguments `α` and `β` are the source and target complete lattices. The two instance arguments supply the `CompleteLattice` structures on `α` and `β`. The argument `f` is the original frame homomorphism being copied. The argument `f'` is the new underlying function that will serve as the coercion of the resulting homomorphism. The proof `h` witnesses that `f'` is propositionally equal to the coercion of `f`, ensuring no mathematical content is altered.

## Conventions

There are no junk-value or edge-case conventions to declare for this definition: it is a total constructor whose inputs are all constrained by the type signature (in particular, `h` must be an actual proof of equality), so no special behaviour arises at boundary inputs.

## Worked examples

- Claim: For any `FrameHom f`, `VTask.copy f (⇑f) rfl` has the same coercion as `f`, namely `⇑f` itself.

- Claim: For any `FrameHom f`, the result of `VTask.copy f (⇑f) rfl` is propositionally equal to `f` as a `FrameHom`.

- Claim: The coercion of `VTask.copy f f' h` is definitionally (and propositionally) equal to `f'`, the explicitly supplied function.

## Boundaries

- The only admissible input for `h` is a proof that `f'` equals the coercion of `f`; the type enforces this, so there is no "out-of-range" case.
- When `f'` is literally `⇑f` (and `h` is `rfl`), the copy is the most trivial possible use: it produces a `FrameHom` that unfolds directly to `f`'s underlying function without any indirection.
- The mathematical structure (preservation of arbitrary suprema, finite infima, and the top element) is entirely inherited from `f`; `copy` introduces no new proof obligations.

## Not to be confused with

- `FrameHom.mk` — constructs a frame homomorphism from scratch by supplying all the required structure fields, rather than starting from an existing homomorphism.
- `sSupHom.copy` — the analogous copy constructor for homomorphisms that only preserve arbitrary suprema, without the infimum and top requirements of a frame homomorphism.
- `InfTopHom.copy` — the analogous copy constructor for homomorphisms preserving finite infima and top, a strictly weaker structure than a frame homomorphism.