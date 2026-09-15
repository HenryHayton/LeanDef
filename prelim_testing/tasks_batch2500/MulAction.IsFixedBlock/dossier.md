## VTask.IsFixedBlock

### Object

A set `B` in a type `X` equipped with a left action of a group (or monoid) `G` is called a *G-fixed block* if every element of `G` maps `B` onto itself: for each `g ∈ G`, the image `g • B` (the set of all points `g • x` with `x ∈ B`) equals `B` exactly. In other words, `B` is simultaneously stable under every element of the acting monoid — not merely carried into itself (the weaker notion of invariance), but mapped *onto* itself bijectively (set equality, not just containment).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsFixedBlock : (G : Type u_1) -> {X : Type u_2} -> [SMul G X] -> (B : Set X) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsFixedBlock : (G : Type u_1) -> {X : Type u_2} -> [SMul G X] -> (B : Set X) -> Prop`

The explicit argument `G` is the type supplying the acting scalars (typically a group or monoid). The implicit argument `X` is the type being acted upon. The instance argument `[SMul G X]` provides the scalar-multiplication structure encoding the action of `G` on `X`. The argument `B` is the subset of `X` whose fixed-block status is being asserted.

### Conventions

There are no special junk-value or edge-case conventions declared for this predicate; it is a straightforward universal quantification and its truth value is determined entirely by the action and the set.

### Worked examples

- Claim: The entire set `Set.univ` (all of `X`) is always a `G`-fixed block for any action of `G` on `X`, because `g • Set.univ = Set.univ` for every `g`.

- Claim: The empty set `∅` is always a `G`-fixed block, since `g • ∅ = ∅` for every `g` (there are no points to move).

- Claim: For the trivial action of any monoid `G` on a type `X` (where `g • x = x` for all `g`, `x`), every singleton `{x}` satisfies `VTask.IsFixedBlock G {x}`, since each `g` maps `{x}` to itself.

- Claim: If `G` acts on itself by left multiplication and `B` is a proper nonempty subset that is not a union of cosets, then `B` need not satisfy `VTask.IsFixedBlock G B`; in particular, for `G = ZMod 3` acting on itself, the singleton `{1}` is not a fixed block since `g • {1} ≠ {1}` for `g ≠ 0`.

### Boundaries

- **Empty set**: `g • ∅ = ∅` holds for any `g` under any `SMul` instance that respects the convention `g • ∅ = ∅`, so `∅` satisfies `VTask.IsFixedBlock G ∅` whenever the action sends empty images to the empty set (which is the standard convention for set-image actions in Mathlib).
- **Full set**: `Set.univ` is always a fixed block because the image of the whole type under any function is the whole type (for group actions, which are bijections).
- **Singletons**: A singleton `{x}` is a fixed block if and only if `x` is a fixed point of every `g ∈ G` (i.e., `g • x = x` for all `g`), since `g • {x} = {g • x}` and `{g • x} = {x}` iff `g • x = x`.
- **The predicate is a `Prop`**: it has no computational content; it merely asserts a universally quantified set-equality.

### Not to be confused with

- **`MulAction.IsBlock`** (or a notion of block in a block system): a block in the sense of permutation group theory need not be fixed by all group elements — it is only required that for each `g`, either `g • B = B` or `g • B` is disjoint from `B`. A fixed block is a special (stronger) case.
- **Set invariance / `G`-stable set**: some formulations only require `g • B ⊆ B` (forward invariance) rather than `g • B = B` (equality). For group actions these coincide, but for general monoid actions they can differ.
- **Pointwise fixed set (`fixedPoints`)**: the set of points `x` with `g • x = x` for all `g` is a set of *points*, not a set *B* that is mapped to itself as a whole.
