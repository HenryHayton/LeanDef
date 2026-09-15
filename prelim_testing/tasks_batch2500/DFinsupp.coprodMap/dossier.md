## VTask.coprodMap

### Object

Given an index type `ι`, a commutative semiring `R`, a family of `R`-modules `M i` (one for each `i : ι`), a target `R`-module `N`, and a family of `R`-linear maps `f i : M i →ₗ[R] N`, `VTask.coprodMap f` is the unique `R`-linear map from the direct sum `Π₀ i, M i` to `N` that extends the family `f`. Concretely, it sends a finitely-supported family `x : Π₀ i, M i` to the finite sum `∑ i, f i (x i)` (where only finitely many terms are nonzero). This is precisely the map whose existence and uniqueness are guaranteed by the universal property of the coproduct (direct sum) in the category of `R`-modules.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.coprodMap : {ι : Type u_1} -> {R : Type u_3} -> {M : ι → Type u_5} -> {N : Type u_6} -> [Semiring R] -> [(i : ι) → AddCommMonoid (M i)] -> [(i : ι) → Module R (M i)] -> [AddCommMonoid N] -> [Module R N] -> [DecidableEq ι] -> (f : (i : ι) → M i →ₗ[R] N) -> (Π₀ (i : ι), M i) →ₗ[R] N
<!-- PINNED-SIGNATURE:END -->


The implicit arguments fix the universe levels, the index type `ι`, the base semiring `R`, the family of domain modules `M i`, and the codomain module `N`, together with all the required algebraic structure instances (semiring, module, additive commutative monoid) and a `DecidableEq` instance on `ι` needed to handle finite-support bookkeeping. The explicit argument `f` is the family of `R`-linear maps, one map `f i : M i →ₗ[R] N` for each index `i : ι`.

### Conventions

No special junk-value or edge conventions are declared for this definition: `VTask.coprodMap` is a genuinely total construction and its behaviour on every input (including the zero element and the empty index type) is determined naturally by the universal property and the module axioms with no special cases.

### Worked Examples

- Claim: When every `f i` is the zero map, `VTask.coprodMap f` is the zero linear map, since the sum of zeros is zero.

- Claim: For a singleton index type `ι = Unit`, `VTask.coprodMap f` applied to an element `x : Π₀ i : Unit, M i` returns `f () (x ())`, because the sum has exactly one nonzero term.

- Claim: For two indices `ι = Fin 2`, with `M i = R` for all `i` and `N = R`, and `f i = LinearMap.id`, `VTask.coprodMap f` applied to the element `x` with `x 0 = a` and `x 1 = b` returns `a + b`.

- Claim: `VTask.coprodMap f` is `R`-linear, meaning for any `r : R` and `x y : Π₀ i, M i`, it satisfies `VTask.coprodMap f (r • x + y) = r • VTask.coprodMap f x + VTask.coprodMap f y`.

### Boundaries

- **Empty index type**: If `ι` is empty (`IsEmpty ι`), the direct sum `Π₀ i, M i` is the trivial module containing only zero, and `VTask.coprodMap f` sends that unique element to `0 : N`. The family `f` is vacuously given and irrelevant.
- **Zero element**: `VTask.coprodMap f 0 = 0` by `R`-linearity (as for any linear map).
- **Single-support element**: On the element `DFinsupp.single i m` (supported only at `i` with value `m : M i`), `VTask.coprodMap f` returns `f i m`, since all other summands vanish.
- **Finite direct sums**: The map correctly handles arbitrary finitely-supported `x` by summing `f i (x i)` over the (finite) support of `x`.

### Not to be confused with

- `LinearMap.coprod` — the binary coproduct version for `M × N → P`, taking two maps rather than an indexed family.
- `DFinsupp.lsum` — a related but more general construction that assembles a linear map out of an indexed family; `VTask.coprodMap` is a specific, self-contained wrapper around the universal property.
- `Finsupp.linearCombination` (formerly `Finsupp.total`) — maps from a finitely-supported function on a type (with coefficients in `R`) to a module; it works with a single module `M` rather than a family `M i`.
