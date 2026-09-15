## Object

`VTask.fixInduction` is a recursion/elimination principle for `PFun.fix`, the fixed-point operator on partial functions. Given a partial function `f : α →. β ⊕ α` that iterates by outputting either a final answer `Sum.inl b` or a new seed `Sum.inr a'`, and given that `b` is indeed the eventual fixed-point output starting from seed `a`, `VTask.fixInduction` constructs a value of a motive `C a` by well-founded recursion along the iteration trace. In effect it says: to build `C a` for any `a` from which `f` eventually reaches `b`, it suffices to show how to build `C a'` for every `a'` reachable from `a`, assuming `C` is already established for every immediately next seed produced by `f` at `a'`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.fixInduction : {α : Type u_1} -> {β : Type u_2} -> {C : α → Sort u_7} -> {f : α →. β ⊕ α} -> {b : β} -> {a : α} -> (h : b ∈ f.fix a) -> (H : (a' : α) → b ∈ f.fix a' → ((a'' : α) → Sum.inr a'' ∈ f a' → C a'') → C a') -> C a
<!-- PINNED-SIGNATURE:END -->


`{α : Type u_1} -> {β : Type u_2} -> {C : α → Sort u_7} -> {f : α →. β ⊕ α} -> {b : β} -> {a : α} -> (h : b ∈ f.fix a) -> (H : ...) -> C a`

- `α` is the type of seeds (the recursive state space).
- `β` is the type of final outputs.
- `C` is the motive: a type family over seeds whose values we want to construct.
- `f` is the underlying partial function driving the iteration; at each seed it either halts with a `β`-value or produces a new seed.
- `b` is the specific final output whose membership in the fixed-point is being tracked.
- `a` is the starting seed about which we want to conclude `C a`.
- `h` is the evidence that `b` is indeed the fixed-point output of `f` starting from `a`; it certifies that the iteration terminates and reaches `b`.
- `H` is the step function: given any seed `a'` from which `b` is reachable (i.e., `b ∈ f.fix a'`), and given the inductive hypothesis that `C a''` holds for every immediate successor seed `a''` of `a'` (any `a''` with `Sum.inr a'' ∈ f a'`), `H` produces `C a'`.

The result is a term of type `C a`, constructed by structural recursion on the termination evidence for the iteration.

## Conventions

No junk-value or out-of-domain conventions are declared for this definition: the function is total on its stated inputs—the hypothesis `h : b ∈ f.fix a` already rules out non-terminating or divergent traces by construction, so there is no meaningful junk-value regime to specify.

## Worked examples

- Claim: `VTask.fixInduction` unfolds according to `fixInduction_spec`: for any `a`, `h`, and step function `H`, the result equals `H a h (fun a'' ha'' => VTask.fixInduction (PFun.fix_fwd h ha'') H)`. This is the key unfolding equation showing the recursion is well-founded and each immediate successor provides a strictly smaller subproblem.

- Claim: When `f` is a simple one-step function that immediately outputs `Sum.inl b` from `a`, and `C a = True` for all `a`, `VTask.fixInduction` applied to that trivial step function yields `trivial : True`. In particular, the step function `H` need only use the base case of its continuation (the continuation for immediate successors is vacuously provided but never called).

- Claim: If `f` counts down from a natural number, halting at 0 and stepping to `n-1` otherwise, then `VTask.fixInduction` on the trace from `n` to `0` gives the `C n` value by composing `n` applications of the step function `H`, one per iteration step.

## Boundaries

- The hypothesis `h : b ∈ f.fix a` is essential: without it the iteration might not terminate and the well-founded recursion would have no base. There is no version of this principle for diverging traces.
- If `f a` is undefined (i.e., `f a = ⊥` as a partial value), then `f.fix a` is also undefined, so `h` cannot be provided and the principle is inapplicable.
- The step function `H` is called once per node in the unfolding trace from `a` to the final halting state; in particular for a one-step computation it is called exactly once.
- The motive `C` lives in `Sort u_7`, so the principle applies equally to propositions (`Prop`), types (`Type`), and higher universes.

## Not to be confused with

- `PFun.fixInduction'` — a variant with separate base-case and inductive-step arguments (splitting the `H` function into two), rather than a single combined step function.
- `PFun.fix` — the fixed-point operator itself, which merely computes the output; `VTask.fixInduction` is the associated elimination/recursion principle, not the operator.
- `WellFounded.recursion` / `Acc.rec` — the general well-founded recursion primitives; `VTask.fixInduction` specialises these to the specific accessibility relation induced by `f`'s iteration steps (`Sum.inr a'' ∈ f a'`).
