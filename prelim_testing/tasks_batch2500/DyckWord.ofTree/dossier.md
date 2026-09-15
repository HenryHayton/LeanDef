## Object

`VTask.ofTree` is a function that converts a binary rooted tree (with trivial node labels of type `Unit`) into a Dyck word. It realises one half of the classical bijection between full binary trees and Dyck paths: the empty tree maps to the empty Dyck word, and a tree whose left subtree is `l` and right subtree is `r` maps to the word obtained by wrapping the image of `l` in a matching open/close pair and then concatenating the image of `r`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ofTree : BinaryTree Unit → DyckWord
<!-- PINNED-SIGNATURE:END -->


VTask.ofTree : BinaryTree Unit → DyckWord

The sole argument is a binary rooted tree whose every internal node carries a trivial `Unit` label. The function returns the Dyck word associated with that tree under the standard bijection.

## Conventions

The empty tree `BinaryTree.nil` maps to the zero element (the empty Dyck word), which is the unique Dyck word of length 0. No junk values arise because the function is total: every binary tree, including `nil`, has a well-defined Dyck word image.

## Worked examples

- Claim: `VTask.ofTree BinaryTree.nil = 0` — the empty tree maps to the empty Dyck word.

- Claim: The Dyck word `VTask.ofTree (BinaryTree.node () BinaryTree.nil BinaryTree.nil)` equals `(VTask.ofTree BinaryTree.nil).nest + VTask.ofTree BinaryTree.nil`, i.e., a single open-close pair followed by nothing, which is the unique Dyck word of semilength 1.

- Claim: For any binary tree `t`, applying `VTask.ofTree` and then `DyckWord.toTree` recovers `t` — the round-trip `DyckWord.toTree (VTask.ofTree t) = t` holds for all `t`.

- Claim: For any Dyck word `p`, applying `DyckWord.toTree` and then `VTask.ofTree` recovers `p` — the round-trip `VTask.ofTree p.toTree = p` holds for all `p`. This, together with the previous fact, shows that `VTask.ofTree` is a bijection whose inverse is `DyckWord.toTree`.

## Boundaries

- The minimal input is `BinaryTree.nil`, which maps to the empty Dyck word (length 0, semilength 0). This is the base case and the only tree of size 0.
- A single-node tree `BinaryTree.node () nil nil` maps to a Dyck word of semilength 1 (one open and one close symbol).
- A right-leaning chain of `n` nodes maps to `n` consecutive nest-wrapped empty words concatenated, yielding a Dyck word of semilength `n`.
- A left-leaning chain of `n` nodes maps to a fully nested Dyck word of semilength `n` (all opens followed by all closes).
- The function is defined on all inputs with no domain restriction; there are no undefined or exceptional cases.

## Not to be confused with

- `DyckWord.toTree`: the inverse function, going from a Dyck word back to a binary tree; `VTask.ofTree` is the forward direction.
- `DyckWord.nest`: an operation on Dyck words that wraps a single word in one extra matching pair; `VTask.ofTree` uses `nest` internally but is a tree-to-word conversion, not a word-to-word operation.
- `DyckWord.semilength` or `DyckWord.length`: numeric properties of a Dyck word; not to be confused with the word itself produced by `VTask.ofTree`.