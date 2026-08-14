## VTask.lookupAll

### Object

`VTask.lookupAll a l` collects, from a list `l` of dependent key-value pairs (sigma types), every value whose key is equal to `a`, returning them as a list indexed by `a`. It is the "gather all matching values" analogue of a dictionary look-up: rather than returning only the first match or an `Option`, it returns the entire sub-list of values associated with the key `a`, in the order they appear in `l`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.lookupAll : {α : Type u} -> {β : α → Type v} -> [DecidableEq α] -> (a : α) -> List (Sigma β) → List (β a)
<!-- PINNED-SIGNATURE:END -->


`{α : Type u} -> {β : α → Type v} -> [DecidableEq α] -> (a : α) -> List (Sigma β) → List (β a)`

The universe-polymorphic key type `α` is implicit, as is the dependent value family `β : α → Type v`. A `DecidableEq α` instance is required so that key equality can be tested at runtime. The explicit argument `a : α` is the key being looked up. The final argument `List (Sigma β)` is the association list of dependent key-value pairs being searched; each entry packages a key of type `α` together with a value whose type depends on that key.

### Conventions

When the input list is empty, the result is the empty list, regardless of the key. When a list entry's key is not equal to `a`, that entry is silently skipped and contributes nothing to the output.

### Worked examples

- Claim: `VTask.lookupAll 1 ([] : List (Sigma (fun _ : Nat => Nat))) = []`
  (Looking up any key in the empty list yields the empty list.)

- Claim: For the list `[⟨1, 10⟩, ⟨2, 20⟩, ⟨1, 30⟩]` with key type `Nat` and constant value type `Nat`, `VTask.lookupAll 1 [⟨1, 10⟩, ⟨2, 20⟩, ⟨1, 30⟩] = [10, 30]`.
  (Both values at key `1` are collected in order; the entry for key `2` is ignored.)

- Claim: If every entry in the list has a key different from `a`, then `VTask.lookupAll a l = []`.
  (Formally: `VTask.lookupAll a l = [] ↔ ∀ b : β a, Sigma.mk a b ∉ l`.)

- Claim: If the list has no duplicate keys (i.e., `NodupKeys`), then `VTask.lookupAll a l` has length at most 1 for every `a`.
  (Under the no-duplicate-keys assumption the function degrades to an option-style look-up.)

### Boundaries

- **Empty list**: `VTask.lookupAll a [] = []` for every `a` and every value family `β`.
- **Single matching entry**: `VTask.lookupAll a (⟨a, b⟩ :: l) = b :: VTask.lookupAll a l`; the matching value is prepended.
- **Single non-matching entry**: `VTask.lookupAll a (⟨a', b⟩ :: l) = VTask.lookupAll a l` when `a ≠ a'`; the entry is skipped entirely.
- **Multiple matches**: All matching values are returned, so the output list can have length greater than 1 when the input list contains repeated keys.
- **NodupKeys input**: When the input list has no duplicate keys, the output list has length at most 1, and it coincides with the `Option.toList` of a dependent look-up (`dlookup`).
- **Sublist relationship**: The output, re-packaged as sigma pairs `⟨a, b⟩`, forms a sublist of the original input list.
- **Permutation invariance**: Under a `NodupKeys` hypothesis, permuting the input list leaves the output unchanged.

### Not to be confused with

- `List.dlookup` — returns only the *first* value for the key as an `Option (β a)`, not all values; `VTask.lookupAll` is the "all matches" version.
- `List.lookup` — the non-dependent analogue for homogeneous association lists `List (α × β)`; does not handle dependent types.
- `List.filter` — filters a list by a predicate on whole elements rather than extracting the dependent value component of matching sigma pairs.