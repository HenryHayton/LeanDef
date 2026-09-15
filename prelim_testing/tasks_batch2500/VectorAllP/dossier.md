## Object

`VTask.VectorAllP p v` is the proposition asserting that a predicate `p` holds for every element of a fixed-length vector `v`. Concretely, it unfolds as a finite conjunction: for a vector `[a₀, a₁, …, aₙ₋₁]` it equals `p a₀ ∧ p a₁ ∧ … ∧ p aₙ₋₁`, and for the empty vector it equals `True`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.VectorAllP : {α : Type u_1} -> {n : ℕ} -> (p : α → Prop) -> (v : Vector3 α n) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.VectorAllP : {α : Type u_1} -> {n : ℕ} -> (p : α → Prop) -> (v : Vector3 α n) -> Prop`

The type parameter `α` is the element type of the vector, inferred implicitly. The natural number `n` is the length of the vector, also inferred implicitly. The argument `p` is the predicate being tested — a function from elements of `α` to `Prop`. The argument `v` is the length-`n` vector whose elements are being tested.

## Conventions

When the vector has length zero (i.e., `v` is the empty vector), `VTask.VectorAllP p v` reduces to `True`, reflecting the fact that a universal statement over an empty collection holds vacuously.

## Worked examples

- Claim: `VTask.VectorAllP (fun n => n > 0) []` is equivalent to `True` (empty vector case is vacuously true).

- Claim: For a single-element vector `v = [3]`, `VTask.VectorAllP (fun n => n > 0) v` is equivalent to `3 > 0`, i.e., a single conjunct.

- Claim: For a three-element vector `v = [1, 2, 3]`, `VTask.VectorAllP (fun n => n > 0) v` is equivalent to `1 > 0 ∧ 2 > 0 ∧ 3 > 0`.

- Claim: `VTask.VectorAllP p v` implies `p (v i)` for any valid index `i` — pointwise consequences follow from the conjunction.

- Claim: If `∀ x, p x → q x` and `VTask.VectorAllP p v` holds, then `VTask.VectorAllP q v` holds — the predicate is monotone with respect to implication.

## Boundaries

- **Empty vector:** `VTask.VectorAllP p` on the empty vector is definitionally equal to `True`, so it is always provable regardless of `p`.
- **Single-element vector:** `VTask.VectorAllP p [a]` reduces to exactly `p a` with no extra conjunction.
- **Longer vectors:** Each additional element contributes one more conjunct; the rightmost conjunct in the unfolded form corresponds to the inner recursive call `IH`.
- **Arbitrary predicates:** There is no restriction on `p`; it can be any `α → Prop`, including undecidable predicates.
- **Equivalence with universal quantification:** The conjunction form is logically equivalent to `∀ i, p (v i)` over the appropriate index type, but the two forms differ definitionally — `VTask.VectorAllP` unfolds to explicit conjunctions rather than a quantifier.

## Not to be confused with

- `∀ i, p (v i)`: The universally quantified form is logically equivalent but does not unfold to a conjunction; `VTask.VectorAllP` is designed to expose a conjunction structure for easier proof manipulation.
- `List.Forall` / `List.All`: Similar predicate for `List`, but that operates on a linked list without a statically-known length, rather than on a length-indexed `Vector3`.
- `Vector3.map` followed by `Vector3.toList`: A computational transform producing a new vector or list; `VTask.VectorAllP` is a purely logical proposition, not a data transformation.