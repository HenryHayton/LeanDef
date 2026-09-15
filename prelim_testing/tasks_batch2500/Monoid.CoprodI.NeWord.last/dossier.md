## Object

`VTask.last` extracts the **last letter** of a non-empty word over a free product of monoids. A `NeWord M i j` is a non-empty, reduced word whose first letter comes from the monoid `M i` and whose last letter comes from the monoid `M j`; `VTask.last` returns that final element of type `M j`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.last : {ι : Type u_1} -> {M : ι → Type u_2} -> [(i : ι) → Monoid (M i)] -> {i j : ι} -> (_w : Monoid.CoprodI.NeWord M i j) -> M j
<!-- PINNED-SIGNATURE:END -->


`VTask.last : {ι : Type u_1} -> {M : ι → Type u_2} -> [(i : ι) → Monoid (M i)] -> {i j : ι} -> (_w : Monoid.CoprodI.NeWord M i j) -> M j`

The index type `ι` labels the family of monoids. `M` assigns a type to each label. The instance argument supplies monoid structure on each `M i`. The implicit indices `i` and `j` are the types of the first and last letters of the word, respectively. The explicit argument `_w` is the non-empty word whose last letter is to be extracted.

## Conventions

No junk-value or edge-case conventions are declared: the function is total and well-defined on every `NeWord`, since `NeWord` is inductively defined and every term in it has a well-determined last letter.

## Worked examples

- Claim: For a singleton word `singleton x hne`, `VTask.last (singleton x hne) = x`.
  This is captured by the theorem `singleton_last`: the last element of a one-letter word is that letter itself.

- Claim: For an appended word `append w₁ hne w₂`, `VTask.last (append w₁ hne w₂) = VTask.last w₂`.
  This is captured by `append_last`: the last letter of a concatenation is the last letter of the right subword, regardless of what the left subword contains.

- Claim: The last letter of the inverse of a word `w` equals the inverse of the head of `w`.
  This is the theorem `inv_last`: `w.inv.last = w.head⁻¹`.

- Claim: The last entry in `w.toList` is `⟨j, VTask.last w⟩` (wrapped in `Option.some`).
  This is the theorem `toList_getLast?`.

## Boundaries

- `NeWord` is a non-empty structure by construction; there is no concept of an empty word here, so `VTask.last` is always defined and never returns a fallback value.
- For a singleton `singleton x hne`, the last letter coincides with the first (and only) letter, so `VTask.last` and `VTask.head` agree on this constructor.
- For an append `append w₁ hne w₂`, the last letter depends solely on `w₂` and is completely independent of `w₁`.
- When the word has exactly two letters (i.e., `append (singleton x _) hne (singleton y _)`), `VTask.last` returns `y`.

## Not to be confused with

- `VTask.head`: extracts the *first* letter `M i` of the word rather than the last.
- `Monoid.CoprodI.NeWord.toList`: produces the full list of letters; `VTask.last` is just the final element of that list.
- `List.getLast`: the standard library's last-element function for plain lists, not directly related to the typed `NeWord` structure.