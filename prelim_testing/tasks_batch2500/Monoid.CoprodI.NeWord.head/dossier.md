## VTask.head

### Object

`VTask.head` extracts the **first letter** (the leftmost non-identity element, together with the index component it belongs to) from a `NeWord`, which is a nonempty reduced word over a family of monoids indexed by `ι`. Concretely, a `NeWord M i j` represents a non-empty, alternating sequence of non-identity elements drawn from the monoids in the family, beginning in component `i` and ending in component `j`; `VTask.head` returns the element of `M i` that sits at the very left of that sequence.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.head : {ι : Type u_1} -> {M : ι → Type u_2} -> [(i : ι) → Monoid (M i)] -> {i j : ι} -> (_w : Monoid.CoprodI.NeWord M i j) -> M i
<!-- PINNED-SIGNATURE:END -->


`{ι : Type u_1} -> {M : ι → Type u_2} -> [(i : ι) → Monoid (M i)] -> {i j : ι} -> (_w : Monoid.CoprodI.NeWord M i j) -> M i`

The index type `ι` labels the component monoids. `M` is the family of types, one per index. The instance argument supplies a `Monoid` structure for each component. The implicit indices `i` and `j` record where the word starts and ends, respectively — in particular, `i` is the index of the first letter. The explicit argument `_w` is the nonempty reduced word whose first letter is to be extracted. The return type `M i` is the monoid at the starting index, confirming that the result is the element occupying the leftmost position.

### Conventions

No junk-value conventions are declared: `VTask.head` is a total function defined on every element of the inductively defined type `NeWord M i j`, and every such word has a well-defined first letter by construction.

### Worked examples

- Claim: For a singleton word built from a single non-identity element `x : M i`, `VTask.head` returns `x` itself.

- Claim: For an appended word `append w₁ hne w₂`, `VTask.head` returns `w₁.head`, i.e., the head of the left sub-word, ignoring `w₂` entirely.

- Claim: If `w : NeWord G i j` is a word over a group family and `w.inv` denotes its inverse word (which ends where `w` began, so has type `NeWord G j i`), then `VTask.head w.inv = (VTask.head (... last ...))⁻¹`; more precisely, `w.inv.head = w.last⁻¹`, showing the head of the inverse is the inverse of the last element of the original.

- Claim: After applying `replaceHead x hnotone w` to replace the head of `w` with a new non-identity element `x`, the head of the resulting word equals `x`.

### Boundaries

- A `NeWord` is required to be nonempty by type; there is no empty word, so `VTask.head` always has a well-defined output and there are no undefined or default-value edge cases.
- The head element is guaranteed to be non-identity (since every letter in a `NeWord` is non-identity by the `NeWord` invariant), so the returned value always satisfies `VTask.head w ≠ 1`.
- For a singleton word `singleton x hne`, the head is exactly `x`.
- For any appended word, no matter how deeply nested the right sub-word is, the head depends only on the left-most sub-word, recursively bottoming out at the leftmost singleton.

### Not to be confused with

- `VTask.last` — extracts the *last* (rightmost) letter of the `NeWord`, living in `M j` rather than `M i`.
- `Monoid.CoprodI.NeWord.toList` — converts the entire `NeWord` into a list of `(index, element)` pairs; `VTask.head` retrieves only the single first element, not the whole list.
- `List.head?` on `w.toList` — while `w.toList.head?` equals `Option.some ⟨i, w.head⟩`, the list head returns an `Option` of a sigma type, whereas `VTask.head` returns a plain element of `M i` with the index information already encoded in the type.