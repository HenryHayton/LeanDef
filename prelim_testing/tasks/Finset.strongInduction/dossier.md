## Object

`VTask.strongInduction` is a **strong induction principle for finite sets**. Given a motive `p` (a type or proposition indexed by finsets), and a step function `H` that produces a value of type `p s` for any finset `s` whenever values of `p t` are already available for every proper subset `t ⊊ s`, the combinator manufactures a value of `p s` for *every* finset `s`. The recursion bottoms out naturally at the empty set (which has no proper subsets, so `H` fires with a vacuously-true hypothesis). The scheme is well-founded because every proper subset has strictly smaller cardinality.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.strongInduction : {α : Type u_1} -> {p : Finset α → Sort u_4} -> (H : (s : Finset α) → ((t : Finset α) → t ⊂ s → p t) → p s) -> (s : Finset α) -> p s
<!-- PINNED-SIGNATURE:END -->


`VTask.strongInduction : {α : Type u_1} -> {p : Finset α → Sort u_4} -> (H : (s : Finset α) → ((t : Finset α) → t ⊂ s → p t) → p s) -> (s : Finset α) -> p s`

The implicit type parameter `α` is the element type of the finsets being inducted over. The implicit `p` is the motive — a family of types (or propositions) indexed by `Finset α`, expressing what is to be constructed or proved for each finset. The explicit argument `H` is the inductive step: a function that, given a finset `s` together with a "recursive oracle" supplying `p t` for every strict subset `t ⊊ s`, produces `p s`. The final explicit argument `s` is the specific finset at which the result is evaluated.

## Conventions

No special junk-value or boundary conventions are declared: the function is total and well-typed for all inputs; in particular, when `s` is the empty set, the oracle argument of `H` is called with an empty domain (no `t` satisfies `t ⊊ ∅`), so `H` receives a vacuously-applicable function and must produce `p ∅` from it alone.

## Worked examples

- Claim: Applying `VTask.strongInduction` unfolds to one call of `H` at `s`, with the recursive oracle being `VTask.strongInduction H` restricted to proper subsets — i.e., `VTask.strongInduction H s = H s (fun t _ => VTask.strongInduction H t)` for every `s`.

- Claim: One can use `VTask.strongInduction` to prove that every finset either is empty or has a nonempty proper subset chain bottoming out at `∅` — the base case (`s = ∅`) is handled by `H` receiving an oracle that is never invoked, and each inductive case reduces to strictly smaller finsets.

- Claim: Taking `p` to be a `Prop` and `H` to assert a property that follows from the same property on all proper subsets, `VTask.strongInduction H` yields a proof of `p s` for every `s : Finset α`, with the proof of `p ∅` produced by `H ∅` (whose oracle is vacuously applicable).

## Boundaries

- **Empty set**: `∅ : Finset α` has no proper subsets, so the oracle passed to `H ∅` maps an empty domain. The step function `H` must be able to produce `p ∅` using only this vacuous information — this is the true base case of the induction.
- **Singleton sets**: `{a}` has only one proper subset, namely `∅`, so the oracle available to `H {a}` delivers only `p ∅`.
- **Equality of cardinalities**: Two distinct finsets of the same cardinality are independent of each other in the inductive order; neither is a proper subset of the other, so neither can appear in the oracle of the other.
- **Universe polymorphism**: The motive `p` lives in an arbitrary `Sort u_4`, so `VTask.strongInduction` can be used both to construct data and to prove propositions.

## Not to be confused with

- `Finset.strongInductionOn`: a flipped variant where the finset argument comes before `H`, useful for term-mode proofs in a different stylistic convention.
- `Nat.strongRecOn` / `Nat.strongInduction`: strong induction over natural numbers by `<`, not over the subset relation on finsets.
- `Finset.induction`: ordinary (non-strong) structural induction on finsets, which only gives `p s` from `p (s \ {a})` rather than from all proper subsets simultaneously.