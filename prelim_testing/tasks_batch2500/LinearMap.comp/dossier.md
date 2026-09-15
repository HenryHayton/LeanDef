## Object

Given two semilinear maps `g : M₁ →ₛₗ[σ₁₂] M₂` and `f : M₂ →ₛₗ[σ₂₃] M₃`, their composition `VTask.comp f g` is the semilinear map `M₁ →ₛₗ[σ₁₃] M₃` that sends each element `x` of `M₁` to `f(g(x))` in `M₃`. The ring homomorphism mediating the scalar action is the composite `σ₁₃ = σ₂₃ ∘ σ₁₂`, recorded via the `RingHomCompTriple` typeclass instance. In other words, this is ordinary function composition lifted to the category of semilinear maps, where the ring homomorphisms compose in the expected way.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {R₁ : Type u_2} -> {R₂ : Type u_3} -> {R₃ : Type u_4} -> {M₁ : Type u_9} -> {M₂ : Type u_10} -> {M₃ : Type u_11} -> [Semiring R₁] -> [Semiring R₂] -> [Semiring R₃] -> [AddCommMonoid M₁] -> [AddCommMonoid M₂] -> [AddCommMonoid M₃] -> {module_M₁ : Module R₁ M₁} -> {module_M₂ : Module R₂ M₂} -> {module_M₃ : Module R₃ M₃} -> {σ₁₂ : R₁ →+* R₂} -> {σ₂₃ : R₂ →+* R₃} -> {σ₁₃ : R₁ →+* R₃} -> [RingHomCompTriple σ₁₂ σ₂₃ σ₁₃] -> (f : M₂ →ₛₗ[σ₂₃] M₃) -> (g : M₁ →ₛₗ[σ₁₂] M₂) -> M₁ →ₛₗ[σ₁₃] M₃
<!-- PINNED-SIGNATURE:END -->


`{R₁ : Type u_2} -> {R₂ : Type u_3} -> {R₃ : Type u_4} -> {M₁ : Type u_9} -> {M₂ : Type u_10} -> {M₃ : Type u_11} -> [Semiring R₁] -> [Semiring R₂] -> [Semiring R₃] -> [AddCommMonoid M₁] -> [AddCommMonoid M₂] -> [AddCommMonoid M₃] -> {module_M₁ : Module R₁ M₁} -> {module_M₂ : Module R₂ M₂} -> {module_M₃ : Module R₃ M₃} -> {σ₁₂ : R₁ →+* R₂} -> {σ₂₃ : R₂ →+* R₃} -> {σ₁₃ : R₁ →+* R₃} -> [RingHomCompTriple σ₁₂ σ₂₃ σ₁₃] -> (f : M₂ →ₛₗ[σ₂₃] M₃) -> (g : M₁ →ₛₗ[σ₁₂] M₂) -> M₁ →ₛₗ[σ₁₃] M₃`

The three scalar rings `R₁`, `R₂`, `R₃` are equipped with semiring structures, and the three module carriers `M₁`, `M₂`, `M₃` are additive commutative monoids, each a module over its respective ring. The three ring homomorphisms `σ₁₂ : R₁ →+* R₂`, `σ₂₃ : R₂ →+* R₃`, and `σ₁₃ : R₁ →+* R₃` describe how scalars are transported; the `RingHomCompTriple` instance asserts that `σ₁₃` is (definitionally) the composite `σ₂₃ ∘ σ₁₂`. The first explicit argument `f` is the outer (second-applied) semilinear map, from `M₂` to `M₃` along `σ₂₃`. The second explicit argument `g` is the inner (first-applied) semilinear map, from `M₁` to `M₂` along `σ₁₂`. The result is their composite, a semilinear map from `M₁` to `M₃` along `σ₁₃`.

## Conventions

No junk-value or edge-case conventions are declared for this definition: it is a total construction on well-typed inputs and its behaviour is fully determined by the mathematical definition of semilinear map composition for all valid arguments.

## Worked examples

- Claim: Composing two ordinary (i.e., `ℤ`-linear) linear maps `f` and `g` gives the pointwise composite: for `g(x) = 2 * x` and `f(y) = y + 1` (as additive-group endomorphisms), `VTask.comp f g` applied to `3` yields `f(g(3)) = f(6) = 7`.

- Claim: For a semilinear map `g : M₁ →ₛₗ[σ₁₂] M₂` and the identity semilinear map `id` on `M₂`, `VTask.comp id g` agrees pointwise with `g` — it maps every `x` in `M₁` to the same element that `g` does.

- Claim: Composition of semilinear maps is associative: for compatible semilinear maps `f`, `g`, `h`, `VTask.comp (VTask.comp f g) h` and `VTask.comp f (VTask.comp g h)` give the same function.

- Claim: The composite `VTask.comp f g` preserves addition: for all `x y : M₁`, `(VTask.comp f g) (x + y) = (VTask.comp f g) x + (VTask.comp f g) y`, because both `f` and `g` individually preserve addition.

## Boundaries

- When `R₁ = R₂ = R₃` and all three ring homomorphisms are the identity, the construction reduces to ordinary composition of `R`-linear maps.
- The `RingHomCompTriple` typeclass constraint is essential: without evidence that `σ₁₃ = σ₂₃ ∘ σ₁₂`, the scalar-compatibility condition for the composite map would not hold, so there is no fallback behaviour — the definition simply cannot be applied.
- The construction is defined for all compatible inputs without any restriction on cardinality or characteristic; in particular, it is valid for the zero module, giving the zero map as the composite.
- If either `f` or `g` is the zero map, the composite is also the zero map.

## Not to be confused with

- `LinearMap.id`: the identity semilinear map on a single module, not a binary composition operation.
- `Function.comp`: plain function composition with no algebraic structure, carrying no linearity or semilinearity guarantees.
- `LinearMap.compRight` / scalar-right variants: operations that compose on the right with an algebra homomorphism rather than producing a semilinear map between modules.