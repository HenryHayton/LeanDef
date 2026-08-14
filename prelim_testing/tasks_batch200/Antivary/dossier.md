## 1. Object

`VTask.Antivary f g` is the proposition that the two functions `f` and `g` (both indexed by a common type `ι`, taking values in preordered types `α` and `β` respectively) *antivary*: whenever the value of `g` strictly increases from index `i` to index `j`, the value of `f` weakly decreases from `i` to `j`. Informally, `f` and `g` move in opposite directions across all pairs of indices.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Antivary : {ι : Type u_1} -> {α : Type u_3} -> {β : Type u_4} -> [Preorder α] -> [Preorder β] -> (f : ι → α) -> (g : ι → β) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit type arguments `ι`, `α`, `β` are the index type and the two value types, equipped with preorder instances on `α` and `β`. The explicit argument `f : ι → α` is the first function, whose values live in the preordered type `α`. The explicit argument `g : ι → β` is the second function, whose values live in the preordered type `β`. The proposition asserts the antivary relationship with `g` playing the role of the "driving" (strictly increasing) function and `f` playing the role of the "responding" (weakly decreasing) function.

## 3. Conventions

No special junk-value or boundary conventions are declared for this definition: it is a universally quantified proposition over all index pairs and is vacuously true whenever no pair `i, j` satisfies `g i < g j` (e.g., when `ι` is empty or `g` is constant).

## 4. Worked Examples

- Claim: The functions `f i = -i` and `g i = i` (on `ℤ`) satisfy `VTask.Antivary f g`, because whenever `g j > g i` (i.e., `j > i`), we have `f j = -j ≤ -i = f i`.

- Claim: The constant functions `f i = 0` and `g i = 0` (on `ℤ`) satisfy `VTask.Antivary f g`, since there are no pairs with `g i < g j`, making the condition vacuously true.

- Claim: `VTask.Antivary f g` implies `VTask.Antivary g f` (the relation is symmetric in the sense that if `f` antivaries with `g`, then `g` antivaries with `f`).

- Claim: If `VTask.Antivary f g` holds, then composing either function with the order-dual map yields a monovariance: `VTask.Antivary (OrderDual.toDual ∘ f) (OrderDual.toDual ∘ g)` also holds.

## 5. Boundaries

- When `ι` is the empty type, `VTask.Antivary f g` holds vacuously for any `f` and `g`, since there are no index pairs to check.
- When `g` is a constant function, `VTask.Antivary f g` holds vacuously regardless of `f`, since `g i < g j` is never satisfied.
- When `f` is a constant function, `VTask.Antivary f g` holds for any `g`, since `f j ≤ f i` is always satisfied.
- The condition uses strict inequality on `g` but only weak inequality on `f`, so `f` and `g` being strictly antitone would satisfy it, but so would weaker combinations.
- The definition uses a preorder, not necessarily a partial order or linear order, so antisymmetry and totality are not assumed.

## 6. Not to be confused with

- **`VTask.AntivaryOn`**: the restriction of antivary to a specified subset `s` of the index type, rather than all indices.
- **`Monovary`** (the co-varying counterpart): asserts that `g i < g j` implies `f i ≤ f j`, i.e., `f` and `g` move in the *same* direction — the opposite conclusion from `VTask.Antivary`.
- **`Antitone`**: a property of a single function between ordered types asserting `a ≤ b → f b ≤ f a`; `VTask.Antivary` involves two separate functions on a common index set and is driven by strict inequality in `g`.