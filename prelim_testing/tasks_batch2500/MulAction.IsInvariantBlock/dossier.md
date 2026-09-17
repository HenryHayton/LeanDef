## VTask.IsInvariantBlock

### Object

A set `B` in a space `X` on which a type `G` acts is called a **G-invariant block** if every element of `G`, when it acts on `B`, maps `B` into itself — that is, the image of `B` under any `g` is a subset of `B`. This is the condition that `B` is closed under the action of every element of `G`. Note that when `G` is merely a type with a scalar multiplication (not necessarily a group), this invariance condition does not automatically make `B` a "block" in the classical sense of the theory of group actions.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsInvariantBlock : (G : Type u_1) -> {X : Type u_2} -> [SMul G X] -> (B : Set X) -> Prop
<!-- PINNED-SIGNATURE:END -->


`(G : Type u_1) -> {X : Type u_2} -> [SMul G X] -> (B : Set X) -> Prop`

The first explicit argument `G` is the type acting on `X`; it need not be a group. The implicit argument `X` is the type being acted upon. The instance argument `[SMul G X]` provides the scalar-multiplication structure, i.e., the action of `G` on `X`. The final explicit argument `B` is the subset of `X` whose invariance is being asserted.

### Conventions

When `G` is not a group (only a type equipped with a scalar multiplication), the predicate may still be stated and may hold, but the resulting `B` is not necessarily a block in the sense of classical group-action theory; the definition is genuinely applicable in that broader context, but the term "invariant block" carries its full meaning only in the group setting.

### Worked examples

- Claim: For the trivial group `Unit` acting on any type `X`, every subset `B : Set X` satisfies `VTask.IsInvariantBlock Unit B`.

- Claim: If `G` is a group acting on `X` and `B = Set.univ`, then `VTask.IsInvariantBlock G (Set.univ : Set X)` holds, because any action maps the whole space into itself.

- Claim: If `G` is a group acting on `X` and `B = ∅`, then `VTask.IsInvariantBlock G (∅ : Set X)` holds, because the image of the empty set is empty, which is a subset of the empty set.

- Claim: For the natural action of `ZMod 2` on `Fin 2` (where `0` fixes everything and `1` swaps the two elements), the singleton `{0}` is NOT a `VTask.IsInvariantBlock` because the element `1` moves `0` to `1`, taking `{0}` outside itself.

### Boundaries

- The empty set `∅` is always an invariant block under any action, since the image of the empty set under any function is empty, which is a subset of the empty set.
- The whole space `Set.univ` is always an invariant block, since any action maps into the same type.
- When `G` is a group, an invariant block actually satisfies `g • B = B` for all `g` (i.e., equality rather than mere inclusion), because `g⁻¹` also acts and gives the reverse inclusion; but the predicate as stated only requires inclusion.
- The predicate is not restricted to groups: it is stated for any type `G` equipped with `SMul G X`.

### Not to be confused with

- **`MulAction.IsBlock`** (classical blocks): a block in the sense of permutation group theory requires additionally that for any `g : G`, either `g • B = B` or `g • B` and `B` are disjoint; invariant blocks satisfy the stronger one-sided containment for all `g`, which in the group case forces equality.
- **`MulAction.stabilizer`**: the stabilizer of a set is the subgroup of elements fixing the set, a subgroup of `G`, whereas `IsInvariantBlock` is a property of the set `B`, not of `G`.
- **Fixed-point sets (`MulAction.fixedPoints`)**: these are sets of points fixed individually by all of `G`, which is a pointwise condition, whereas `IsInvariantBlock` is a set-level condition.
