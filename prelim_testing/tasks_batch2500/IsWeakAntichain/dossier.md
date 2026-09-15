## VTask.IsWeakAntichain

### Object

A weak antichain in a product of preordered types is a set of functions such that no two distinct elements stand in the strong (strict componentwise) less-than relation to one another. Concretely, if `a` and `b` are two elements of the set and `a` is strongly less than `b` (meaning `a ≤ b` in every component and `a ≠ b` in some sense captured by the strong order), then `a` and `b` must be equal. The condition is symmetric: neither element may strictly dominate the other across all components.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsWeakAntichain : {ι : Type u_1} -> {α : ι → Type u_2} -> [(i : ι) → Preorder (α i)] -> (s : Set ((i : ι) → α i)) -> Prop
<!-- PINNED-SIGNATURE:END -->


The index type `ι` parameterises the product; `α` assigns a type to each index; the typeclass constraint equips each fibre `α i` with a preorder. The set `s` is the subset of the product `Π i, α i` being tested for the weak antichain property.

### Conventions

No junk-value or edge conventions are declared for this predicate: it is a universally-quantified proposition whose truth value is determined entirely by the elements of `s` and the preorders on the fibres, with no special treatment of empty sets, singletons, or out-of-domain inputs.

### Worked examples

- Claim: Every subsingleton set (containing at most one element) satisfies `VTask.IsWeakAntichain`.

- Claim: Every set that is an antichain under the componentwise partial order `≤` (i.e., `IsAntichain (· ≤ ·) s`) also satisfies `VTask.IsWeakAntichain s`, because the strong order `≺` is implied by `≤` on distinct elements.

- Claim: If `VTask.IsWeakAntichain s` holds and `t ⊆ s`, then `VTask.IsWeakAntichain t` holds.

- Claim: For `a ∈ s`, `b ∈ s`, if `a ≺ b` and `VTask.IsWeakAntichain s`, then `a = b`.

### Boundaries

- The empty set trivially satisfies `VTask.IsWeakAntichain`, since the universal quantification over pairs of elements is vacuously true.
- A singleton set also satisfies `VTask.IsWeakAntichain`, again vacuously (there are no two distinct elements to compare).
- The condition is strictly weaker than being an antichain under `≤`: a set can fail to be an antichain under `≤` but still be a weak antichain, because two elements could satisfy `a ≤ b` without satisfying the strong order `a ≺ b`.
- When the preorders are all discrete (equality only), every set is a weak antichain because the strong less-than relation is empty.

### Not to be confused with

- `IsAntichain (· ≤ ·) s`: an antichain under the ordinary partial order, which is a strictly stronger condition than `VTask.IsWeakAntichain`.
- `IsAntichain (· ≺ ·) s`: this is exactly the unfolded definition of `VTask.IsWeakAntichain`; presenting it as a separate object could cause confusion, but the two are definitionally equal.
- A strong antichain (no two distinct elements are comparable under `≤` in either direction), which is stronger than both the above notions.