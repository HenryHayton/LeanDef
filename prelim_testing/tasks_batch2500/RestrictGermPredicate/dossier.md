## VTask.RestrictGermPredicate

### Object

Given a predicate `P` that assigns to each point `x` in a topological space `X` a proposition about germs of functions at `x`, and given a subset `A ⊆ X`, `VTask.RestrictGermPredicate P A` is a new predicate on germs — one that at a point `x` and germ `φ` holds if and only if, when `x ∈ A`, the predicate `P y φ` holds for all `y` in some neighborhood of `x`. The key effect is that universally quantifying the new predicate over all `x : X` is equivalent to saying `P x f` holds for *eventually* every point in the neighborhood filter of the set `A` (written `∀ᶠ x near A, P x f`).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.RestrictGermPredicate : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> (P : (x : X) → (nhds x).Germ Y → Prop) -> (A : Set X) -> (x : X) -> (nhds x).Germ Y → Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.RestrictGermPredicate : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> (P : (x : X) → (nhds x).Germ Y → Prop) -> (A : Set X) -> (x : X) -> (nhds x).Germ Y → Prop`

- `X` is the topological space of base points; it is inferred implicitly.
- `Y` is the target type (the codomain of the functions whose germs are considered); it is inferred implicitly.
- The `TopologicalSpace X` instance supplies the neighborhood filters used throughout.
- `P` is the original predicate on germs: for each point `x : X` it specifies which germs `(nhds x).Germ Y` satisfy the property.
- `A` is the subset of `X` to which the predicate is being restricted.
- `x` is a base point at which the restricted predicate is evaluated.
- The final argument is a germ in `(nhds x).Germ Y`, i.e., an equivalence class of functions `X → Y` under eventual equality at `x`, about which the restricted predicate returns a truth value.

### Conventions

When `x ∉ A`, the predicate `VTask.RestrictGermPredicate P A x φ` holds vacuously for every germ `φ`; the restriction to `A` is enforced by requiring `x ∈ A` as a hypothesis inside the definition.

### Worked examples

- Claim: If `P x φ` holds for every `x : X` and every germ `φ`, then `VTask.RestrictGermPredicate P A x φ` also holds for every `x` and every germ — this is the content of `forall_restrictGermPredicate_of_forall`.

- Claim: Universally quantifying `VTask.RestrictGermPredicate P A` over all `x : X` at a fixed germ `f` is equivalent to: `P y f` holds for eventually every point `y` in the neighborhood filter `𝓝ˢ A` of the set `A`. Formally, `(∀ x, VTask.RestrictGermPredicate P A x f) ↔ ∀ᶠ x in 𝓝ˢ A, P x f`.

- Claim: If `VTask.RestrictGermPredicate P A x f` holds and `g` agrees with `f` eventually on a neighborhood of `A` (i.e., `∀ᶠ z in 𝓝ˢ A, g z = f z`), then `VTask.RestrictGermPredicate P A x g` also holds.

### Boundaries

- **Points outside `A`:** For `x ∉ A`, the predicate is trivially satisfied at any germ; the condition `x ∈ A` is vacuously false, so no constraint is imposed.
- **Empty `A`:** When `A = ∅`, the predicate holds everywhere regardless of `P` or the germ, and the neighborhood filter `𝓝ˢ ∅` is the bottom filter, so `∀ᶠ x in 𝓝ˢ ∅, P x f` is also trivially true.
- **`A = univ`:** When `A` is all of `X`, the restriction is no restriction; `VTask.RestrictGermPredicate P univ x φ` at a point reduces to requiring `P y φ` to hold in a neighborhood of every `x`, which (under the universal quantifier) matches the original predicate `P` behaving near every point.
- **Germ representatives:** The predicate is well-defined on germs (not just on individual function representatives): if two functions agree eventually at `x`, they define the same germ, and the truth value of the predicate is the same for both.

### Not to be confused with

- **`Filter.Germ.liftOn`:** The primitive used to lift a function on representatives to a function on germs; `VTask.RestrictGermPredicate` uses this internally but is a higher-level construction with a specific topological meaning.
- **`Set.restrict` (function restriction to a subtype):** That object restricts the *domain* of a function; `VTask.RestrictGermPredicate` instead restricts *where* a germ predicate is non-vacuous, leaving the domain of `x` as all of `X`.
- **`Filter.Eventually` on `𝓝ˢ A` directly:** One might write `∀ᶠ x in 𝓝ˢ A, P x f` directly; `VTask.RestrictGermPredicate` is the pointwise predicate whose universal quantification over all `x` is *equivalent* to that filter-level statement, not the statement itself.