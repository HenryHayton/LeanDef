## VTask.Shortlex

### Object

Given a relation `r` on a type `α`, `VTask.Shortlex r` is the **shortlex (short-lexicographic) strict order** on lists over `α`. Under this order, a list `s` precedes a list `t` if and only if either `s` is strictly shorter than `t`, or `s` and `t` have the same length and `s` precedes `t` in the lexicographic order induced by `r`. This is the standard ordering used, for example, to enumerate words over an alphabet in "length-first" fashion: all shorter words come before all longer ones, and words of equal length are sorted by the underlying relation applied position-by-position from left to right.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Shortlex : {α : Type u_1} -> (r : α → α → Prop) -> List α → List α → Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Shortlex : {α : Type u_1} -> (r : α → α → Prop) -> List α → List α → Prop`

The implicit type argument `α` is the element type shared by both lists. The explicit argument `r` is the base relation on elements of `α` that induces the lexicographic comparison when two lists have equal length. The first `List α` argument is the "smaller" candidate (the left-hand side of the relation), and the second `List α` argument is the "larger" candidate (the right-hand side). The whole expression is a `Prop` asserting that the first list strictly precedes the second in the shortlex order.

### Conventions

The empty list is shortlex-minimal: `VTask.Shortlex r [] s` holds for every non-empty list `s`, because any non-empty list has strictly greater length than `[]`. No list precedes the empty list, since nothing has length strictly less than zero.

### Worked examples

- Claim: `VTask.Shortlex r [] [a]` holds for any relation `r` and element `a`, because `[].length < [a].length`.

- Claim: `VTask.Shortlex r [a] [b] ↔ r a b` — two singleton lists are shortlex-ordered exactly when their single elements are related by `r`.

- Claim: `¬ VTask.Shortlex r s []` for any list `s` — no list precedes the empty list in the shortlex order.

- Claim: `VTask.Shortlex r [0, 1] [2, 3, 4]` holds (over `Nat` with `r = (· < ·)`) because `[0,1]` has length 2, strictly less than length 3.

- Claim: `VTask.Shortlex (· < ·) [1, 2] [1, 3]` holds (over `Nat`) because both lists have length 2 and `[1, 2] <lex [1, 3]` under the natural order.

### Boundaries

- **Empty list on the left**: `VTask.Shortlex r [] s` holds for every non-empty `s` (strict length increase). It does **not** hold when `s = []`, since lengths are equal and the empty list is not lexicographically before itself.
- **Empty list on the right**: `VTask.Shortlex r s []` never holds for any `s`, because no list has length strictly less than 0, and the lex comparison of `s` with `[]` also fails (a non-empty list is not lex-before the empty list).
- **Equal lists**: `VTask.Shortlex r s s` is always false, because equal lengths push to the lex comparison, and `List.Lex r s s` is never satisfied (lex order is irreflexive whenever `r` is).
- **Relation `r` is never used when lengths differ**: if `s.length ≠ t.length`, the ordering is determined purely by length comparison, regardless of what `r` says about the elements.
- **`r` can be any relation**, including non-transitive or non-total ones; the resulting shortlex order inherits good properties (e.g., well-foundedness) only under appropriate assumptions on `r`.

### Not to be confused with

- **`List.Lex r`**: the purely lexicographic order on lists, which does *not* prioritise shorter lists — a short list can be larger than a long list if its elements are greater.
- **`List.Sublist`**: a different structural relation on lists about containment of subsequences, not an ordering based on element comparison.
- **`Prod.Lex`**: the lexicographic order on pairs; `VTask.Shortlex` uses `Prod.Lex` internally (on the pair `(length, list)`) but is a relation on lists, not on pairs.
