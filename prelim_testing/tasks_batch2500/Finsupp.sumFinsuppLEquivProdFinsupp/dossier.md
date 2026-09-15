## Object

`VTask.sumFinsuppLEquivProdFinsupp` is a linear equivalence (an invertible, `R`-linear map) between the `R`-module of finitely-supported functions from a disjoint-union type `α ⊕ β` into an `R`-module `M`, and the product of the two `R`-modules of finitely-supported functions from `α` and from `β` into `M` separately. Concretely, a finitely-supported function on `α ⊕ β` is the same data as a pair of finitely-supported functions, one on `α` and one on `β`, obtained by restricting to each summand.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumFinsuppLEquivProdFinsupp : {M : Type u_2} -> (R : Type u_5) -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> {α : Type u_7} -> {β : Type u_8} -> (α ⊕ β →₀ M) ≃ₗ[R] (α →₀ M) × (β →₀ M)
<!-- PINNED-SIGNATURE:END -->


`VTask.sumFinsuppLEquivProdFinsupp : {M : Type u_2} -> (R : Type u_5) -> [Semiring R] -> [AddCommMonoid M] -> [Module R M] -> {α : Type u_7} -> {β : Type u_8} -> (α ⊕ β →₀ M) ≃ₗ[R] (α →₀ M) × (β →₀ M)`

The argument `R` is the semiring of scalars over which the linear equivalence is defined. The implicit argument `M` is the coefficient type (an `R`-module) in which all finitely-supported functions take values. The implicit type arguments `α` and `β` are the two index types whose disjoint union forms the domain of the source finsupp.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a totally-defined bundled linear equivalence whose inputs are determined entirely by the type-class assumptions.

## Worked examples

- Claim: Applying `VTask.sumFinsuppLEquivProdFinsupp` to the finsupp supported at `Sum.inl a` with value `m` yields the pair `(Finsupp.single a m, 0)`.

- Claim: Applying `VTask.sumFinsuppLEquivProdFinsupp` to the finsupp supported at `Sum.inr b` with value `m` yields the pair `(0, Finsupp.single b m)`.

- Claim: The inverse of `VTask.sumFinsuppLEquivProdFinsupp` applied to a pair `(f, g)` is the finsupp whose value at `Sum.inl a` is `f a` and whose value at `Sum.inr b` is `g b`.

- Claim: `VTask.sumFinsuppLEquivProdFinsupp` respects scalar multiplication: for any scalar `r : R` and finsupp `h : α ⊕ β →₀ M`, `VTask.sumFinsuppLEquivProdFinsupp R (r • h) = r • VTask.sumFinsuppLEquivProdFinsupp R h`.

## Boundaries

- When `α` or `β` is an empty type, the corresponding component of the product is the zero module (the only finsupp on an empty type is zero), and the equivalence reduces to an isomorphism between `β →₀ M` (or `α →₀ M`) and the product with a trivial factor.
- When both `α` and `β` are empty, both sides are isomorphic to the zero module and the equivalence is the unique isomorphism between two zero modules.
- The equivalence is defined for any semiring `R` and any `R`-module `M`; in particular it applies to the case `R = ℕ` (the trivial semiring case), recovering additive structure.

## Not to be confused with

- `Finsupp.sumFinsuppEquivProdFinsupp`: the underlying *additive* equivalence (`≃+`) that this linear equivalence extends; `VTask.sumFinsuppLEquivProdFinsupp` adds the `R`-linearity.
- `Finsupp.domCoprod` or related constructions: combining finsupps via a coproduct in a different sense (e.g., summing values rather than splitting domains).
- `DirectSum.lequivProdDirectSum`: a related but distinct construction for direct sums of modules rather than finitely-supported functions on a sum type.