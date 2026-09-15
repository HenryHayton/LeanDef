## Object

`VTask.orderEmbOfFin s h` is the unique strictly increasing bijection from `Fin k` onto the finite set `s`, viewed as an order embedding into the ambient linearly ordered type `α`. Concretely, if the elements of `s` are listed in increasing order as `a₀ < a₁ < … < a_{k-1}`, then index `i : Fin k` maps to `aᵢ`. Because it is an order embedding, it automatically preserves and reflects the order, and it is injective.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.orderEmbOfFin : {α : Type u_1} -> [LinearOrder α] -> (s : Finset α) -> {k : ℕ} -> (h : s.card = k) -> Fin k ↪o α
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> [LinearOrder α] -> (s : Finset α) -> {k : ℕ} -> (h : s.card = k) -> Fin k ↪o α`

The type `α` is the ambient linearly ordered type in which `s` lives. The instance `[LinearOrder α]` supplies the total order needed to sort the elements of `s`. The argument `s` is the finite set whose elements are being enumerated. The natural number `k` is implicit and is inferred from context; it serves as the upper bound for the domain `Fin k`. The proof `h : s.card = k` witnesses that `s` has exactly `k` elements, allowing the domain and codomain sizes to match without any casting.

## Conventions

When `k = 0` (i.e., `s` is the empty finset), the function is the unique map out of the empty type `Fin 0`; it is vacuously an order embedding and its range is empty, consistent with `s = ∅`. The parameter `k` is chosen to be an explicit natural-number variable rather than using `s.card` directly so that downstream uses of the embedding avoid coercions when `k` has already been fixed in context.

## Worked examples

- Claim: For `s = {1, 3, 5} : Finset ℕ` with `h : s.card = 3`, the embedding sends `⟨0, _⟩` to `1`, `⟨1, _⟩` to `3`, and `⟨2, _⟩` to `5` (the elements in increasing order).

- Claim: For `s = {2, 7} : Finset ℕ` with `h : s.card = 2`, the map `VTask.orderEmbOfFin s h` is strictly increasing: applying it to `⟨0, _⟩` gives a value strictly less than applying it to `⟨1, _⟩`.

- Claim: For any finset `s : Finset α` with `h : s.card = k`, the set-theoretic range of `VTask.orderEmbOfFin s h` equals `↑s` as a `Set α`.

- Claim: For `s : Finset α` with `h : s.card = k` and `0 < k`, applying `VTask.orderEmbOfFin s h` to `⟨k - 1, _⟩` yields the maximum element of `s`.

## Boundaries

- **Empty finset (`k = 0`):** `Fin 0` is an empty type, so the embedding exists but has no inputs to evaluate. It is the unique map from the empty type, and its range is the empty set, matching `s = ∅`.
- **Singleton finset (`k = 1`):** The only index is `⟨0, _⟩` and it maps to the single element of `s`. Monotonicity and injectivity are trivially satisfied.
- **The proof `h` only witnesses cardinality:** The embedding's definition does not depend on any additional structure of `h` beyond the fact that `s.card = k`; in particular, a different proof of the same statement yields the same embedding.
- **Order embedding, not merely a function:** The bundled type `Fin k ↪o α` guarantees that the map is both injective and strictly monotone (equivalently, `i < j → f i < f j`).

## Not to be confused with

- `Finset.orderIsoOfFin s h`: the closely related order *isomorphism* `Fin k ≃o s` mapping into the subtype `↥s` rather than directly into `α`; `VTask.orderEmbOfFin` is obtained from this by composing with the subtype inclusion.
- `Finset.sort`: returns the sorted `List α` of elements of `s`, the list analogue of the same enumeration without the order-embedding structure.
- `Fin.orderEmbOfFin` (if it existed): there is no standard separate definition for finite types; the present definition is specifically for `Finset`s inside a linear order.