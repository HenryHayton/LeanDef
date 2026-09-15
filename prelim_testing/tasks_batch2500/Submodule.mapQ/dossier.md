## VTask.mapQ

### Object

Given modules `M` and `M₂` over rings `R` and `R₂` (connected by a ring homomorphism `τ₁₂ : R →+* R₂`), submodules `p ⊆ M` and `q ⊆ M₂`, a semilinear map `f : M →ₛₗ[τ₁₂] M₂`, and the condition that `p` is carried into `q` by `f` (i.e., `f(p) ⊆ q`, expressed as `p ≤ comap f q`), `VTask.mapQ` produces the canonical induced semilinear map between quotient modules `M ⧸ p →ₛₗ[τ₁₂] M₂ ⧸ q`. It sends the coset `x + p` to the coset `f(x) + q`, and is the unique semilinear map making the obvious square commute: the composite (quotient map of `M`) then (induced map) equals (apply `f`) then (quotient map of `M₂`).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mapQ : {R : Type u_1} -> {M : Type u_2} -> [Ring R] -> [AddCommGroup M] -> [Module R M] -> (p : Submodule R M) -> {R₂ : Type u_3} -> {M₂ : Type u_4} -> [Ring R₂] -> [AddCommGroup M₂] -> [Module R₂ M₂] -> {τ₁₂ : R →+* R₂} -> (q : Submodule R₂ M₂) -> (f : M →ₛₗ[τ₁₂] M₂) -> (h : p ≤ Submodule.comap f q) -> M ⧸ p →ₛₗ[τ₁₂] M₂ ⧸ q
<!-- PINNED-SIGNATURE:END -->


`VTask.mapQ : {R : Type u_1} -> {M : Type u_2} -> [Ring R] -> [AddCommGroup M] -> [Module R M] -> (p : Submodule R M) -> {R₂ : Type u_3} -> {M₂ : Type u_4} -> [Ring R₂] -> [AddCommGroup M₂] -> [Module R₂ M₂] -> {τ₁₂ : R →+* R₂} -> (q : Submodule R₂ M₂) -> (f : M →ₛₗ[τ₁₂] M₂) -> (h : p ≤ Submodule.comap f q) -> M ⧸ p →ₛₗ[τ₁₂] M₂ ⧸ q`

The argument `p` is the submodule of `M` being quotiented out in the domain. The argument `q` is the submodule of `M₂` being quotiented out in the codomain. The argument `f` is the underlying semilinear map from `M` to `M₂` whose action descends to the quotients. The argument `h` is the compatibility condition asserting that `f` maps `p` into `q` (equivalently, `p` is contained in the preimage of `q` under `f`), which is exactly the condition needed for `f` to respect the equivalence relations defining the two quotients.

### Conventions

There are no junk-value or edge conventions to declare for this definition: it is a total function on well-typed inputs, and the compatibility hypothesis `h` is a genuine mathematical precondition rather than a convention about degenerate input.

### Worked examples

- Claim: For any `x : M`, the image of the coset `⟦x⟧` in `M ⧸ p` under `VTask.mapQ p q f h` is the coset `⟦f x⟧` in `M₂ ⧸ q`. This is `mapQ_apply`: `VTask.mapQ p q f h (Submodule.Quotient.mk x) = Submodule.Quotient.mk (f x)`.

- Claim: When `f = LinearMap.id` and `p = q` with `h : p ≤ comap LinearMap.id p` (trivially satisfied), `VTask.mapQ p p LinearMap.id h = LinearMap.id`. That is, the identity map on `M` induces the identity map on `M ⧸ p`.

- Claim: For composable semilinear maps `f : M →ₛₗ[τ₁₂] M₂` and `g : M₂ →ₛₗ[τ₂₃] M₃` with intermediate submodule `p₂` and compatibility hypotheses `hf : p ≤ p₂.comap f` and `hg : p₂ ≤ p₃.comap g`, we have `VTask.mapQ p p₃ (g.comp f) h = (VTask.mapQ p₂ p₃ g hg).comp (VTask.mapQ p p₂ f hf)`. That is, `mapQ` is functorial with respect to composition of semilinear maps.

- Claim: When `f = 0` (the zero semilinear map, which sends every element of `M` to `0 ∈ M₂`), `VTask.mapQ p q 0 h = 0`. That is, the zero map induces the zero map on quotients.

### Boundaries

- **Degenerate submodules**: When `p = ⊥` (the zero submodule), the domain `M ⧸ ⊥` is canonically isomorphic to `M` itself, and `VTask.mapQ ⊥ q f h` recovers (up to this isomorphism) the composition of `f` with the quotient map `M₂ → M₂ ⧸ q`.
- **Full submodules**: When `q = ⊤`, the codomain `M₂ ⧸ ⊤` is the trivial module `{0}`, and the induced map is necessarily zero regardless of `f`.
- **Equal submodules**: When `p = q` and `f = LinearMap.id`, the induced map is the identity on `M ⧸ p`.
- **Minimally satisfied hypothesis**: The condition `h : p ≤ comap f q` is the weakest possible: any `f` with `f(p) ⊈ q` cannot produce a well-defined map on quotients, so the boundary is sharp.

### Not to be confused with

- `Submodule.liftQ`: Lifts a map `M → N` to a map `M ⧸ p → N` (plain codomain, no quotient in the target), requiring only that the kernel contains `p`. `VTask.mapQ` additionally quotients the codomain.
- `Submodule.mkQ`: The canonical projection `M → M ⧸ p`; this is just the quotient map itself, not a map between two distinct quotients.
- `LinearMap.quotKerEquivRange`: An isomorphism `M ⧸ ker f ≅ range f`; this is a specific equivalence from the first isomorphism theorem, whereas `VTask.mapQ` works with arbitrary (not necessarily the kernel) submodules.
