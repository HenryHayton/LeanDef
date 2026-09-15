## VTask.prod

### Object

Given two multiplicative semigroup homomorphisms `f : M →ₙ* N` and `g : M →ₙ* P` from a common source semigroup `M`, `VTask.prod f g` is the unique multiplicative semigroup homomorphism `M →ₙ* N × P` that sends every element `x : M` to the pair `(f x, g x)`. It is the canonical diagonal or pairing map into a direct product of semigroups.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {M : Type u_3} -> {N : Type u_4} -> {P : Type u_5} -> [Mul M] -> [Mul N] -> [Mul P] -> (f : M →ₙ* N) -> (g : M →ₙ* P) -> M →ₙ* N × P
<!-- PINNED-SIGNATURE:END -->


`VTask.prod : {M : Type u_3} -> {N : Type u_4} -> {P : Type u_5} -> [Mul M] -> [Mul N] -> [Mul P] -> (f : M →ₙ* N) -> (g : M →ₙ* P) -> M →ₙ* N × P`

The implicit type arguments `M`, `N`, and `P` are the source semigroup and two target semigroups, respectively. The instance arguments supply the multiplication operations on each type. The argument `f` is the first component homomorphism, mapping `M` into `N`; the argument `g` is the second component homomorphism, mapping `M` into `P`. The result is the paired homomorphism into the product `N × P`.

### Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total construction with no edge cases requiring special treatment.

### Worked examples

- Claim: For any semigroup homomorphisms `f : M →ₙ* N` and `g : M →ₙ* P`, applying `VTask.prod f g` to any element `x` yields the pair `(f x, g x)`.

- Claim: The first projection of `VTask.prod f g`, composed with the canonical projection `fst`, recovers `f`; that is, `(fst N P).comp (VTask.prod f g) = f`.

- Claim: The second projection of `VTask.prod f g`, composed with the canonical projection `snd`, recovers `g`; that is, `(snd N P).comp (VTask.prod f g) = g`.

- Claim: The pairing construction is unique: given any `h : M →ₙ* N × P`, the homomorphism `VTask.prod ((fst N P).comp h) ((snd N P).comp h)` equals `h`.

### Boundaries

The construction is fully general: `M`, `N`, and `P` need only be types equipped with a multiplication (no associativity, identity, or commutativity is required). The product type `N × P` is given the componentwise multiplication. When `f` or `g` is the trivial map (if such exists), `VTask.prod f g` maps every element to a pair whose first or second component is trivial, respectively.

### Not to be confused with

- `MulHom.coprod`: Takes two homomorphisms `f : M →ₙ* P` and `g : N →ₙ* P` with a *common target* and combines them into `M × N →ₙ* P`, which is the opposite direction from `VTask.prod`.
- `MulHom.prodMap`: Lifts a pair of homomorphisms `f : M →ₙ* N`, `g : M' →ₙ* N'` to a homomorphism `M × M' →ₙ* N × N'` on product types, rather than diagonally pairing two maps with the same source.
- `Function.prod f g`: The underlying function `M → N × P` sending `x` to `(f x, g x)`, which is not a bundled semigroup homomorphism and carries no `map_mul` proof.