## Object

`VTask.torsion'` is the **S-torsion submodule** of an R-module M. It is the submodule of M consisting of all elements x ∈ M for which there exists some scalar a ∈ S such that a • x = 0. In classical language, these are the elements of M that are "killed" (annihilated) by at least one element of S. The construction makes sense whenever S acts on M compatibly with the R-module structure.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.torsion' : (R : Type u_1) -> (M : Type u_2) -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> (S : Type u_3) -> [CommMonoid S] -> [DistribMulAction S M] -> [SMulCommClass S R M] -> Submodule R M
<!-- PINNED-SIGNATURE:END -->


VTask.torsion' : (R : Type u_1) -> (M : Type u_2) -> [CommSemiring R] -> [AddCommMonoid M] -> [Module R M] -> (S : Type u_3) -> [CommMonoid S] -> [DistribMulAction S M] -> [SMulCommClass S R M] -> Submodule R M

The first two explicit arguments, `R` and `M`, are the coefficient semiring and the module, respectively. The third explicit argument, `S`, is the "torsion monoid": its elements serve as the scalars used to test whether an element of M is torsion. The instance arguments impose that R is a commutative semiring, M is an additive commutative monoid carrying an R-module structure, S is a commutative monoid acting distributively on M, and that the S-action and the R-module structure commute with each other.

## Conventions

There are no declared junk-value or boundary conventions for this definition: it is a total construction returning a `Submodule R M` for every valid combination of inputs, and no degenerate inputs produce a meaningfully "junk" output requiring special documentation.

## Worked examples

- Claim: The zero element of any R-module M always belongs to `VTask.torsion' R M S`, because 1 • 0 = 0 witnesses the torsion condition.

- Claim: For R = ℤ, M = ℤ/nℤ (with n ≥ 2), and S = ℤ, every element of M belongs to `VTask.torsion' ℤ M ℤ`, because multiplication by n kills every element.

- Claim: For R = ℤ, M = ℤ (the integers as a module over themselves), and S = ℤ, `VTask.torsion' ℤ ℤ ℤ` contains only 0, since no nonzero integer is annihilated by a nonzero integer.

- Claim: If S = {1} (the trivial one-element monoid) acting trivially, then `VTask.torsion' R M S` contains exactly those x with 1 • x = 0, i.e., x = 0, so the torsion submodule is the zero submodule.

## Boundaries

- **Zero element**: The zero element of M always lies in `VTask.torsion' R M S`, witnessed by the identity element 1 ∈ S satisfying 1 • 0 = 0.
- **S = trivial monoid**: If S has only one element (the identity), the torsion submodule collapses to {0}, since the only witness available is 1 and 1 • x = 0 forces x = 0.
- **M = 0**: If M is the zero module, then `VTask.torsion' R M S` is the zero submodule, which is all of M.
- **Torsion-free modules**: When M is torsion-free with respect to S (e.g., M = ℤ over S = ℤ), the torsion submodule is {0}.
- **The entire module**: When every element of M is killed by some element of S (e.g., a finite abelian group over S = ℤ), the torsion submodule equals all of M.
- **No upper bound on the witness**: Different elements of M may require different elements of S as witnesses; there is no single annihilator required to work uniformly.

## Not to be confused with

- **`Module.torsion R M`** (the torsion submodule with S taken to be the non-zero-divisors of R, or specifically the multiplicative submonoid of nonzero elements): that is the classical torsion submodule of R-module theory, a special case of `VTask.torsion'`.
- **`Module.torsionBy R M a`** (torsion by a single fixed element a): that consists of elements killed by one specific scalar, not by some element of a whole monoid.
- **The annihilator of a module** (`Module.annihilator`): that is the set of ring elements that kill every element of M, living inside R, not inside M.