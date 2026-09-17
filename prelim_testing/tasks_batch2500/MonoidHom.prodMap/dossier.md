## Object

`VTask.prodMap f g` is the monoid homomorphism from the product monoid `M × N` to the product monoid `M' × N'` that applies `f` to the first component and `g` to the second component simultaneously. Concretely, it sends a pair `(m, n)` to the pair `(f m, g n)`. It is the monoid-homomorphism incarnation of the set-theoretic operation `Prod.map`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prodMap : {M : Type u_3} -> {N : Type u_4} -> [MulOneClass M] -> [MulOneClass N] -> {M' : Type u_6} -> {N' : Type u_7} -> [MulOneClass M'] -> [MulOneClass N'] -> (f : M →* M') -> (g : N →* N') -> M × N →* M' × N'
<!-- PINNED-SIGNATURE:END -->


`{M : Type u_3} -> {N : Type u_4} -> [MulOneClass M] -> [MulOneClass N] -> {M' : Type u_6} -> {N' : Type u_7} -> [MulOneClass M'] -> [MulOneClass N'] -> (f : M →* M') -> (g : N →* N') -> M × N →* M' × N'`

The type parameters `M`, `N`, `M'`, `N'` are the four monoid types involved, each required to carry a `MulOneClass` instance (the minimal structure needed for monoid homomorphisms). The argument `f` is a monoid homomorphism from `M` to `M'`, acting on the first component of the product. The argument `g` is a monoid homomorphism from `N` to `N'`, acting on the second component of the product. The result is a monoid homomorphism from `M × N` to `M' × N'`.

## Conventions

No special junk-value or boundary conventions are declared for this definition: it is a total construction that is well-defined for all valid inputs without any degenerate edge cases requiring special treatment.

## Worked examples

- Claim: `VTask.prodMap f g` applied to a pair `(m, n)` yields `(f m, g n)` — that is, `(VTask.prodMap f g) (m, n) = (f m, g n)` for any monoid homomorphisms `f` and `g`.

- Claim: Taking `f` and `g` both to be the identity monoid homomorphism on a monoid `M`, `VTask.prodMap (MonoidHom.id M) (MonoidHom.id N)` is the identity on `M × N`, meaning it sends every pair `(m, n)` to `(m, n)` unchanged.

- Claim: `VTask.prodMap f g` preserves the identity: `(VTask.prodMap f g) (1, 1) = (1, 1)`, since both `f 1 = 1` and `g 1 = 1` by the homomorphism property.

- Claim: `VTask.prodMap f g` preserves multiplication: for pairs `(m₁, n₁)` and `(m₂, n₂)`, `(VTask.prodMap f g) ((m₁, n₁) * (m₂, n₂)) = (VTask.prodMap f g) (m₁, n₁) * (VTask.prodMap f g) (m₂, n₂)`, because the product monoid multiplies componentwise and `f`, `g` each preserve multiplication.

## Boundaries

- When `f` is the trivial (constant-one) homomorphism and `g` is arbitrary, `VTask.prodMap f g` sends every pair `(m, n)` to `(1, g n)`, collapsing the first component.
- When `M = M'` and `N = N'` and both `f` and `g` are the identity, the result is the identity homomorphism on `M × N`.
- The construction is defined for any `MulOneClass` instances, including groups, abelian groups, and trivial one-element monoids, without any restriction.
- If either monoid is the trivial monoid (with only one element), the corresponding component of the output is always the identity element.

## Not to be confused with

- `MonoidHom.fst` / `MonoidHom.snd`: these are the projection homomorphisms from `M × N` to `M` or `N`, not a map between two different product monoids.
- `MonoidHom.prod`: this takes two homomorphisms with a *common domain* `M →* N` and `M →* P` and produces a single homomorphism `M →* N × P` into a product; `VTask.prodMap` instead takes homomorphisms on each factor separately.
- `Prod.map` (as a plain function): the set-theoretic version which applies two functions componentwise to a product type, with no monoid or homomorphism structure guaranteed or tracked.