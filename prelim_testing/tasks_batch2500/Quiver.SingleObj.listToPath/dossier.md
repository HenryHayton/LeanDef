## Object

`VTask.listToPath` converts a list of elements of type `α` into a path in the `SingleObj α` quiver — the quiver that has exactly one vertex (written `star α`) and whose edges from that vertex back to itself are precisely the elements of `α`. The resulting path starts and ends at the unique vertex, and its edges, read in order, reproduce the original list.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.listToPath : {α : Type u_1} -> List α → Quiver.Path (Quiver.SingleObj.star α) (Quiver.SingleObj.star α)
<!-- PINNED-SIGNATURE:END -->


The only explicit argument is a `List α`, the list of elements to be encoded as edges. The implicit type argument `α` determines what type the list elements — and therefore the edges of the path — have. The source and target of the returned path are both fixed at `Quiver.SingleObj.star α`, the unique vertex of the single-object quiver.

## Conventions

No special junk-value or edge conventions have been declared for this definition: it is a structurally total function whose output is fully determined by the recursive structure of the input list.

## Worked examples

- Claim: `VTask.listToPath ([] : List Nat)` equals the empty (nil) path at `Quiver.SingleObj.star Nat`.

- Claim: `VTask.listToPath [1, 2, 3]` produces a path of length 3 in the `SingleObj Nat` quiver, whose edges (read from outermost cons inward) are `1`, `2`, `3`.

- Claim: Applying `Quiver.SingleObj.pathToList` to `VTask.listToPath l` recovers `l`, i.e., the round-trip `pathToList ∘ listToPath = id` holds for every list `l : List α`.

- Claim: `VTask.listToPath` is a left inverse of `Quiver.SingleObj.pathToList`, so every path in the single-object quiver is in the image of `VTask.listToPath`.

## Boundaries

- On the empty list `[]`, the function returns `Path.nil`, the zero-length path at `star α`.
- On a cons `a :: l`, the function recurses on `l` and prepends edge `a`, so the length of the resulting path equals the length of the input list.
- Because `SingleObj α` has exactly one vertex, both endpoints of every output path are definitionally equal; there is no distinction between the source and target types.

## Not to be confused with

- `Quiver.SingleObj.pathToList` — the inverse direction, converting a path back to a list; `VTask.listToPath` is its left inverse.
- `Quiver.Path.cons` — the primitive operation that prepends a single edge to a path; `VTask.listToPath` applies it recursively across a whole list.
- `Quiver.Path.nil` — the empty path; `VTask.listToPath []` returns exactly this, but for non-empty lists the result is a strictly longer path.
