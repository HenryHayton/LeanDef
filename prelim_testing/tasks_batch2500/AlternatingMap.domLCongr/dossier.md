## VTask.domLCongr

### Object

Given a linear equivalence `e : M ≃ₗ[R] M₂` between two `R`-modules, `VTask.domLCongr` produces a linear equivalence (over a second scalar ring `S`) between the space of alternating multilinear maps `M [⋀^ι]→ₗ[R] N` and the space of alternating multilinear maps `M₂ [⋀^ι]→ₗ[R] N`, by precomposing every alternating map with `e` or its inverse. In other words, it says that the space of alternating maps is independent of the choice of domain up to linear isomorphism, provided the domains are themselves linearly isomorphic.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.domLCongr : (R : Type u_1) -> [Semiring R] -> {M : Type u_2} -> [AddCommMonoid M] -> [Module R M] -> (N : Type u_3) -> [AddCommMonoid N] -> [Module R N] -> (ι : Type u_7) -> {M₂ : Type u_10} -> [AddCommMonoid M₂] -> [Module R M₂] -> (S : Type u_12) -> [Semiring S] -> [Module S N] -> [SMulCommClass R S N] -> (e : M ≃ₗ[R] M₂) -> M [⋀^ι]→ₗ[R] N ≃ₗ[S] M₂ [⋀^ι]→ₗ[R] N
<!-- PINNED-SIGNATURE:END -->


`VTask.domLCongr : (R : Type u_1) -> [Semiring R] -> {M : Type u_2} -> [AddCommMonoid M] -> [Module R M] -> (N : Type u_3) -> [AddCommMonoid N] -> [Module R N] -> (ι : Type u_7) -> {M₂ : Type u_10} -> [AddCommMonoid M₂] -> [Module R M₂] -> (S : Type u_12) -> [Semiring S] -> [Module S N] -> [SMulCommClass R S N] -> (e : M ≃ₗ[R] M₂) -> M [⋀^ι]→ₗ[R] N ≃ₗ[S] M₂ [⋀^ι]→ₗ[R] N`

`R` is the base (scalar) ring over which all modules and linear maps are defined. `M` is the source module of the input alternating maps; `N` is the common target module; `ι` is the index type that controls the arity of the alternating maps. `M₂` is the second domain module, linearly isomorphic to `M` via `e`. `S` is a second ring that acts on `N` compatibly with `R` (via `SMulCommClass`), and the resulting linear equivalence is `S`-linear. `e` is the linear equivalence between `M` and `M₂` that drives the construction.

### Conventions

The forward direction of the equivalence sends an alternating map `f : M [⋀^ι]→ₗ[R] N` to the alternating map obtained by precomposing with `e.symm`, i.e., to `fun x => f(e.symm ∘ x)`. The inverse direction sends an alternating map `g : M₂ [⋀^ι]→ₗ[R] N` to `fun x => g(e ∘ x)`.

### Worked examples

- Claim: When `e` is the identity equivalence on `M`, `VTask.domLCongr R N ι S (LinearEquiv.refl R M)` equals the identity `S`-linear equivalence on `M [⋀^ι]→ₗ[R] N`.

- Claim: The inverse of `VTask.domLCongr R N ι S e` equals `VTask.domLCongr R N ι S e.symm`, reflecting the fact that flipping the domain equivalence corresponds to taking the inverse linear equivalence on alternating maps.

- Claim: Composing `VTask.domLCongr R N ι S e` with `VTask.domLCongr R N ι S f` (where `f : M₂ ≃ₗ[R] M₃`) equals `VTask.domLCongr R N ι S (e.trans f)`, so the construction is compatible with composition of domain equivalences.

- Claim: For any `f : M [⋀^ι]→ₗ[R] N` and tuple `x : ι → M₂`, the value of the forward image at `x` equals `f` applied to `e.symm ∘ x` componentwise.

### Boundaries

- When `ι` is the empty type (arity 0), alternating maps are just elements of `N`, and the equivalence acts as the identity (since there are no domain inputs to precompose). The construction is still well-defined.
- When `e` is already the identity equivalence, the equivalence is the identity; the refl theorem confirms this.
- No finiteness condition on `ι` is required; the construction is valid for any type `ι`.
- The `S`-linearity of the output equivalence relies on `SMulCommClass R S N`; if `S = R` this is the canonical case and the commutation condition is automatic.

### Not to be confused with

- `AlternatingMap.compLinearMap`: this is the underlying map operation (not packaged as a linear equivalence) that precomposes a single alternating map with a linear map; `VTask.domLCongr` assembles this into a full `≃ₗ` isomorphism.
- `LinearEquiv.multilinearMapCongrLeft`: the analogous construction for *multilinear* maps (without the alternating condition); `VTask.domLCongr` imposes and preserves the alternating property.
- Codomain change constructions (sometimes called `codLCongr`): those replace `N` by an isomorphic module, whereas `VTask.domLCongr` changes the *domain* `M`.
