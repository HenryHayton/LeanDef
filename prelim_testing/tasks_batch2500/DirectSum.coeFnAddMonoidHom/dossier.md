## Object

`VTask.coeFnAddMonoidHom` is the canonical additive monoid homomorphism that casts (coerces) an element of a direct sum of abelian monoids into the corresponding pi-type (i.e., a dependent function). Concretely, it packages the natural "evaluation at each index" map as a structure-preserving map of additive monoids, witnessing that the inclusion of a direct sum into the full product space respects both the zero element and addition.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.coeFnAddMonoidHom : {ι : Type v} -> (β : ι → Type w) -> [(i : ι) → AddCommMonoid (β i)] -> (DirectSum ι fun i => β i) →+ (i : ι) → β i
<!-- PINNED-SIGNATURE:END -->


`VTask.coeFnAddMonoidHom : {ι : Type v} -> (β : ι → Type w) -> [(i : ι) → AddCommMonoid (β i)] -> (DirectSum ι fun i => β i) →+ (i : ι) → β i`

The first argument `ι` is the index type over which the direct sum and the pi type are formed. The second argument `β` is the family of types, one for each index in `ι`. The instance argument `[(i : ι) → AddCommMonoid (β i)]` provides the additive commutative monoid structure on each component `β i`. No further explicit arguments are needed: the result is the additive monoid homomorphism itself, carrying the coercion map as its underlying function together with proofs that it preserves zero and addition.

## Conventions

No junk-value or boundary conventions are declared for this definition: it is a total construction on well-typed inputs and every direct sum element is validly mapped to its pi-type representative without any special-cased behaviour.

## Worked examples

- Claim: Applying `VTask.coeFnAddMonoidHom` to the zero element of a direct sum yields the zero element of the pi type (i.e., the function constantly zero).

- Claim: For index type `Fin 2` with each `β i = ℕ`, if `x` and `y` are elements of `DirectSum (Fin 2) (fun _ => ℕ)`, then `VTask.coeFnAddMonoidHom (fun _ => ℕ) (x + y) = VTask.coeFnAddMonoidHom (fun _ => ℕ) x + VTask.coeFnAddMonoidHom (fun _ => ℕ) y`.

## Boundaries

- When `ι` is an empty type, the direct sum has only one element (zero), and the homomorphism sends it to the unique element of the empty-indexed pi type. The construction is still well-defined.
- When `ι` is infinite, a direct sum element is still finitely supported, but the image in the pi type may have entries at every index; the homomorphism faithfully records all of them, including the implicit zeros beyond the support.
- The homomorphism is injective: two distinct direct sum elements always map to distinct pi-type elements, because the coercion forgets nothing.

## Not to be confused with

- The *component projections* `DirectSum.component ι β i : DirectSum ι β →+ β i`, which extract a single component rather than the whole tuple.
- `DFinsupp.coeFnAddMonoidHom`, the analogous construction for finitely supported functions (`DFinsupp`) without the direct-sum wrapper; `VTask.coeFnAddMonoidHom` is built on top of this but lives at the `DirectSum` level.
- The bare coercion function `DirectSum → Π i, β i`, which has the same underlying map but is not packaged as an `AddMonoidHom` and therefore cannot be used in contexts that require the homomorphism structure.