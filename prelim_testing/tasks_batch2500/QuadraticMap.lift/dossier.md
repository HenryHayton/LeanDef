## VTask.lift

### Object

Given a quadratic map `Q : M → P` over a commutative ring `R`, and a submodule `N` of `M` that is contained in the radical of `Q` (i.e., every element of `N` is mapped to zero by `Q` and pairs trivially with all of `M` under the associated polar form), `VTask.lift` produces a well-defined quadratic map on the quotient module `M ⧸ N` with values in `P`. In other words, it descends `Q` to the quotient, which is possible precisely because the elements being quotiented out do not affect the value of `Q`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lift : {R : Type u_1} -> {M : Type u_2} -> {P : Type u_4} -> [AddCommGroup M] -> [AddCommGroup P] -> [CommRing R] -> [Module R M] -> [Module R P] -> (Q : QuadraticMap R M P) -> (N : Submodule R M) -> (hN : N ≤ Q.radical) -> QuadraticMap R (M ⧸ N) P
<!-- PINNED-SIGNATURE:END -->


`VTask.lift : {R : Type u_1} -> {M : Type u_2} -> {P : Type u_4} -> [AddCommGroup M] -> [AddCommGroup P] -> [CommRing R] -> [Module R M] -> [Module R P] -> (Q : QuadraticMap R M P) -> (N : Submodule R M) -> (hN : N ≤ Q.radical) -> QuadraticMap R (M ⧸ N) P`

The implicit type arguments `R`, `M`, and `P` are, respectively: the commutative ring of scalars, the module being quotiented, and the target abelian group in which the quadratic map takes values. The type-class arguments supply the algebraic structures on these types. The explicit argument `Q` is the quadratic map defined on the original module `M`. The argument `N` is the submodule that will be quotiented out. The argument `hN` is the proof obligation that `N` is contained in the radical of `Q`, which is the condition that makes the descent well-defined.

### Conventions

No junk-value or edge-case conventions are declared for this definition: it is a total construction whose output is fully determined whenever the inputs satisfy the stated inequality `N ≤ Q.radical`, and there are no degenerate inputs that produce unspecified or arbitrary outputs.

### Worked examples

- Claim: For any commutative ring `R`, `R`-module `M`, quadratic map `Q : QuadraticMap R M P`, and submodule `N ≤ Q.radical`, evaluating `VTask.lift Q N hN` at the coset `⟦m⟧` of any `m : M` returns the same value as `Q m`.

- Claim: If `N` is the zero submodule, then `N ≤ Q.radical` holds trivially (the zero element is always in the radical of any quadratic map), and `VTask.lift Q ⊥ h` is a quadratic map on `M ⧸ ⊥ ≅ M` that computes identically to `Q`.

- Claim: If `N = Q.radical` itself (taking `hN` to be `le_refl _`), then `VTask.lift Q Q.radical hN` is a quadratic map on `M ⧸ Q.radical`, and its own radical is trivial (i.e., the map is non-degenerate on the quotient by its radical).

### Boundaries

- The construction requires `N ≤ Q.radical` as a proof argument; if this condition fails, no lift is produced (the definition simply does not apply).
- When `N = ⊥` (the zero submodule), the quotient `M ⧸ ⊥` is canonically isomorphic to `M`, and the lifted map corresponds to `Q` itself under this isomorphism.
- When `N = Q.radical`, the lifted map is the canonical non-degenerate (or anisotropic-radical-free) quadratic map on the quotient by the full radical.
- The key compatibility property is `VTask.lift Q N hN ⟦m⟋ = Q m` for all `m : M`, which characterizes the lift uniquely.

### Not to be confused with

- `QuadraticMap.radical`: the radical submodule of `Q` itself, which is the domain constraint used as input to `VTask.lift`, not the output.
- `LinearMap.liftQ` or `Submodule.liftQ`: analogous descent constructions for linear maps to quotient modules, which do not account for the quadratic (degree-2) structure.
- `QuadraticMap.associated` or `QuadraticMap.polarBilin`: the associated bilinear/polar form of `Q`, which is a related but distinct object used internally to verify well-definedness of the lift.