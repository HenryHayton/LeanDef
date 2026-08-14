## VTask.InfIrred

### Object

An element `a` of a semilattice with meets (infima) is **inf-irreducible** if it satisfies two conditions simultaneously: (1) it is not a maximal element of the order (equivalently, in a bounded lattice, it is not the top element ⊤), and (2) whenever `a` equals the meet (infimum) `b ⊓ c` of two elements `b` and `c`, then at least one of `b` or `c` must already equal `a` itself. Informally, `a` cannot be expressed as the meet of two strictly larger elements; any meet-factorisation of `a` is trivial.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.InfIrred : {α : Type u_2} -> [SemilatticeInf α] -> (a : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_2} -> [SemilatticeInf α] -> (a : α) -> Prop`

The type parameter `α` is a type equipped with a semilattice structure providing binary meets (infima). The instance argument provides that semilattice structure. The explicit argument `a` is the element whose inf-irreducibility is being asserted.

### Conventions

In a lattice with a top element ⊤, inf-irreducibility implies `a ≠ ⊤`, since ⊤ is a maximal (indeed the maximum) element and the non-maximality condition excludes it. The concept is the order-dual of sup-irreducibility: `a` is inf-irreducible in `α` if and only if `a` (viewed via the dual embedding) is sup-irreducible in the opposite order `αᵒᵈ`.

### Worked examples

- Claim: In a linear order, every non-maximal element is inf-irreducible, because in a total order `b ⊓ c` equals either `b` or `c`, so `b ⊓ c = a` forces `b = a` or `c = a`.

- Claim: The top element ⊤ of any bounded semilattice is never inf-irreducible, since ⊤ is maximal and `VTask.InfIrred ⊤` is false.

- Claim: If `VTask.InfIrred a` holds and `s.inf f = a` for some finite indexed family `f` over a non-empty index set `s`, then there exists some index `i ∈ s` with `f i = a` (the inf is witnessed by one of the factors coinciding with `a`).

- Claim: For any element `a` of a bounded lattice, there exists a finite set `s` of inf-irreducible elements whose infimum equals `a`, i.e., every element admits an inf-irreducible decomposition.

### Boundaries

- The top element (or any maximal element) of the semilattice always fails to be inf-irreducible, because the non-maximality condition is part of the definition.
- In a linear (totally ordered) semilattice, every non-maximal element is automatically inf-irreducible, since the meet of any two elements is one of them.
- In a distributive lattice, inf-irreducibility coincides with inf-primeness (`VTask.InfIrred a ↔ InfPrime a`), but in a general semilattice the two notions may diverge.
- If `a` itself is a bottom element but is not maximal (which can happen in non-trivial lattices), inf-irreducibility is still possible and must be checked against the universal condition.

### Not to be confused with

- **`SupIrred a`**: The order-dual notion; `a` is sup-irreducible when it is not minimal and any sup-factorisation is trivial. They are related by duality but are distinct predicates on the same type.
- **`InfPrime a`**: A strictly stronger (in general) condition requiring that whenever `a` is below a meet `b ⊓ c`, then `a ≤ b` or `a ≤ c`; coincides with inf-irreducibility in distributive lattices but not in general.
- **`IsMin a`** / **`IsMax a`**: The non-maximality condition in inf-irreducibility exactly prohibits `IsMax a`, but `IsMin` (being a bottom element) is unrelated and does not prevent inf-irreducibility.
