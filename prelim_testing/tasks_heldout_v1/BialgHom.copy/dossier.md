## Object

`VTask.copy` constructs a bialgebra homomorphism from an existing one by replacing its underlying function with a definitionally equal one. The result is a new `BialgHom` (a map of bialgebras over a commutative semiring `R`) whose action on elements is given by the supplied function `f'`, which is required to be equal — as a bare function — to the coercion of the original homomorphism `f`. The purpose is to allow the user to name or unfold a specific function in contexts where definitional equality matters, without changing the mathematical content of the map.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.copy : {R : Type u_1} -> {A : Type u_2} -> {B : Type u_3} -> [CommSemiring R] -> [Semiring A] -> [Semiring B] -> [Algebra R A] -> [Algebra R B] -> [CoalgebraStruct R A] -> [CoalgebraStruct R B] -> (f : A →ₐc[R] B) -> (f' : A → B) -> (h : f' = ⇑f) -> A →ₐc[R] B
<!-- PINNED-SIGNATURE:END -->


`VTask.copy` takes the following arguments:

- The type-class arguments (`R`, `A`, `B` together with their algebra, semiring, and coalgebra-structure instances) fix the ambient setting: `R` is the base commutative semiring, while `A` and `B` are `R`-bialgebras.
- `f` is the source bialgebra homomorphism from `A` to `B` whose structure (multiplicativity, unitality, and compatibility with the coalgebra structure) will be inherited by the copy.
- `f'` is the new underlying function `A → B` that the copy will use.
- `h` is the proof that `f'` is equal (as a plain function) to the coercion of `f` to a bare function, ensuring no mathematical content is altered.

## Conventions

There are no junk-value or edge conventions to declare: the operation is total and well-defined for every valid triple `(f, f', h)` without any boundary cases or special output conventions.

## Worked examples

- Claim: For any bialgebra homomorphism `f : A →ₐc[R] B`, the copy with `f' = ⇑f` and proof `rfl` is equal to `f` as a bialgebra homomorphism (i.e., `VTask.copy f (⇑f) rfl = f`).

- Claim: For any bialgebra homomorphism `f : A →ₐc[R] B`, the coercion of `VTask.copy f f' h` to a bare function equals `f'` (i.e., `⇑(VTask.copy f f' h) = f'`).

- Claim: If `f : A →ₐc[R] B` is a bialgebra homomorphism and `f' : A → B` with `h : f' = ⇑f`, then for any element `a : A`, applying the copied homomorphism to `a` yields the same result as applying `f` to `a`.

## Boundaries

- The proof `h` must be an equality of functions `f' = ⇑f`; the definition is vacuous if this obligation is not met, but when it is satisfied the copy is definitionally interchangeable with `f` up to unfolding `f'`.
- The copy carries the same algebraic laws (multiplicativity, unitality, `R`-linearity, and coalgebra-compatibility) as the original `f`; none of these need to be re-verified by the caller.
- When `f'` happens to be syntactically identical to `⇑f`, the copy is equal to the original `f` (as a bialgebra homomorphism), not merely extensionally equivalent.

## Not to be confused with

- `CoalgHom.copy`: the analogous copy construction for bare coalgebra homomorphisms, which lacks the multiplicativity and unitality structure of a bialgebra map.
- `AlgHom.copy`: the copy construction for algebra homomorphisms only, which does not carry any coalgebra (comultiplication/counit) compatibility.
- `BialgHom.mk`: direct construction of a `BialgHom` from scratch, which requires the caller to supply and prove all algebraic and coalgebraic axioms explicitly, rather than inheriting them from an existing map.