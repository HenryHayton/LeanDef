## Object

`VTask.pi` constructs a single monoid homomorphism from `γ` into the product type `(i : I) → f i` from a family of monoid homomorphisms `g i : γ →* f i`, one for each index `i : I`. The resulting homomorphism sends each element `x : γ` to the function `i ↦ g i x`, i.e., it evaluates every component homomorphism at `x` simultaneously.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.pi : {I : Type u} -> {f : I → Type v} -> [(i : I) → MulOneClass (f i)] -> {γ : Type w} -> [MulOneClass γ] -> (g : (i : I) → γ →* f i) -> γ →* (i : I) → f i
<!-- PINNED-SIGNATURE:END -->


`{I : Type u} -> {f : I → Type v} -> [(i : I) → MulOneClass (f i)] -> {γ : Type w} -> [MulOneClass γ] -> (g : (i : I) → γ →* f i) -> γ →* (i : I) → f i`

- `I` is the index type parametrising the product.
- `f` is the family of types indexed by `I`; each `f i` must carry a `MulOneClass` structure (provided by the instance argument).
- `γ` is the source type, which must also carry a `MulOneClass` structure (provided by the instance argument).
- `g` is the family of monoid homomorphisms, one per index, each mapping `γ` into the corresponding component `f i`.

The result is a monoid homomorphism from `γ` into the product `(i : I) → f i`.

## Conventions

There are no junk-value or edge conventions to declare: the definition is total and well-defined for any index type `I`, any family `f`, and any family of homomorphisms `g`, including the case when `I` is empty, in which case the product type is the terminal object and the homomorphism is the unique map into it.

## Worked examples

- Claim: For the family `g` consisting of the identity homomorphism on `ℕ →* ℕ` repeated at each index in `Fin 1`, applying `VTask.pi g` to `3` yields the constant function with value `3`.

- Claim: The evaluation of `VTask.pi g x` at index `i` equals `g i x` for all `x : γ` and `i : I`.

- Claim: `VTask.pi g` maps the identity element of `γ` to the identity element of `(i : I) → f i`, i.e., the function sending every `i` to the identity of `f i`.

- Claim: If every component homomorphism `g i` is injective and `I` is nonempty, then `VTask.pi g` is injective.

## Boundaries

- **Empty index type**: When `I` is empty, `(i : I) → f i` is the terminal (trivial) monoid. The resulting homomorphism is the unique map from `γ` to it and is trivially a monoid homomorphism.
- **Singleton index type**: With a single index, `VTask.pi g` is essentially just `g` viewed as a map into the one-element product, which is naturally isomorphic to `f` of the single element.
- **Injectivity boundary**: Injectivity of `VTask.pi g` requires `I` to be nonempty *and* all component maps `g i` to be injective; if `I` is empty, the map cannot be injective (unless `γ` itself is trivial).
- **Surjectivity**: `VTask.pi g` is not in general surjective even when all `g i` are, since surjectivity into a product is a stronger condition.

## Not to be confused with

- `MonoidHom.pi_ext`: a theorem about *uniqueness* of homomorphisms out of a product, not the construction of a homomorphism into a product.
- `Pi.evalMonoidHom`: the projection homomorphism `((i : I) → f i) →* f j` picking out a single component from the product; this is a map *out of* the product, dual to `VTask.pi`.
- `MonoidHom.prod` (for two factors): the special case of `VTask.pi` for `I = Fin 2`, constructing a homomorphism into a binary product `f 0 × f 1`; `VTask.pi` generalises this to arbitrary index types.