## Object

`VTask.choose` picks out the **first element** of a list `l` that satisfies a predicate `p`. Given a proof that at least one such element exists in `l`, it returns a concrete witness of type `α` from the list. The result is always a member of the list and always satisfies the predicate.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.choose : {α : Type u_1} -> (p : α → Prop) -> [DecidablePred p] -> (l : List α) -> (hp : ∃ a ∈ l, p a) -> α
<!-- PINNED-SIGNATURE:END -->


`VTask.choose : {α : Type u_1} -> (p : α → Prop) -> [DecidablePred p] -> (l : List α) -> (hp : ∃ a ∈ l, p a) -> α`

The implicit type argument `α` is the element type of the list. The argument `p` is the predicate that we want some element to satisfy. The instance `[DecidablePred p]` supplies the ability to evaluate `p` computably at each position. The argument `l` is the list being searched. The argument `hp` is a proof that some element of `l` satisfies `p`; it guarantees the search will succeed and makes the function total.

## Conventions

When multiple elements of `l` satisfy `p`, the function always returns the **first** one (leftmost in the list), not an arbitrary one. The proof `hp` is used only to guarantee termination and totality; the actual element returned is determined solely by `l` and `p` via a left-to-right scan.

## Worked examples

- Claim: `VTask.choose (· = 3) [1, 2, 3, 4] ⟨3, by simp⟩ = 3`
  ```lean
  example : VTask.choose (· = 3) [1, 2, 3, 4] ⟨3, by simp⟩ = 3 := by decide
  ```

- Claim: When two elements satisfy the predicate, `VTask.choose` returns the first one: `VTask.choose (· % 2 = 0) [1, 2, 4, 5] ⟨2, by simp⟩ = 2`
  ```lean
  example : VTask.choose (· % 2 = 0) [1, 2, 4, 5] ⟨2, by simp⟩ = 2 := by decide
  ```

- Claim: The chosen element is a member of the list: for any `hp : ∃ a ∈ l, p a`, `VTask.choose p l hp ∈ l` (established by `List.choose_mem`).

- Claim: The chosen element satisfies the predicate: for any `hp : ∃ a ∈ l, p a`, `p (VTask.choose p l hp)` (established by `List.choose_property`).

## Boundaries

- The list `l` cannot be empty when `hp` is provided (since `hp` asserts existence of a member satisfying `p`), so the edge case of an empty list is excluded by the type.
- If the first element of `l` satisfies `p`, it is returned immediately without inspecting the rest of the list.
- If `l` has exactly one element and `hp` certifies it satisfies `p`, that element is returned.
- The proof `hp` does not influence which element is chosen — only `l` and `p` do; `hp` merely makes the operation total.

## Not to be confused with

- `Classical.choose` — chooses a witness from a bare existence proof without any list or decidability requirement; not constrained to be the *first* element of anything.
- `List.find?` — returns `Option α` (no existence proof required) rather than `α`; does not require a proof of existence.
- `Nat.choose` — the binomial coefficient "n choose k"; entirely unrelated despite the shared name.