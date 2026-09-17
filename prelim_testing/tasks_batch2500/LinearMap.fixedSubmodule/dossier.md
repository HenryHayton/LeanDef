## Object

`VTask.fixedSubmodule f` is the **fixed-point submodule** of a linear endomorphism `f : V →ₗ[R] V`. It is the set of all vectors `x ∈ V` satisfying `f x = x`, together with the inherited `R`-submodule structure. In other words, it is the largest subspace of `V` on which `f` acts as the identity.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.fixedSubmodule : {R : Type u_1} -> [Semiring R] -> {V : Type u_3} -> [AddCommMonoid V] -> [Module R V] -> (f : V →ₗ[R] V) -> Submodule R V
<!-- PINNED-SIGNATURE:END -->


`VTask.fixedSubmodule : {R : Type u_1} -> [Semiring R] -> {V : Type u_3} -> [AddCommMonoid V] -> [Module R V] -> (f : V →ₗ[R] V) -> Submodule R V`

The scalar type `R` is a semiring; `V` is an `R`-module (additive commutative monoid with a compatible scalar action). The single explicit argument `f` is the linear endomorphism whose fixed points we collect. Both `R` and `V` are inferred from `f`.

## Conventions

No special junk-value or out-of-domain conventions are declared: the definition is total and well-defined for every linear endomorphism over every semiring-module pair.

## Worked examples

- Claim: The zero vector belongs to `VTask.fixedSubmodule f` for every linear map `f`, since `f 0 = 0`.

- Claim: For the identity linear map `LinearMap.id` on any module `V`, every element of `V` belongs to `VTask.fixedSubmodule LinearMap.id`, i.e., `VTask.fixedSubmodule LinearMap.id = ⊤`.

- Claim: For the zero linear map `0 : V →ₗ[R] V`, `VTask.fixedSubmodule (0 : V →ₗ[R] V)` equals the trivial submodule `⊥` (containing only `0`), because `0 · x = 0 = x` forces `x = 0`.

- Claim: If `p : Submodule R V` is a submodule and `f` is the projection onto `p` (a linear map satisfying `f ∘ f = f`), then every element of `p` lies in `VTask.fixedSubmodule f`.

## Boundaries

- The zero vector `0` is always a member, since every linear map sends `0` to `0`.
- When `f = LinearMap.id`, the fixed submodule is the entire module `V`.
- When `f = 0` (the zero map), the fixed submodule contains only the zero vector (assuming `V` is nontrivial), because `0 = x` implies `x = 0`.
- The fixed submodule is closed under addition: if `f x = x` and `f y = y`, then `f (x + y) = f x + f y = x + y`.
- The fixed submodule is closed under scalar multiplication: if `f x = x`, then `f (r • x) = r • f x = r • x`.
- For a general semiring `R`, the result is a `Submodule R V`; no commutativity or field structure is required.

## Not to be confused with

- **`LinearMap.ker (f - LinearMap.id)`**: The kernel of `f - id` is the same set as the fixed submodule, but stated as a kernel; these coincide when subtraction is available (i.e., when `R` is a ring, not merely a semiring).
- **`Module.End.eigenspace f 1`**: The eigenspace for eigenvalue `1` coincides with the fixed submodule over a field, but eigenspaces require a field and the notion of eigenvalue, whereas `VTask.fixedSubmodule` works over any semiring-module.
- **`Submodule.map f p`** (image of a submodule under `f`): This computes the image of a given submodule, not the fixed-point locus of `f`.