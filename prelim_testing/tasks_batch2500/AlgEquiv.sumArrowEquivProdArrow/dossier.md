## Object

This is the canonical algebra isomorphism between the algebra of functions from a disjoint union (sum type) `α ⊕ β` into an `R`-algebra `S`, and the product algebra of functions from `α` into `S` paired with functions from `β` into `S`. Concretely, a function `f : α ⊕ β → S` is identified with the pair `(f ∘ Sum.inl, f ∘ Sum.inr)`, and this identification respects the full `R`-algebra structure — pointwise addition, multiplication, scalar multiplication by `R`, and the unit — on both sides.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumArrowEquivProdArrow : (α : Type u_1) -> (β : Type u_2) -> (R : Type u_3) -> [CommSemiring R] -> (S : Type u_8) -> [Semiring S] -> [Algebra R S] -> (α ⊕ β → S) ≃ₐ[R] (α → S) × (β → S)
<!-- PINNED-SIGNATURE:END -->


`VTask.sumArrowEquivProdArrow : (α : Type u_1) -> (β : Type u_2) -> (R : Type u_3) -> [CommSemiring R] -> (S : Type u_8) -> [Semiring S] -> [Algebra R S] -> (α ⊕ β → S) ≃ₐ[R] (α → S) × (β → S)`

- `α` is the left summand type indexing part of the domain of functions.
- `β` is the right summand type indexing the remaining part of the domain.
- `R` is the commutative semiring of scalars; the `CommSemiring R` instance equips it with the algebraic structure needed to define `R`-algebras.
- `S` is the target `R`-algebra, equipped with a `Semiring` instance and an `Algebra R S` instance expressing how `R` acts on `S`.

The output is an `R`-algebra equivalence (`≃ₐ[R]`) between `(α ⊕ β → S)` and `(α → S) × (β → S)`, both carrying pointwise algebra structures.

## Conventions

No junk-value or edge conventions are declared for this definition: it is a total construction on arbitrary types `α`, `β`, `S` and a commutative semiring `R`, with no degenerate inputs producing meaningfully different output by convention.

## Worked examples

- Claim: For `α = β = Unit` and `S = ℤ` (as a `ℤ`-algebra), the forward direction of `VTask.sumArrowEquivProdArrow Unit Unit ℤ ℤ` sends the constant function `fun _ => 5` to the pair `(fun _ => 5, fun _ => 5)`.

- Claim: For `α = Fin 2`, `β = Fin 3`, `S = ℤ`, the forward map `VTask.sumArrowEquivProdArrow (Fin 2) (Fin 3) ℤ ℤ` on a function `f : Fin 2 ⊕ Fin 3 → ℤ` produces `(fun i => f (Sum.inl i), fun j => f (Sum.inr j))`.

- Claim: The inverse of `VTask.sumArrowEquivProdArrow α β R S` applied to a pair `(g, h)` returns the function that maps `Sum.inl a` to `g a` and `Sum.inr b` to `h b`.

- Claim: `VTask.sumArrowEquivProdArrow α β R S` is an `R`-algebra homomorphism in both directions, meaning it commutes with addition, multiplication, and scalar multiplication by elements of `R`.

## Boundaries

- When `α` or `β` is the empty type `Empty`, one component of the product becomes the algebra of functions from `Empty` into `S`, which is a trivial (terminal) algebra. The equivalence still holds perfectly; the empty-type component carries no information.
- When `α = β`, the two components of the product are naturally isomorphic to each other, but `VTask.sumArrowEquivProdArrow` makes no special identification — they remain distinct components.
- When `S = R` (the base ring itself, as an algebra over itself), the equivalence still applies: functions from a sum type into `R` split as a product of function-algebras over each summand.
- The equivalence is strict (not just a natural isomorphism of functors in some weaker sense): it is a definitional algebra equivalence, invertible on both sides.

## Not to be confused with

- `Equiv.sumArrowEquivProdArrow`: the plain type equivalence (or ring equivalence) without the algebra structure; `VTask.sumArrowEquivProdArrow` is the strictly stronger `R`-algebra version.
- The product of `R`-algebras `S × S` for a fixed `S`: the product here is `(α → S) × (β → S)` with pointwise algebra structure, which is not the same as a tensor product or a single function algebra.
- `Pi.algEquiv` or splitting over an indexed family: this equivalence is specific to a binary sum (disjoint union of two types), not an arbitrary indexed family.