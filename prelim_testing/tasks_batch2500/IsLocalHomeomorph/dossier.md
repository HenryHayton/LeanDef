## VTask.IsLocalHomeomorph

### Object

A function `f : X → Y` between topological spaces is a **local homeomorphism** if every point of `X` has an open neighbourhood on which `f` restricts to a homeomorphism onto an open subset of `Y`. More precisely, `f` is a local homeomorphism if, for every point `x ∈ X`, there exists an open partial homeomorphism `e` (a homeomorphism between two specified open sets) such that `x` lies in the domain of `e` and `f` agrees with `e` everywhere (as functions). In classical terms, this is the standard notion of a local homeomorphism: a continuous open map that is locally injective and locally a homeomorphism.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsLocalHomeomorph : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (f : X → Y) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsLocalHomeomorph : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (f : X → Y) -> Prop`

The implicit type arguments `X` and `Y` are the source and target types. The instance arguments supply the topological structures on `X` and `Y` respectively. The explicit argument `f` is the function under consideration: the proposition asserts that `f` is a local homeomorphism.

### Conventions

There are no declared junk-value conventions for this definition. The predicate is a genuine mathematical condition on a function between topological spaces; no special junk outputs or boundary fill-in choices arise.

### Worked Examples

- Claim: Every homeomorphism `f : X ≃ₜ Y` satisfies `VTask.IsLocalHomeomorph f.toFun`, since a global homeomorphism is in particular a local one at every point.

- Claim: The exponential map `Circle.exp : ℝ → Circle` (wrapping the real line around the unit circle) satisfies `VTask.IsLocalHomeomorph Circle.exp`, because every real number has a small interval neighbourhood on which the map is a homeomorphism onto an open arc.

- Claim: If `f : X → Y` is an open embedding (a topological embedding onto an open subset), then `VTask.IsLocalHomeomorph f` holds, since the entire space `X` serves as the single open domain on which `f` is already a homeomorphism.

- Claim: The identity function `id : X → X` satisfies `VTask.IsLocalHomeomorph (id : X → X)` for any topological space `X`, since `id` is itself a homeomorphism.

### Boundaries

- For a constant function between non-trivial spaces, the property fails: a constant map cannot be locally injective at any point (unless the source has at most one point).
- On a one-point space, every continuous function satisfies the property trivially, since the single point has a neighbourhood homeomorphic to the whole space.
- The property is strictly weaker than being a homeomorphism: a covering map (such as `Circle.exp`) is a local homeomorphism but need not be globally injective.
- A local homeomorphism need not be surjective; an open embedding onto a proper open subset is a local homeomorphism.
- If `X` is empty, the property holds vacuously for every function out of `X`, since the universal quantifier over points of `X` is vacuously true.

### Not to be confused with

- `IsLocalHomeomorphOn f s`: the relativised version, asserting local homeomorphism only at points of a given subset `s ⊆ X`, not at every point of `X`.
- `OpenPartialHomeomorph X Y`: the data of a single homeomorphism between two specified open sets; `VTask.IsLocalHomeomorph` is a property of a global function asserting that such partial homeomorphisms exist locally at every point.
- `Homeomorph` (`X ≃ₜ Y`): a global homeomorphism, which implies `VTask.IsLocalHomeomorph` but is strictly stronger (it also requires global bijectivity).