## Object

`VTask.pullSub T x` constructs a new descriptive tree (a prefix-closed set of lists over `A`) whose elements are exactly those lists `y` such that the first `x.length` entries of `y` form a prefix of `x` **and** the remaining tail `y.drop x.length` belongs to the tree `T`. Informally, it is the tree obtained by "prepending" the list `x` in front of every element of `T`, together with all proper prefixes of `x` itself. This operation is the left adjoint (in the sense of a Galois connection) to `subAt`, which restricts a tree to the subtree rooted at a given node.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pullSub : {A : Type u_1} -> (T : ↥(Descriptive.tree A)) -> (x : List A) -> ↥(Descriptive.tree A)
<!-- PINNED-SIGNATURE:END -->


VTask.pullSub : {A : Type u_1} -> (T : ↥(Descriptive.tree A)) -> (x : List A) -> ↥(Descriptive.tree A)

The first argument `T` is the target tree — the tree that will be "translated" or "prepended to" in the construction. The second argument `x` is the list of labels that is pasted before the root: every element of the resulting tree either is a prefix of `x` (a partial prefix of the prepended path) or is `x` concatenated with some element of `T` (an extension beyond the prepended path into `T`).

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total function whose output is always a well-formed descriptive tree, and both `T` and `x` are unconstrained.

## Worked examples

- Claim: When `x = []`, `VTask.pullSub T []` has the same membership as `T` itself, because the "prepended" path is empty and the drop condition reduces to membership in `T` unchanged.

- Claim: When `T` is the minimal tree containing only the empty list `[]` and `x = [a]`, the elements of `VTask.pullSub T [a]` are exactly `[]` and `[a]` — namely the proper prefix `[]` of `[a]` and `[a]` itself (since `[].drop 1 = []` which is in `T`).

- Claim: A list `y` belongs to `VTask.pullSub T x` if and only if `y.take x.length` is a prefix of `x` and `y.drop x.length` is a member of `T`.

- Claim: If `y ∈ VTask.pullSub T x` and `z` is a prefix of `y`, then `z ∈ VTask.pullSub T x` (prefix-closure is preserved, so the result is indeed a valid descriptive tree).

## Boundaries

- **Empty prepend path (`x = []`):** The length condition becomes vacuous (`y.take 0 = []` is always a prefix of `[]`), so membership reduces entirely to `y ∈ T`. Thus `pullSub T []` is extensionally equal to `T`.
- **Empty tree `T`:** If `T` contains only the empty list (the minimal prefix-closed set), then `pullSub T x` contains exactly the prefixes of `x` (including `x` itself, since `x.drop x.length = []` is in any tree).
- **Very long `y`:** If `y` is longer than `x`, the take-condition pins the first `x.length` entries to be a prefix of `x`, while the suffix is checked against `T`; there is no upper bound on the length of elements in the result beyond what `T` permits.
- **`x` not in the original tree:** `pullSub` does not require `x` to have any relationship with `T`; it freely constructs a new tree regardless.

## Not to be confused with

- **`subAt T x`**: The inverse/adjoint operation — it restricts `T` to the subtree rooted at node `x`, dropping the `x`-prefix from each surviving element. `pullSub` goes in the opposite direction, prepending `x`.
- **List concatenation / `append`**: `pullSub` is not simply element-wise concatenation of `x` with all members of `T`; it also includes all proper prefixes of `x`, making it a genuine prefix-closed tree.
- **`Descriptive.tree.map`** (if it existed): A hypothetical map operation would transform elements bijectively; `pullSub` instead produces a tree whose membership is defined by a split condition on prefixes, which is a richer structure than a simple image.