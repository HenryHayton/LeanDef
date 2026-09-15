## Object

A total function that converts a Dyck word (a balanced sequence of up-steps U and down-steps D) into a binary rooted tree with unit-labelled nodes. The empty Dyck word maps to the empty (nil) tree; every non-empty Dyck word is recursively decoded into a tree by splitting it at the "first return" down-step: the material strictly between the opening U and its matching D becomes the left subtree, and the material strictly after that D becomes the right subtree, joined at a fresh root node.

This map is one half of a canonical bijection between Dyck words and binary rooted trees (the inverse being `VTask.ofTree`).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toTree : (p : DyckWord) -> BinaryTree Unit
<!-- PINNED-SIGNATURE:END -->


VTask.toTree : (p : DyckWord) -> BinaryTree Unit

The single argument `p` is the Dyck word to be converted. It may be the empty word (zero) or any nonempty balanced path.

## Conventions

The empty Dyck word (the additive identity, also written `0`) maps to `BinaryTree.nil`, the unique leaf-free tree. There is no junk value: the function is defined on every Dyck word.

## Worked examples

- Claim: `VTask.toTree 0 = BinaryTree.nil` (the empty Dyck word converts to the nil tree).

- Claim: The Dyck word `UD` (one up followed by one down, semilength 1) converts to a single-node tree `BinaryTree.nil △ BinaryTree.nil`, because the inside part is empty and the outside part is empty.

- Claim: For any binary tree `t : BinaryTree Unit`, `VTask.toTree (VTask.ofTree t) = t` — round-tripping through `ofTree` and then `toTree` is the identity on trees.

- Claim: For any Dyck word `p`, `(VTask.toTree p).numNodes = p.semilength` — the number of internal nodes of the resulting tree equals the semilength (half the length) of the Dyck word.

## Boundaries

- **Empty word**: `p = 0` is the only base case; it always yields `BinaryTree.nil` regardless of how `0` arises.
- **Length-2 word `UD`**: both the inside part and the outside part are the empty word, so the result is `nil △ nil`, a single root with two nil children — the smallest nonempty tree.
- **Concatenation structure**: a Dyck word of the form `x.nest + y` (where `nest` wraps `x` in one U/D pair) splits cleanly: `toTree` produces `toTree x △ toTree y`. This is the recursive contract and there are no irregular inputs where the recursion would not terminate, since every recursive call is on a strictly shorter word.

## Not to be confused with

- **`VTask.ofTree`**: the inverse map, going from `BinaryTree Unit` back to a `DyckWord`; `toTree` and `ofTree` are mutual inverses establishing a bijection.
- **`BinaryTree.ofList` / list-based encodings**: other bijections between combinatorial objects and binary trees that do not pass through the Dyck-word representation.
- **`DyckWord.toTriangulation` or other Catalan-object maps**: Dyck words admit several bijections to different Catalan families; `toTree` targets specifically *binary rooted trees*, not triangulations, parenthesizations, or other such objects.