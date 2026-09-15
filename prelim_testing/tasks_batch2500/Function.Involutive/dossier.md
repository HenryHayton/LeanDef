## VTask.Involutive

### Object

A function `f : α → α` is *involutive* if applying it twice returns the original input: `f(f(x)) = x` for every `x`. Geometrically, `f` is its own inverse — a self-inverse map. Classic examples include negation on integers, logical negation on booleans, matrix transposition, and reflection about a hyperplane.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Involutive : {α : Sort u_1} -> (f : α → α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.Involutive : {α : Sort u_1} -> (f : α → α) -> Prop`

The implicit type argument `α` is the type on which the function acts; `f` is the endofunction whose involutivity is being asserted.

### Conventions

No special junk-value or edge conventions are declared: the predicate is a universally quantified proposition over all elements of `α`, and is simply vacuously true (via the universal quantifier) when `α` is empty.

### Worked examples

- Claim: Boolean negation `not : Bool → Bool` is involutive (since `¬¬b = b` for all `b : Bool`).

- Claim: The identity function `id : α → α` is involutive for any type `α`, because `id(id(x)) = x`.

- Claim: The function `fun (n : Int) => -n` is involutive, since negating an integer twice yields the original integer.

- Claim: If `f` is involutive then it is bijective, because it is its own two-sided inverse, hence an equivalence.

### Boundaries

- When `α` is the empty type, the universal quantifier ranges over no elements, so every endofunction on the empty type is vacuously involutive.
- The constant function `fun _ => c` is involutive on a type only when `c` is a fixed point of itself, i.e., `f(c) = c`, meaning only when the type is a singleton `{c}`.
- Involutivity is a strictly stronger condition than having order dividing 2; it coincides with it for the action on elements, but also pinpoints that there are *no other* elements in an orbit.
- A function can be involutive on a `Sort` (not just `Type`), so `α` ranges over propositions as well.

### Not to be confused with

- **`Function.IsInvolution`** (if present elsewhere): same mathematical notion but potentially with a different name or universe constraint — check the precise spelling.
- **`Function.Idempotent`**: the condition `f(f(x)) = f(x)` for all `x`, which is *not* the same as involutivity (`f(f(x)) = x`) unless `f = id`.
- **`Equiv`** (or self-inverse equivalences): an `Equiv` with `e.symm = e` packages involutivity into a bundled structure, whereas `VTask.Involutive` is the bare unbundled proposition.