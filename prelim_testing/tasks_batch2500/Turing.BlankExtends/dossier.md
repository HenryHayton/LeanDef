## Object

`VTask.BlankExtends l₁ l₂` is a binary relation on lists over an inhabited type asserting that `l₂` is obtained by appending zero or more copies of the *default* element of the type to the end of `l₁`. In other words, `l₁` is an initial segment of `l₂` in which all the extra trailing elements are "blank" (the canonical default value). This gives a partial order on lists: every list blank-extends itself (reflexivity), the relation is transitive, and two lists that blank-extend each other must be equal.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.BlankExtends : {Γ : Type u_1} -> [Inhabited Γ] -> (l₁ l₂ : List Γ) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.BlankExtends : {Γ : Type u_1} -> [Inhabited Γ] -> (l₁ l₂ : List Γ) -> Prop`

The implicit type parameter `Γ` is the element type of the lists. The instance `[Inhabited Γ]` supplies the distinguished "blank" value (`default : Γ`) that is used as the padding element. The explicit argument `l₁` is the shorter (or equal) list, and `l₂` is the list that is claimed to extend `l₁` by blanks at the tail.

## Conventions

The blank element used for padding is always `default : Γ` as supplied by the `Inhabited` instance; no other element of `Γ` qualifies as a blank for this relation, regardless of its value.

## Worked examples

- Claim: `VTask.BlankExtends [1, 2, 3] [1, 2, 3, 0, 0]` holds over `ℕ` (with `default = 0`), because appending two zeros to the first list yields the second.

- Claim: `VTask.BlankExtends ([] : List ℕ) [0, 0, 0]` holds, since the empty list blank-extended by three defaults is `[0, 0, 0]`.

- Claim: `VTask.BlankExtends l l` holds for any list `l` (reflexivity), witnessed by appending zero copies of `default`.

- Claim: If `VTask.BlankExtends l₁ l₂` and `VTask.BlankExtends l₂ l₃`, then `VTask.BlankExtends l₁ l₃` (transitivity), since the concatenation of two replicates is still a replicate of the same element.

- Claim: `VTask.BlankExtends [1, 2, 3] [1, 2, 4]` does **not** hold over `ℕ`, because `[1, 2, 4]` differs from `[1, 2, 3]` in a non-tail position and no suffix of zeros can produce it.

## Boundaries

- When `n = 0`, `l₂ = l₁` (the witness is an empty replicate), so the relation is reflexive: every list blank-extends itself.
- The empty list blank-extends any list consisting entirely of `default` values, e.g., `BlankExtends [] [default, default]`.
- The relation is **not** symmetric in general: `BlankExtends l₁ l₂` with `l₁ ≠ l₂` means `l₂` is strictly longer; reversing the direction then requires `l₁` to equal `l₂` (antisymmetry).
- The relation says nothing about the *interior* of `l₁`; only the appended suffix must consist of blank elements. Interior occurrences of `default` in `l₁` are unrestricted.

## Not to be confused with

- **`List.isPrefixOf` / `List.IsPrefix`**: records that one list is a prefix of another with *arbitrary* trailing elements, not specifically copies of `default`.
- **`VTask.BlankExtends` vs. equality**: two lists that mutually blank-extend each other are equal; blank-extension with nonzero padding strictly lengthens the list.
- **`List.replicate n default` alone**: this is just the suffix appended; `BlankExtends` is the relation on the *full* lists before and after appending that suffix.