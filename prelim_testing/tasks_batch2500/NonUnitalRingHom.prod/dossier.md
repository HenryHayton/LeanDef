## VTask.prod

### Object

Given two non-unital ring homomorphisms `f : R →ₙ+* S` and `g : R →ₙ+* T` sharing the same source ring `R`, `VTask.prod f g` is their **diagonal product**: the unique non-unital ring homomorphism from `R` into the product ring `S × T` that sends every element `x : R` to the pair `(f x, g x)`. It is the canonical map induced by the universal property of the product, making the two coordinate projections recover `f` and `g` respectively.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {R : Type u_1} -> {S : Type u_3} -> {T : Type u_5} -> [NonUnitalNonAssocSemiring R] -> [NonUnitalNonAssocSemiring S] -> [NonUnitalNonAssocSemiring T] -> (f : R →ₙ+* S) -> (g : R →ₙ+* T) -> R →ₙ+* S × T
<!-- PINNED-SIGNATURE:END -->


`{R : Type u_1} -> {S : Type u_3} -> {T : Type u_5} -> [NonUnitalNonAssocSemiring R] -> [NonUnitalNonAssocSemiring S] -> [NonUnitalNonAssocSemiring T] -> (f : R →ₙ+* S) -> (g : R →ₙ+* T) -> R →ₙ+* S × T`

The three universe-polymorphic type arguments `R`, `S`, `T` are the source ring and the two target rings, all equipped with `NonUnitalNonAssocSemiring` instances (supplied as instance arguments). The explicit argument `f` is the first component homomorphism, mapping `R` to `S`; the explicit argument `g` is the second component homomorphism, mapping `R` to `T`. The result is a single non-unital ring homomorphism from `R` to the product type `S × T`.

### Conventions

No junk-value or edge conventions are declared for this definition: it is a total constructor taking two well-typed non-unital ring homomorphisms and always produces a valid non-unital ring homomorphism; there are no degenerate inputs or out-of-domain cases.

### Worked examples

- Claim: For any `x : R`, `(VTask.prod f g) x = (f x, g x)` — the result evaluates pointwise to the pair of the two component values.

- Claim: Composing the first projection `fst` with `VTask.prod f g` recovers `f` — that is, `(fst S T).comp (VTask.prod f g) = f`.

- Claim: Composing the second projection `snd` with `VTask.prod f g` recovers `g` — that is, `(snd S T).comp (VTask.prod f g) = g`.

- Claim: The product construction is unique: for any `h : R →ₙ+* S × T`, pairing the compositions with the two projections gives back `h` — that is, `VTask.prod ((fst S T).comp h) ((snd S T).comp h) = h`.

### Boundaries

- When `S = T`, both `f` and `g` may be the same homomorphism; `VTask.prod f f` sends every `x` to the diagonal element `(f x, f x)`.
- When `R`, `S`, or `T` is the trivial (zero) ring, the result is still well-formed, and the only map is the zero homomorphism sending everything to `(0, 0)`.
- The definition requires only `NonUnitalNonAssocSemiring` structure — no unit, no associativity, no commutativity — so it applies in very general algebraic settings.
- The output type `S × T` carries the componentwise ring structure, and `VTask.prod f g` respects both addition and multiplication componentwise precisely because `f` and `g` each do.

### Not to be confused with

- `NonUnitalRingHom.prodMap`: takes *two* homomorphisms `f : R →ₙ+* S` and `g : R' →ₙ+* S'` with *different* source rings and acts on `R × R'`, lifting them componentwise; unlike `VTask.prod`, it does not share a single source.
- `NonUnitalRingHom.fst` / `NonUnitalRingHom.snd`: these are the *projection* homomorphisms from `S × T` to `S` or `T`, which are the left inverses of `VTask.prod`, not the construction itself.
- `Pi.ringHom` (or the n-ary product variant): generalises the binary product to an arbitrary family of target rings, whereas `VTask.prod` is specifically the binary case.
