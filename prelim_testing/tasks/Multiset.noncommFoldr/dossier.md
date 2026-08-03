## Object

`VTask.noncommFoldr` computes the right-fold of a multiset `s` using a binary function `f : α → β → β`, starting from an initial accumulator `b : β`. Because a multiset has no canonical ordering, the fold is well-defined only when the elements of `s` are pairwise *left-commuting* with respect to `f` — that is, for every pair `x, y` of distinct elements of `s`, swapping the order in which they are applied to `f` yields the same result for any accumulator. The function produces the same value that a `List.foldr` over any list representative of `s` would give, and the pairwise commutativity hypothesis is exactly what makes this value independent of which representative list is chosen.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.noncommFoldr : {α : Type u_3} -> {β : Type u_4} -> (f : α → β → β) -> (s : Multiset α) -> (comm : {x | x ∈ s}.Pairwise fun x y => ∀ (b : β), f x (f y b) = f y (f x b)) -> (b : β) -> β
<!-- PINNED-SIGNATURE:END -->


`VTask.noncommFoldr : {α : Type u_3} -> {β : Type u_4} -> (f : α → β → β) -> (s : Multiset α) -> (comm : {x | x ∈ s}.Pairwise fun x y => ∀ (b : β), f x (f y b) = f y (f x b)) -> (b : β) -> β`

The first implicit argument is the element type `α`; the second implicit argument is the accumulator type `β`. The argument `f` is the folding function that combines an element of `α` with an accumulated value of type `β`. The argument `s` is the multiset of elements to fold over. The argument `comm` is a proof that every pair of distinct members of `s` left-commutes through `f`: for any `x, y ∈ s` (with `x ≠ y` in the pairwise sense) and any accumulator `b`, applying `x` then `y` gives the same result as applying `y` then `x`. The final argument `b` is the initial accumulator value from which the fold starts.

## Conventions

When the multiset `s` is empty, the fold returns `b` unchanged — there are no elements to apply. When the global hypothesis `LeftCommutative f` holds, the commutativity argument can be filled trivially and the result coincides with the standard `Multiset.foldr`.

## Worked examples

- Claim: `VTask.noncommFoldr (fun (n : ℕ) acc => n + acc) (0 : Multiset ℕ) (by simp [Set.Pairwise]) 7 = 7`
  (Folding over the empty multiset with any function returns the initial accumulator, here `7`.)

- Claim: For `s = [1, 2, 3]` coerced to a multiset and `f = (· + ·)`, `VTask.noncommFoldr (· + ·) (↑[1, 2, 3] : Multiset ℕ) (by decide) 0 = 6`
  (Addition is commutative so the commutativity condition is trivially satisfied; the fold sums all elements plus the initial `0`.)

- Claim: For a singleton multiset `{a}`, `VTask.noncommFoldr f {a} h b = f a b` for any `f`, `h`, and `b`.
  (Folding a single-element multiset applies `f` once to the element and the initial accumulator.)

- Claim: `VTask.noncommFoldr (fun (x : ℕ) acc => x * acc) (↑[2, 3] : Multiset ℕ) (by intro x hx y hy _; fin_cases hx <;> fin_cases hy <;> simp [mul_assoc]) 1 = 6`
  (Multiplication is commutative, so folding `[2, 3]` starting from `1` gives `2 * (3 * 1) = 6`.)

## Boundaries

- **Empty multiset**: The fold immediately returns `b`; the commutativity proof is vacuously satisfied and can always be provided.
- **Singleton multiset `{a}`**: The result is `f a b`; the pairwise commutativity condition is again vacuous (no two distinct elements exist).
- **Globally left-commutative `f`**: When `LeftCommutative f` holds everywhere, `VTask.noncommFoldr` agrees with the standard `Multiset.foldr`, and the commutativity argument degenerates to a trivial instance-derived proof.
- **List coercion**: When `s` is a list cast to a multiset, the result equals `List.foldr f b l` for that list, confirming representational independence.
- **Duplicate elements**: Elements may appear more than once; each occurrence is folded separately. The pairwise condition is on the underlying set `{x | x ∈ s}`, so duplicates of the same value are not required to commute with themselves (the condition is reflexivity-free in the Pairwise sense, but the supplied proof uses a reflexive extension internally).

## Not to be confused with

- `Multiset.foldr`: the standard fold requiring a globally left-commutative function; `VTask.noncommFoldr` weakens this to a local, element-specific commutativity hypothesis.
- `Multiset.noncommProd` / `Finset.noncommProd`: analogous constructions for a multiplicative monoid structure where `f` is the group multiplication and the accumulator is the identity element, rather than an arbitrary fold with a seed.
- `List.foldr`: a fold over an *ordered* list requiring no commutativity at all; `VTask.noncommFoldr` lifts this to unordered multisets by demanding just enough commutativity to make the order irrelevant.