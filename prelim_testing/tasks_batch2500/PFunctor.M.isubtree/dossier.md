## VTask.isubtree

### Object

Given a polynomial functor `F`, a path through its coinductive fixed point `M F`, and a value of type `M F`, `VTask.isubtree` navigates the tree structure of the value by following the path step-by-step and returns the subtree rooted at the node reached at the end of the path. If at any step the label stored at the current node does not match the label demanded by the next step of the path (i.e., the path is not valid for this particular value), the function returns the default element of `M F` instead of continuing.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.isubtree : {F : PFunctor.{uA, uB}} -> [DecidableEq F.A] -> [Inhabited F.M] -> PFunctor.Approx.Path F → F.M → F.M
<!-- PINNED-SIGNATURE:END -->


`{F : PFunctor.{uA, uB}} -> [DecidableEq F.A] -> [Inhabited F.M] -> PFunctor.Approx.Path F → F.M → F.M`

`F` is the polynomial functor whose coinductive fixed point `M F` is the type of infinite trees being navigated. The `DecidableEq F.A` instance is needed to compare node labels (elements of the shape type `F.A`) at each step of the traversal. The `Inhabited F.M` instance provides the default value returned when the path is found to be invalid. The first explicit argument is the path — a finite list of pairs `⟨a, i⟩` where `a` is an expected node label and `i` is a branch index selecting a child — encoding a route through the tree. The second explicit argument is the tree value of type `M F` to navigate.

### Conventions

When the path is invalid at some step — specifically, when the label at the current node does not equal the label demanded by the path — the function returns the default element of `M F` as a junk value rather than signalling an error or returning an `Option`.

### Worked examples

- Claim: Following an empty path through any tree returns the tree itself unchanged (i.e., `VTask.isubtree [] x = x` for all `x : F.M`).

- Claim: Following a one-step path `⟨a, i⟩ :: []` through the tree `M.mk ⟨a, f⟩` (whose root label matches `a`) returns `f i`, the subtree at branch `i`. This is a direct instance of `isubtree_cons` with an empty continuation.

- Claim: Following a path `⟨a, i⟩ :: ps` through a tree `M.mk ⟨a', f⟩` where `a ≠ a'` (label mismatch) returns `default`, the default element of `M F`.

- Claim: For any tree related by a bisimulation `R` and any path `ps` valid for one of the trees, `VTask.isubtree ps s₁` and `VTask.isubtree ps s₂` both have the same root label `a` and their respective children are themselves bisimilar — as stated by `nth_of_bisim`.

### Boundaries

- **Empty path**: The empty path `[]` is always valid for any tree, and the function simply returns the tree itself — there is no branching on labels.
- **Label mismatch at first step**: If the head of a non-empty path demands label `a` but the root of the tree has label `a' ≠ a`, the function immediately returns `default` without inspecting further steps of the path.
- **Label mismatch partway through**: If the path is valid for several steps and then encounters a mismatch, the function returns `default` at that point; the subtrees along the valid prefix are not returned.
- **Valid path**: If every step of the path matches the labels encountered in the tree, the function returns the subtree at the end of the path.
- **Default value**: The returned default has no guaranteed structural relationship to the input tree; it is purely a junk value required by the total-function convention.

### Not to be confused with

- **`PFunctor.M.iselect`**: Extracts the *head label* (element of `F.A`) at the node reached by a path, rather than the entire subtree rooted there.
- **`PFunctor.Approx.isubtree`** (approximation variant): Operates on finite approximations of `M F` rather than on the coinductive fixed point itself, so it works at a fixed depth level.
- **`PFunctor.M.IsPath`**: A predicate asserting that a path *is* valid for a given tree, without performing the navigation or returning a subtree.