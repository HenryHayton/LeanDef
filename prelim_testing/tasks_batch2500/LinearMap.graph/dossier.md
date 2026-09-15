## VTask.graph

### Object

Given a linear map `f : M →ₗ[R] M₂` between modules over a commutative semiring `R`, `VTask.graph f` is the **graph of `f`**: the submodule of the product module `M × M₂` consisting of all pairs `(m, n)` such that `n = f m`. This is the module-theoretic analogue of the graph of a function, carrying the extra structure of a submodule because `f` is linear.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.graph : {R : Type u} -> {M : Type v} -> {M₂ : Type w} -> [Semiring R] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> [Module R M] -> [Module R M₂] -> (f : M →ₗ[R] M₂) -> Submodule R (M × M₂)
<!-- PINNED-SIGNATURE:END -->


`VTask.graph : {R : Type u} -> {M : Type v} -> {M₂ : Type w} -> [Semiring R] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> [Module R M] -> [Module R M₂] -> (f : M →ₗ[R] M₂) -> Submodule R (M × M₂)`

The implicit type arguments `R`, `M`, and `M₂` are, respectively, the scalar semiring and the two module types. The instance arguments supply the semiring and module structures on these types. The single explicit argument `f` is the linear map whose graph is being formed.

### Conventions

No junk-value or boundary conventions are declared for this definition: it is a total construction defined for every linear map between modules over any semiring, with no edge cases that produce a degenerate or conventionally chosen value.

### Worked examples

- Claim: For the zero linear map `0 : M →ₗ[R] M₂`, a pair `(m, n)` lies in `VTask.graph 0` if and only if `n = 0`.

- Claim: For the identity linear map `LinearMap.id : M →ₗ[R] M`, a pair `(m₁, m₂)` lies in `VTask.graph LinearMap.id` if and only if `m₂ = m₁`.

- Claim: The graph of `f` equals the range of the linear map `(LinearMap.id.prod f) : M →ₗ[R] M × M₂` that sends `m` to `(m, f m)`.

- Claim: A pair `x : M × M₂` belongs to `VTask.graph f` if and only if `x.2 = f x.1`.

### Boundaries

- The construction is valid over any semiring `R`; commutativity of `R` is not required.
- If `f` is the zero map, the graph is the submodule `{(m, 0) | m ∈ M}`, isomorphic to `M`.
- If `f` is the identity on `M`, the graph is the diagonal submodule `{(m, m) | m ∈ M}` inside `M × M`.
- The graph is never empty: it always contains the zero element `(0, 0)`, since `f 0 = 0`.
- Every submodule of `M × M₂` for which the projection onto the first factor is bijective arises as the graph of some linear map.

### Not to be confused with

- `LinearMap.range f`: the image submodule `{f m | m ∈ M}` inside `M₂` alone, not inside the product.
- `Submodule.prod P Q`: the direct-product submodule `P × Q ⊆ M × M₂`, which is not the graph of any map unless the submodules are specially related.
- The kernel `LinearMap.ker f`: the submodule `{m | f m = 0}` inside `M`, not inside the product.