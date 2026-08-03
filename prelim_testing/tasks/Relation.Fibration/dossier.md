## VTask.Fibration

### Object

A fibration between two relational structures is a property of a function `f : α → β` asserting that `f` reflects the relational structure of `rβ` back to `rα` in a lifting sense. Concretely, whenever two elements in `β` are related by `rβ` with the second element being in the image of `f`, the first element is also in the image of `f`, and moreover a preimage can be chosen so that its preimage is related to the original preimage by `rα`. In other words, every `rβ`-predecessor of a point in the image of `f` is itself in the image of `f`, witnessed by a point that is an `rα`-predecessor of the original fiber element. This is the relational analogue of a fibration or surjective-on-morphisms functor: paths in the base can always be lifted to paths in the total space.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Fibration : {α : Type u_1} -> {β : Type u_2} -> (rα : α → α → Prop) -> (rβ : β → β → Prop) -> (f : α → β) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.Fibration : {α : Type u_1} -> {β : Type u_2} -> (rα : α → α → Prop) -> (rβ : β → β → Prop) -> (f : α → β) -> Prop
```

The first explicit argument `rα` is a binary relation on the domain type `α`. The second explicit argument `rβ` is a binary relation on the codomain type `β`. The third explicit argument `f` is the function from `α` to `β` being tested for the fibration property. The universe-polymorphic type arguments `α` and `β` are implicit and inferred from context.

### Conventions

The direction of the relational arguments matters: `rβ b (f a)` means `b` is an `rβ`-predecessor of `f a` (the first argument to `rβ` is the predecessor). There are no junk-value conventions: the predicate is a well-formed universally-quantified proposition for all inputs, so no degenerate inputs produce undefined or meaningless results.

### Worked examples

- Claim: The identity function on any type is a fibration from any relation `r` to itself, because any `r`-predecessor of `id a` is its own preimage.

- Claim: For the natural number order, the function `f : ℕ → ℕ` defined by `f n = 2 * n` is NOT a fibration from `(· < ·)` to `(· < ·)`, because `1 < f 1 = 2` but `1` is not in the image of `f` (it is odd), so no `n' < 1` satisfies `f n' = 1`.

- Claim: The canonical map `toAntisymmetrization (· ≤ ·) : α → Antisymmetrization α (· ≤ ·)` is a fibration from `(· < ·)` to `(· < ·)` (this is `antisymmetrization_fibration` in the neighborhood).

- Claim: For preorders, `VTask.Fibration (· ≤ ·) (· ≤ ·) f` holds if and only if for every `x : α`, the image of the down-set `Iic x` under `f` equals `Iic (f x)` (when `f` is monotone), which shows the fibration condition precisely expresses that lower sets of principal filters are preserved by `f`.

### Boundaries

- If `rβ` is the empty relation (i.e., `rβ b c` is always false), then `VTask.Fibration rα rβ f` holds vacuously for any `rα` and any `f`, since the antecedent `rβ b (f a)` is never satisfied.
- If `f` is a constant function, say `f _ = c`, then `VTask.Fibration rα rβ f` requires that every `rβ`-predecessor of `c` is also `c`, and that there exists an `rα`-predecessor of every element of `α` mapping to itself; this is a strong condition on `rβ` and `rα` simultaneously.
- The property is not symmetric in `rα` and `rβ`: swapping the two relations generally changes whether the fibration condition holds.
- When `α = β` and `f = id`, the fibration condition `VTask.Fibration rα rβ id` becomes: for all `a b`, `rβ b a → ∃ a', rα a' a ∧ a' = b`, which simplifies to `rβ` being contained in `rα` (every `rβ`-predecessor is an `rα`-predecessor).

### Not to be confused with

- `Relation.Map`: a condition asserting that `f` maps `rα`-related pairs to `rβ`-related pairs (covariant direction), which is the opposite direction from fibration.
- `Function.Surjective`: plain surjectivity of `f` without any relational condition; fibration is a relational strengthening that controls the fiber structure.
- `RelHom` / order homomorphisms: these require `f` to preserve or reflect relations in a covariant (forward) sense, whereas fibration is a lifting condition on predecessors (contravariant sense).