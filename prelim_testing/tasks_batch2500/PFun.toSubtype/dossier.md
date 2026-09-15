## Object

`VTask.toSubtype p f` is the partial function from `α` to the subtype `{b : β // p b}` that, given an input `a : α`, is defined (returns a value) precisely when `p (f a)` holds, and when defined yields the element `f a` packaged as a member of the subtype.

In other words, it lifts an ordinary total function `f : α → β` to a partial function targeting those elements of `β` satisfying the predicate `p`, with the domain of partiality being exactly the pre-image of `p` under `f`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.toSubtype : {α : Type u_1} -> {β : Type u_2} -> (p : β → Prop) -> (f : α → β) -> α →. Subtype p
<!-- PINNED-SIGNATURE:END -->


VTask.toSubtype : {α : Type u_1} -> {β : Type u_2} -> (p : β → Prop) -> (f : α → β) -> α →. Subtype p

The type parameters `α` and `β` are the source and target types, inferred implicitly. The argument `p` is the predicate on `β` that carves out the subtype; it determines which outputs of `f` are considered valid. The argument `f` is the underlying total function from `α` to `β` whose image is being restricted by `p`.

## Conventions

No special junk-value or edge-case conventions are declared for this definition: the partiality is entirely governed by whether `p (f a)` holds for a given input `a`, and no artificial default or fallback value is assigned when it does not hold.

## Worked examples

- Claim: For `f : ℕ → ℕ` defined by `f n = n` and `p n = (n = 3)`, the partial function `VTask.toSubtype p f` is defined at input `3` (i.e., `(VTask.toSubtype p f).Dom 3` holds).

- Claim: For `f : ℕ → ℕ` defined by `f n = n` and `p n = (n = 3)`, the partial function `VTask.toSubtype p f` is not defined at input `5` (i.e., `¬ (VTask.toSubtype p f).Dom 5`).

- Claim: For `f : ℕ → ℤ` defined by `f n = (n : ℤ)` and `p z = (0 ≤ z)`, the domain of `VTask.toSubtype p f` is all of `ℕ`, since every natural number maps to a non-negative integer.

## Boundaries

- When `p` is the always-true predicate (`fun _ => True`), the partial function is defined everywhere and every input yields a value; the resulting partial function is effectively total.
- When `p` is the always-false predicate (`fun _ => False`), the partial function has an empty domain and is nowhere defined.
- The subtype `{b : β // p b}` is not inhabited by any default value for elements where `p` fails; the partial function simply has no value there.
- If `f` is a constant function `fun _ => c`, then the domain of the resulting partial function is either all of `α` (if `p c` holds) or empty (if `p c` does not hold).

## Not to be confused with

- `PFun.restrict`: restricts the domain of an already-partial function by an additional condition, rather than constructing a partial function from a total one and a predicate on the codomain.
- `Set.codRestrict` / `Subtype.coind`: these produce a *total* function into a subtype by requiring a proof that the image lies in the subtype for *all* inputs, rather than yielding a partial function whose domain is where the condition holds.
- `PFun.lift`: lifts a total function to a partial function that is always defined, without restricting to a subtype.