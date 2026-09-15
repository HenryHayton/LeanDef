## Object

`VTask.toList` converts a `NeWord` — a non-empty, well-formed word over a family of monoids indexed by `ι` — into a plain list of dependent pairs `(i : ι) × M i`, where each pair records a component index together with the non-identity monoid element sitting at that position. The word's leftmost letter becomes the list's first entry and its rightmost letter becomes the last entry, with appended sub-words contributing their letters in left-to-right order.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toList : {ι : Type u_1} -> {M : ι → Type u_2} -> [(i : ι) → Monoid (M i)] -> {i j : ι} -> (_w : Monoid.CoprodI.NeWord M i j) -> List ((i : ι) × M i)
<!-- PINNED-SIGNATURE:END -->


The first implicit argument is the index type `ι` whose values name the constituent monoids. The second implicit argument is the family `M` assigning a type to each index. The instance argument supplies a `Monoid` structure for each `M i`. The arguments `i` and `j` are the implicit indices of the starting and ending letter of the word (the type-level "endpoints"). The explicit argument `_w` is the `NeWord` being converted.

## Conventions

There are no junk-value conventions: `VTask.toList` is a total function defined by structural recursion on `NeWord`, which is inductively defined and cannot be empty, so no degenerate or junk input exists.

## Worked examples

- Claim: For a singleton `NeWord` carrying index `i` and element `x`, `VTask.toList` returns the one-element list `[⟨i, x⟩]`.

- Claim: For an appended `NeWord` built from left sub-word `w₁` and right sub-word `w₂`, `VTask.toList` returns `w₁.toList ++ w₂.toList`.

- Claim: `VTask.toList w` is never the empty list, for any `NeWord w`.

- Claim: The first element of `VTask.toList w` is `⟨i, w.head⟩` where `i` is the starting index of `w`.

- Claim: The last element of `VTask.toList w` is `⟨j, w.last⟩` where `j` is the ending index of `w`.

## Boundaries

- **Non-emptiness**: Because `NeWord` is non-empty by construction, `VTask.toList` always produces a list with at least one entry. The empty list is never a possible output.
- **Singleton case**: A `NeWord.singleton x h` (a single non-identity element `x : M i`) maps to the one-element list `[⟨i, x⟩]`; start and end index coincide and are both `i`.
- **Append case**: Concatenation of words translates directly to list concatenation; no reordering or deduplication occurs.
- **Head and last correspondence**: The head of the list always corresponds to `w.head` at starting index `i`; the last element always corresponds to `w.last` at ending index `j`.

## Not to be confused with

- `Monoid.CoprodI.NeWord.prod`: evaluates a `NeWord` to a single element of the coproduct monoid rather than producing a list of its letters.
- `List.tail` or sub-lists of the output: the full list from `VTask.toList` includes all letters; no sub-structure is automatically extracted.
- A `Word` in `Monoid.CoprodI` (which allows the empty word): `NeWord` is strictly non-empty, so `VTask.toList` never produces `[]`, unlike a conversion from the nullable `Word` type.