## Object

`VTask.copy` constructs a new continuous open map that is definitionally equal to a given continuous open map `f : α →CO β`, but whose underlying function is recorded as `f'` rather than the coercion of `f`. The result is an identical map for all mathematical purposes; the operation exists solely to adjust the definitional presentation of the underlying function, which is sometimes needed to satisfy Lean's definitional equality checker.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [TopologicalSpace α] -> [TopologicalSpace β] -> (f : α →CO β) -> (f' : α → β) -> (h : f' = ⇑f) -> α →CO β
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [TopologicalSpace α] -> [TopologicalSpace β] -> (f : α →CO β) -> (f' : α → β) -> (h : f' = ⇑f) -> α →CO β`

The implicit type arguments `α` and `β` are the domain and codomain topological spaces, respectively; their topological space structures are provided by the two typeclass arguments. The explicit argument `f` is the continuous open map being copied. The argument `f'` is the new bare function that will serve as the definitional body of the result. The proof `h` witnesses that `f'` is propositionally equal to the coercion of `f` as a function, ensuring that all mathematical content (continuity, openness) is inherited.

## Conventions

There are no junk-value or boundary conventions for this definition: it is a total constructor whose only input is a proof of equality, so every well-typed call yields a well-defined continuous open map.

## Worked examples

- Claim: For any continuous open map `f` and any proof `h : f' = ⇑f`, the result `VTask.copy f f' h` is propositionally equal to `f` as a continuous open map (i.e., `VTask.copy f f' h = f`).

- Claim: For any continuous open map `f` and any proof `h : f' = ⇑f`, the coercion of `VTask.copy f f' h` to a bare function is definitionally `f'` (i.e., `⇑(VTask.copy f f' h) = f'`).

- Claim: Copying `f` with its own coercion (i.e., `f' = ⇑f` and `h = rfl`) yields a map whose underlying function is `⇑f`.

## Boundaries

- The proof `h` is required to go in the direction `f' = ⇑f` (not `⇑f = f'`). The copy operation is only valid when `f'` equals the coercion of `f`, so there is no regime in which the copy could differ behaviourally from the original.
- When `f' = ⇑f` holds by `rfl` (i.e., they are definitionally equal as well as propositionally equal), the copy is completely transparent and the result is indistinguishable from `f` in every context.
- The topological properties (continuity and openness of `f`) are automatically transferred to the copy; no extra proof work is needed by the caller.

## Not to be confused with

- `ContinuousMap.copy`: the analogous operation for continuous maps without the open-map condition; `VTask.copy` additionally preserves the open-map structure.
- The identity map `ContinuousOpenMap.id`: that constructs a canonical identity morphism, not a definitional alias of an existing map.
- Subtype coercion or bundling: `VTask.copy` does not change the mathematical map at all; it only changes which term represents the underlying function definitionally.