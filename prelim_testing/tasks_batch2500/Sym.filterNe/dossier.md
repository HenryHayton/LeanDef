## Object

`VTask.filterNe a m` removes every occurrence of a fixed element `a` from a symmetric multiset `m` of size `n`. It returns a dependent pair: the first component is the number of copies of `a` that were removed (as a `Fin (n + 1)`, so it is bounded by `n`), and the second component is the remaining symmetric multiset, which has size `n − i` where `i` is that count.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.filterNe : {α : Type u_1} -> {n : ℕ} -> [DecidableEq α] -> (a : α) -> (m : Sym α n) -> (i : Fin (n + 1)) × Sym α (n - ↑i)
<!-- PINNED-SIGNATURE:END -->


The type variable `α` is the element type, which must support decidable equality. The natural number `n` is the size of the input multiset. The argument `a` is the element to be filtered out — every copy of `a` is removed. The argument `m` is the symmetric multiset of size `n` from which copies of `a` are removed. The result is a sigma type pairing the count `i : Fin (n + 1)` of removed copies with a symmetric multiset of the complementary size `n − i`.

## Conventions

The count `i` is packaged as a `Fin (n + 1)` rather than a bare `ℕ`; the upper bound `n + 1` is exclusive, so the count is guaranteed to lie in `{0, 1, …, n}`. The subtraction `n − ↑i` in the return type is natural-number subtraction; because `i ≤ n` always holds, this subtraction never underflows.

## Worked examples

- Claim: Applying `VTask.filterNe` to the element `1` and the singleton `{1}` yields count `1` and the empty multiset of size `0`.

- Claim: Applying `VTask.filterNe` to the element `2` and the multiset `{1, 2, 2}` (size 3) yields count `2` and a multiset of size `1` containing only `1`.

- Claim: Applying `VTask.filterNe` to an element `a` not present in `m` yields count `0` and a multiset of the same size `n` equal to `m` itself.

- Claim: The round-trip property holds: re-inserting the removed copies of `a` back into the filtered result via `fill` recovers the original multiset `m`.

## Boundaries

- If `a` does not appear in `m`, the count component is `⟨0, …⟩ : Fin (n + 1)` and the multiset component equals `m` unchanged (size remains `n`).
- If `m` consists entirely of copies of `a` (e.g., `m = {a, a, …, a}`), the count component is `⟨n, …⟩ : Fin (n + 1)` and the multiset component is the empty symmetric multiset of size `0`.
- The empty symmetric multiset (n = 0) is a valid input; the only possible result is count `0` and the empty multiset.
- The count is always at most `n`, so the `Fin (n + 1)` bound is tight but never exceeded.

## Not to be confused with

- `Sym.fill`: the inverse operation that inserts a given number of copies of `a` into a symmetric multiset, recovering the original from a `filterNe` result.
- `Multiset.filter`: filters a plain (non-symmetric, non-size-indexed) multiset by a predicate, without packaging a size witness in a sigma type.
- `Sym.erase`: removes a single copy of an element from a symmetric multiset, rather than all copies at once.