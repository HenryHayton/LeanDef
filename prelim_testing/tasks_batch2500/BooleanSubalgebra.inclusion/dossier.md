## VTask.inclusion

### Object

Given a Boolean algebra `α` and two Boolean subalgebras `L ≤ M` of `α`, `VTask.inclusion h` is the canonical inclusion homomorphism that sends each element of `L` to the same element viewed as a member of `M`. It is a morphism in the category of bounded lattices, meaning it preserves the bottom element ⊥, the top element ⊤, binary meets (∧), and binary joins (∨).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inclusion : {α : Type u_2} -> [BooleanAlgebra α] -> {L M : BooleanSubalgebra α} -> (h : L ≤ M) -> BoundedLatticeHom ↥L ↥M
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_2} -> [BooleanAlgebra α] -> {L M : BooleanSubalgebra α} -> (h : L ≤ M) -> BoundedLatticeHom ↥L ↥M`

The ambient type `α` is the Boolean algebra in which both subalgebras live. The instance `[BooleanAlgebra α]` supplies the Boolean algebra structure on `α`. The implicit arguments `L` and `M` are two Boolean subalgebras of `α`. The explicit argument `h` is the proof that `L` is contained in `M` (i.e., every element of `L` is also an element of `M`). The result is a bounded lattice homomorphism from the subtype `↥L` to the subtype `↥M`.

### Conventions

No junk-value or edge conventions are declared for this definition: it is a total construction—whenever `h : L ≤ M` is provided, the homomorphism is well-defined with no special-casing required at any boundary.

### Worked examples

- Claim: For any Boolean subalgebra `L` with `h : L ≤ L` (reflexivity), applying `VTask.inclusion h` to an element `a : ↥L` returns an element of `↥L` with the same underlying value.

- Claim: The homomorphism `VTask.inclusion h` is injective for any `h : L ≤ M`: distinct elements of `L` map to distinct elements of `M`.

- Claim: `VTask.inclusion h` preserves ⊥ — the image of the bottom element of `↥L` is the bottom element of `↥M`.

- Claim: `VTask.inclusion h` preserves ⊤ — the image of the top element of `↥L` is the top element of `↥M`.

### Boundaries

- When `L = M` and `h` is the reflexivity proof `le_refl L`, the resulting homomorphism acts as the identity on elements of `↥L` (up to the subtype coercion).
- When `L` is the smallest Boolean subalgebra (containing only ⊥ and ⊤), the map sends the two-element subalgebra into any larger subalgebra `M` that contains it.
- The homomorphism is always injective (since it merely re-tags the same underlying element as belonging to the larger subalgebra), so it never collapses distinct elements.

### Not to be confused with

- `BooleanSubalgebra.subtype`: the coercion from `↥L` into the ambient algebra `α` itself, rather than into a larger subalgebra `↥M`.
- `BoundedLatticeHom.id`: the identity homomorphism on a single bounded lattice, which does not involve two distinct subalgebras or a containment proof.
- `Set.inclusion`: the underlying set-theoretic function between subtypes induced by `L ≤ M`; `VTask.inclusion` wraps this with the full bounded lattice homomorphism structure.