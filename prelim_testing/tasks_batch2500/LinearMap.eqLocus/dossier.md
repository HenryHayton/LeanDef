## Object

`VTask.eqLocus f g` is the **equalizer submodule** of two semilinear maps `f` and `g`. Concretely, it is the set of all elements `x` of the domain module `M` on which `f` and `g` agree — i.e., `{x : M | f x = g x}` — equipped with the natural structure making it a submodule of `M` over the ring `R`. It is the module-theoretic analogue of the equalizer of two group homomorphisms.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.eqLocus : {R : Type u_1} -> {R₂ : Type u_2} -> {M : Type u_3} -> {M₂ : Type u_4} -> [Semiring R] -> [Semiring R₂] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> [Module R M] -> [Module R₂ M₂] -> {τ₁₂ : R →+* R₂} -> (f g : M →ₛₗ[τ₁₂] M₂) -> Submodule R M
<!-- PINNED-SIGNATURE:END -->


VTask.eqLocus : {R : Type u_1} -> {R₂ : Type u_2} -> {M : Type u_3} -> {M₂ : Type u_4} -> [Semiring R] -> [Semiring R₂] -> [AddCommMonoid M] -> [AddCommMonoid M₂] -> [Module R M] -> [Module R₂ M₂] -> {τ₁₂ : R →+* R₂} -> (f g : M →ₛₗ[τ₁₂] M₂) -> Submodule R M

The implicit type arguments `R`, `R₂`, `M`, `M₂` are the scalar rings and the domain and codomain modules. The instance arguments supply semiring and module structures. The implicit argument `τ₁₂` is the ring homomorphism that mediates the semilinearity (scalar twisting) between `R` and `R₂`. The two explicit arguments `f` and `g` are the semilinear maps being compared; they share the same domain `M`, codomain `M₂`, and semilinearity parameter `τ₁₂`.

## Conventions

There are no declared junk-value or edge-case conventions for this definition: the construction is total and well-defined for any pair of semilinear maps, including the case `f = g`.

## Worked examples

- Claim: For any semilinear map `f`, the equalizer `VTask.eqLocus f f` equals the entire module (i.e., is `⊤` as a submodule).

- Claim: An element `x` belongs to `VTask.eqLocus f g` if and only if `f x = g x`.

- Claim: `VTask.eqLocus f g = ⊤` if and only if `f = g` as semilinear maps.

- Claim: The equalizer `VTask.eqLocus f g` coincides with the kernel of the difference `f - g` (when subtraction is available, i.e., for linear maps to a module over a ring with subtraction).

## Boundaries

- When `f = g`, the equalizer is the whole module: `VTask.eqLocus f f = ⊤`.
- When `f` and `g` agree nowhere except at zero (e.g., `f = 0`, `g` injective and nonzero), the equalizer equals the zero submodule.
- The equalizer is always a submodule (not merely a subset or subgroup): it is closed under the `R`-scalar action because `τ₁₂` is a ring homomorphism and both `f` and `g` are semilinear.
- The underlying `AddSubmonoid` of `VTask.eqLocus f g` equals the `eqLocusM` of the underlying additive monoid homomorphisms of `f` and `g`.
- A submodule `S` is contained in `VTask.eqLocus f g` if and only if `f` and `g` agree on all elements of `S` (i.e., `f` and `g` are equal as functions on `S`).

## Not to be confused with

- `LinearMap.ker (f - g)`: the kernel of the difference map; this equals `VTask.eqLocus f g` when subtraction is defined, but `ker` requires more structure (a module over a ring, not just a semiring).
- `AddMonoidHom.eqLocusM f g`: the equalizer at the level of additive monoid homomorphisms; `VTask.eqLocus` extends this with the full `R`-submodule structure.
- `Subalgebra.equalizer φ ψ` (for algebra homomorphisms): a subalgebra-level equalizer whose underlying submodule coincides with `VTask.eqLocus` when the maps are algebra homomorphisms, but which carries additional ring/algebra structure.