## VTask.prod

### Object

Given two Lie algebra homomorphisms `f : L → L₁` and `g : L → L₂` (both over the same commutative ring `R` and with the same domain `L`), `VTask.prod f g` is the unique Lie algebra homomorphism `L → L₁ × L₂` that simultaneously extends both: it sends each element `x ∈ L` to the pair `(f x, g x)` in the direct product Lie algebra `L₁ × L₂`. The direct product here carries the component-wise Lie bracket, addition, and scalar multiplication.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {R : Type u_1} -> {L₁ : Type u_2} -> {L₂ : Type u_3} -> {L : Type u_4} -> [CommRing R] -> [LieRing L₁] -> [LieAlgebra R L₁] -> [LieRing L₂] -> [LieAlgebra R L₂] -> [LieRing L] -> [LieAlgebra R L] -> (f : L →ₗ⁅R⁆ L₁) -> (g : L →ₗ⁅R⁆ L₂) -> L →ₗ⁅R⁆ L₁ × L₂
<!-- PINNED-SIGNATURE:END -->


`VTask.prod : {R : Type u_1} -> {L₁ : Type u_2} -> {L₂ : Type u_3} -> {L : Type u_4} -> [CommRing R] -> [LieRing L₁] -> [LieAlgebra R L₁] -> [LieRing L₂] -> [LieAlgebra R L₂] -> [LieRing L] -> [LieAlgebra R L] -> (f : L →ₗ⁅R⁆ L₁) -> (g : L →ₗ⁅R⁆ L₂) -> L →ₗ⁅R⁆ L₁ × L₂`

- `R` is the commutative ring of scalars over which all three Lie algebras are defined.
- `L₁` and `L₂` are the two target Lie algebras, forming the components of the codomain product.
- `L` is the common source Lie algebra.
- The typeclass arguments supply the ring, Lie ring, and Lie algebra structures on each of `L`, `L₁`, `L₂`.
- `f` is the first component homomorphism, mapping `L` into `L₁`.
- `g` is the second component homomorphism, mapping `L` into `L₂`.

### Conventions

No junk-value or edge conventions are declared for this definition: it is a total, well-defined construction whenever the typeclass hypotheses are satisfied, and all arguments are meaningful Lie algebra homomorphisms with no degenerate boundary cases requiring special treatment.

### Worked examples

- Claim: For any `x : L`, applying `VTask.prod f g` to `x` yields `(f x, g x)` in `L₁ × L₂`.

- Claim: `VTask.prod f g` respects the Lie bracket: `VTask.prod f g ⁅x, y⁆ = ⁅VTask.prod f g x, VTask.prod f g y⁆` in `L₁ × L₂`.

- Claim: When `g` is the zero homomorphism, `VTask.prod f 0` maps `x` to `(f x, 0)` in `L₁ × L₂`.

- Claim: When both `f` and `g` are identity homomorphisms on `L`, `VTask.prod (LieHom.id R L) (LieHom.id R L)` is the diagonal embedding `L → L × L` sending `x` to `(x, x)`.

### Boundaries

- The definition is valid for any commutative ring `R`, including fields, integers, and trivial rings.
- If `L` is the trivial (zero) Lie algebra, the result is the zero homomorphism into `L₁ × L₂`.
- If `L₁` or `L₂` is trivial, the product homomorphism collapses one component to zero and the result essentially factors through the non-trivial component.
- The construction is symmetric in spirit but not literally: swapping `f` and `g` gives a homomorphism into `L₂ × L₁`, which is isomorphic but not equal to the product into `L₁ × L₂`.

### Not to be confused with

- `LieHom.fst` / `LieHom.snd`: these are the *projection* homomorphisms from `L₁ × L₂` onto each factor, going in the opposite direction to `VTask.prod`.
- `LinearMap.prod`: the analogous construction for linear maps; `VTask.prod` lifts this to Lie algebra homomorphisms, additionally verifying compatibility with the Lie bracket.
- `LieHom.coprod` (if it exists): a dual construction combining two homomorphisms out of two *different* domains into a single codomain, rather than out of a single domain into a product.