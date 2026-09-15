## Object

`VTask.prod f₁ f₂` is the simultaneous application of two continuous `R`-algebra homomorphisms sharing the same domain: given continuous `R`-algebra maps `f₁ : A →A[R] B` and `f₂ : A →A[R] C`, it produces the continuous `R`-algebra homomorphism `A →A[R] B × C` that sends each element `a : A` to the pair `(f₁ a, f₂ a)` in the Cartesian product `B × C`, equipped with the product topology and product algebra structure.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {R : Type u_1} -> [CommSemiring R] -> {A : Type u_2} -> [Semiring A] -> [TopologicalSpace A] -> {B : Type u_3} -> [Semiring B] -> [TopologicalSpace B] -> [Algebra R A] -> [Algebra R B] -> {C : Type u_4} -> [Semiring C] -> [Algebra R C] -> [TopologicalSpace C] -> (f₁ : A →A[R] B) -> (f₂ : A →A[R] C) -> A →A[R] B × C
<!-- PINNED-SIGNATURE:END -->


VTask.prod : {R : Type u_1} -> [CommSemiring R] -> {A : Type u_2} -> [Semiring A] -> [TopologicalSpace A] -> {B : Type u_3} -> [Semiring B] -> [TopologicalSpace B] -> [Algebra R A] -> [Algebra R B] -> {C : Type u_4} -> [Semiring C] -> [Algebra R C] -> [TopologicalSpace C] -> (f₁ : A →A[R] B) -> (f₂ : A →A[R] C) -> A →A[R] B × C

`R` is the commutative semiring of scalars shared by all algebras. `A` is the common source algebra. `B` and `C` are the two target algebras. The typeclass arguments provide the semiring, topological, and algebra-over-`R` structure for each type. `f₁` is the first continuous `R`-algebra homomorphism, mapping `A` into `B`. `f₂` is the second continuous `R`-algebra homomorphism, mapping `A` into `C`. The result is a single continuous `R`-algebra homomorphism from `A` into the product `B × C`.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: the construction is total and well-defined whenever both inputs are valid continuous algebra morphisms, and the product topology and algebra structure on `B × C` are determined entirely by the typeclass instances.

## Worked examples

- Claim: For any continuous `R`-algebra morphism `f₁ : A →A[R] B` and `f₂ : A →A[R] C`, composing `VTask.prod f₁ f₂` with the first projection `B × C → B` recovers `f₁` pointwise, i.e., `∀ a, (VTask.prod f₁ f₂) a = (f₁ a, f₂ a)`.

- Claim: When both `f₁` and `f₂` are the identity on a single algebra `A` (with `B = C = A`), `VTask.prod id id` sends each element `a : A` to the diagonal pair `(a, a)` in `A × A`.

- Claim: The underlying algebra homomorphism of `VTask.prod f₁ f₂` agrees with the algebraic product of `f₁` and `f₂` as `R`-algebra maps, so it preserves addition, multiplication, scalar multiplication, and the unit.

- Claim: The underlying continuous map of `VTask.prod f₁ f₂` is continuous with respect to the topology on `A` and the product topology on `B × C`.

## Boundaries

- The definition is total: it requires no conditions beyond the typeclass structure already present.
- When `B` or `C` is a trivial algebra (e.g., the zero ring), the corresponding component of the output is fixed, but the construction still produces a valid morphism.
- The product topology on `B × C` is the standard one; no separate hypothesis about the topology is needed since it is inferred from the `TopologicalSpace` instances on `B` and `C`.
- If `f₁` and `f₂` happen to be equal (and `B = C`), the result is the diagonal morphism into `B × B`, not a morphism into `B`.

## Not to be confused with

- `AlgHom.prod`: The purely algebraic (not continuous) Cartesian product of two `R`-algebra homomorphisms; `VTask.prod` adds and enforces continuity.
- `ContinuousLinearMap.prod`: The analogous construction for continuous linear maps between modules, which does not require multiplicativity or an algebra structure.
- `VTask.prodMap`: A related but different construction that maps a product `A × B` into a product `C × D` by applying two separate morphisms to each component, rather than fanning out from a single source.