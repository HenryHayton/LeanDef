## Object

`VTask.copy` produces a new star algebra homomorphism from `A` to `B` over `R` whose underlying function is a prescribed function `f'`, given a proof that `f'` coincides (as a bare function) with an already-known star algebra homomorphism `f`. The result carries exactly the same algebraic structure as `f` but is packaged with `f'` as its `toFun` field. The purpose is to manufacture a definitionally distinct but propositionally equal morphism, which can be useful when Lean's definitional equality checker needs to see a specific syntactic form for the underlying function.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {R : Type u_2} -> {A : Type u_3} -> {B : Type u_4} -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [Star A] -> [Semiring B] -> [Algebra R B] -> [Star B] -> (f : A →⋆ₐ[R] B) -> (f' : A → B) -> (h : f' = ⇑f) -> A →⋆ₐ[R] B
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {R : Type u_2} -> {A : Type u_3} -> {B : Type u_4} -> [CommSemiring R] -> [Semiring A] -> [Algebra R A] -> [Star A] -> [Semiring B] -> [Algebra R B] -> [Star B] -> (f : A →⋆ₐ[R] B) -> (f' : A → B) -> (h : f' = ⇑f) -> A →⋆ₐ[R] B`

The implicit type arguments `R`, `A`, and `B` are the scalar semiring and the source and target star `R`-algebras, respectively. The typeclass arguments supply the ring, algebra, and star structure on each type. The explicit argument `f` is the reference star algebra homomorphism whose algebraic axioms are to be inherited. The argument `f'` is the new bare function that will serve as the underlying map of the result. The argument `h` is the proof that `f'` and the coercion of `f` are equal as functions `A → B`.

## Conventions

The copy is propositionally equal to the original morphism `f` (the theorem `VTask.copy_eq` holds), even though the underlying function field is syntactically `f'`. There are no junk-value conventions because every argument is fully constrained: `h` must be a proof of equality and the function `f'` must agree with `f` everywhere.

## Worked examples

- Claim: For any `f : A →⋆ₐ[R] B`, the coercion of `VTask.copy f (⇑f) rfl` equals `⇑f`.

- Claim: For any `f : A →⋆ₐ[R] B`, `VTask.copy f (⇑f) rfl = f` as star algebra homomorphisms (i.e., the copy with `f' = ⇑f` and `h = rfl` is the same morphism as `f`).

- Claim: For any star algebra homomorphism `f : A →⋆ₐ[R] B` and any function `f' : A → B` with proof `h : f' = ⇑f`, applying `VTask.copy f f' h` to an element `a : A` gives `f' a`.

## Boundaries

- The function `f'` must be propositionally equal to the coercion of `f`; a weaker notion such as pointwise equality is not accepted — `h` must be a proof of equality of functions `f' = ⇑f`.
- When `f' = ⇑f` and `h = rfl`, the copy is definitionally equal to `f` in its `toFun` field and propositionally equal to `f` as a bundled morphism.
- The operation is total: as long as `h` is provided, the result is a well-formed star algebra homomorphism with all the required axioms automatically transferred from `f`.
- If `f'` is chosen to be a lambda expression that is definitionally but not syntactically equal to `⇑f`, the caller must supply the corresponding proof `h` explicitly; `VTask.copy` does not attempt to infer it.

## Not to be confused with

- The original morphism `f` itself: `VTask.copy f f' h` and `f` are propositionally equal as bundled morphisms, but their `toFun` fields may differ syntactically, which is precisely why `copy` exists.
- `AlgHom.copy`: the analogous copy constructor for plain (non-star) algebra homomorphisms, which does not carry or preserve the `map_star` axiom.
- `StarHom.copy` (if it exists): a copy constructor for star homomorphisms without the algebra structure, operating in a different category.