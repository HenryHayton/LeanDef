## VTask.compLinearMap

### Object

Given an alternating multilinear map `f` from `ι`-tuples of elements of `M` to `N`, and a linear map `g` from `M₂` to `M`, this construction produces a new alternating multilinear map from `ι`-tuples of elements of `M₂` to `N`. Concretely, the resulting map applies `g` to each of the `ι` input arguments (independently and with the same linear map) before feeding them into `f`. The result is again alternating: if any two input arguments are equal, the output is zero.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.compLinearMap : {R : Type u_1} -> [Semiring R] -> {M : Type u_2} -> [AddCommMonoid M] -> [Module R M] -> {N : Type u_3} -> [AddCommMonoid N] -> [Module R N] -> {ι : Type u_7} -> {M₂ : Type u_10} -> [AddCommMonoid M₂] -> [Module R M₂] -> (f : M [⋀^ι]→ₗ[R] N) -> (g : M₂ →ₗ[R] M) -> M₂ [⋀^ι]→ₗ[R] N
<!-- PINNED-SIGNATURE:END -->


The type parameters `R`, `M`, `N`, `M₂`, and `ι` are, respectively: the commutative semiring of scalars; the domain module of `f`; the codomain module; the new domain module (whose elements are mapped into `M` by `g`); and the index type parameterising the number and labelling of arguments. The instance arguments supply the required algebraic structure. The argument `f` is the alternating multilinear map being pre-composed; `g` is the linear map applied uniformly to every input argument before passing them to `f`.

### Conventions

No junk-value or edge conventions are declared for this definition: it is a total, algebraically well-typed construction with no inputs that could be considered degenerate or out-of-domain.

### Worked examples

- Claim: For the zero alternating map `f = 0 : M [⋀^ι]→ₗ[R] N` and any linear map `g : M₂ →ₗ[R] M`, `VTask.compLinearMap 0 g = 0`.

- Claim: If `ι` is empty (`ι = Fin 0`), then `VTask.compLinearMap f g` applied to the empty tuple equals `f` applied to the empty tuple, since `g` is never actually called.

- Claim: For a scalar semiring `R = ℤ`, modules `M = M₂ = N = ℤ`, index type `ι = Fin 2`, alternating map `f` sending `(a, b)` to `a * b - b * a = 0`, and any linear map `g`, `VTask.compLinearMap f g` is also the zero alternating map on pairs.

- Claim: Applying `VTask.compLinearMap f g` to a tuple `v : ι → M₂` yields the same result as applying `f` to the tuple `g ∘ v : ι → M`.

### Boundaries

- When `ι` is an empty type, `VTask.compLinearMap f g` is a well-defined alternating map with no inputs (a "constant" in `N`), and `g` plays no role in the output.
- When `g` is the zero linear map, `VTask.compLinearMap f g` maps every input to `f(0, 0, …, 0)`; since `f` is alternating, if `ι` has at least two elements the result is identically zero.
- When `g` is the identity on `M = M₂`, `VTask.compLinearMap f id` recovers `f`.
- The construction is defined for any `R`-semiring, not merely fields or rings, so no invertibility of scalars is assumed.

### Not to be confused with

- `AlternatingMap.compMultilinearMap`: composition of an alternating map with a *multilinear* (not necessarily linear) map, rather than a single linear map applied uniformly to each argument.
- `MultilinearMap.compLinearMap`: the analogous construction for multilinear maps that are not required to be alternating; `VTask.compLinearMap` is the specialisation that preserves the alternating property.
- `LinearMap.comp`: ordinary composition of two linear maps (single-argument), which does not involve multilinear or alternating structure.