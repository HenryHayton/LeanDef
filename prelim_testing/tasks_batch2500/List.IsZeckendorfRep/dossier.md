## Object

`VTask.IsZeckendorfRep l` is the predicate asserting that a list of natural numbers `l` is a valid *Zeckendorf index list*: its entries are strictly increasing (from right to left, i.e., listed in decreasing order with each successive pair differing by at least 2), and every entry is at least `2`. Concretely, consecutive entries `a, b` in the list (with `a` appearing before `b`) must satisfy `b + 2 ≤ a`, so adjacent Fibonacci indices are non-consecutive. This is precisely the condition that guarantees the sum `(l.map Nat.fib).sum` is a Zeckendorf representation — a sum of distinct, non-consecutive Fibonacci numbers — and cannot be simplified further using the identities `fib 0 = 0`, `fib 1 = fib 2`, or `fib n + fib (n+1) = fib (n+2)`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsZeckendorfRep : (l : List ℕ) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsZeckendorfRep : (l : List ℕ) -> Prop`

The sole argument `l` is a list of natural numbers representing *Fibonacci indices*: the intended sum is `(l.map Nat.fib).sum`. The predicate checks that `l` encodes a proper Zeckendorf representation by requiring the indices to be listed in strictly decreasing order with gaps of at least 2 between every adjacent pair, and all indices at least 2.

## Conventions

The empty list `[]` satisfies `VTask.IsZeckendorfRep` and represents the Zeckendorf representation of `0`. When the list is appended with a sentinel `0` for the chain comparison, entries in `l` that equal `0` or `1` would violate the non-consecutive condition with the sentinel (since `0 + 2 = 2 > 0` fails for a prior entry of `1` or `0`), enforcing the "indices ≥ 2" requirement.

## Worked examples

- Claim: `VTask.IsZeckendorfRep []` (the empty list is a valid Zeckendorf representation, corresponding to the number 0)

- Claim: `VTask.IsZeckendorfRep [2]` (the singleton list `[2]` is valid; its single entry is 2, satisfying all conditions)

- Claim: `VTask.IsZeckendorfRep [5, 3, 2]` is false because 3 and 2 are consecutive (differ by only 1, violating the gap-of-2 requirement)

- Claim: `VTask.IsZeckendorfRep [5, 2]` holds; 5 and 2 differ by 3 ≥ 2, and both are ≥ 2

- Claim: `VTask.IsZeckendorfRep [3, 1]` does not hold because 1 < 2 is not an allowed index

## Boundaries

- **Empty list**: `VTask.IsZeckendorfRep []` holds unconditionally; it is the base case corresponding to the Zeckendorf representation of 0.
- **Singleton list**: `VTask.IsZeckendorfRep [k]` holds if and only if `k ≥ 2`, because the chain condition with the appended sentinel `0` requires `0 + 2 ≤ k`.
- **Index 0 or 1**: Any list containing `0` or `1` fails the predicate, since those values are too small to maintain a gap of 2 above the sentinel `0`.
- **Adjacent entries differing by exactly 1**: Consecutive Fibonacci indices (gap = 1) violate the predicate, preventing the identity `fib n + fib (n+1) = fib (n+2)` from being applicable.
- **Non-decreasing or repeated entries**: Any list that is not strictly decreasing with gap ≥ 2 will fail; in particular, equal adjacent entries fail.

## Not to be confused with

- **`List.Chain`** or **`List.Pairwise`**: These are general list structure predicates in Mathlib; `VTask.IsZeckendorfRep` is a specific instance encoding the Zeckendorf gap condition with a sentinel.
- **Zeckendorf representation as a set of indices**: Some formulations use a `Finset` or `Set` rather than an ordered `List`; here the list ordering itself encodes the decreasing property.
- **`Nat.fib`-sum predicates**: The predicate does *not* mention Fibonacci numbers or sums at all — it is purely a structural condition on the list of natural number indices, independent of what those indices are used to index into.