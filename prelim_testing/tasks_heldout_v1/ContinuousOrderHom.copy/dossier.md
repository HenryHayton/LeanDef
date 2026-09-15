## Object

`VTask.copy` constructs a new continuous order homomorphism from an existing one by replacing its underlying function with a definitionally equal copy. The result is a `ContinuousOrderHom` (a map that is both continuous and order-preserving) whose underlying function is `f'` rather than the coercion of `f`, while remaining equal to `f` as a `ContinuousOrderHom`. This is a bookkeeping device that allows Lean's type checker to see a preferred definitional form of the underlying function without changing any mathematical content.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [TopologicalSpace α] -> [Preorder α] -> [TopologicalSpace β] -> [Preorder β] -> (f : α →Co β) -> (f' : α → β) -> (h : f' = ⇑f) -> α →Co β
<!-- PINNED-SIGNATURE:END -->


`(f : α →Co β) -> (f' : α → β) -> (h : f' = ⇑f) -> α →Co β`

The first argument `f` is the original continuous order homomorphism being copied. The second argument `f'` is a bare function intended to serve as the new underlying function of the result; it may look syntactically different from the coercion of `f` while being provably equal to it. The third argument `h` is the proof that `f'` is equal to the coercion of `f`, establishing that the replacement is mathematically harmless.

## Conventions

There are no junk-value conventions to declare: the definition is total and its inputs are fully constrained by the type of `h`, which ensures `f'` is always equal to `⇑f`.

## Worked examples

- Claim: For any `f : α →Co β`, `VTask.copy f (⇑f) rfl` has the same coercion as `f`.

- Claim: For any `f : α →Co β` and any proof `h : f' = ⇑f`, the result of `VTask.copy f f' h` is equal to `f` as a `ContinuousOrderHom`.

- Claim: For any `f : α →Co β` and any proof `h : f' = ⇑f`, applying `⇑(VTask.copy f f' h)` to any element `x : α` yields `f' x`.

## Boundaries

- The proof `h` must go in the direction `f' = ⇑f` (not `⇑f = f'`); swapping the sides would require `h.symm`. This is a syntactic asymmetry with no mathematical content.
- When `f' = ⇑f` holds by `rfl` (i.e., they are definitionally equal), `VTask.copy f (⇑f) rfl` simply reproduces `f` with no change whatsoever.
- The output is provably equal to the input `f` (by `copy_eq`) and its coercion is definitionally `f'` (by `coe_copy`); both facts hold unconditionally whenever `h` typechecks.

## Not to be confused with

- `OrderHom.copy`: the analogous copy constructor for plain order homomorphisms, which does not carry topological structure.
- `ContinuousMap.copy`: a copy constructor for continuous maps that ignores the order structure entirely.
- The identity map `ContinuousOrderHom.id`: produces a specific canonical element, not a renamed copy of an arbitrary given map.