## VTask.unitsFstOne

### Object

`VTask.unitsFstOne R A` is the subgroup of the group of units of the unitization `Unitization R A` consisting precisely of those units whose scalar (first) component equals `1`. Concretely, the unitization `Unitization R A` pairs a scalar in `R` with an element of `A`; a unit of this ring belongs to `VTask.unitsFstOne R A` if and only if the `R`-component of its underlying element is `1 ∈ R`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.unitsFstOne : (R : Type u_1) -> (A : Type u_2) -> [CommSemiring R] -> [NonUnitalSemiring A] -> [Module R A] -> [IsScalarTower R A A] -> [SMulCommClass R A A] -> Subgroup (Unitization R A)ˣ
<!-- PINNED-SIGNATURE:END -->


`(R : Type u_1) -> (A : Type u_2) -> [CommSemiring R] -> [NonUnitalSemiring A] -> [Module R A] -> [IsScalarTower R A A] -> [SMulCommClass R A A] -> Subgroup (Unitization R A)ˣ`

`R` is the commutative semiring that provides the scalar part of the unitization. `A` is the non-unital semiring that provides the non-scalar part. The remaining arguments are the typeclass hypotheses: `CommSemiring R` makes `R` a commutative semiring; `NonUnitalSemiring A` makes `A` a non-unital semiring; `Module R A` equips `A` with an `R`-module structure; `IsScalarTower R A A` and `SMulCommClass R A A` ensure the scalar multiplication is compatible with the multiplication on `A` in the two standard ways required for the unitization construction.

### Conventions

There are no junk-value or boundary conventions to declare: the definition is a global construction depending only on the typeclass structure; it is total and well-defined for any choice of `R` and `A` satisfying the hypotheses.

### Worked examples

- Claim: An element `x : (Unitization R A)ˣ` belongs to `VTask.unitsFstOne R A` if and only if `x.val.fst = 1`.

- Claim: The identity element `1 : (Unitization R A)ˣ` belongs to `VTask.unitsFstOne R A`, because the first component of the multiplicative identity in the unitization is `1 ∈ R`.

- Claim: If `x ∈ VTask.unitsFstOne R A` and `y ∈ VTask.unitsFstOne R A`, then `x * y ∈ VTask.unitsFstOne R A`; the scalar part of a product in the unitization is the product of the scalar parts, and `1 * 1 = 1`.

- Claim: If `x ∈ VTask.unitsFstOne R A`, then `x⁻¹ ∈ VTask.unitsFstOne R A`; the scalar component of the inverse of a unit with scalar part `1` is again `1`.

### Boundaries

- When `A` is the zero ring (or the trivial module), the unitization `Unitization R A` is isomorphic to `R` itself, and `VTask.unitsFstOne R A` reduces to the trivial subgroup `{1}` inside `Rˣ`.
- If `R` itself has no elements other than `1` (for instance when `R` is the trivial ring), then `VTask.unitsFstOne R A` coincides with the entire unit group `(Unitization R A)ˣ`.
- The membership condition `x.val.fst = 1` refers to the underlying element `x.val : Unitization R A` of the unit `x`, not to the unit itself; one must unfold one level of the `Units` wrapper to access the scalar part.
- Both `x.val.fst = 1` and `x⁻¹.val.fst = 1` hold simultaneously for any member, as guaranteed by `unitsFstOne_val_inv_val_fst`.

### Not to be confused with

- `(Unitization R A)ˣ` itself: the full unit group of the unitization, which imposes no condition on the scalar part.
- The kernel of the ring homomorphism `fstHom R A` restricted to units: while closely related, `VTask.unitsFstOne R A` is specifically the fiber over `1`, not over `0`.
- Units of `A` embedded into `(Unitization R A)ˣ`: those would have scalar part `0` (the zero of `R`), not `1`.
