## Object

`VTask.prod f g` is the **diagonal product** ring homomorphism from a ring `R` into the product ring `S × T`. Given two ring homomorphisms `f : R →+* S` and `g : R →+* T` sharing the same source ring `R`, the combined map sends each element `x : R` to the pair `(f x, g x)` in `S × T`. This construction is the ring-theoretic analogue of the universal property of the binary product: a ring homomorphism into a product is the same data as a pair of ring homomorphisms into each factor.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.prod : {R : Type u_1} -> {S : Type u_3} -> {T : Type u_5} -> [NonAssocSemiring R] -> [NonAssocSemiring S] -> [NonAssocSemiring T] -> (f : R →+* S) -> (g : R →+* T) -> R →+* S × T
<!-- PINNED-SIGNATURE:END -->


`VTask.prod : {R : Type u_1} -> {S : Type u_3} -> {T : Type u_5} -> [NonAssocSemiring R] -> [NonAssocSemiring S] -> [NonAssocSemiring T] -> (f : R →+* S) -> (g : R →+* T) -> R →+* S × T`

The universe-polymorphic type variables `R`, `S`, `T` are the underlying types of the three (non-associative) semirings involved, inferred implicitly. The three `NonAssocSemiring` instance arguments equip `R`, `S`, and `T` with their semiring structures. The first explicit argument `f` is the ring homomorphism from `R` to the first factor `S`; the second explicit argument `g` is the ring homomorphism from `R` to the second factor `T`. The result is a ring homomorphism from `R` into the product `S × T`.

## Conventions

There are no junk-value or boundary conventions to declare: the definition is a total construction on two ring homomorphisms with no degenerate or edge cases in its domain.

## Worked examples

- Claim: For the identity ring homomorphism `id : ℤ →+* ℤ` and the zero homomorphism `0 : ℤ →+* ℤ`, the product sends `3` to `(3, 0)`.

- Claim: The composite of the first-projection ring homomorphism `fst S T` with `VTask.prod f g` equals `f`, i.e., projecting the first component of `VTask.prod f g` recovers `f`.

- Claim: The composite of the second-projection ring homomorphism `snd S T` with `VTask.prod f g` equals `g`, i.e., projecting the second component of `VTask.prod f g` recovers `g`.

- Claim: Every ring homomorphism `h : R →+* S × T` is uniquely recovered as `VTask.prod ((fst S T).comp h) ((snd S T).comp h)`, expressing the universal property of the product.

## Boundaries

- When `S = T` and `f = g`, the result is the diagonal homomorphism `R →+* S × S` sending every `x` to `(f x, f x)`; no special casing is needed, the construction handles this uniformly.
- When either `f` or `g` is the zero ring homomorphism (mapping everything to `0`), the product homomorphism still produces well-formed output with that component identically `0`.
- The construction works for `NonAssocSemiring`, which is weaker than a full ring; in particular neither associativity of multiplication nor additive inverses are required.
- If `R` is the zero ring (the trivial ring with one element `0 = 1`), then `VTask.prod f g` is also a ring homomorphism from that trivial ring, and its output is always `(0, 0) = (1, 1)` in the product.

## Not to be confused with

- `RingHom.prodMap`: maps `R × S →+* T × U` from pairs of homomorphisms `R →+* T` and `S →+* U`; it acts on both components of the *source* product, whereas `VTask.prod` fans out from a single source into a product target.
- `RingHom.fst` / `RingHom.snd`: these are the *projection* ring homomorphisms `S × T →+* S` and `S × T →+* T` going *out of* a product, the duals of `VTask.prod`.
- `Pi.ringHom`: the analogous construction for an arbitrary (possibly infinite) family of rings, generalising `VTask.prod` from a binary product to an indexed product.