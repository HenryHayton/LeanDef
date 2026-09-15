## Object

`VTask.sumFinsuppAddEquivProdFinsupp` is the canonical additive isomorphism that splits a finitely-supported function on a disjoint-union type `α ⊕ β` into a pair of finitely-supported functions, one on `α` and one on `β`. Concretely, a function `f : α ⊕ β →₀ M` is sent to the pair `(f ∘ Sum.inl, f ∘ Sum.inr)`, and the inverse reassembles a pair `(g, h)` into the single function that is `g` on `α`-tagged inputs and `h` on `β`-tagged inputs. The isomorphism respects the additive monoid structure: pointwise addition of finsupp functions on `α ⊕ β` corresponds exactly to componentwise addition of the pair.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sumFinsuppAddEquivProdFinsupp : {M : Type u_5} -> [AddMonoid M] -> {α : Type u_12} -> {β : Type u_13} -> (α ⊕ β →₀ M) ≃+ (α →₀ M) × (β →₀ M)
<!-- PINNED-SIGNATURE:END -->


`VTask.sumFinsuppAddEquivProdFinsupp : {M : Type u_5} -> [AddMonoid M] -> {α : Type u_12} -> {β : Type u_13} -> (α ⊕ β →₀ M) ≃+ (α →₀ M) × (β →₀ M)`

- `M` is the value type, the codomain of all finitely-supported functions; it must carry an `AddMonoid` structure so that addition is defined.
- `α` and `β` are the two index types whose disjoint union `α ⊕ β` forms the domain of the source finsupp.
- No explicit value arguments are needed; the result is itself a bundled additive equivalence.

## Conventions

All three type parameters `M`, `α`, and `β` are implicit and inferred from context. There are no special junk-value conventions: the equivalence is defined for every additive monoid `M` and every types `α`, `β`, with no restrictions or edge-case overrides.

## Worked examples

- Claim: For `f : (Fin 1 ⊕ Fin 1 →₀ ℕ)`, applying `VTask.sumFinsuppAddEquivProdFinsupp` and then projecting onto the first component gives `fun i => f (Sum.inl i)`.

- Claim: The forward map of `VTask.sumFinsuppAddEquivProdFinsupp` is a group homomorphism: for any `f g : α ⊕ β →₀ M`, `VTask.sumFinsuppAddEquivProdFinsupp (f + g) = VTask.sumFinsuppAddEquivProdFinsupp f + VTask.sumFinsuppAddEquivProdFinsupp g`.

- Claim: Composing `VTask.sumFinsuppAddEquivProdFinsupp` with its inverse yields the identity on `α ⊕ β →₀ M`.

- Claim: The first component of `VTask.sumFinsuppAddEquivProdFinsupp f` evaluated at `a : α` equals `f (Sum.inl a)`.

## Boundaries

- When `α` or `β` is empty (e.g., `α = Empty` or `β = Empty`), the equivalence still holds: functions on `Empty ⊕ β` are canonically equivalent to functions on `β` alone, and the product factor for `Empty` is the zero finsupp.
- When `M` is the trivial monoid (only the zero element), all finsupps are zero and the equivalence sends the unique element to the unique pair, consistently.
- The equivalence is an `AddEquiv`, not merely an `Equiv`: it preserves and reflects addition and zero, making it a full additive monoid isomorphism.
- The underlying set-equivalence (forgetting the additive structure) agrees with `Equiv.sum_arrow_equiv_prod_arrow` specialized to finitely-supported functions.

## Not to be confused with

- `Equiv.sum_arrow_equiv_prod_arrow`: the plain type equivalence between `(α ⊕ β → M)` and `(α → M) × (β → M)` for unrestricted (not necessarily finitely-supported) functions; `VTask.sumFinsuppAddEquivProdFinsupp` is its finsupp analogue with additive structure.
- `Finsupp.sumFinsuppEquivProdFinsupp`: the underlying bare `Equiv` (without the `AddEquiv` bundling) between the same finsupp types; `VTask.sumFinsuppAddEquivProdFinsupp` adds and certifies the additive homomorphism property on top.
- `Finsupp.prodFinsuppAddEquiv` or similar product-to-sum directions: these go in the opposite direction or concern product types rather than sum types.