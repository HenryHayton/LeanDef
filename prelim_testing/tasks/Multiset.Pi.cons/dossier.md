## Object

`VTask.cons` constructs a dependent function over a multiset obtained by prepending one element. Concretely, given a type-family `δ` indexed by `α`, a multiset `m`, a distinguished element `a : α`, a value `b : δ a` for that element, and a function `f` that produces a `δ a'`-value for every `a'` already in `m`, `VTask.cons m a b f` is a new function that produces a `δ a'`-value for every `a'` in the extended multiset `a ::ₘ m`. When queried at `a` itself, it returns `b`; when queried at any other element already in `m`, it delegates to `f`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cons : {α : Type u_1} -> [DecidableEq α] -> {δ : α → Sort u_2} -> (m : Multiset α) -> (a : α) -> (b : δ a) -> (f : (a : α) → a ∈ m → δ a) -> (a' : α) -> a' ∈ a ::ₘ m → δ a'
<!-- PINNED-SIGNATURE:END -->


`VTask.cons : {α : Type u_1} -> [DecidableEq α] -> {δ : α → Sort u_2} -> (m : Multiset α) -> (a : α) -> (b : δ a) -> (f : (a : α) → a ∈ m → δ a) -> (a' : α) -> a' ∈ a ::ₘ m → δ a'`

- `α` is the index type; it is implicit and inferred from context.
- The `DecidableEq α` instance is required to decide, for any query element `a'`, whether `a' = a`.
- `δ` is the dependent type-family assigning a sort to each element of `α`; it is implicit.
- `m` is the base multiset before prepending.
- `a` is the element being prepended to `m`.
- `b` is the value of type `δ a` that the resulting function returns when queried at `a`.
- `f` is the existing dependent function over `m`, supplying values for all members of `m`.
- `a'` is the element at which the resulting function is being evaluated.
- The final argument is the proof that `a'` belongs to `a ::ₘ m`, which is needed to obtain a well-typed result.

## Conventions

When `a' = a`, the function returns `b`, ignoring `f` entirely even if `a` also happens to lie in `m`. In other words, the freshly provided value `b` takes priority over any value `f` might supply for `a`.

## Worked examples

- Claim: Evaluating `VTask.cons m a b f` at `a` (with the canonical membership proof) always returns `b`, regardless of what `f` says.
  (This is the content of `cons_same`: `VTask.cons m a b f a h = b` for any proof `h : a ∈ a ::ₘ m`.)

- Claim: Evaluating `VTask.cons m a b f` at an element `a'` different from `a`, with `h' : a' ∈ a ::ₘ m` and `h : a' ≠ a`, returns the same value as `f a'` applied to the derived membership proof `(mem_cons.1 h').resolve_left h`.
  (This is the content of `cons_ne`.)

- Claim: Swapping two consecutive `VTask.cons` calls for distinct elements `a ≠ a'` produces extensionally equal functions over the larger multiset.
  (This is `cons_swap`: the two orders of prepending agree on all query elements.)

- Claim: If `g : ∀ a' ∈ a ::ₘ m, δ a'` is any dependent function over `a ::ₘ m`, then `VTask.cons m a (g a (mem_cons_self a m)) (fun a' ha' => g a' (mem_cons_of_mem ha'))` equals `g`.
  (This is `cons_eta`: every such function is in the image of `VTask.cons`.)

## Boundaries

- If `a` already appears in `m`, the function is still well-defined; when queried at `a`, it always returns `b` (the new value), never the value `f` would give. No error or ambiguity arises.
- If `m` is the empty multiset, then `f` has an empty domain and the result is a function over the singleton multiset `{a}`, returning `b` for the sole query `a' = a`.
- The membership proof passed as the final argument is required for dependent-type reasons but does not otherwise influence the result; two calls with different proofs of the same membership yield the same value (proof-irrelevance of membership holds for multisets).
- The function is injective in `f` when `a ∉ m` (theorem `cons_injective`), but not necessarily otherwise.

## Not to be confused with

- `Multiset.Pi.empty`: provides a dependent function over the *empty* multiset; `VTask.cons` extends such a base case by one element.
- `List.Pi.cons` or function extension for lists: similar in spirit but operates on lists rather than multisets, so order matters there.
- Plain `Multiset.cons` (`a ::ₘ m`): that operation prepends an element to a multiset of elements, whereas `VTask.cons` prepends a *point-value pair* to a dependent function over a multiset.