## VTask.coprod

### Object

Given two multiplicative homomorphisms `f : M →ₙ* P` and `g : N →ₙ* P` whose common codomain `P` is a commutative semigroup, `VTask.coprod f g` is the unique multiplicative homomorphism `M × N →ₙ* P` that sends a pair `(m, n)` to `f(m) * g(n)`. It is the coproduct of `f` and `g` in the category of semigroups (taking advantage of commutativity to combine the two components multiplicatively).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.coprod : {M : Type u_3} -> {N : Type u_4} -> {P : Type u_5} -> [Mul M] -> [Mul N] -> [CommSemigroup P] -> (f : M →ₙ* P) -> (g : N →ₙ* P) -> M × N →ₙ* P
<!-- PINNED-SIGNATURE:END -->


`VTask.coprod : {M : Type u_3} -> {N : Type u_4} -> {P : Type u_5} -> [Mul M] -> [Mul N] -> [CommSemigroup P] -> (f : M →ₙ* P) -> (g : N →ₙ* P) -> M × N →ₙ* P`

The implicit type arguments `M`, `N`, and `P` are the domain components and the codomain, respectively. The `[Mul M]` and `[Mul N]` instances supply the binary operations on the two factor semigroups, while `[CommSemigroup P]` supplies the commutative multiplication on the codomain (commutativity is required to ensure the result is a homomorphism). The argument `f` is the homomorphism from the first factor `M` to `P`, and `g` is the homomorphism from the second factor `N` to `P`.

### Conventions

The codomain `P` is required to be a commutative semigroup; without commutativity the pointwise product of two homomorphisms need not be a homomorphism. When commutativity cannot be assumed, a non-commutative variant must be used instead.

### Worked examples

- Claim: For `f g : ℕ →ₙ* ℕ` both equal to the identity (under multiplication), `VTask.coprod f g (3, 5) = 3 * 5 = 15`.
  (Pointwise evaluation: the result sends `(m, n)` to `f m * g n`.)

- Claim: If `f : M →ₙ* P` and `g : N →ₙ* P`, then for any pair `p : M × N`, `VTask.coprod f g p = f p.1 * g p.2`.
  (This is the defining pointwise formula, confirmed by `coprod_apply`.)

- Claim: For a further homomorphism `h : P →ₙ* Q` into another commutative semigroup, post-composing distributes: `h.comp (VTask.coprod f g) = VTask.coprod (h.comp f) (h.comp g)`.
  (This is the universal-property statement `comp_coprod`, showing the construction is natural.)

### Boundaries

- The construction is total: it is defined for all `f` and `g` with matching commutative codomain `P`.
- When `M` or `N` has a trivial (one-element) semigroup, the corresponding component `f` or `g` contributes a trivial factor and the coproduct reduces to the other homomorphism composed with a projection.
- The commutativity hypothesis on `P` is essential: it is used to verify that the pointwise product of two homomorphisms is itself a homomorphism (multiplicativity of the product requires swapping terms, which uses commutativity).

### Not to be confused with

- `MulHom.noncommCoprod`: the analogue for non-commutative codomains, which requires extra conditions or a different form.
- `MulHom.prod`: the homomorphism `M →ₙ* N × P` that pairs two maps into a product, as opposed to combining two maps *from* a product.
- `MulHom.prodMap`: the map `M × N →ₙ* P × Q` induced componentwise from `f : M →ₙ* P` and `g : N →ₙ* Q` (different codomains, no merging).
