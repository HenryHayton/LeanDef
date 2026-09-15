## VTask.Lex

### Object

`VTask.Lex r s x y` is the **lexicographic order relation** on finitely-supported functions `α →₀ N`. It holds when there exists some index `a : α` such that (1) for every index `b` that is strictly before `a` in the ordering `r`, the two functions `x` and `y` agree at `b`, and (2) at the index `a` itself, `s (x a) (y a)` holds. Intuitively, to compare `x` and `y` one scans through the indices in the order given by `r`, looking for the first position where they differ, and then compares the values at that position using `s`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Lex : {α : Type u_1} -> {N : Type u_2} -> [Zero N] -> (r : α → α → Prop) -> (s : N → N → Prop) -> (x y : α →₀ N) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Lex : {α : Type u_1} -> {N : Type u_2} -> [Zero N] -> (r : α → α → Prop) -> (s : N → N → Prop) -> (x y : α →₀ N) -> Prop`

The type `α` is the index type of the finitely-supported functions; `N` is the value type, which must carry a distinguished zero (so that the notion of finite support is meaningful). The relation `r` is the ordering used to scan through the indices; `s` is the ordering used to compare values once the first differing index is found. The arguments `x` and `y` are the two finitely-supported functions being compared, and the result is the proposition that `x` is lexicographically less than `y` with respect to `r` on indices and `s` on values.

### Conventions

No junk-value or edge conventions are formally declared for this definition: the relation is a `Prop`-valued predicate on two finitely-supported functions and its truth value is fully determined by the mathematical definition. There is no special behaviour at boundary inputs that differs from the general rule.

### Worked examples

- Claim: For finitely-supported functions on a two-element type ordered with the natural strict order on `ℕ` values, `VTask.Lex (· < ·) (· < ·) x y` holds when `x` and `y` first differ at some index `a` and `x a < y a` while they agree at all indices preceding `a`.

- Claim: If `x` and `y` are finitely-supported functions `α →₀ ℕ` with `x = Finsupp.single a 3` and `y = Finsupp.single a 5` (and `a` is the minimum element under `r`), then `VTask.Lex r (· < ·) x y` holds because the first differing index is `a` and `3 < 5`.

- Claim: If `x = y` (both are the zero function), then `VTask.Lex r s x y` does not hold for any irreflexive `s`, because there is no index at which the functions differ.

- Claim: `VTask.Lex r s` is well-founded whenever `s` has no element strictly below `0`, `s` is well-founded, and the reverse of `r` is well-founded (i.e., `r` is a well-order scanning from the largest index first).

### Boundaries

- When `α` is empty, no index exists, so `VTask.Lex r s x y` is vacuously false for every pair `x`, `y` (the only function is the zero function and there is no witnessing index).
- When both `x` and `y` are the zero function, `VTask.Lex r s x y` is false because `x` and `y` agree everywhere and there is no first differing index.
- If `s` is irreflexive, then `VTask.Lex r s` is irreflexive as well: a function cannot be lexicographically strictly less than itself.
- The relation depends on `r` only to determine the order in which indices are scanned; if `r` has no minimal element (e.g., `r` is not well-founded from the right), well-foundedness of `VTask.Lex r s` may fail.
- The zero instance on `N` matters for determining finite support but does not affect the comparison logic directly.

### Not to be confused with

- `DFinsupp.Lex r s`: the analogous lexicographic relation on *dependent* finitely-supported functions `Π₀ i, α i`, where the value ordering can vary by index.
- `Pi.Lex r s`: the lexicographic relation on all functions `α → N` (not necessarily finitely supported); `VTask.Lex r s x y` is definitionally equal to `Pi.Lex r s x y` when `x` and `y` are viewed as ordinary functions.
- `Finsupp.DegLex r s`: a refinement of the lexicographic order that first compares the total degree of the finitely-supported function, and only uses the lex order as a tiebreaker.