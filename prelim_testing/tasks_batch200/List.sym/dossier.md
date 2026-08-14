## Object

`VTask.sym n xs` is the list of all unordered `n`-tuples (multisets of size `n`) whose elements are drawn from the list `xs`, allowing repetition. Concretely, each output element is an element of `Sym α n`, the type of unordered `n`-tuples over `α`. The output lists all such multisets in some fixed recursive order.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sym : {α : Type u_1} -> (n : ℕ) -> List α → List (Sym α n)
<!-- PINNED-SIGNATURE:END -->


`VTask.sym : {α : Type u_1} -> (n : ℕ) -> List α → List (Sym α n)`

The implicit type parameter `α` is the element type. The first explicit argument `n` is the size (or degree) of the unordered tuples to be formed. The second argument `xs` is the source list from which elements are drawn (with repetition allowed).

## Conventions

The output is a `List`, so the unordered tuples appear in some fixed recursive order that depends on the order of elements in `xs`; no canonical or sorted ordering of the output is guaranteed. When `n = 0`, the result is always the singleton list containing the unique empty tuple `Sym.nil`, regardless of the source list (even if it is empty). When `n ≥ 1` and `xs` is empty, the result is the empty list, since no elements are available to fill a nonempty tuple.

## Worked examples

- Claim: `VTask.sym 0 ([] : List ℕ)` has length 1 — the empty source list still yields exactly one 0-tuple.

- Claim: `VTask.sym 0 [1, 2, 3]` has length 1 — any source list yields exactly one 0-tuple.

- Claim: `VTask.sym 1 [10, 20]` has length 2 — the two 1-tuples are `{10}` and `{20}`.

- Claim: `VTask.sym 2 [1, 2]` has length 3 — the three 2-tuples with repetition from `{1, 2}` are `{1,1}`, `{1,2}`, `{2,2}`.

- Claim: `VTask.sym 2 ([] : List ℕ)` has length 0 — no 2-tuples can be formed from an empty list.

- Claim: If `xs` has no duplicates, then `VTask.sym n xs` also has no duplicates (the `Nodup` property is preserved).

## Boundaries

- **`n = 0`, any `xs`**: always returns `[Sym.nil]`, the one-element list containing the unique empty multiset. This includes the case `xs = []`.
- **`n ≥ 1`, `xs = []`**: returns `[]`, because no element is available to start a nonempty tuple.
- **`n = 1`**: returns a list of singletons, one per element of `xs` (in the same order).
- **Length**: when `xs` has length `k`, the output has length `Nat.choose (k + n - 1) n` (the multiset coefficient), i.e., the number of multisets of size `n` over a `k`-element alphabet.
- **Duplicates in `xs`**: if `xs` contains repeated elements, the output may also contain repeated `Sym α n` values; the `Nodup` preservation theorem applies only when `xs` itself is duplicate-free.

## Not to be confused with

- `List.sym2` — the specialisation to unordered *pairs* (degree 2), which returns `List (Sym2 α)` rather than `List (Sym α 2)`; the two are related by a map through an equivalence.
- `List.Sym` (the type) — `Sym α n` is the *type* of unordered `n`-tuples; `VTask.sym` is the *function* that enumerates them from a list.
- `List.permutations` or `List.combinations` — those produce *ordered* tuples or subsets *without* repetition, whereas `VTask.sym` produces *unordered* tuples *with* repetition.