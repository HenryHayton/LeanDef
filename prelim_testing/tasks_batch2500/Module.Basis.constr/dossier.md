## Object

`VTask.constr b S f` is the **linear equivalence** (as an `S`-linear map) between the type of functions `ι → M'` and the type of `R`-linear maps `M →ₗ[R] M'`, built from a fixed basis `b : Basis ι R M`. In one direction it sends a function `f : ι → M'` to the unique `R`-linear map `M →ₗ[R] M'` that extends `f` (i.e., sends each basis vector `b i` to `f i`). In the other direction it restricts any `R`-linear map to the basis elements. The two maps are mutual inverses and the whole package is an `S`-linear equivalence of the function/map spaces.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.constr : {M' : Type u_7} -> [AddCommMonoid M'] -> {ι : Type u_10} -> {R : Type u_11} -> {M : Type u_12} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> (b : Module.Basis ι R M) -> [Module R M'] -> (S : Type u_13) -> [Semiring S] -> [Module S M'] -> [SMulCommClass R S M'] -> (ι → M') ≃ₗ[S] M →ₗ[R] M'
<!-- PINNED-SIGNATURE:END -->


`VTask.constr : {M' : Type u_7} -> [AddCommMonoid M'] -> {ι : Type u_10} -> {R : Type u_11} -> {M : Type u_12} -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> (b : Module.Basis ι R M) -> [Module R M'] -> (S : Type u_13) -> [Semiring S] -> [Module S M'] -> [SMulCommClass R S M'] -> (ι → M') ≃ₗ[S] M →ₗ[R] M'`

- `b` is the `R`-basis of the source module `M`, indexed by `ι`. It determines which `R`-linear map extends a given function on the index set.
- `S` is an auxiliary semiring with respect to which the equivalence is linear. Typical choices are `S = R` (when `R` is commutative) or `S = ℕ` (to recover at least an additive equivalence when `R` is non-commutative).
- The implicit type arguments `M'`, `ι`, `R`, `M` are the codomain, index type, scalar ring, and source module, respectively.
- The instance `SMulCommClass R S M'` ensures that `R`-scaling and `S`-scaling on `M'` commute, which is the key compatibility needed for the equivalence to be `S`-linear.

## Conventions

There are no junk-value or edge conventions to declare for this definition: it is a total construction that is well-defined for every valid set of arguments satisfying the stated type-class assumptions.

## Worked examples

- Claim: Applying `VTask.constr b S` to the function `f : ι → M'` and then evaluating at a basis vector `b i` returns `f i`.

- Claim: For `b : Basis (Fin 2) ℝ (Fin 2 → ℝ)` (the standard basis) and `S = ℝ`, the linear map obtained from `VTask.constr b ℝ f` satisfies `(VTask.constr b ℝ f) (b 0) = f 0`.

- Claim: The inverse direction of `VTask.constr b S`, applied to an `R`-linear map `g : M →ₗ[R] M'`, yields the function `i ↦ g (b i)`. That is, `(VTask.constr b S).symm g = fun i => g (b i)`.

- Claim: `VTask.constr b S` is an `S`-linear equivalence, so for any two functions `f g : ι → M'` and scalar `c : S`, `VTask.constr b S (c • f + g) = c • VTask.constr b S f + VTask.constr b S g` as `R`-linear maps.

## Boundaries

- When `ι` is empty (no basis elements), both sides of the equivalence are essentially trivial: every function `ι → M'` is the empty function, and `M = 0`, so the unique linear map is the zero map. The construction handles this correctly as a degenerate case.
- When `M'` is the zero module, every function `ι → M'` and every linear map `M →ₗ[R] M'` is zero, and the equivalence collapses to a trivial bijection between one-element sets.
- The choice `S = ℕ` always works because `ℕ`-linearity coincides with additive-group homomorphism behaviour, providing the weakest useful structure. The choice `S = R` additionally requires `R` to be commutative (so that `SMulCommClass R R M'` holds).
- If `ι` is an infinite type, the basis `b` is still a valid Hamel basis and the construction still applies; the underlying `Finsupp`-based decomposition ensures only finitely many non-zero coefficients are used in any particular evaluation.

## Not to be confused with

- `Finsupp.linearCombination`: the map sending a formal linear combination (a `Finsupp`) to an element of a module; `VTask.constr` builds on this but packages it as a linear equivalence indexed by basis values, not by arbitrary finsupp data.
- `Module.Basis.repr`: the inverse direction of the basis isomorphism `M ≃ₗ[R] ι →₀ R`; `VTask.constr` uses `repr` internally but is about maps *out of* `M`, not coordinates.
- `LinearMap.funLeft` / `LinearMap.pi`: other ways to build linear maps from index-type data, but these do not use a basis and do not produce an equivalence with the module of linear maps out of `M`.