## VTask.inclusion

### Object

Given two sublattices `L` and `M` of a common lattice `α` with `L ≤ M` (meaning every element of `L` is also an element of `M`), `VTask.inclusion h` is the canonical inclusion map from `L` into `M`, regarded as a homomorphism of lattices. It sends each element of `L` to the same element viewed inside `M`, and it preserves both the meet (infimum) and join (supremum) operations.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.inclusion : {α : Type u_2} -> [Lattice α] -> {L M : Sublattice α} -> (h : L ≤ M) -> LatticeHom ↥L ↥M
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_2} -> [Lattice α] -> {L M : Sublattice α} -> (h : L ≤ M) -> LatticeHom ↥L ↥M`

The ambient type `α` is the lattice in which everything lives; it is inferred implicitly. The `Lattice α` instance supplies the lattice structure. `L` and `M` are sublattices of `α`, both inferred implicitly from context. The explicit argument `h` is the proof that `L` is contained in `M` (i.e., `L ≤ M` as sublattices). The result is a lattice homomorphism from the carrier type of `L` to the carrier type of `M`.

### Conventions

No special junk-value or boundary conventions are declared for this definition: the map is total and well-defined whenever `h : L ≤ M` is supplied, and the lattice operations are preserved definitionally (by reflexivity).

### Worked examples

- Claim: For any sublattices `L ≤ M` of a lattice `α` and any element `a : L`, applying `VTask.inclusion h` to `a` yields the canonical coercion of `a` into `M` (i.e., the underlying element is unchanged).

- Claim: The map `VTask.inclusion h` is injective for any `h : L ≤ M`.

- Claim: For sublattices `L ≤ M` of a lattice and elements `a b : L`, `VTask.inclusion h (a ⊔ b) = VTask.inclusion h a ⊔ VTask.inclusion h b` (join is preserved).

- Claim: For sublattices `L ≤ M` of a lattice and elements `a b : L`, `VTask.inclusion h (a ⊓ b) = VTask.inclusion h a ⊓ VTask.inclusion h b` (meet is preserved).

### Boundaries

- When `L = M` (and `h` is the reflexivity proof `le_refl L`), the inclusion is the identity homomorphism on `L`, mapping each element to itself (viewed in `M = L`).
- The definition is total: it is defined for any proof `h : L ≤ M`, with no additional hypotheses needed.
- Because the underlying function is `Set.inclusion h`, which simply repackages the element with a new membership proof, the map never changes the underlying value in `α`.

### Not to be confused with

- `Sublattice.subtype`: the coercion from a single sublattice `L` into the ambient lattice `α` itself, rather than into another sublattice `M`.
- `LatticeHom.id`: the identity homomorphism on a single sublattice, which is the special case of inclusion when `L = M` but is constructed differently.
- `Set.inclusion`: the underlying set-theoretic function (not a bundled lattice homomorphism) used inside the definition.