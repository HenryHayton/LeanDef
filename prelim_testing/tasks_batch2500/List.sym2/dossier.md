## Object

`VTask.sym2 xs` is the list of all unordered pairs (elements of `Sym2 α`) whose two components both come from `xs`. Concretely, every pair `s(a, b)` with `a ∈ xs` and `b ∈ xs` appears in the output list, including pairs where both components are the same element (diagonal pairs such as `s(a, a)`). The output is a list, so it carries an ordering and can contain repetitions when `xs` itself contains duplicates.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.sym2 : {α : Type u_1} -> List α → List (Sym2 α)
<!-- PINNED-SIGNATURE:END -->


The single explicit argument is the source list `xs : List α` whose elements are to be paired. The implicit argument `α` is the element type of that list.

## Conventions

Diagonal pairs `s(a, a)` are included: if `a ∈ xs` then `s(a, a) ∈ xs.sym2`. Because `Sym2` is unordered, `s(a, b)` and `s(b, a)` are the same element, so each unordered pair appears exactly once (not twice) when `xs` has no duplicates.

## Worked examples

- Claim: `VTask.sym2 ([] : List Nat) = []`
  ```lean
  example : VTask.sym2 ([] : List Nat) = [] := by decide
  ```

- Claim: `VTask.sym2 [1] = [s(1, 1)]`
  ```lean
  example : VTask.sym2 [1] = [s(1, 1)] := by decide
  ```

- Claim: `VTask.sym2 [1, 2] = [s(1, 1), s(1, 2), s(2, 2)]`
  ```lean
  example : VTask.sym2 [1, 2] = [s(1, 1), s(1, 2), s(2, 2)] := by decide
  ```

- Claim: The length of `VTask.sym2 xs` equals `Nat.choose (xs.length + 1) 2`, i.e., `C(n+1, 2)` where `n = xs.length`.

- Claim: An element `z : Sym2 α` belongs to `VTask.sym2 xs` if and only if every component of `z` is in `xs`.

- Claim: If `xs` has no duplicate elements, then `VTask.sym2 xs` has no duplicate elements.

## Boundaries

- **Empty list**: `VTask.sym2 [] = []` — no pairs can be formed, so the result is empty. This is the unique list for which `VTask.sym2 xs = []`.
- **Singleton list `[a]`**: Only the diagonal pair `s(a, a)` is produced, giving `[s(a, a)]`.
- **Diagonal pairs always present**: For any `a ∈ xs`, the pair `s(a, a)` always appears in `VTask.sym2 xs`; this function does not restrict to strictly off-diagonal pairs.
- **Duplicates in input**: If `xs` contains repeated elements, then `VTask.sym2 xs` may also contain repeated unordered pairs. Deduplication commutes: `(VTask.sym2 xs).dedup = (xs.dedup).sym2`.
- **Length formula**: The output list has length `Nat.choose (xs.length + 1) 2`, which equals `n*(n+1)/2` for a list of length `n`.

## Not to be confused with

- `List.sym xs 2`: The list of length-2 multisets (`Sym α 2`) from `xs`; related by a bijection but a different type from `Sym2 α`.
- `Sym2.sym2` (set-level construction): The set-theoretic version of all unordered pairs from a set, as opposed to this list-level function.
- `List.Sym2` (if it existed as a subtype): Not the same as this function; `VTask.sym2` produces a plain `List (Sym2 α)`, not a subtype or finset.