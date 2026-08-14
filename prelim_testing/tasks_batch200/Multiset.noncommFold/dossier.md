## Object

`VTask.noncommFold op s comm a` computes the fold (aggregate) of a multiset `s` under an associative binary operation `op`, starting from an initial accumulator value `a`, given only that `op` is commutative *pairwise on the elements of `s`* — not necessarily globally commutative. The result is the same element you would get by arranging the elements of `s` in any order, applying `op` from right to left, with `a` as the rightmost term. Because only pairwise commutativity within `s` is assumed, this generalises the ordinary multiset fold while still being well-defined (independent of the representative list chosen for `s`).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.noncommFold : {α : Type u_3} -> (op : α → α → α) -> [assoc : Std.Associative op] -> (s : Multiset α) -> (comm : {x | x ∈ s}.Pairwise fun x y => op x y = op y x) -> α → α
<!-- PINNED-SIGNATURE:END -->


`VTask.noncommFold : {α : Type u_3} -> (op : α → α → α) -> [assoc : Std.Associative op] -> (s : Multiset α) -> (comm : {x | x ∈ s}.Pairwise fun x y => op x y = op y x) -> α → α`

The implicit type argument `α` is the carrier type of the elements being combined. `op` is the associative binary operation used to combine elements; it is required to be associative via the instance argument `assoc`. `s` is the multiset of elements to be folded. `comm` is a proof that `op` is pairwise commutative on the members of `s`: for any two distinct elements `x` and `y` that both belong to `s`, we have `op x y = op y x`. The final argument is the initial accumulator value from which folding begins (playing the role of a "base" or "identity" in the computation).

## Conventions

Folding the empty multiset ignores all elements and returns the initial accumulator unchanged. When `op` is globally (fully) commutative, `VTask.noncommFold` coincides with the ordinary `Multiset.fold`. The pairwise-commutativity hypothesis is only needed to prove well-definedness; the fold is computed as a right fold over some representative list of `s`.

## Worked examples

- Claim: Folding the empty multiset with any associative operation and any initial value `a` returns `a`.

- Claim: `VTask.noncommFold op {1, 2, 3} comm 0 = op 1 (op 2 (op 3 0))` when `op` is integer addition (which is fully commutative and associative), so `noncommFold` agrees with folding the list `[1, 2, 3]` right-to-left from `0`, giving `1 + (2 + (3 + 0)) = 6`.

- Claim: For a singleton multiset `{a}`, `VTask.noncommFold op {a} comm x = op a x` for any initial value `x`, since the only element is `a` and there are no pairs to check for commutativity.

- Claim: When `op` is globally commutative, `VTask.noncommFold op s (fun x _ y _ _ => comm x y) a = Multiset.fold op a s` for all `s` and `a`.

## Boundaries

- **Empty multiset**: `VTask.noncommFold op 0 h a = a` for any `h` and any initial value `a`; the pairwise commutativity hypothesis is vacuously satisfied and the accumulator is returned unchanged.
- **Singleton multiset**: `VTask.noncommFold op {x} h a = op x a`; the pairwise condition is vacuous (no two distinct elements) so any proof suffices.
- **Cons decomposition**: `VTask.noncommFold op (a ::ₘ s) h x = op a (VTask.noncommFold op s h' x)` where `h'` is the restriction of `h` to `s`.
- **Commutativity hypothesis is membership-local**: the proof `comm` need only cover pairs from `s`; globally non-commutative operations are allowed as long as their elements from `s` happen to commute pairwise.
- **Initial accumulator is mandatory**: unlike some fold variants that work on non-empty structures, this fold always requires an explicit initial value `a` of type `α`.

## Not to be confused with

- `Multiset.fold`: the ordinary multiset fold requiring global commutativity of `op` as a typeclass instance, rather than the weaker pairwise condition on `s`.
- `VTask.noncommFoldr`: the heterogeneous analogue that folds a multiset `α` into a different type `β`; `VTask.noncommFold` is the homogeneous special case where input and output share the same type `α`.
- `List.foldl` / `List.foldr`: list folds that are order-dependent and do not require any commutativity, operating on an ordered list rather than an unordered multiset.