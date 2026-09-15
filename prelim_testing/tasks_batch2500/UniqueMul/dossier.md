## VTask.UniqueMul

### Object

`VTask.UniqueMul A B a0 b0` is a proposition asserting that the product `a0 * b0` has a **unique factorisation** over the pair of finite sets `(A, B)`: whenever `a ∈ A`, `b ∈ B`, and `a * b = a0 * b0`, it must be the case that `a = a0` and `b = b0`. In other words, among all pairs `(a, b)` drawn from `A × B`, the element `a0 * b0` is the product of at most one such pair, namely `(a0, b0)` itself.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.UniqueMul : {G : Type u_1} -> [Mul G] -> (A B : Finset G) -> (a0 b0 : G) -> Prop
<!-- PINNED-SIGNATURE:END -->


`{G : Type u_1} -> [Mul G] -> (A B : Finset G) -> (a0 b0 : G) -> Prop`

The implicit type argument `G` is the ambient type carrying the multiplication. The instance `[Mul G]` supplies the binary operation. `A` and `B` are the two finite subsets of `G` from which left and right factors are drawn, respectively. `a0` is the distinguished left factor (which must lie in `A` for the statement to be non-trivially useful) and `b0` is the distinguished right factor (which must lie in `B`). Together `a0 * b0` is the product whose unique factorisation is being asserted.

### Conventions

No junk-value or edge-case conventions are declared for this definition: it is a universally quantified proposition that is vacuously true whenever `A` or `B` is empty (there are simply no pairs `(a, b)` with `a ∈ A` and `b ∈ B` to serve as counterexamples), and it places no syntactic requirement that `a0 ∈ A` or `b0 ∈ B`.

### Worked examples

- Claim: `VTask.UniqueMul A B a0 b0` holds vacuously when `A` is the empty `Finset ℤ`, for any `B`, `a0`, `b0`, because no pair `(a, b)` with `a ∈ ∅` exists.

- Claim: For `G = ℤ`, `A = {2}`, `B = {3}`, `a0 = 2`, `b0 = 3`, `VTask.UniqueMul A B a0 b0` holds: the only pair `(a, b) ∈ {2} × {3}` is `(2, 3)`, which trivially satisfies `a = a0` and `b = b0`.

- Claim: For `G = ℤ` with addition written multiplicatively, `A = {0, 1}`, `B = {0, 1}`, `a0 = 0`, `b0 = 1`, `VTask.UniqueMul A B a0 b0` does **not** hold in general because the product `0 * 1 = 1 * 0` (in an additive group, `0 + 1 = 1 + 0`) gives a second factorisation `(1, 0) ≠ (0, 1)`.

- Claim: If `VTask.UniqueMul A B a0 b0` holds and `A' ⊆ A`, `B' ⊆ B`, then `VTask.UniqueMul A' B' a0 b0` also holds (monotonicity under taking subsets).

### Boundaries

- **Empty sets**: If `A = ∅` or `B = ∅`, the proposition is vacuously true for any `a0`, `b0` because the universal quantifier ranges over an empty domain.
- **`a0` or `b0` outside the respective sets**: The proposition can still be stated and may be vacuously true or false; however, if `a0 ∉ A` or `b0 ∉ B`, no pair `(a, b)` from `A × B` can equal `(a0, b0)`, making the hypothesis `a * b = a0 * b0` possibly satisfiable by other pairs, so uniqueness can fail.
- **Singleton sets**: If `|A| ≤ 1` and `|B| ≤ 1` and both are nonempty, a unique factorisation always exists for the sole elements.
- **Non-cancellative monoids**: Even in structures without cancellation, `VTask.UniqueMul` is a well-posed proposition; it simply may be harder to establish.

### Not to be confused with

- **`UniqueProds` / `UniqueSums`**: These are typeclasses asserting that *every* nonempty finite pair of sets `(A, B)` admits at least one pair `(a0, b0)` with `VTask.UniqueMul A B a0 b0`; `VTask.UniqueMul` itself is the pointwise building block, not the global class.
- **`Finset.card_mul_le`**: A cardinality bound on the product set `A * B`; related in spirit but quantitative rather than a uniqueness assertion about a specific product.
- **Unique factorisation in the sense of UFDs**: That concerns prime decomposition of ring elements, whereas `VTask.UniqueMul` is purely about representing a fixed element as a product of one factor from each of two finite sets.
