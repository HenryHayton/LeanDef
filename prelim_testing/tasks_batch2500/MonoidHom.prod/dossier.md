## VTask.prod

### Object

Given two monoid homomorphisms `f : M →* N` and `g : M →* P` from the same source monoid `M`, `VTask.prod f g` is the monoid homomorphism `M →* N × P` that sends each element `x : M` to the pair `(f x, g x)`. It is the universal "diagonal" or "pairing" morphism into a product monoid, induced by two maps out of the same source.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {M : Type u_3} -> {N : Type u_4} -> {P : Type u_5} -> [MulOneClass M] -> [MulOneClass N] -> [MulOneClass P] -> (f : M →* N) -> (g : M →* P) -> M →* N × P
<!-- PINNED-SIGNATURE:END -->


`VTask.prod : {M : Type u_3} -> {N : Type u_4} -> {P : Type u_5} -> [MulOneClass M] -> [MulOneClass N] -> [MulOneClass P] -> (f : M →* N) -> (g : M →* P) -> M →* N × P`

The type parameters `M`, `N`, `P` are the source and two target types, each equipped with a `MulOneClass` structure (a type with a distinguished identity element and a multiplication). The argument `f` is the first component homomorphism, mapping `M` into `N`; the argument `g` is the second component homomorphism, mapping `M` into `P`. The result is a single monoid homomorphism from `M` into the product `N × P`.

### Conventions

No junk-value or edge conventions are declared for this definition: it is a total construction on well-formed monoid homomorphisms with no special treatment of degenerate inputs.

### Worked examples

- Claim: For any element `x : M`, applying `VTask.prod f g` yields the pair `(f x, g x)` — concretely, if `M = N = P = ℤ` (under multiplication), `f = id`, `g = id`, then `(VTask.prod f g) x = (x, x)`.

- Claim: `VTask.prod f g` maps the identity of `M` to `(1, 1)` in `N × P`, since `f 1 = 1` and `g 1 = 1` by the homomorphism property.

- Claim: For `f : M →* N` and `g : M →* P`, composing the first projection `Prod.fst` with `VTask.prod f g` recovers `f`, and composing the second projection `Prod.snd` recovers `g`.

- Claim: The underlying function of `VTask.prod f g` equals `Function.prod f g`, i.e., the pointwise pairing of `f` and `g`.

### Boundaries

- If either `f` or `g` is the trivial (constant-one) homomorphism, `VTask.prod f g` maps every element to a pair whose corresponding component is always `1`.
- When `N = P` and `f = g`, the result is the diagonal homomorphism `x ↦ (f x, f x)`.
- The construction is valid for any `MulOneClass` types; it does not require groups or commutativity.
- The product monoid `N × P` is given the componentwise multiplication and identity, which is the standard Mathlib instance.

### Not to be confused with

- `MonoidHom.prodMap` (also written `f.prodMap g`): takes `f : M →* N` and `g : M' →* N'` with *different* sources and produces `M × M' →* N × N'`, acting componentwise — a different morphism than the diagonal pairing.
- `MonoidHom.fst` / `MonoidHom.snd`: these are the *projection* homomorphisms `M × N →* M` and `M × N →* N`, not a construction from two maps.
- `Pi.monoidHom` / `MonoidHom.pi`: the analogous construction for arbitrary (possibly infinite) index families of targets, rather than a binary product.
