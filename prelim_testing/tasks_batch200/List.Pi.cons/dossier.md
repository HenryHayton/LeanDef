## Object

`VTask.cons` constructs a dependent function over a cons-extended list. Given a type family `α` indexed by `ι`, a head element `i : ι`, a tail list `l : List ι`, a witness `a : α i` at the head, and a dependent function `f` that assigns a term of type `α j` to every `j` occurring in `l`, `VTask.cons i l a f` produces a new dependent function `g` such that for every `j` with a proof that `j ∈ i :: l`, we have `g j : α j`. Concretely, `g` returns `a` (suitably transported) when `j = i`, and delegates to `f` when `j` is found in the tail `l`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cons : {ι : Type u_1} -> [DecidableEq ι] -> {α : ι → Sort u_2} -> (i : ι) -> (l : List ι) -> (a : α i) -> (f : (j : ι) → j ∈ l → α j) -> (j : ι) -> j ∈ i :: l → α j
<!-- PINNED-SIGNATURE:END -->


`VTask.cons : {ι : Type u_1} -> [DecidableEq ι] -> {α : ι → Sort u_2} -> (i : ι) -> (l : List ι) -> (a : α i) -> (f : (j : ι) → j ∈ l → α j) -> (j : ι) -> j ∈ i :: l → α j`

- `ι` is the implicit index type over which the type family is parameterised.
- The `DecidableEq ι` instance is required so that membership in the cons-list can be decided by comparing indices.
- `α` is the implicit dependent type family mapping each index `i : ι` to a type (or sort).
- `i` is the head index being prepended to the list.
- `l` is the tail list of indices.
- `a` is the term of type `α i` that the resulting function should return at the head index.
- `f` is the existing dependent function over the tail `l`, supplying a term of `α j` for each `j ∈ l`.
- The final two arguments `j` and a proof `j ∈ i :: l` are the index and membership witness at which the resulting function is evaluated; they are produced when the function is applied.

## Conventions

When the query index `j` is definitionally equal to `i`, the function returns `a` (with a type-equality transport if needed); when `j ≠ i`, membership in `i :: l` is resolved to membership in `l` and `f` is consulted. No special junk values are declared for inputs outside any intended range, because the function is total over all `j ∈ i :: l`.

## Worked examples

- Claim: For `ι = Nat`, `α = fun _ => Bool`, `i = 0`, `l = [1]`, `a = true`, and `f` mapping `1` to `false`, evaluating `VTask.cons 0 [1] true f` at index `0` with proof `0 ∈ [0, 1]` yields `true`.

- Claim: For the same setup, evaluating `VTask.cons 0 [1] true f` at index `1` with proof `1 ∈ [0, 1]` yields `false` (the value supplied by `f`).

- Claim: For `ι = Fin 3`, `α = fun k => Fin (k.val + 1)`, `i = ⟨2, by omega⟩`, `l = []`, `a = ⟨0, by omega⟩`, the resulting function from `VTask.cons` has domain `{j | j ∈ [⟨2, _⟩]}` and at the single element returns a term of type `Fin 3`.

## Boundaries

- If `l = []`, the resulting function has domain `{j | j ∈ [i]}`, which contains only `i`; the tail function `f` is vacuous (it has type `∀ j ∈ [], α j`) and is never called.
- If `i` already appears in `l` (i.e. the list has a duplicate), membership `j ∈ i :: l` for `j = i` is still handled by the head case; the duplicate occurrence in the tail is reachable via `f` but the head case takes priority when `j = i`.
- The function is well-typed at every `j` that has a proof of `j ∈ i :: l`; there is no undefined or junk behaviour within this domain.
- The `DecidableEq` instance is essential: without the ability to decide equality of indices, the case split on `j = i` vs `j ≠ i` cannot be performed computationally.

## Not to be confused with

- `Multiset.Pi.cons`: the analogous construction for multisets rather than lists; `VTask.cons` is the list-specific version and is in fact defined via the multiset version.
- `List.Pi.empty` (or the empty dependent function over `[]`): the base case of the same construction, producing a function over an empty list rather than extending one.
- `Pi.cons` from `Finset`-based dependent products: a similar cons operation but for `Finset`-indexed dependent functions, not `List`-indexed ones.