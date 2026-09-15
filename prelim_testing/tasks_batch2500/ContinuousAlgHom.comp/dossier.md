## Object

`VTask.comp` is the composition of two continuous algebra homomorphisms over a commutative semiring `R`. Given a continuous `R`-algebra homomorphism `f : A →A[R] B` and another `g : B →A[R] C`, it produces the composite continuous `R`-algebra homomorphism `g ∘ f : A →A[R] C`. The resulting map is simultaneously an `R`-algebra homomorphism (preserving the ring structure and the `R`-scalar action) and a continuous map between the topological spaces underlying `A` and `C`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {R : Type u_1} -> [CommSemiring R] -> {A : Type u_2} -> [Semiring A] -> [TopologicalSpace A] -> {B : Type u_3} -> [Semiring B] -> [TopologicalSpace B] -> [Algebra R A] -> [Algebra R B] -> {C : Type u_4} -> [Semiring C] -> [Algebra R C] -> [TopologicalSpace C] -> (g : B →A[R] C) -> (f : A →A[R] B) -> A →A[R] C
<!-- PINNED-SIGNATURE:END -->


VTask.comp : {R : Type u_1} -> [CommSemiring R] -> {A : Type u_2} -> [Semiring A] -> [TopologicalSpace A] -> {B : Type u_3} -> [Semiring B] -> [TopologicalSpace B] -> [Algebra R A] -> [Algebra R B] -> {C : Type u_4} -> [Semiring C] -> [Algebra R C] -> [TopologicalSpace C] -> (g : B →A[R] C) -> (f : A →A[R] B) -> A →A[R] C

`R` is the commutative semiring of scalars shared by all three algebras. `A`, `B`, and `C` are the source, intermediate, and target algebras, each carrying a semiring structure, a topological space structure, and an `R`-algebra structure. `g` is the outer continuous `R`-algebra homomorphism from `B` to `C`; `f` is the inner continuous `R`-algebra homomorphism from `A` to `B`. Note the order: `g` comes before `f` in the argument list, mirroring mathematical notation for composition (the outer map first).

## Conventions

No special junk-value or edge conventions are declared: the definition is total on all valid inputs and produces a well-defined composite morphism whenever the types and instances match.

## Worked examples

- Claim: For the identity continuous algebra homomorphism `id : A →A[R] A` and any continuous algebra homomorphism `f : A →A[R] B`, `VTask.comp f id` agrees pointwise with `f`.

- Claim: For continuous algebra homomorphisms `f : A →A[R] B`, `g : B →A[R] C`, and `h : C →A[R] D`, composing in either order of association yields the same morphism: `VTask.comp (VTask.comp h g) f` and `VTask.comp h (VTask.comp g f)` agree pointwise.

- Claim: If `f : A →A[R] B` and `g : B →A[R] C`, then for any `a : A`, applying `VTask.comp g f` to `a` gives the same result as first applying `f` to `a` and then applying `g`.

## Boundaries

- When `A = B = C` and both `f` and `g` are identity maps, the composition is again the identity map.
- The definition is entirely structural and total: it places no restrictions on the specific algebras or topologies involved beyond what is required by the type class assumptions.
- The order of arguments (`g` before `f`) means that `VTask.comp g f` denotes `g` after `f`, consistent with standard mathematical composition notation but potentially surprising to those expecting left-to-right pipeline order.
- The composite inherits continuity from the continuity of both `f` and `g` (continuity of compositions of continuous maps).

## Not to be confused with

- The underlying plain algebra homomorphism composition `AlgHom.comp`: that forgets the topological/continuity data and works purely algebraically.
- `ContinuousMap.comp`: composition of bare continuous maps, which forgets the `R`-algebra structure entirely.
- `ContinuousLinearMap.comp`: composition for continuous `R`-linear maps between modules, which does not require a multiplicative (ring) structure on the domain and codomain.