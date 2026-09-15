## Object

`VTask.comp` is the composition of two star monoid homomorphisms, packaged as a single star monoid homomorphism. Given a star monoid homomorphism `f : B →⋆* C` and a star monoid homomorphism `g : A →⋆* B`, it produces the composite map `A →⋆* C` that sends each element `a : A` to `f(g(a))`. The resulting map is again a star monoid homomorphism: it preserves the monoid multiplication, the unit, and the star (involution) operation.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {A : Type u_2} -> {B : Type u_3} -> {C : Type u_4} -> [Monoid A] -> [Star A] -> [Monoid B] -> [Star B] -> [Monoid C] -> [Star C] -> (f : B →⋆* C) -> (g : A →⋆* B) -> A →⋆* C
<!-- PINNED-SIGNATURE:END -->


`VTask.comp : {A : Type u_2} -> {B : Type u_3} -> {C : Type u_4} -> [Monoid A] -> [Star A] -> [Monoid B] -> [Star B] -> [Monoid C] -> [Star C] -> (f : B →⋆* C) -> (g : A →⋆* B) -> A →⋆* C`

The implicit type arguments `A`, `B`, and `C` are the source, intermediate, and target types respectively; they each carry monoid and star structures supplied by the corresponding typeclass instances. The first explicit argument `f` is the outer star monoid homomorphism, mapping from `B` to `C`. The second explicit argument `g` is the inner star monoid homomorphism, mapping from `A` to `B`. The output is the composite star monoid homomorphism from `A` to `C`.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: it is a total construction on well-typed inputs, and every star monoid homomorphism input yields a valid star monoid homomorphism output with no degenerate cases.

## Worked examples

- Claim: Composing the identity star monoid homomorphism with any `g : A →⋆* B` yields a map that acts the same as `g` on every element.

- Claim: For star monoid homomorphisms `f : B →⋆* C`, `g : A →⋆* B`, and any `a : A`, we have `VTask.comp f g a = f (g a)` (the underlying function of the composite is the ordinary function composition).

- Claim: For any star monoid homomorphisms `f : B →⋆* C`, `g : A →⋆* B`, the composite `VTask.comp f g` maps the unit of `A` to the unit of `C`, since each factor preserves the unit.

- Claim: For any star monoid homomorphisms `f : B →⋆* C`, `g : A →⋆* B`, and any `a : A`, `VTask.comp f g (star a) = star (VTask.comp f g a)`, confirming the composite preserves the star operation.

## Boundaries

- When `A = B = C` and `f` and `g` are both the identity star monoid homomorphism, `VTask.comp f g` is again the identity.
- The operation is defined for any triple of types with monoid and star structures; there is no restriction on the nature of these structures (they need not be C*-algebras, groups, or anything beyond monoids with a star).
- Composition is associative: composing three star monoid homomorphisms in either parenthesisation yields the same result.

## Not to be confused with

- `MonoidHom.comp`: the composition of plain monoid homomorphisms, which does not track or enforce the star-preservation property.
- `StarHom.comp` (hypothetical): a composition for star homomorphisms that does not require the monoid structure; `VTask.comp` requires both the monoid and star laws.
- Function composition `Function.comp`: the raw function-level composition, which carries none of the algebraic structure or bundled proofs that `VTask.comp` provides.