## VTask.mapDomain

### Object

Given a function `f : M → N` between two types (typically monoids or magmas) and a formal `R`-linear combination of elements of `M` — i.e., an element of the monoid algebra `R[M]` — `VTask.mapDomain f x` produces the corresponding element of `R[N]` by pushing forward the support through `f` and summing up coefficients that land on the same element of `N`. Concretely, for each `n : N`, the coefficient of `n` in the result is the sum of all coefficients `x[m]` over those `m` in the support of `x` with `f m = n`. When `f` is injective, this is simply relabelling; when `f` is not injective, coefficients over the same fiber are added together.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mapDomain : {R : Type u_3} -> {M : Type u_6} -> {N : Type u_7} -> [Semiring R] -> (f : M → N) -> (x : MonoidAlgebra R M) -> MonoidAlgebra R N
<!-- PINNED-SIGNATURE:END -->


The implicit arguments fix the coefficient semiring `R`, the source monoid/type `M`, and the target type `N`, together with a `Semiring` instance on `R`. The argument `f` is the function from `M` to `N` along which the support is pushed forward. The argument `x` is the element of the monoid algebra `R[M]` whose domain is being mapped.

### Conventions

This definition is total: there are no restrictions on `f` or `x`. When `f` is not injective, the coefficients of distinct elements of `M` in the same fiber of `f` are added together in `R`; no coefficient is discarded.

### Worked examples

- Claim: Mapping the constant function (sending every element to a single point) on a monoid algebra collapses all coefficients into the coefficient of that point in `R[N]`.

- Claim: For a single-term element `single m r` in `R[M]`, applying `VTask.mapDomain f` produces `single (f m) r` in `R[N]`.

- Claim: If `x` has support `{m₁, m₂}` with `f m₁ = f m₂ = n₀`, then the coefficient of `n₀` in `VTask.mapDomain f x` equals `x.coeff m₁ + x.coeff m₂`.

- Claim: If `f` is injective, then for every `m` in the support of `x`, the coefficient of `f m` in `VTask.mapDomain f x` equals the coefficient of `m` in `x`.

### Boundaries

- If `x = 0` (the zero element of `R[M]`), then `VTask.mapDomain f x = 0` in `R[N]`, regardless of `f`.
- If `f` maps every element of the support of `x` to the same element `n₀ : N`, the result is `single n₀ (sum of all coefficients of x)`.
- If `f` is the identity, `VTask.mapDomain f x = x` (up to the canonical identification of `R[M]` with `R[M]`).
- The support of the result is contained in the image of the support of `x` under `f`; it may be strictly smaller when `f` is not injective.
- When `R` has characteristic zero and `f` identifies two elements with nonzero coefficients of opposite sign (if `R` is a ring), the corresponding coefficient in the result may be zero, so the support of the result can be strictly smaller than the image of the support.

### Not to be confused with

- `MonoidAlgebra.lift`: lifts a monoid homomorphism `M → A` to an `R`-algebra map `R[M] → A`, not merely a set function on the underlying type.
- `Finsupp.mapDomain`: the analogous operation on `Finsupp` functions (finitely supported functions), which `VTask.mapDomain` wraps; it works purely with the underlying coefficient function and does not carry the `MonoidAlgebra` structure.
- `MonoidAlgebra.mapDomainRingHom` (or similar): a version of domain mapping that additionally requires `f` to be a monoid homomorphism and produces a ring homomorphism, not merely an `R`-linear map on underlying modules.