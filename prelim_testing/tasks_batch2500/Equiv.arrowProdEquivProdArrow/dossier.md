## Object

`VTask.arrowProdEquivProdArrow` is the canonical equivalence (bijection with explicit inverse) between two naturally isomorphic types:
- the type of dependent functions from `α` into a pointwise product, i.e., functions `f : (i : α) → β i × γ i`, and
- the product of two separate dependent function types, i.e., pairs `(g, h)` where `g : (i : α) → β i` and `h : (i : α) → γ i`.

Informally, a single function that returns a pair at every index is the same data as a pair of functions, one returning each component. This equivalence is the type-theoretic version of the set-theoretic identity `(A → B × C) ≅ (A → B) × (A → C)`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.arrowProdEquivProdArrow : (α : Type u_9) -> (β : α → Type u_10) -> (γ : α → Type u_11) -> ((i : α) → β i × γ i) ≃ ((i : α) → β i) × ((i : α) → γ i)
<!-- PINNED-SIGNATURE:END -->


`VTask.arrowProdEquivProdArrow : (α : Type u_9) -> (β : α → Type u_10) -> (γ : α → Type u_11) -> ((i : α) → β i × γ i) ≃ ((i : α) → β i) × ((i : α) → γ i)`

The first argument `α` is the index type — the common domain of all the functions involved. The second argument `β` is a type family over `α`, providing the first component type at each index. The third argument `γ` is another type family over `α`, providing the second component type at each index. The result is a bundled equivalence (`≃`) between the dependent function-into-product type and the product-of-dependent-function-types.

## Conventions

No special junk-value or edge-case conventions are declared: the equivalence is total and well-defined for every choice of `α`, `β`, and `γ`, including when `α` is empty or a singleton.

## Worked examples

- Claim: When `α = Unit`, `β = fun _ => ℕ`, `γ = fun _ => Bool`, the forward direction maps the function `fun _ => (3, true)` to the pair `(fun _ => 3, fun _ => true)`.

- Claim: For any index type `α`, applying the forward map and then the inverse map of `VTask.arrowProdEquivProdArrow α β γ` returns the original function, i.e., the composite is the identity on `(i : α) → β i × γ i`.

- Claim: When `α = Fin 2`, `β = fun _ => ℤ`, `γ = fun _ => ℤ`, the forward map sends `fun i => (i.val, i.val + 1)` to `(fun i => ↑i.val, fun i => ↑i.val + 1)`.

- Claim: When `α = Empty`, the equivalence specialises to an equivalence between `Empty → β × γ` and `(Empty → β) × (Empty → γ)`, all of which are singletons, so the equivalence is trivially the unique map between them.

## Boundaries

- **Empty index type (`α = Empty` or any uninhabited type):** Both sides of the equivalence are singletons (there is exactly one function out of an empty type), and the equivalence maps the unique element on each side to the unique element on the other. Everything is well-typed and well-defined.
- **Singleton index type (`α = Unit`):** The equivalence reduces to the familiar non-dependent bijection `(β × γ) ≃ β × γ` (up to the trivial wrapping of constant functions), which is the identity.
- **Non-dependent case (`β` and `γ` constant families):** The equivalence specialises to `(α → β × γ) ≃ (α → β) × (α → γ)`, the standard currying/splitting for ordinary function types into a product.
- The equivalence is a definitional (computation-preserving) bijection; both the forward and inverse maps are given by simple projections and pairing, so the equivalence is transparent to reduction.

## Not to be confused with

- **`Equiv.arrowArrowEquivProdArrow`**: an equivalence involving iterated function types `(α → β → γ)` rather than functions into a product; these are dual in a certain sense but are distinct constructions.
- **`Equiv.prodEquiv` or `Equiv.prodCongr`**: equivalences that act on a product type by replacing each component, rather than transposing function-into-product with product-of-functions.
- **`MeasurableEquiv.arrowProdEquivProdArrow`**: the measurable version of this equivalence, which additionally carries measurability structure; not to be confused with the plain type-theoretic `Equiv` version documented here.