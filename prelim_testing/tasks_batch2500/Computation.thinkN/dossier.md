## Object

`VTask.thinkN c n` is a **delayed computation**: given a computation `c` of type `α` and a natural number `n`, it produces a new computation that first idles for exactly `n` time steps ("ticks") and then behaves exactly like `c`. In the vocabulary of coinductive computation sequences, prepending `n` "think" (delay) steps to `c` yields `thinkN c n`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.thinkN : {α : Type u} -> (c : Computation α) -> ℕ → Computation α
<!-- PINNED-SIGNATURE:END -->


`VTask.thinkN : {α : Type u} -> (c : Computation α) -> ℕ → Computation α`

The implicit type parameter `α` is the result type of the computation. The first explicit argument `c` is the base computation whose execution is to be deferred. The second argument is the number of ticks of delay to prepend; zero delay returns the original computation unchanged.

## Conventions

When the delay count is `0`, the result is definitionally equal to the original computation `c` with no delay added. When the delay count is `n + 1`, the result is one additional "think" step wrapping the computation with `n` delays already applied — so the delays are added one at a time starting from the outermost layer.

## Worked examples

- Claim: `VTask.thinkN c 0 = c` for any computation `c` — zero ticks of delay is the identity.

- Claim: `VTask.thinkN c 1` is the computation that thinks for one tick and then runs `c`; it equals `Computation.think c`.

- Claim: Composing delays is additive: `VTask.thinkN (VTask.thinkN c m) n = VTask.thinkN c (m + n)` — prepending `n` delays to a computation that already has `m` delays prepended gives a total of `m + n` delays before `c` runs.

- Claim: `VTask.thinkN c 3` equals three nested `think` applications around `c`, i.e., `Computation.think (Computation.think (Computation.think c))`.

## Boundaries

- At `n = 0`: The function is the identity; `thinkN c 0 = c` exactly, with no wrapping.
- At `n = 1`: Exactly one `think` is prepended; `thinkN c 1 = think c`.
- The function is total for all natural numbers `n`; there is no upper bound on the delay count.
- Because `α` is a `Type u`, the construction works uniformly for any type, including `Unit` (for side-effectful computations whose result is trivial).
- Termination of the underlying computation `c` is unaffected in principle — `thinkN` merely shifts when the computation's steps are observed, not whether they eventually terminate.

## Not to be confused with

- `Computation.think`: Prepends exactly **one** tick of delay, whereas `thinkN` prepends an arbitrary natural-number count of ticks.
- `Computation.pure` / `Computation.return`: Produces a computation that **immediately** returns a value with zero delay; `thinkN` with nonzero `n` is specifically non-immediate.
- Iteration or looping constructs on computations: `thinkN` adds a fixed finite delay, not an infinite loop or a data-dependent number of steps.