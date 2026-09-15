## Object

`VTask.op` is a canonical equivalence (a bijection that is natural in all arguments) between the type of `R`-algebra homomorphisms `A →ₐ[R] B` and the type of `R`-algebra homomorphisms `Aᵐᵒᵖ →ₐ[R] Bᵐᵒᵖ`, where `Aᵐᵒᵖ` and `Bᵐᵒᵖ` denote the opposite algebras (same underlying additive group, but with multiplication reversed). Concretely, given an algebra map `f : A →ₐ[R] B`, the equivalence produces an algebra map between the opposite algebras that sends `aᵒᵖ` to `f(a)ᵒᵖ`, and the inverse direction undoes this passage. This is the functorial action of the "take opposites" involution on `R`-algebra homomorphisms.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.op : {R : Type u_1} -> {A : Type u_3} -> {B : Type u_4} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Algebra R A] -> [Algebra R B] -> (A →ₐ[R] B) ≃ (Aᵐᵒᵖ →ₐ[R] Bᵐᵒᵖ)
<!-- PINNED-SIGNATURE:END -->


`VTask.op : {R : Type u_1} -> {A : Type u_3} -> {B : Type u_4} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Algebra R A] -> [Algebra R B] -> (A →ₐ[R] B) ≃ (Aᵐᵒᵖ →ₐ[R] Bᵐᵒᵖ)`

`R` is the commutative semiring of scalars over which both algebras are defined. `A` and `B` are the source and target semiring algebras over `R`, respectively. The instance arguments provide the semiring and algebra structures on `R`, `A`, and `B`. No explicit value arguments are required: the equivalence is determined entirely by the types.

## Conventions

The equivalence is self-inverse: applying `VTask.op` and then its inverse returns the original algebra homomorphism, and applying the inverse followed by `VTask.op` likewise returns the identity. There are no junk-value conventions declared for this definition because it is a total equivalence between well-formed types with no edge cases.

## Worked examples

- Claim: For any `R`-algebra `A`, applying `VTask.op` to the identity map `AlgHom.id R A` yields the identity map on `Aᵐᵒᵖ`, i.e., `(VTask.op (AlgHom.id R A)) = AlgHom.id R Aᵐᵒᵖ`.

- Claim: The equivalence `VTask.op` is an involution on algebra hom types: for any `f : A →ₐ[R] B`, applying `VTask.op.symm` to `VTask.op f` recovers `f`, i.e., `VTask.op.symm (VTask.op f) = f`.

- Claim: For `R = ℤ`, `A = B = ℤ`, and `f = AlgHom.id ℤ ℤ`, the forward map `VTask.op f` sends every element `nᵒᵖ` of `ℤᵐᵒᵖ` to `nᵒᵖ`.

## Boundaries

- The equivalence is defined for all semiring algebras over a commutative semiring; there are no restrictions beyond the stated typeclasses, and no degenerate or empty cases to handle.
- When `A = B` (endomorphism case), `VTask.op` restricts to an equivalence `(A →ₐ[R] A) ≃ (Aᵐᵒᵖ →ₐ[R] Aᵐᵒᵖ)`, but this is not a special case from the definition's point of view.
- The equivalence `VTask.op` is an involution at the level of equivalences: `VTask.op.trans VTask.op` (suitably composed for opposite-of-opposite) corresponds to the canonical identification of `(Aᵐᵒᵖ)ᵐᵒᵖ` with `A`.
- Because `ᵐᵒᵖ` reverses multiplication, algebra homomorphisms in the image of `VTask.op` satisfy the opposite-multiplication compatibility, not just the original ring-hom law.

## Not to be confused with

- `MulOpposite.op` / `MulOpposite.unop`: These are the element-level coercions that wrap and unwrap individual elements into/from the opposite type; `VTask.op` operates on whole algebra homomorphisms.
- `RingHom.op`: The analogous equivalence for plain ring homomorphisms (without scalar action), which `VTask.op` extends by additionally preserving the `R`-algebra structure.
- `AlgEquiv.op`: An equivalence between *algebra isomorphisms* `A ≃ₐ[R] B` and `Aᵐᵒᵖ ≃ₐ[R] Bᵐᵒᵖ`, which is the invertible analogue of `VTask.op` but lives in the world of `AlgEquiv` rather than `AlgHom`.