## 1. Object

A *partial bijection* (PEquiv) between types `α` and `β` that maps exactly one element to one element: the forward direction sends `a` to `b` and everything else to `none`; the backward direction sends `b` to `a` and everything else to `none`. It is the smallest possible PEquiv connecting two specific elements.

## 2. Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.single : {α : Type u} -> {β : Type v} -> [DecidableEq α] -> [DecidableEq β] -> (a : α) -> (b : β) -> α ≃. β
<!-- PINNED-SIGNATURE:END -->


The first two implicit type arguments are the domain type `α` and the codomain type `β`, which may be different types. The two instance arguments supply decidable equality for `α` and `β`, needed to compare elements with `a` and `b` respectively. The explicit argument `a : α` is the single element in the domain that is in scope; the explicit argument `b : β` is the single element in the codomain that is in scope. The result is a partial bijection `α ≃. β`.

## 3. Conventions

Every input in `α` other than `a` maps to `none` under the forward function; every input in `β` other than `b` maps to `none` under the inverse function. There are no further junk-value conventions declared for this definition.

## 4. Worked examples

- Claim: `VTask.single 1 2` applied to `1` returns `some 2`.
  ```lean
  example : VTask.single 1 2 1 = some 2 := by decide
  ```

- Claim: `VTask.single 1 2` applied to `3` (which is not `1`) returns `none`.
  ```lean
  example : VTask.single 1 2 3 = none := by decide
  ```

- Claim: The symmetry (inverse) of `VTask.single a b` is `VTask.single b a`.

- Claim: Composing `VTask.single a b` with `VTask.single b c` gives `VTask.single a c`.

- Claim: Composing `VTask.single a b₁` with `VTask.single b₂ c` where `b₁ ≠ b₂` gives the empty/bottom PEquiv.

- Claim: When `α` is a subsingleton, `VTask.single a b` equals the identity PEquiv `PEquiv.refl α`.

## 5. Boundaries

- When `a` is the only element of `α` (i.e., `α` is a subsingleton), `VTask.single a b` collapses to the reflexive/identity PEquiv on `α`, because all elements of `α` are equal to `a`.
- When `α = β` and `a = b`, `VTask.single a a` is a valid (partial) identity on the singleton `{a}` — it still returns `none` for all inputs other than `a`.
- The bottom PEquiv `⊥` results from composing `VTask.single a b` with any PEquiv `f` such that `f b = none`, and similarly on the other side.
- The membership predicate `b ∈ VTask.single a b a` always holds, confirming the core mapping is always defined.

## 6. Not to be confused with

- `PEquiv.refl α`: the identity PEquiv that sends *every* element of `α` to itself; `VTask.single` only covers one pair.
- `Equiv.swap i j`: a total bijection that transposes two elements and fixes all others; `VTask.single` is a *partial* map that is undefined everywhere except at `a`.
- `Pi.single`: a function returning a value at one index and a default (typically zero) elsewhere; not a partial bijection and not related to `α ≃. β`.