## Object

Given two composable morphisms of Lie modules over a commutative ring `R` and a Lie ring `L` — a morphism `f : N → P` and a morphism `g : M → N`, both respecting the `R`-module structure and the Lie bracket action — `VTask.comp f g` is their composite morphism `M → P`, which again respects both the `R`-module structure and the Lie bracket action. In other words, it is the usual function composition `f ∘ g` equipped with a proof that the composite is itself a Lie module morphism.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {R : Type u} -> {L : Type v} -> {M : Type w} -> {N : Type w₁} -> {P : Type w₂} -> [CommRing R] -> [LieRing L] -> [AddCommGroup M] -> [AddCommGroup N] -> [AddCommGroup P] -> [Module R M] -> [Module R N] -> [Module R P] -> [LieRingModule L M] -> [LieRingModule L N] -> [LieRingModule L P] -> (f : N →ₗ⁅R,L⁆ P) -> (g : M →ₗ⁅R,L⁆ N) -> M →ₗ⁅R,L⁆ P
<!-- PINNED-SIGNATURE:END -->


`VTask.comp : {R : Type u} -> {L : Type v} -> {M : Type w} -> {N : Type w₁} -> {P : Type w₂} -> [CommRing R] -> [LieRing L] -> [AddCommGroup M] -> [AddCommGroup N] -> [AddCommGroup P] -> [Module R M] -> [Module R N] -> [Module R P] -> [LieRingModule L M] -> [LieRingModule L N] -> [LieRingModule L P] -> (f : N →ₗ⁅R,L⁆ P) -> (g : M →ₗ⁅R,L⁆ N) -> M →ₗ⁅R,L⁆ P`

The implicit type arguments `R`, `L`, `M`, `N`, `P` are, respectively: the commutative ring of scalars, the Lie ring acting on all modules, and the three module types forming the composable chain. The typeclass arguments supply the necessary ring, group, module, and Lie-module structures. The explicit argument `f` is the outer morphism (from `N` to `P`), and `g` is the inner morphism (from `M` to `N`); the result is the composite morphism from `M` to `P`.

## Conventions

No special junk-value or boundary conventions are declared: the operation is total and well-defined for any two composable Lie module morphisms; there are no degenerate inputs requiring special-cased output values.

## Worked examples

- Claim: For any Lie module morphism `f : N →ₗ⁅R,L⁆ P` and `g : M →ₗ⁅R,L⁆ N`, the underlying function of `VTask.comp f g` is the pointwise composite, i.e., `(VTask.comp f g) m = f (g m)` for all `m : M`.

- Claim: Composition is associative: for composable Lie module morphisms `f`, `g`, `h`, one has `VTask.comp f (VTask.comp g h) = VTask.comp (VTask.comp f g) h`.

- Claim: For a Lie module morphism `f : M →ₗ⁅R,L⁆ N` and the identity morphism `id : N →ₗ⁅R,L⁆ N`, composing `VTask.comp id f` yields a morphism that acts the same as `f` on all elements.

- Claim: The result `VTask.comp f g` satisfies the Lie module morphism compatibility condition: for all `x : L` and `m : M`, `⁅x, (VTask.comp f g) m⁆ = (VTask.comp f g) ⁅x, m⁆`.

## Boundaries

- The operation is total: it is defined for any two composable Lie module morphisms, with no restriction on whether they are injective, surjective, or zero.
- If either `f` or `g` is the zero morphism, the composite is again the zero morphism.
- If `M = N = P` and both `f` and `g` are the identity morphism, the composite is the identity morphism.
- There is no special behaviour for trivial modules or the zero ring; the definition applies uniformly.

## Not to be confused with

- `LinearMap.comp`: composition of plain `R`-linear maps, without the Lie bracket compatibility; `VTask.comp` is strictly richer, living in the Lie module morphism category.
- The function-level composition `Function.comp f g`: this is just set-theoretic function composition and carries none of the algebraic structure; `VTask.comp` packages the composite together with a proof that it is a Lie module morphism.
- Lie algebra morphism composition (for maps between Lie algebras themselves, not Lie modules): that concerns maps respecting the bracket on the algebra, whereas `VTask.comp` composes maps between modules on which a fixed Lie algebra acts.