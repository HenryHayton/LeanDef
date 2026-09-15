## VTask.postcomp

### Object

Given a system of module relations `relations` over a ring `A`, a *solution* to those relations in an `A`-module `M` is an assignment of module elements to the generators that satisfies every relation. `VTask.postcomp` transports such a solution along an `A`-linear map `f : M →ₗ[A] N`, producing a new solution in the target module `N`: the generators are sent to the images under `f` of the original generator assignments, and every relation is automatically satisfied because `f` is linear.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.postcomp : {A : Type u} -> [Ring A] -> {relations : Module.Relations A} -> {M : Type v} -> [AddCommGroup M] -> [Module A M] -> (solution : relations.Solution M) -> {N : Type v'} -> [AddCommGroup N] -> [Module A N] -> (f : M →ₗ[A] N) -> relations.Solution N
<!-- PINNED-SIGNATURE:END -->


The implicit argument `A` is the coefficient ring. The instance `[Ring A]` equips `A` with ring structure. The implicit `relations : Module.Relations A` is the system of generators and relations being solved. The implicit `M` is the source module (with its `AddCommGroup` and `Module A` structure), and `solution : relations.Solution M` is the given assignment of generators to elements of `M` that satisfies all relations. The implicit `N` is the target module (with its `AddCommGroup` and `Module A` structure), and `f : M →ₗ[A] N` is the `A`-linear map along which the solution is transported.

### Conventions

No junk-value conventions are declared: the definition is a total construction — whenever valid inputs are provided, it returns a well-typed `relations.Solution N` with no degenerate cases.

### Worked examples

- Claim: For the trivial system of relations with no generators and no relations, postcomposing the (unique) solution in any module `M` with any linear map `f : M →ₗ[A] N` yields a solution in `N` whose generator-assignment function is the empty function.

- Claim: If `relations` has a single generator `g` with no relations, `solution.var g = m ∈ M`, and `f : M →ₗ[A] N` is a linear map, then `(VTask.postcomp solution f).var g = f m` in `N`.

- Claim: If `f` is the zero linear map `M →ₗ[A] N`, then `(VTask.postcomp solution f).var g = 0` for every generator `g`.

- Claim: Postcomposing a solution sequentially by `f : M →ₗ[A] N` and then `g : N →ₗ[A] P` produces the same solution as postcomposing once by the composition `g.comp f : M →ₗ[A] P`.

### Boundaries

- When the set of generators is empty, `postcomp` still produces a valid (vacuous) solution in `N`; there are simply no assignments to make.
- When the set of relations is empty, the satisfaction condition is vacuously true for the resulting solution regardless of `f`.
- When `f` is the identity linear map on `M`, `postcomp solution (LinearMap.id)` yields a solution definitionally equal to `solution` in all meaningful respects.
- When `f` is the zero map, every generator is assigned `0 ∈ N`; this is valid precisely because the zero element satisfies any homogeneous linear relation.

### Not to be confused with

- `Module.Relations.Solution.var`: the field accessor that retrieves the assignment of a single generator from a solution — not the operation of transporting a whole solution along a linear map.
- A *precomposition* operation (changing the relations or the indexing of generators) — `VTask.postcomp` acts on the *module side* by applying a linear map to the values, leaving the relations and generator indices unchanged.
- `LinearMap.comp`: the composition of two linear maps at the level of the maps themselves, without any reference to solutions to a system of relations.