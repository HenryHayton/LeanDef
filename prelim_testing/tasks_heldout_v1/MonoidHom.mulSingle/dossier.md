## VTask.mulSingle

### Object

`VTask.mulSingle f i` is the canonical monoid homomorphism that embeds the monoid `f i` into the product monoid `∀ j, f j` by "including a single factor". Concretely, it sends an element `x : f i` to the function that equals `x` at index `i` and equals the identity (multiplicative one) at every other index. This is the monoid-homomorphism packaged version of the point-supported function `Pi.mulSingle`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mulSingle : {I : Type u} -> (f : I → Type v) -> [DecidableEq I] -> [(i : I) → MulOneClass (f i)] -> (i : I) -> f i →* (i : I) → f i
<!-- PINNED-SIGNATURE:END -->


`VTask.mulSingle : {I : Type u} -> (f : I → Type v) -> [DecidableEq I] -> [(i : I) → MulOneClass (f i)] -> (i : I) -> f i →* (i : I) → f i`

The first argument `f` is the family of types over the index type `I`, assigning to each index `i` the monoid `f i` whose elements are to be embedded. The `DecidableEq I` instance is needed to decide whether two indices are equal, which is required when defining a function that behaves differently at one distinguished index versus all others. The instance `(i : I) → MulOneClass (f i)` equips every fiber with the multiplicative-one-class structure needed for the product monoid. The argument `i : I` is the distinguished index at which the embedding is supported — the "slot" being included. The return type `f i →* (∀ i, f i)` is the resulting monoid homomorphism from the single fiber into the whole product.

### Conventions

There are no junk-value or out-of-domain conventions for this definition: it is a total construction and every argument has a canonical mathematical meaning with no degenerate cases.

### Worked examples

- Claim: For `f = fun (_ : Fin 3) => Multiplicative ℤ` and index `1 : Fin 3`, the homomorphism `VTask.mulSingle f 1` sends `x` to a function that is `x` at `1` and `1` (the identity) at `0` and `2`.

- Claim: The composite of `VTask.mulSingle f i` and the projection `fun g => g i` is the identity on `f i`, i.e., evaluating `VTask.mulSingle f i x` at index `i` returns `x`.

- Claim: For any index `j ≠ i`, evaluating `VTask.mulSingle f i x` at `j` returns the identity element `1 : f j`.

- Claim: `VTask.mulSingle f i` is a monoid homomorphism, meaning it preserves multiplication: `VTask.mulSingle f i (x * y) = VTask.mulSingle f i x * VTask.mulSingle f i y`.

### Boundaries

- When `I` is a type with exactly one element (a singleton type), `VTask.mulSingle f i` is essentially the identity isomorphism, since all indices are equal and the "other" indices do not exist.
- When `I` is an empty type, the product `∀ i, f i` is the trivial (terminal) type, and the homomorphism vacuously maps into it; however, `i : I` cannot be provided so the homomorphism cannot be instantiated.
- When `x = 1 : f i`, the result of `VTask.mulSingle f i x` is the everywhere-one function, coinciding with the identity of the product monoid.
- The image of `VTask.mulSingle f i` in `∀ j, f j` consists precisely of functions whose support is contained in `{i}` (i.e., functions that equal `1` at every index other than `i`).

### Not to be confused with

- `Pi.mulSingle i x` — the underlying bare function (not packaged as a monoid homomorphism); `VTask.mulSingle f i` is its `MonoidHom` wrapper.
- The additive analogue `AddMonoidHom.single` / `Pi.single` — the same construction for additive monoids, where `0` plays the role of `1`.
- `MonoidHom.Pi.eval i` (projection) — the homomorphism going in the *opposite* direction, projecting the product onto the `i`-th factor, rather than including the `i`-th factor into the product.