## Object

`VTask.copy` constructs a new star-monoid homomorphism from `A` to `B` that is definitionally equal to a given one, but whose underlying function has been replaced by a (propositionally) equal function. It is a bookkeeping tool used to adjust definitional equalities—for example, to make the underlying function reduce in a particular way—without changing the mathematical content of the homomorphism.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {A : Type u_2} -> {B : Type u_3} -> [Monoid A] -> [Star A] -> [Monoid B] -> [Star B] -> (f : A →⋆* B) -> (f' : A → B) -> (h : f' = ⇑f) -> A →⋆* B
<!-- PINNED-SIGNATURE:END -->


`VTask.copy : {A : Type u_2} -> {B : Type u_3} -> [Monoid A] -> [Star A] -> [Monoid B] -> [Star B] -> (f : A →⋆* B) -> (f' : A → B) -> (h : f' = ⇑f) -> A →⋆* B`

The implicit types `A` and `B` are the source and target monoids equipped with star operations. The instance arguments provide the monoid and star structures on each. The argument `f` is the original star-monoid homomorphism being copied. The argument `f'` is the new underlying function that will be used; it must be a plain function `A → B`. The argument `h` is a proof that `f'` equals the coercion of `f` to a function, establishing that the replacement is propositionally the same map.

## Conventions

No special junk-value or edge conventions are declared: the definition is total and well-defined for all inputs satisfying the stated types, and no boundary regime with distinguished junk behavior arises.

## Worked examples

- Claim: For any star-monoid homomorphism `f : A →⋆* B`, the copy obtained with `f' = ⇑f` and `h = rfl` satisfies `⇑(VTask.copy f (⇑f) rfl) = ⇑f` (the coercion of the copy equals `f'`).

- Claim: For any star-monoid homomorphism `f : A →⋆* B`, the copy obtained with `f' = ⇑f` and `h = rfl` is equal (as a star-monoid homomorphism) to `f` itself, i.e., `VTask.copy f (⇑f) rfl = f`.

- Claim: Given `f : A →⋆* B` and a function `g : A → B` with a proof `h : g = ⇑f`, the value of `VTask.copy f g h` at any element `a : A` equals `g a`.

## Boundaries

- The proof `h` must witness that `f'` equals the coercion `⇑f` (not merely that they agree pointwise); this is a strict propositional equality of functions.
- When `f' = ⇑f` and `h = rfl`, the copy is provably equal to `f` as a bundled homomorphism (by `copy_eq`).
- The definition does not impose any new mathematical content: the resulting morphism preserves multiplication, unit, and the star operation in exactly the same way as `f`.
- There is no restriction on the monoids `A` and `B`; the definition is valid for any types carrying the required structures.

## Not to be confused with

- `StarMonoidHom.mk` / the bundled constructor: that constructs a star-monoid homomorphism from scratch by providing all fields, whereas `VTask.copy` derives all fields from an existing homomorphism and merely substitutes the underlying function.
- Function composition of star-monoid homomorphisms: composing changes the mathematical map itself, while `VTask.copy` keeps the same mathematical map and only adjusts definitional presentation.
- Subtype casting or coercion: coercions convert between types without producing a new bundled morphism, whereas `VTask.copy` always returns a fully bundled `A →⋆* B`.