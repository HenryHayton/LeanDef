## VTask.toAddMonoidEnd

### Object

Given a monoid `M` acting on an additive monoid `A` via a distributive multiplicative action, `VTask.toAddMonoidEnd M A` is the canonical **monoid homomorphism** from `M` into the monoid of additive monoid endomorphisms of `A` (written `AddMonoid.End A`). Concretely, it sends each element `m : M` to the map `a ↦ m • a`, which is an additive monoid homomorphism from `A` to itself; and the assignment `m ↦ (a ↦ m • a)` itself respects multiplication (i.e., acting by `m * n` equals acting first by `n` then by `m`).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toAddMonoidEnd : (M : Type u_1) -> (A : Type u_7) -> [Monoid M] -> [AddMonoid A] -> [DistribMulAction M A] -> M →* AddMonoid.End A
<!-- PINNED-SIGNATURE:END -->


`VTask.toAddMonoidEnd : (M : Type u_1) -> (A : Type u_7) -> [Monoid M] -> [AddMonoid A] -> [DistribMulAction M A] -> M →* AddMonoid.End A`

The first explicit argument `M` is the acting monoid whose elements are being represented as endomorphisms. The second explicit argument `A` is the additive monoid being acted upon. The three instance arguments supply, respectively, the monoid structure on `M`, the additive monoid structure on `A`, and the distributive multiplicative action of `M` on `A` that ties them together.

### Conventions

There are no junk-value or out-of-domain conventions to declare: the definition is total and well-defined for every monoid `M`, additive monoid `A`, and distributive multiplicative action of `M` on `A`.

### Worked examples

- Claim: For any `m : M`, evaluating `VTask.toAddMonoidEnd M A` at `m` and then applying the resulting endomorphism to `a : A` yields `m • a`.

- Claim: `VTask.toAddMonoidEnd M A 1` equals the identity endomorphism on `A`, because the identity element of `M` acts trivially (by `one_smul`).

- Claim: For `m n : M`, `VTask.toAddMonoidEnd M A (m * n)` equals the composition `VTask.toAddMonoidEnd M A m ∘ VTask.toAddMonoidEnd M A n` as additive monoid endomorphisms of `A`, reflecting that `(m * n) • a = m • (n • a)`.

- Claim: The map `VTask.toAddMonoidEnd M A` is a monoid homomorphism, i.e., it preserves the monoid structure: the image of `1` is the identity and the image of a product is the composite of images.

### Boundaries

- When `M` is the trivial one-element monoid, the resulting monoid homomorphism maps the unique element to the identity endomorphism of `A`.
- When `A` is the trivial zero additive monoid, every element of `M` maps to the unique (zero) endomorphism, so the homomorphism is trivially defined but well-formed.
- The construction works even if the action is not faithful; the homomorphism need not be injective in general.
- The distributivity condition (that `m • (a + b) = m • a + m • b` and `m • 0 = 0`) is essential: it is exactly what makes each `m`-action an additive monoid homomorphism.

### Not to be confused with

- `DistribSMul.toAddMonoidHom A m` — this is the *individual* additive monoid homomorphism `A →+ A` corresponding to a single element `m`; `VTask.toAddMonoidEnd` packages all of these together into a single monoid homomorphism `M →* AddMonoid.End A`.
- `MulAction.toPermHom` — the analogous construction for group actions on sets, sending group elements to permutations rather than additive monoid endomorphisms.
- `Module.toLinearMap` / scalar multiplication viewed as a linear map — a more structured analogue that requires additionally a ring/module structure rather than just a monoid/additive-monoid structure.