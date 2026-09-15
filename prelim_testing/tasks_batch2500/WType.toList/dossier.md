## Object

`VTask.toList` converts a `WType`-encoded list into an ordinary Lean `List`. The `WType` construction provides a general way to encode inductive types as well-founded trees; `VTask.toList` extracts the concrete list that a particular such tree represents, acting as one half of an isomorphism between `WType (WType.Listβ γ)` and `List γ`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toList : (γ : Type u) -> WType (WType.Listβ γ) → List γ
<!-- PINNED-SIGNATURE:END -->


VTask.toList : (γ : Type u) -> WType (WType.Listβ γ) → List γ

The first argument `γ` is the type of elements that the list contains. The second argument is the `WType`-encoded list to be converted; it is a well-founded tree built from the `WType.Listβ γ` blueprint that encodes the nil and cons constructors of ordinary lists.

## Conventions

No special junk-value or edge conventions are declared for this function: it is a total structural recursion over a well-founded type with no undefined inputs.

## Worked examples

- Claim: `VTask.toList` applied to the `WType` encoding of an empty list yields `[]`.

- Claim: `VTask.toList` applied to the `WType` encoding of a single-element list `[x]` yields `[x]`.

- Claim: `VTask.toList` applied to the `WType` encoding of `[1, 2, 3]` (built from three nested cons nodes followed by a nil node) yields `[1, 2, 3]`.

- Claim: `VTask.toList` is a left inverse of `fromList`: for any `l : List γ`, `VTask.toList (fromList l) = l`.

## Boundaries

- The `WType` nil node (constructed with `Listα.nil`) is mapped to the empty list `[]`; this is the base case.
- A `WType` cons node carrying head element `hd` and a subtree `f` is mapped to `hd :: VTask.toList (f PUnit.unit)`, recursing on the unique child.
- Because `WType (WType.Listβ γ)` is in bijection with `List γ`, every well-formed input has a uniquely determined output; no input is degenerate or out of range.
- The function is defined by structural recursion on the `WType`, so it terminates for all inputs.

## Not to be confused with

- `List.toArray` or similar coercions: those convert lists to other data structures, not from `WType`-encoded lists to lists.
- `WType.Listβ` itself: that is the shape functor (blueprint) used to define the `WType`, not a conversion function.
- `fromList` (the inverse direction): that maps `List γ → WType (WType.Listβ γ)`, which is the opposite direction of this isomorphism.