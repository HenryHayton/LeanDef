## VTask.comp

### Object

Given three Lie algebras $L_1$, $L_2$, $L_3$ over a commutative ring $R$, and Lie algebra homomorphisms $f : L_2 \to L_3$ and $g : L_1 \to L_2$, `VTask.comp f g` is the composite map $f \circ g : L_1 \to L_3$, viewed as a Lie algebra homomorphism. That is, it is the unique map sending each $x \in L_1$ to $f(g(x)) \in L_3$, and this composite preserves the $R$-linear structure as well as the Lie bracket: $(f \circ g)([x, y]) = [f(g(x)), f(g(y))]$.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {R : Type u} -> {L₁ : Type v} -> {L₂ : Type w} -> {L₃ : Type w₁} -> [CommRing R] -> [LieRing L₁] -> [LieAlgebra R L₁] -> [LieRing L₂] -> [LieAlgebra R L₂] -> [LieRing L₃] -> [LieAlgebra R L₃] -> (f : L₂ →ₗ⁅R⁆ L₃) -> (g : L₁ →ₗ⁅R⁆ L₂) -> L₁ →ₗ⁅R⁆ L₃
<!-- PINNED-SIGNATURE:END -->


The implicit arguments `R`, `L₁`, `L₂`, `L₃` are, respectively, the commutative ring of scalars and the three Lie algebras involved in the composition, each equipped with appropriate `LieRing` and `LieAlgebra` instances. The argument `f` is the *outer* (second-applied) Lie algebra morphism, going from $L_2$ to $L_3$. The argument `g` is the *inner* (first-applied) Lie algebra morphism, going from $L_1$ to $L_2$. The result is a Lie algebra morphism from $L_1$ to $L_3$.

### Conventions

Argument order follows the usual mathematical convention for composition of functions: `f` is written to the left of `g`, meaning $f$ is applied *after* $g$, so `(VTask.comp f g) x = f (g x)`. There are no junk-value conventions since the definition is total and well-typed by construction.

### Worked examples

- Claim: For any Lie algebra $L$ over $R$ and the identity homomorphism `id : L →ₗ⁅R⁆ L`, composing `f` with `id` on the right yields a morphism that acts the same as `f` on every element: `VTask.comp f LieHom.id` evaluated at `x` equals `f x`.

- Claim: For any Lie algebra homomorphisms `f : L₂ →ₗ⁅R⁆ L₃`, `g : L₁ →ₗ⁅R⁆ L₂`, and any `x : L₁`, the element `VTask.comp f g x` equals `f (g x)`.

- Claim: The composite of two Lie algebra homomorphisms preserves the Lie bracket: for all `x y : L₁`, `VTask.comp f g ⁅x, y⁆ = ⁅VTask.comp f g x, VTask.comp f g y⁆`.

- Claim: Composition is associative: for homomorphisms `h : L₃ →ₗ⁅R⁆ L₄`, `f : L₂ →ₗ⁅R⁆ L₃`, `g : L₁ →ₗ⁅R⁆ L₂`, `VTask.comp (VTask.comp h f) g` and `VTask.comp h (VTask.comp f g)` agree on every element of `L₁`.

### Boundaries

- When $L_1 = L_2 = L_3$ and both `f` and `g` are the identity morphism, `VTask.comp f g` is again the identity morphism.
- When either `f` or `g` is the zero map (i.e., maps everything to $0$), the composite is also the zero map.
- There is no restriction on the Lie algebras: they may be abelian, finite-dimensional, infinite-dimensional, or over any commutative ring. The definition is total.
- The underlying linear map of `VTask.comp f g` is exactly the composition of the underlying linear maps of `f` and `g`.

### Not to be confused with

- `LieHom.id`: the identity morphism on a single Lie algebra, not a composition of two morphisms.
- `LinearMap.comp`: composition of plain $R$-linear maps, which does not track or guarantee preservation of the Lie bracket.
- Function composition (`Function.comp`): operates on bare functions with no algebraic structure, and does not produce a bundled Lie algebra morphism.