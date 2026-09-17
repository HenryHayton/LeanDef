## Object

The composition of two multiplication-preserving maps (multiplicative homomorphisms between magmas, i.e., types equipped with a binary multiplication). Given a map `hmn : M →ₙ* N` and a map `hnp : N →ₙ* P`, the result `VTask.comp hnp hmn : M →ₙ* P` is the multiplicative homomorphism obtained by first applying `hmn` and then `hnp`. The resulting map preserves multiplication: it sends `x * y` to `(hnp ∘ hmn)(x) * (hnp ∘ hmn)(y)`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.comp : {M : Type u_4} -> {N : Type u_5} -> {P : Type u_6} -> [Mul M] -> [Mul N] -> [Mul P] -> (hnp : N →ₙ* P) -> (hmn : M →ₙ* N) -> M →ₙ* P
<!-- PINNED-SIGNATURE:END -->


`{M : Type u_4} -> {N : Type u_5} -> {P : Type u_6} -> [Mul M] -> [Mul N] -> [Mul P] -> (hnp : N →ₙ* P) -> (hmn : M →ₙ* N) -> M →ₙ* P`

The implicit type arguments `M`, `N`, and `P` are the source, intermediate, and target types respectively. The instance arguments `[Mul M]`, `[Mul N]`, `[Mul P]` supply the binary multiplication operations on each type. The first explicit argument `hnp` is the multiplicative homomorphism from the intermediate type `N` to the target type `P`. The second explicit argument `hmn` is the multiplicative homomorphism from the source type `M` to the intermediate type `N`. Note the order mirrors standard mathematical composition notation: the outer (second-applied) map is listed first.

## Conventions

The argument order is `hnp` before `hmn`, matching the conventional mathematical notation for composition where the outer function appears to the left of the inner function (as in `g ∘ f`). The result is a fully bundled multiplicative homomorphism, not merely a function, so it carries along the proof that multiplication is preserved.

## Worked examples

- Claim: For the `MulHom` sending every natural number to itself (identity), composing it with any `MulHom` `f : M →ₙ* ℕ` on the right yields a map with the same underlying function as `f`.

- Claim: If `f : ℤ →ₙ* ℤ` is given by `f x = x * 2` (treated as a multiplicative endomorphism of the integers under multiplication) and `g : ℤ →ₙ* ℤ` is given by `g x = x * 3`, then `VTask.comp g f` sends `x` to `g (f x) = (x * 2) * 3`.

- Claim: Composition is associative: for `MulHom`s `f : M →ₙ* N`, `g : N →ₙ* P`, `h : P →ₙ* Q`, the underlying functions of `VTask.comp (VTask.comp h g) f` and `VTask.comp h (VTask.comp g f)` are equal pointwise.

## Boundaries

- The definition is total; it is valid for any types `M`, `N`, `P` each equipped with a multiplication, and for any pair of compatible multiplicative homomorphisms. No restrictions apply.
- When `hmn` is the identity homomorphism on `N`, `VTask.comp hnp hmn` has the same underlying function as `hnp`.
- When `hnp` is the identity homomorphism on `N`, `VTask.comp hnp hmn` has the same underlying function as `hmn`.
- Composition of two injective (or surjective) multiplicative homomorphisms remains injective (or surjective), though this is a property of the result, not enforced by the constructor.

## Not to be confused with

- `MonoidHom.comp`: the analogue for monoid homomorphisms (where the types additionally have a neutral element and the map preserves it); the present definition applies to bare magmas with no identity requirement.
- Function composition (`Function.comp`): operates on bare functions with no algebraic structure, producing a function rather than a bundled homomorphism.
- `MulEquiv.trans`: composition for multiplicative isomorphisms (bijective homomorphisms), which additionally tracks the inverse and bijectivity.