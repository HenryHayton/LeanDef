## Object

`VTask.Results s a n` is a proposition that simultaneously asserts two things about a computation `s` of type `Computation α`:
1. The computation `s` terminates and its result is `a`.
2. The computation takes **exactly** `n` steps to produce that result.

Informally, it is the precise "termination certificate" for a computation: it pins down both the output value and the exact running time.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Results : {α : Type u} -> (s : Computation α) -> (a : α) -> (n : ℕ) -> Prop
<!-- PINNED-SIGNATURE:END -->


The implicit argument `α` is the type of values the computation may produce. The first explicit argument `s` is the computation being characterized. The second explicit argument `a` is the claimed result value. The third explicit argument `n` is the claimed exact number of steps after which `s` yields `a`.

## Conventions

The step count `n` is interpreted as the 0-based index at which the result first appears: a computation that produces its result immediately (without any internal delay) has `n = 0`. There are no junk-value conventions because the proposition is simply false whenever either the membership condition or the length condition fails.

## Worked examples

- Claim: `VTask.Results (Computation.pure a) a 0` holds for any value `a`, because `pure a` returns immediately in 0 steps.

- Claim: If `VTask.Results s a n` holds, then `a` is a member of `s` (i.e., `s` terminates with result `a`), because membership is the first conjunct encoded in `Results`.

- Claim: If `VTask.Results s a n` and `VTask.Results s a' n'` both hold, then `a = a'` and `n = n'`, because a deterministic computation can have at most one result and one termination time.

## Boundaries

- When `n = 0`: the computation must deliver its result immediately, with no delay steps. `pure a` is the canonical example.
- When `s` does not terminate: `VTask.Results s a n` is false for every `a` and every `n`, because the membership witness `a ∈ s` cannot be satisfied.
- The value of `n` is unique: there is exactly one step count for which a terminating computation satisfies `Results`, so the proposition can be satisfied for at most one `n` for a given `s` and `a`.
- Because `Results` is a `Prop`, it carries no computational content beyond the truth value; the existential witness is proof-irrelevant.

## Not to be confused with

- `a ∈ s` (membership alone): that predicate only asserts termination with result `a`, without saying anything about how many steps are required.
- `Computation.terminates s`: that predicate asserts mere termination of `s`, without specifying the result or the step count.
- `Computation.length s h`: that is the *function* (given a termination proof `h`) returning the number of steps, not the combined characterization proposition that `Results` provides.