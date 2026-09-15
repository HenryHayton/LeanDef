## Object

`VTask.coeFnAddMonoidHom` is the canonical additive monoid homomorphism that "forgets" the finite-support constraint on a `DFinsupp` (a finitely-supported dependent function) and regards it simply as an ordinary dependent function (a `Pi` type). Concretely, it packages the coercion `(Π₀ i, β i) → (∀ i, β i)` into an `AddMonoidHom`, witnessing that this coercion respects addition and sends the zero `DFinsupp` to the zero function.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.coeFnAddMonoidHom : {ι : Type u} -> {β : ι → Type v} -> [(i : ι) → AddZeroClass (β i)] -> (Π₀ (i : ι), β i) →+ (i : ι) → β i
<!-- PINNED-SIGNATURE:END -->


`{ι : Type u} -> {β : ι → Type v} -> [(i : ι) → AddZeroClass (β i)] -> (Π₀ (i : ι), β i) →+ (i : ι) → β i`

The implicit type `ι` is the index type whose elements label the components of the dependent function. The implicit family `β` assigns to each index `i` the type of the value at that position. The instance argument `(i : ι) → AddZeroClass (β i)` supplies each fibre with the additive zero-class structure needed to define what "zero" and "addition" mean componentwise; this is required to form an `AddMonoidHom`. The definition itself takes no further explicit arguments: it produces the `AddMonoidHom` directly.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is total and well-defined for any index type `ι`, any dependent family `β`, and any choice of `AddZeroClass` instances on the fibres.

## Worked examples

- Claim: Applying `VTask.coeFnAddMonoidHom` to the zero `DFinsupp` yields the zero function.

- Claim: Applying `VTask.coeFnAddMonoidHom` to the sum of two `DFinsupp` elements `f` and `g` equals the pointwise sum of the functions `VTask.coeFnAddMonoidHom f` and `VTask.coeFnAddMonoidHom g`.

- Claim: `VTask.coeFnAddMonoidHom` is injective, since two `DFinsupp` functions that agree everywhere as ordinary dependent functions are equal.

## Boundaries

- When `ι` is empty, both `Π₀ i, β i` and `∀ i, β i` are singletons (the unique empty function), so the homomorphism is trivially an isomorphism.
- When all `β i` are trivial (`β i = Unit` with trivial `AddZeroClass`), the homomorphism again reduces to a trivial map between one-element types.
- The map is always injective (the coercion from `DFinsupp` to `Pi` is injective), though `VTask.coeFnAddMonoidHom` is not generally surjective: not every `∀ i, β i` has finite support.
- There is no finiteness requirement on `ι` itself; the definition is equally valid for infinite index types.

## Not to be confused with

- `DFinsupp.equivFunOnFintype`: an equivalence (not merely a homomorphism) between `DFinsupp` and `Pi` valid only when `ι` is a `Fintype`.
- The bare coercion `⇑ : (Π₀ i, β i) → ∀ i, β i`: this is the same underlying function, but `VTask.coeFnAddMonoidHom` additionally carries the algebraic `AddMonoidHom` structure.
- `Finsupp.toFun` or `Finsupp.lcoeFun`: analogous constructions for `Finsupp` (finitely-supported functions to a single type), not the dependent `DFinsupp` setting.