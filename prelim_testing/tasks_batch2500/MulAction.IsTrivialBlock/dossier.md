## VTask.IsTrivialBlock

### Object

A subset `B` of a type `X` is called a **trivial block** if it satisfies at least one of two extremal conditions: either `B` contains at most one element (it is a subsingleton), or `B` is the entire type `univ`. In other words, `B` is trivial in the sense that it occupies the smallest or largest possible "block-like" position — a singleton (or empty set) at one extreme and the whole space at the other.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsTrivialBlock : {X : Type u_2} -> (B : Set X) -> Prop
<!-- PINNED-SIGNATURE:END -->


The sole argument `B` is the subset of `X` whose triviality is being tested. The ambient type `X` is inferred from `B`.

### Conventions

No special junk-value or edge-case conventions are declared for this definition: the predicate is a straightforward disjunction between two well-defined set-theoretic conditions and is total on all subsets of any type.

### Worked examples

- Claim: The empty set `(∅ : Set X)` satisfies `VTask.IsTrivialBlock ∅` because the empty set is a subsingleton.

- Claim: A singleton `({x} : Set X)` satisfies `VTask.IsTrivialBlock {x}` because a singleton is a subsingleton.

- Claim: `Set.univ` satisfies `VTask.IsTrivialBlock (Set.univ : Set X)` because it equals `univ`.

- Claim: A two-element subset `{x, y}` with `x ≠ y` does **not** satisfy `VTask.IsTrivialBlock {x, y}` when `{x, y} ≠ univ`.

### Boundaries

- The **empty set** is a subsingleton (vacuously, any two elements in it are equal), so it qualifies as a trivial block under the first disjunct.
- A **singleton** `{x}` is also a subsingleton, hence trivial.
- `Set.univ` is trivial via the second disjunct regardless of how many elements `X` has; in particular, if `X` itself is a subsingleton, `univ` is simultaneously trivial by both disjuncts.
- Any subset with at least two distinct elements that is not all of `X` is **not** a trivial block.
- The definition makes no reference to a group action and is purely set-theoretic; the note in the docstring cautions that such a set need not be a genuine block in the dynamical sense unless an appropriate group action is present.

### Not to be confused with

- **`MulAction.IsBlock`**: a set `B` that is a block for a specific group action, meaning every group element either fixes `B` setwise or moves it to a disjoint translate; trivial blocks are the degenerate cases of this concept but the definitions are separate.
- **`Set.Subsingleton`**: the first disjunct of `IsTrivialBlock`; a subsingleton is trivially a trivial block, but `IsTrivialBlock` is strictly weaker because `univ` also qualifies even when it has many elements.
- **`Set.Nontrivial`**: the negation of `Set.Subsingleton`; a nontrivial set in this sense can still be a trivial block if it equals `univ`.
