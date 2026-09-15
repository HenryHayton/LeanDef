## VTask.mulHead

### Object

Given a non-empty reduced word `w` in a free product of monoids (indexed by some type `ι`), whose first letter belongs to the monoid `M i`, and given an element `x` in that same monoid `M i`, `VTask.mulHead` produces the new reduced word obtained by multiplying `x` onto the left of `w`. The operation is well-defined and stays a valid non-empty reduced word precisely because `x` times the current head does not equal the identity element — so no cancellation collapses the word's leading entry.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.mulHead : {ι : Type u_1} -> {M : ι → Type u_2} -> [(i : ι) → Monoid (M i)] -> {i j : ι} -> (w : Monoid.CoprodI.NeWord M i j) -> (x : M i) -> (hnotone : x * w.head ≠ 1) -> Monoid.CoprodI.NeWord M i j
<!-- PINNED-SIGNATURE:END -->


The first implicit argument is the index type `ι` of the family of monoids. The second implicit argument is the family `M` itself. The typeclass argument supplies a `Monoid` instance for each `M i`. The implicit arguments `i` and `j` are the starting and ending indices of the word (a `NeWord M i j` is a reduced word whose first letter is in `M i` and whose last letter is in `M j`). The argument `w` is the non-empty reduced word being modified. The argument `x` is the element of `M i` to prepend. The argument `hnotone` is the proof that `x * w.head ≠ 1`, i.e. the product of `x` with the current head does not collapse to the identity, ensuring the result is still a valid non-empty reduced word.

### Conventions

There are no junk-value or out-of-domain conventions to declare: the function is total on all inputs satisfying the stated types and the non-cancellation hypothesis `hnotone`.

### Worked examples

- Claim: For a singleton word with head element `a` in some monoid, `VTask.mulHead` on input `x` (with `x * a ≠ 1`) produces a word whose head is `x * a`.

- Claim: For an append (concatenated) word `w = w₁ ++ w₂` whose head comes from `w₁`, applying `VTask.mulHead x hnotone` yields a word whose head is `x * w.head` and whose overall shape (length, tail) is otherwise unchanged.

- Claim: If `w` is a singleton word with head `a` and `x = 1` is the identity, then `hnotone` cannot be satisfied (since `1 * a = a` is allowed to be `1` only if `a = 1`, but a singleton word requires `a ≠ 1`), so the hypothesis `hnotone` is genuinely non-trivial and excludes cases where multiplication would produce a trivial letter.

### Boundaries

- The hypothesis `hnotone : x * w.head ≠ 1` is essential: without it the product `x * w.head` might equal the identity, which is not permitted as the leading letter of a `NeWord`. The function does not exist (is not callable) without this proof.
- When `x` is itself the identity element `1`, the hypothesis forces `w.head ≠ 1` (which is already guaranteed by the `NeWord` invariant), and `mulHead` simply returns a word with the same head as `w` (since `1 * w.head = w.head`).
- The ending index `j` of the word is unchanged: left-multiplying only affects the head, not the tail, so the word still ends in `M j`.
- The structure of the word beyond the head (the tail and its index) is preserved exactly.

### Not to be confused with

- `Monoid.CoprodI.NeWord.replaceHead` — the lower-level primitive that replaces the head element with an arbitrary non-trivial element; `VTask.mulHead` is a convenient wrapper that computes the new head as a product `x * w.head`.
- `Monoid.CoprodI.NeWord.append` — concatenates two `NeWord`s end-to-end, producing a longer word, rather than updating the leading letter of an existing word.
- `Monoid.CoprodI.NeWord.mulTail` (if it exists) — the analogous operation on the rightmost letter of a `NeWord`, not the leftmost.
