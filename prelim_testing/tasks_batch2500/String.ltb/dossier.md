## Object

`VTask.ltb` is the strict-less-than comparison for string iterators, returning `true` exactly when the remaining suffix of the first iterator is lexicographically strictly less than the remaining suffix of the second iterator, where the ordering on characters is the standard Unicode (code-point) order and the ordering on lists of characters is the usual lexicographic order (shorter prefix-equal strings come first).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ltb : (s₁ s₂ : String.Legacy.Iterator) -> Bool
<!-- PINNED-SIGNATURE:END -->


```
VTask.ltb : (s₁ s₂ : String.Legacy.Iterator) -> Bool
```

The first argument `s₁` is a string iterator whose current position marks the start of the substring being compared. The second argument `s₂` is similarly a string iterator; the function tests whether the remaining characters of `s₁` are strictly less than those of `s₂` in lexicographic order.

## Conventions

When both iterators are exhausted (both remaining suffixes are empty), the function returns `false` — an empty suffix is not strictly less than another empty suffix. When the first iterator is exhausted but the second is not, the function returns `true` — an empty suffix is strictly less than any non-empty suffix. When the second iterator is exhausted (regardless of the first), the function returns `false`.

## Worked examples

- Claim: `VTask.ltb (String.Legacy.iter "") (String.Legacy.iter "") = false` (empty is not less than empty)

- Claim: `VTask.ltb (String.Legacy.iter "") (String.Legacy.iter "a") = true` (empty string is less than any non-empty string)

- Claim: `VTask.ltb (String.Legacy.iter "a") (String.Legacy.iter "") = false` (non-empty is not less than empty)

- Claim: `VTask.ltb (String.Legacy.iter "abc") (String.Legacy.iter "abd") = true` (lexicographic comparison: 'c' < 'd')

- Claim: `VTask.ltb (String.Legacy.iter "abd") (String.Legacy.iter "abc") = false` (reverse: 'd' > 'c')

- Claim: `VTask.ltb (String.Legacy.iter "ab") (String.Legacy.iter "abc") = true` (proper prefix is less)

- Claim: `VTask.ltb (String.Legacy.iter "abc") (String.Legacy.iter "ab") = false` (proper extension is not less than its prefix)

- Claim: `VTask.ltb (String.Legacy.iter "abc") (String.Legacy.iter "abc") = false` (equal strings are not strictly less)

## Boundaries

- When both remaining suffixes are empty, the result is `false` (strict inequality is reflexively false).
- When the first suffix is empty and the second is non-empty, the result is `true` (empty is the minimum under this order).
- When the second suffix is empty and the first is non-empty, the result is `false`.
- The function operates on the *remaining* part of each iterator (from the current position to the end), not necessarily the full underlying string.
- The comparison coincides with `<` on `String` when the iterators are initialized at the beginning of their respective strings (i.e., via `String.Legacy.iter`).
- The ordering is strict: `VTask.ltb s s = false` for any iterator `s`.

## Not to be confused with

- `String.decLt` / `String.lt`: the Prop-valued strict ordering on strings; `VTask.ltb` is its Bool-valued (computable) counterpart at the iterator level.
- `BEq`/`==` on string iterators: that tests equality of the remaining suffixes, not strict ordering.
- `String.Legacy.Iterator.hasNext`: a predicate that tests whether an iterator has remaining characters, not how two iterators compare to each other.
