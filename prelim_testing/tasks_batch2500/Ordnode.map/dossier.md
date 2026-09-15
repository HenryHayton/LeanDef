## Object

`VTask.map f t` applies the function `f` to every element stored in the ordered-node tree `t`, preserving the tree's shape and size exactly. The result has the same branching structure as the input; only the values at each node are replaced by their images under `f`. The operation is **only semantically valid** (i.e., the output is a well-formed ordered set tree) when `f` is strictly monotone: `x < y → f x < f y`. Applying a non-monotone function produces a tree whose shape no longer reflects a valid ordering of its elements.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {α : Type u_1} -> {β : Type u_2} -> (f : α → β) -> Ordnode α → Ordnode β
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {α : Type u_1} -> {β : Type u_2} -> (f : α → β) -> Ordnode α → Ordnode β`

The type parameters `α` and `β` are the element types of the input and output trees, respectively, and are inferred implicitly. The argument `f` is the function to apply to each stored element. The final argument is the `Ordnode α` tree to transform.

## Conventions

No special junk-value or edge-case conventions are declared for this definition beyond the documented precondition: the caller is responsible for ensuring `f` is strictly monotone; violating this precondition silently produces a structurally intact but semantically invalid ordered tree.

## Worked examples

- Claim: Mapping over the empty tree (`Ordnode.nil`) always returns the empty tree, regardless of `f`.
  ```lean
  example (f : ℕ → ℕ) : VTask.map f Ordnode.nil = Ordnode.nil := by rfl
  ```

- Claim: Mapping `(· + 2)` over a single-node tree holding `3` yields a single-node tree holding `5`.
  ```lean
  example : VTask.map (· + 2) (Ordnode.node 1 Ordnode.nil 3 Ordnode.nil) =
      Ordnode.node 1 Ordnode.nil 5 Ordnode.nil := by rfl
  ```

- Claim: `VTask.map` preserves the `size` field of every node, regardless of the function applied.

- Claim: When `f` is strictly monotone and the input tree is `Valid`, the output tree is also `Valid` (and has the same size).

## Boundaries

- **Empty tree**: `VTask.map f Ordnode.nil = Ordnode.nil` — the empty tree maps to the empty tree for any `f`.
- **Single-node tree**: the result is a single-node tree with the same left/right subtrees (both empty) and value `f x`.
- **Non-monotone `f`**: the function is still total — it always returns a well-typed `Ordnode β` — but the ordering invariants of the result are not guaranteed. This is a documented precondition violation, not a runtime error.
- **Size preservation**: the `size` stored at each node is copied verbatim, so `(VTask.map f t).size = t.size` for all trees `t`.

## Not to be confused with

- `Ordnode.mapMonotone` / similar wrappers: higher-level functions that bundle the strict-monotonicity proof together with the mapping operation and guarantee a `Valid` output.
- `Ordnode.filter` or `Ordnode.partition`: these change the *structure* (and size) of the tree by removing elements, unlike `VTask.map` which strictly preserves structure.
- `Ordset.map`: the ordered-set layer wrapper that enforces the strict-monotonicity precondition at the type level, producing a certified `Ordset` rather than a raw `Ordnode`.