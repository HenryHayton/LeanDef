## Object

`VTask.DirectSum ι β` is the **direct sum** of a family of additive commutative monoids indexed by a type `ι`. Concretely, an element of the direct sum is a function from `ι` to the disjoint union of the family members `β i` that is **finitely supported**: all but finitely many index values map to the identity element (zero) of the corresponding monoid. This is the coproduct construction in the category of additive commutative monoids, and it generalises the finite direct sum of abelian groups to arbitrary (possibly infinite) index types.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.DirectSum : (ι : Type v) -> (β : ι → Type w) -> [(i : ι) → AddCommMonoid (β i)] -> Type (max w v)
<!-- PINNED-SIGNATURE:END -->


VTask.DirectSum : (ι : Type v) -> (β : ι → Type w) -> [(i : ι) → AddCommMonoid (β i)] -> Type (max w v)

The first argument `ι` is the **index type** that labels the summands. The second argument `β` is the **family of carrier types**, one additive commutative monoid per index. The third argument is a typeclass instance that supplies the `AddCommMonoid` structure on each fibre `β i`; it is typically inferred automatically. The resulting type lives in `Type (max w v)`, the universe large enough to contain the finitely-supported functions from `ι` into the disjoint union of the `β i`.

## Conventions

An element of `VTask.DirectSum ι β` is treated as zero at every index not explicitly assigned a nonzero value; in particular, the type is inhabited by the zero element for any choice of `ι` and `β`. There are no junk values declared: every term of this type is a legitimate finitely-supported family of elements, and the type itself is always well-formed for any `ι` and any `β` satisfying the monoid constraint.

## Worked examples

- Claim: `VTask.DirectSum (Fin 2) (fun _ => ℕ)` is a type that is inhabited (it contains at least the zero element).

- Claim: The zero element of `VTask.DirectSum ι β`, for any `ι` and family `β`, has the property that evaluating it at any index `i` yields `0 : β i`.

- Claim: For `ι = Fin 3` and `β i = ℤ` for all `i`, the direct sum `VTask.DirectSum (Fin 3) (fun _ => ℤ)` carries an `AddCommMonoid` instance, and hence admits addition and a zero.

- Claim: When `ι` is a `Fintype`, `VTask.DirectSum ι β` is naturally isomorphic (as additive commutative monoids) to the ordinary product `Π i, β i`.

## Boundaries

- **Empty index type** (`ι = Empty` or `ι = Fin 0`): The direct sum is a one-element type — its only element is the zero function. This is consistent with the direct sum of an empty family being the trivial monoid.
- **Singleton index type** (`ι = Unit`): The direct sum is isomorphic to `β ()` itself, since finite support is automatic for a one-element domain.
- **Infinite index type**: The type is still well-formed. Elements must be finitely supported, so they differ from `0` at only finitely many indices. The underlying type is **not** the full product `Π i, β i` in this case.
- **Trivial summands** (each `β i` is the zero monoid): Every element is zero, and the direct sum is again a one-element type.

## Not to be confused with

- **`Π i, β i` (the dependent product / Pi type)**: This holds *all* functions from `ι` to the family, with no finiteness restriction; the direct sum is the finitely-supported submonoid of this product.
- **`DirectProduct`** or finite products of groups: Those require `ι` to be finite and do not impose a finite-support condition separately; for finite `ι` the notions coincide, but for infinite `ι` they diverge.
- **`Dfinsupp ι β` (dependent finitely supported functions)**: This is the underlying representation type. `VTask.DirectSum ι β` is definitionally equal to `Π₀ i, β i`, but it is presented as the algebraic direct sum with its own API and notation, not as a general finitely-supported function type.