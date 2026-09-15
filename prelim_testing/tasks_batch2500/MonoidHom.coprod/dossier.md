## Object

`VTask.coprod f g` is the **coproduct** of two monoid homomorphisms `f : M →* P` and `g : N →* P` into a common commutative codomain. It is the unique monoid homomorphism `M × N →* P` whose value on a pair `(m, n)` is the product `f(m) · g(n)`. Because `P` is commutative, this pointwise product is again a monoid homomorphism, giving the universal "copairing" map on the direct product.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.coprod : {M : Type u_3} -> {N : Type u_4} -> {P : Type u_5} -> [MulOneClass M] -> [MulOneClass N] -> [CommMonoid P] -> (f : M →* P) -> (g : N →* P) -> M × N →* P
<!-- PINNED-SIGNATURE:END -->


`VTask.coprod : {M : Type u_3} -> {N : Type u_4} -> {P : Type u_5} -> [MulOneClass M] -> [MulOneClass N] -> [CommMonoid P] -> (f : M →* P) -> (g : N →* P) -> M × N →* P`

The implicit types `M` and `N` are the two source monoids, and `P` is the (commutative) target monoid. The instance arguments supply the necessary algebraic structures on `M`, `N`, and `P`. The explicit argument `f` is the monoid homomorphism from `M` to `P`; `g` is the monoid homomorphism from `N` to `P`. The result is a monoid homomorphism from the direct product `M × N` to `P`.

## Conventions

No junk-value or edge conventions are declared for this definition: it is a total construction on well-typed inputs, and every input satisfying the stated type class constraints yields a well-defined monoid homomorphism with no special boundary treatment.

## Worked examples

- Claim: For any commutative monoid `P` with homomorphisms `f : M →* P` and `g : N →* P`, evaluating `VTask.coprod f g` at a pair `(m, n)` gives `f m * g n`.

- Claim: The composition of `VTask.coprod f g` with the left inclusion `inl : M →* M × N` recovers `f`.
  That is, `(VTask.coprod f g).comp (MonoidHom.inl M N) = f`.

- Claim: The composition of `VTask.coprod f g` with the right inclusion `inr : N →* M × N` recovers `g`.
  That is, `(VTask.coprod f g).comp (MonoidHom.inr M N) = g`.

- Claim: For the trivial case where both `f` and `g` are the identity on a commutative monoid `P`, `VTask.coprod (MonoidHom.id P) (MonoidHom.id P)` sends `(p₁, p₂)` to `p₁ * p₂`.

- Claim: Given any monoid homomorphism `h : P →* Q` (with `Q` a commutative monoid), postcomposing distributes over coprod: `h.comp (VTask.coprod f g) = VTask.coprod (h.comp f) (h.comp g)`.

## Boundaries

- When `f` is the trivial (constant-one) homomorphism, `VTask.coprod f g (m, n) = g n`; the `M`-component contributes `1` and is absorbed.
- When `g` is the trivial homomorphism, `VTask.coprod f g (m, n) = f m`.
- When `M` or `N` is the trivial monoid (containing only the identity), the coprod reduces to essentially a single homomorphism from the remaining factor.
- The commutativity of `P` is essential: without it the pointwise product of two homomorphisms need not be a homomorphism. For the non-commutative case a different construction (`noncommCoprod`) is needed.
- The uniqueness theorem states that every homomorphism `h : M × N →* P` equals `VTask.coprod (h.comp inl) (h.comp inr)`, so the coprod construction covers all such maps.

## Not to be confused with

- `MonoidHom.prod` (or `VTask.prod`): pairs two homomorphisms with *different* codomains into `M →* P × Q`, the categorical product map — this goes in the opposite direction to `coprod`.
- `AddMonoidHom.coprod`: the additive analogue, where the formula reads `f p.1 + g p.2` instead of `f p.1 * g p.2`; structurally identical but for additive monoids.
- `MonoidHom.noncommCoprod`: the generalization to non-commutative codomains, which requires additional hypotheses (commuting images) and is distinct from the simple pointwise-product construction here.