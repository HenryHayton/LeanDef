## VTask.radical

### Object

The radical of a quadratic map `Q : M → P` over a commutative ring `R` is the largest submodule `N` of the domain `M` with the property that `Q` descends to a well-defined quadratic map on the quotient `M ⧸ N`. Concretely, it is the set of all vectors `x ∈ M` that simultaneously vanish under `Q` itself and under the polarization (associated bilinear form) of `Q` in every direction. It measures the degeneracy of `Q`: when the radical is trivial (`{0}`), the quadratic map is nondegenerate.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.radical : {R : Type u_1} -> {M : Type u_2} -> {P : Type u_4} -> [AddCommGroup M] -> [AddCommGroup P] -> [CommRing R] -> [Module R M] -> [Module R P] -> (Q : QuadraticMap R M P) -> Submodule R M
<!-- PINNED-SIGNATURE:END -->


`{R : Type u_1} -> {M : Type u_2} -> {P : Type u_4} -> [AddCommGroup M] -> [AddCommGroup P] -> [CommRing R] -> [Module R M] -> [Module R P] -> (Q : QuadraticMap R M P) -> Submodule R M`

- `R` is the commutative ring of scalars.
- `M` is the domain module on which the quadratic map is defined.
- `P` is the codomain additive commutative group (also an `R`-module) into which `Q` takes values.
- `Q` is the quadratic map whose radical is being computed; the result is a submodule of `M`.

### Conventions

An element `x : M` belongs to `VTask.radical Q` if and only if `Q x = 0` **and** the polar bilinear form `polarBilin Q` satisfies `polarBilin Q x = 0` (as a linear map `M → P`). These two conditions together are required even in characteristic 2, where the polar form alone may be insufficient to capture all degenerate directions.

### Worked examples

- Claim: For any quadratic map `Q`, an element `x` lies in `VTask.radical Q` if and only if `Q x = 0` and for every `n : M`, `Q (x + n) = Q n`.

- Claim: A quadratic map `Q` is nondegenerate if and only if `VTask.radical Q = ⊥` (the zero submodule).

- Claim: The radical `VTask.radical Q` is contained in the kernel of `polarBilin Q`; in characteristic other than 2 these coincide (i.e., `VTask.radical Q = (polarBilin Q).ker`).

- Claim: For any submodule `N ≤ VTask.radical Q` and any `m : M`, the lift of `Q` to `M ⧸ N` evaluated at the image of `m` equals `Q m`.

### Boundaries

- The zero vector always lies in `VTask.radical Q` because `Q 0 = 0` and the polar bilinear form vanishes at 0, so the radical is never empty.
- If `Q` is the zero quadratic map, then every element satisfies both conditions, so `VTask.radical Q = ⊤`.
- If `Q` is nondegenerate, then `VTask.radical Q = ⊥`.
- The radical is a genuine submodule (closed under addition and scalar multiplication), not merely a set.
- In characteristic 2, the polarization `polarBilin Q` is alternating and can vanish even for non-zero `Q`, so the condition `Q x = 0` is essential and cannot be dropped.

### Not to be confused with

- **`LinearMap.ker` of `polarBilin Q`**: The kernel of the polar bilinear form alone; this equals `VTask.radical Q` when `2` is invertible in `R`, but can be strictly larger in characteristic 2.
- **`QuadraticMap.Nondegenerate`**: A predicate asserting that `VTask.radical Q = ⊥`; it is a property of `Q`, not the submodule itself.
- **The radical of an ideal**: An entirely different notion (the set of elements with some power in the ideal), unrelated to quadratic forms.