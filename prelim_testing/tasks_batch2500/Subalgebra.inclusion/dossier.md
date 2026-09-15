## VTask.inclusion

### Object

`VTask.inclusion` is the canonical inclusion algebra homomorphism from a subalgebra `S` into a larger subalgebra `T`, valid whenever `S` is contained in `T`. It sends each element of `S` to the same element viewed as a member of `T`, respecting the full `R`-algebra structure (addition, multiplication, scalar action by `R`, and the unit).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inclusion : {R : Type u} -> {A : Type v} -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> {S T : Subalgebra R A} -> (h : S ≤ T) -> ↥S →ₐ[R] ↥T
<!-- PINNED-SIGNATURE:END -->


The implicit type arguments fix a commutative semiring of scalars `R`, an ambient `R`-algebra `A`, and the two subalgebras `S` and `T` of `A`. The explicit argument `h` is a proof that `S` is a subalgebra of `T` (i.e., `S ≤ T` in the lattice of subalgebras), which is the only condition required for the inclusion to be well-defined. The result is an `R`-algebra homomorphism from `S` (as a type) to `T` (as a type).

### Conventions

There are no junk-value or edge conventions: the map is completely determined by the containment proof `h`, and its value on every element of `S` is definitionally equal to the element's natural image in `T` — no special behaviour is assigned at degenerate inputs.

### Worked examples

- Claim: When `S = T` (i.e., `h` witnesses `S ≤ S`), `VTask.inclusion h` acts as the identity on every element of `S` viewed inside `T`.

- Claim: For subalgebras `S ≤ T ≤ U`, the composition of `VTask.inclusion (S ≤ T)` followed by `VTask.inclusion (T ≤ U)` equals `VTask.inclusion (S ≤ U)` as algebra homomorphisms.

- Claim: `VTask.inclusion h` is injective whenever `S ≤ T`, because it is a coercion of the underlying set inclusion, which is always injective.

### Boundaries

- When `S = T` exactly, the inclusion is the identity algebra homomorphism (up to the isomorphism `S ≅ T`).
- The definition is total: it is well-typed for any proof `h : S ≤ T`, including the case where `S` or `T` is the zero subalgebra or the entire ambient algebra `A`.
- The case `S ≤ ⊤` gives an algebra homomorphism from `S` into the top subalgebra, which can be identified with `A` itself.

### Not to be confused with

- `Submodule.inclusion`: the analogous construction for submodules, which is only a linear map, not an algebra homomorphism.
- `Subring.inclusion`: the analogous construction for subrings, which forgets the scalar algebra structure over `R`.
- The coercion `Subalgebra.val : S →ₐ[R] A`: this maps `S` into the full ambient algebra `A`, not into an intermediate subalgebra `T`.