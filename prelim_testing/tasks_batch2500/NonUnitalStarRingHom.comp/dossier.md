## Object

The composition of two non-unital ⋆-ring homomorphisms, yielding a new non-unital ⋆-ring homomorphism. Specifically, given a non-unital ⋆-ring homomorphism `f : B →⋆ₙ+* C` and another `g : A →⋆ₙ+* B`, the composite `f ∘ g` (first apply `g`, then `f`) is itself a non-unital ⋆-ring homomorphism `A →⋆ₙ+* C`, respecting addition, multiplication, and the star (involution) operation — without requiring a multiplicative unit.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {A : Type u_1} -> {B : Type u_2} -> {C : Type u_3} -> [NonUnitalNonAssocSemiring A] -> [Star A] -> [NonUnitalNonAssocSemiring B] -> [Star B] -> [NonUnitalNonAssocSemiring C] -> [Star C] -> (f : B →⋆ₙ+* C) -> (g : A →⋆ₙ+* B) -> A →⋆ₙ+* C
<!-- PINNED-SIGNATURE:END -->


VTask.comp : {A : Type u_1} -> {B : Type u_2} -> {C : Type u_3} -> [NonUnitalNonAssocSemiring A] -> [Star A] -> [NonUnitalNonAssocSemiring B] -> [Star B] -> [NonUnitalNonAssocSemiring C] -> [Star C] -> (f : B →⋆ₙ+* C) -> (g : A →⋆ₙ+* B) -> A →⋆ₙ+* C

The implicit type arguments `A`, `B`, and `C` are the source, intermediate, and target types, each equipped with the structure of a non-unital non-associative semiring and a star operation (the instance arguments). The first explicit argument `f` is the outer (second-applied) non-unital ⋆-ring homomorphism from `B` to `C`. The second explicit argument `g` is the inner (first-applied) non-unital ⋆-ring homomorphism from `A` to `B`. The result is the composite homomorphism from `A` to `C`.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a total construction on well-typed inputs, and any non-unital ⋆-ring homomorphisms `f` and `g` with matching intermediate type yield a valid composite.

## Worked examples

- Claim: For any non-unital ⋆-ring homomorphisms `f : B →⋆ₙ+* C` and `g : A →⋆ₙ+* B`, the underlying function of `VTask.comp f g` maps an element `a : A` to `f (g a)`.

- Claim: For any non-unital ⋆-ring homomorphism `f : B →⋆ₙ+* C` and `g : A →⋆ₙ+* B`, and any element `a : A`, we have `VTask.comp f g (star a) = star (VTask.comp f g a)`, reflecting that the composition preserves the star involution.

- Claim: Composition of non-unital ⋆-ring homomorphisms is associative: for homomorphisms `f : C →⋆ₙ+* D`, `g : B →⋆ₙ+* C`, and `h : A →⋆ₙ+* B`, the composites `VTask.comp f (VTask.comp g h)` and `VTask.comp (VTask.comp f g) h` agree as functions on `A`.

## Boundaries

- The definition requires no unit element; it works for non-unital non-associative semirings equipped with a star operation.
- If either `f` or `g` is the zero homomorphism (constantly zero), the composite is also the zero homomorphism.
- The construction is fully compositional: the resulting morphism `VTask.comp f g` is itself a valid non-unital ⋆-ring homomorphism, so it can itself serve as an argument to further applications of `VTask.comp`.
- There is no restriction that the intermediate type `B` be non-trivial; even degenerate or trivial rings are handled uniformly.

## Not to be confused with

- `NonUnitalRingHom.comp`: composition of non-unital ring homomorphisms without any star structure; it does not track or verify preservation of the star involution.
- `StarRingHom.comp` (or the unital variant): composition of unital ⋆-ring homomorphisms, which additionally requires and preserves the multiplicative unit.
- Function composition (`Function.comp`): plain function composition with no algebraic structure, which does not bundle the proof that the result is a non-unital ⋆-ring homomorphism.