## Object

A constructor that produces a new `LocallyBoundedMap` (a map of bornological spaces that sends bounded sets to bounded sets in the reverse direction — i.e., the preimage of every bounded set is bounded) from an existing one, replacing its underlying function with a definitionally equal copy. The result is equal to the original map as a `LocallyBoundedMap`, but carries the new function at the definitional level, which can be useful when Lean's definitional equality checker needs a particular syntactic form of the underlying function.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {α : Type u_2} -> {β : Type u_3} -> [Bornology α] -> [Bornology β] -> (f : LocallyBoundedMap α β) -> (f' : α → β) -> (h : f' = ⇑f) -> LocallyBoundedMap α β
<!-- PINNED-SIGNATURE:END -->


`VTask.copy (f : LocallyBoundedMap α β) (f' : α → β) (h : f' = ⇑f) : LocallyBoundedMap α β`

The first argument `f` is the original locally bounded map being copied. The second argument `f'` is the new underlying function that will appear as the `toFun` field of the returned map. The third argument `h` is a proof that `f'` is pointwise equal (in fact, definitionally equal as functions) to the coercion of `f` to a bare function; this proof is what allows the bornological property of `f` to be transferred to the new map.

## Conventions

There are no junk-value or edge-case conventions to declare for this definition: it is a total constructor whose inputs are fully constrained by the types and the equality hypothesis, and it always returns a well-formed `LocallyBoundedMap`.

## Worked examples

- Claim: For any locally bounded map `f`, calling `VTask.copy f ⇑f rfl` yields a map whose underlying function is `⇑f`.

- Claim: For any locally bounded map `f`, `VTask.copy f ⇑f rfl = f` as `LocallyBoundedMap` values (this is the `copy_eq` theorem).

- Claim: The coercion of `VTask.copy f f' h` to a function equals `f'` (this is the `coe_copy` theorem).

## Boundaries

- The hypothesis `h` must be an equality `f' = ⇑f`; there is no meaningful sense in which this definition can be applied with a non-equal `f'`, since `h` enforces equality.
- When `f' = ⇑f` and `h` is `rfl`, the copy is definitionally the same structure as the original.
- The definition is total: it works for all bornological types `α` and `β` and for all locally bounded maps.

## Not to be confused with

- `LocallyBoundedMap.mk`: the primary constructor for `LocallyBoundedMap`, which requires supplying the bornological property directly rather than inheriting it from a pre-existing map.
- Function composition of locally bounded maps: that produces a genuinely new map with potentially different behaviour, not merely a renamed copy.
- `Set.BoundedMap` or similar: `LocallyBoundedMap` is about bornological spaces and bounded sets in the bornological sense, not metric or topological boundedness in a direct sense.