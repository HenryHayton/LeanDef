## Object

`VTask.pathToList` converts a path in the single-object quiver built from a type `α` into a list of elements of `α`. The single-object quiver `SingleObj α` has exactly one vertex (the unique "star" element) and uses elements of `α` as its arrows. A path from the star to itself is therefore just a sequence of `α`-valued arrows; `pathToList` reads those arrows off in order and assembles them into an ordinary `List α`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pathToList : {α : Type u_1} -> {x : Quiver.SingleObj α} -> Quiver.Path (Quiver.SingleObj.star α) x → List α
<!-- PINNED-SIGNATURE:END -->


`VTask.pathToList : {α : Type u_1} -> {x : Quiver.SingleObj α} -> Quiver.Path (Quiver.SingleObj.star α) x → List α`

The implicit type argument `α` is the type whose elements serve as arrows in the single-object quiver. The implicit argument `x` is the target vertex of the path (which, since there is only one vertex, must equal the star, but is left implicit for generality). The explicit argument is the path itself, a `Quiver.Path` starting at the unique star vertex and ending at `x`; this is the object being converted into a list.

## Conventions

There are no junk-value or special-case conventions: the function is total and well-defined on all valid inputs. The empty path (`Path.nil`) maps to the empty list, which is the natural base case.

## Worked examples

- Claim: `VTask.pathToList` applied to the nil path yields the empty list.

- Claim: For any path `p` from the star to the star and any arrow `a : α`, `VTask.pathToList (Path.cons p a) = a :: VTask.pathToList p`. (Cons prepends `a` to the list for the tail path.)

- Claim: The round-trip `VTask.pathToList (listToPath [1, 2, 3]) = [1, 2, 3]` holds for any list of natural numbers, establishing that `pathToList` is a left inverse to `listToPath`.

- Claim: If `p` is any path in `SingleObj α` starting at the star, then `listToPath (VTask.pathToList p)` equals `p` up to a cast, establishing that `pathToList` is also a right inverse to `listToPath` (up to the trivial cast).

## Boundaries

- The nil path (`Path.nil`) is mapped to `[]`, the empty list — this is the base case of the recursion.
- A cons path `Path.cons p a` is mapped to `a :: pathToList p`, placing the outermost arrow at the head of the resulting list.
- Because `SingleObj α` has only one vertex, the target `x` is always definitionally equal to `star α`; the implicit argument `x` therefore does not affect the output.
- The function is defined for all types `α`, including `α = Empty` (giving only the nil path) or `α = Unit`.

## Not to be confused with

- `Quiver.SingleObj.listToPath`: the inverse direction — converts a `List α` back into a `Quiver.Path`; together the two form the equivalence `pathEquivList`.
- `Quiver.Path.length`: extracts the *length* of a path as a natural number rather than materialising the arrows as a list.
- `Quiver.SingleObj.pathEquivList`: the bundled equivalence `Path (star α) (star α) ≃ List α` of which `pathToList` is one component (the forward map).