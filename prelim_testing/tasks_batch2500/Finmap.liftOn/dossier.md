## Object

`VTask.liftOn` takes a finite map (a `Finmap`) and a function defined on association lists (`AList`), and evaluates that function at a representative association list for the finite map. Because a `Finmap` is an equivalence class of association lists under reordering of their entries, the function must agree on all permuted representatives; `VTask.liftOn` then produces a well-defined value in the target type.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.liftOn : {α : Type u} -> {β : α → Type v} -> {γ : Type u_1} -> (s : Finmap β) -> (f : AList β → γ) -> (H : ∀ (a b : AList β), a.entries.Perm b.entries → f a = f b) -> γ
<!-- PINNED-SIGNATURE:END -->


VTask.liftOn : {α : Type u} -> {β : α → Type v} -> {γ : Type u_1} -> (s : Finmap β) -> (f : AList β → γ) -> (H : ∀ (a b : AList β), a.entries.Perm b.entries → f a = f b) -> γ

- `α` is the key type, implicit.
- `β` is the value type family indexed by keys, implicit.
- `γ` is the target type of the lifted function, implicit.
- `s` is the finite map being evaluated.
- `f` is the function on association lists whose lift is desired.
- `H` is the proof that `f` respects permutations of entries, i.e., it returns the same value on any two `AList`s whose underlying entry lists are permutations of one another.

## Conventions

The function `f` is required to be permutation-invariant on association-list entries, and this invariance is encoded by the hypothesis `H`. There are no junk values or out-of-domain conventions: the function is well-defined for every `Finmap` and every permutation-respecting `f`.

## Worked examples

- Claim: Evaluating `VTask.liftOn` on the `Finmap` obtained by quotienting an `AList` `s` yields the same result as applying `f` directly to `s`. Formally, for any `s : AList β`, `f`, and `H`, `VTask.liftOn ⟦s⟧ f H = f s`.

- Claim: If `f` is the function that returns the list of keys of an `AList`, then `VTask.liftOn s f H` computes the keys of `s` as an association list, and this is independent of which permuted representative of `s` is chosen, since key-sets are permutation-invariant.

- Claim: If two `AList`s `a` and `b` satisfy `a.entries.Perm b.entries`, then `VTask.liftOn ⟦a⟧ f H = VTask.liftOn ⟦b⟧ f H`, because `⟦a⟧ = ⟦b⟧` as `Finmap` values and `f` is permutation-respecting.

## Boundaries

- The function is defined for every `Finmap`, including the empty finite map. For the empty `Finmap` (quotient of the empty `AList`), `VTask.liftOn` simply applies `f` to the empty association list.
- The hypothesis `H` is checked only on pairs of association lists whose entries are permutations of each other; no other constraint is placed on `f`.
- The output type `γ` is unrestricted; in particular, `γ` may itself be a `Prop`, a `Type`, or any other sort.

## Not to be confused with

- `VTask.liftOn₂`: the two-argument version, lifting a function of two `AList`s to a function of two `Finmap`s.
- `Quotient.liftOn`: the general quotient lifting operation; `VTask.liftOn` is the specialised version for `Finmap`, handling the additional no-duplicate-keys invariant automatically.
- `AList` function application directly: calling `f` on an `AList` does not require the permutation-invariance proof, but also does not yield a result that is independent of entry ordering.