## Object

`VTask.finsuppLequivDFinsupp` is a linear equivalence (over a semiring `R`) between two kinds of "finitely supported" functions on an index type `ι` with values in an `R`-module `M`:

- **`ι →₀ M`** (Finsupp): finitely-supported functions where the support is stored as a `Finset`, bundled with an addition.
- **`Π₀ x : ι, M`** (DFinsupp): dependent finitely-supported functions (direct sum style), where the type family is constant `M`.

The equivalence is not merely a bijection or even an additive-group isomorphism; it respects the `R`-module structure, sending scalar multiples and sums in `Finsupp` to scalar multiples and sums in `DFinsupp` and vice versa.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.finsuppLequivDFinsupp : {ι : Type u_1} -> (R : Type u_2) -> {M : Type u_3} -> [DecidableEq ι] -> [Semiring R] -> [AddCommMonoid M] -> [(m : M) → Decidable (m ≠ 0)] -> [Module R M] -> (ι →₀ M) ≃ₗ[R] Π₀ (x : ι), M
<!-- PINNED-SIGNATURE:END -->


VTask.finsuppLequivDFinsupp : {ι : Type u_1} -> (R : Type u_2) -> {M : Type u_3} -> [DecidableEq ι] -> [Semiring R] -> [AddCommMonoid M] -> [(m : M) → Decidable (m ≠ 0)] -> [Module R M] -> (ι →₀ M) ≃ₗ[R] Π₀ (x : ι), M

The explicit argument `R` is the scalar semiring over which the linear equivalence is defined; it must be spelled out because Lean cannot infer it from the source and target types alone. The implicit argument `ι` is the common index type of the finitely-supported functions. The implicit argument `M` is the module of values, shared by both sides. The instance arguments supply decidable equality on indices (needed to manipulate finite supports), a semiring structure on `R`, an additive commutative monoid structure on `M`, a procedure for deciding whether any particular value of `M` is nonzero (needed by the `DFinsupp` side to track support), and an `R`-module structure on `M`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total construction producing a bundled linear equivalence, and every valid combination of the required type-class instances yields a well-defined equivalence with no exceptional cases.

## Worked examples

- Claim: Applying `VTask.finsuppLequivDFinsupp ℤ` to the zero element of `ℕ →₀ ℤ` yields the zero element of `Π₀ _ : ℕ, ℤ`.

- Claim: The forward map of `VTask.finsuppLequivDFinsupp R` agrees with `Finsupp.toDFinsupp`, i.e., for any `f : ι →₀ M`, `(VTask.finsuppLequivDFinsupp R) f = Finsupp.toDFinsupp f`.

- Claim: The inverse map of `VTask.finsuppLequivDFinsupp R` agrees with `DFinsupp.toFinsupp`, i.e., for any `g : Π₀ _ : ι, M`, `(VTask.finsuppLequivDFinsupp R).symm g = DFinsupp.toFinsupp g`.

- Claim: `VTask.finsuppLequivDFinsupp R` respects scalar multiplication: for any `r : R` and `f : ι →₀ M`, `(VTask.finsuppLequivDFinsupp R) (r • f) = r • (VTask.finsuppLequivDFinsupp R) f`.

## Boundaries

- When `ι` is empty, both `ι →₀ M` and `Π₀ _ : ι, M` each contain only the zero element, and the equivalence maps that unique element to the unique element.
- When `M` is the zero module, every function is zero regardless of support, and the equivalence is still well-defined and trivial.
- The equivalence is marked `noncomputable` because the `add` operation on `Finsupp` (used internally) is noncomputable; this does not affect the mathematical content but means it cannot be evaluated by the Lean kernel's reduction engine.
- The `DecidableEq ι` and `∀ m : M, Decidable (m ≠ 0)` instances are purely structural prerequisites; the mathematical content of the equivalence does not depend on the particular decidability witnesses chosen.

## Not to be confused with

- `Finsupp.finsuppEquivDFinsupp`: the underlying *setoid/type* equivalence (as types or additive-group equiv) without the `R`-linear structure; `VTask.finsuppLequivDFinsupp` adds and proves the module-map axioms on top.
- `Finsupp.toDFinsupp`: the bare function (forward direction only) from `Finsupp` to `DFinsupp`, with no inverse, linearity bundle, or `≃ₗ` wrapper.
- `DFinsupp.toFinsupp`: the bare function in the reverse direction; again, not a bundled equivalence and carries no module-map structure.
