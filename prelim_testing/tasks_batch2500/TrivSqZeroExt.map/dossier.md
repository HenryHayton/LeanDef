## Object

`VTask.map` lifts a linear map between modules to an algebra homomorphism between their trivial square-zero extensions. Concretely, if `R'` is a commutative semiring and `f : M →ₗ[R'] N` is an `R'`-linear map, then `VTask.map f` is the unique `R'`-algebra map `TrivSqZeroExt R' M →ₐ[R'] TrivSqZeroExt R' N` that acts as the identity on the `R'`-component and applies `f` to the `M`-component. In other words, on pairs it sends `(r, m)` to `(r, f m)`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.map : {R' : Type u} -> {M : Type v} -> [CommSemiring R'] -> [AddCommMonoid M] -> [Module R' M] -> [Module R'ᵐᵒᵖ M] -> [IsCentralScalar R' M] -> {N : Type u_3} -> [AddCommMonoid N] -> [Module R' N] -> [Module R'ᵐᵒᵖ N] -> [IsCentralScalar R' N] -> (f : M →ₗ[R'] N) -> TrivSqZeroExt R' M →ₐ[R'] TrivSqZeroExt R' N
<!-- PINNED-SIGNATURE:END -->


`VTask.map : {R' : Type u} -> {M : Type v} -> [CommSemiring R'] -> [AddCommMonoid M] -> [Module R' M] -> [Module R'ᵐᵒᵖ M] -> [IsCentralScalar R' M] -> {N : Type u_3} -> [AddCommMonoid N] -> [Module R' N] -> [Module R'ᵐᵒᵖ N] -> [IsCentralScalar R' N] -> (f : M →ₗ[R'] N) -> TrivSqZeroExt R' M →ₐ[R'] TrivSqZeroExt R' N`

The implicit type `R'` is the commutative semiring serving as the scalar ring. The implicit type `M` is the module whose trivial square-zero extension is the source algebra. The implicit type `N` is the module whose trivial square-zero extension is the target algebra. The six instance arguments supply the algebraic structure: `R'` must be a commutative semiring, both `M` and `N` must be abelian groups (`AddCommMonoid`) carrying left `R'`-module structures, right `R'`-module structures (via the opposite ring), and the centrality condition (`IsCentralScalar`) ensuring left and right scalar actions coincide. The explicit argument `f` is the `R'`-linear map from `M` to `N` being lifted.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total construction that is well-defined for every `R'`-linear map `f` satisfying the stated typeclass hypotheses, and there are no degenerate inputs that produce silently chosen fallback values.

## Worked examples

- Claim: For the zero linear map `0 : M →ₗ[R'] N`, `VTask.map 0` sends every pair `(r, m)` to `(r, 0)`, i.e., it acts as the identity on the `R'`-component and kills the `M`-component.

- Claim: For the identity linear map `LinearMap.id : M →ₗ[R'] M`, `VTask.map LinearMap.id` is the identity algebra homomorphism on `TrivSqZeroExt R' M`, so every element `(r, m)` maps to `(r, m)`.

- Claim: `VTask.map` is functorial: for linear maps `f : M →ₗ[R'] N` and `g : N →ₗ[R'] P`, the composite algebra map `(VTask.map g).comp (VTask.map f)` equals `VTask.map (g.comp f)`, reflecting that the construction respects composition.

- Claim: For any `r : R'` and `m : M`, the element `TrivSqZeroExt.inl r` (the pure scalar part) satisfies `VTask.map f (TrivSqZeroExt.inl r) = TrivSqZeroExt.inl r`, since `VTask.map f` is an `R'`-algebra map and therefore fixes scalar multiples of the unit.

## Boundaries

- When `f` is the zero linear map, `VTask.map f` still yields a valid algebra homomorphism; the `M`-coordinate of every output is `0`, but the `R'`-coordinate is untouched.
- When `M = N` and `f = LinearMap.id`, `VTask.map f` is the identity algebra automorphism.
- The construction requires `R'` to be commutative (`CommSemiring`). The non-commutative analogue is not available because there is no natural notion of bimodule morphism that fits into the same framework.
- Both source and target modules must satisfy `IsCentralScalar R' _`, ensuring left and right scalar multiplication coincide; without this, the trivial square-zero extension does not have a canonical commutative algebra structure compatible with lifting.

## Not to be confused with

- `TrivSqZeroExt.inrHom`: the algebra map that embeds `N` as the purely nilpotent ideal inside `TrivSqZeroExt R' N`, rather than lifting a map between two different extensions.
- `TrivSqZeroExt.liftEquivOfComm`: the general equivalence used to construct algebra maps out of `TrivSqZeroExt`; `VTask.map` is the specialised functorial version derived from it.
- `TrivSqZeroExt.fst`/`TrivSqZeroExt.snd`: the projection maps that split an element of a trivial square-zero extension into its two components, which go in the opposite direction to `VTask.map`.