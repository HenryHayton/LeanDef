## Object

`VTask.orElse c₁ c₂` is a **racing combinator** on possibly-non-terminating computations. Given two computations `c₁` and `c₂` over the same result type `α`, it runs both in lock-step (one step of each per round) and returns the result of whichever one produces a value first. If both produce a value in the same round, `c₁`'s result wins. If neither computation ever terminates, the combined computation also diverges.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.orElse : {α : Type u} -> (c₁ : Computation α) -> (c₂ : Unit → Computation α) -> Computation α
<!-- PINNED-SIGNATURE:END -->


VTask.orElse : {α : Type u} -> (c₁ : Computation α) -> (c₂ : Unit → Computation α) -> Computation α

The implicit type argument `α` is the type of values both computations may eventually produce. `c₁` is the first (left) computation; it is given priority if both yield a result simultaneously. `c₂` is the second (right) computation, wrapped under a `Unit` arrow to allow for lazy evaluation (reflecting the `OrElse` typeclass convention in Lean 4); it is forced immediately when `orElse` is called.

## Conventions

The second argument `c₂` is a thunk (`Unit → Computation α`) purely to satisfy the `OrElse` typeclass interface; it is evaluated eagerly (forced with `()`) at the point `orElse` is invoked, so there is no meaningful laziness in practice — both computations are live from the first step.

When both computations produce a result in the very same step, `c₁`'s result is returned, giving `c₁` priority over `c₂`.

## Worked examples

- Claim: If `c₁` terminates immediately with value `a`, then `VTask.orElse c₁ c₂ = pure a` regardless of `c₂`.

- Claim: If `c₁` is `empty` (never terminates), then `VTask.orElse c₁ (fun _ => c₂) = c₂` for any `c₂`.

- Claim: If both computations are `think`-wrapped, the result is `think` of their race: `VTask.orElse (think c₁) (fun _ => think c₂) = think (VTask.orElse c₁ (fun _ => c₂))`.

- Claim: If `c₁ = think c₁'` and `c₂ = pure a`, then `VTask.orElse c₁ (fun _ => c₂) = pure a`, meaning a ready right-hand computation beats a delayed left-hand one.

## Boundaries

- If `c₁` terminates immediately (`pure a`), the result is immediately `pure a`; `c₂` is never inspected beyond its initial forcing.
- If `c₁` is `empty` (diverges), the result is exactly `c₂ ()`, as confirmed by `empty_orElse`.
- If `c₂ ()` is `empty` (diverges), the result is exactly `c₁`, as confirmed by `orElse_empty`.
- If both computations diverge, the combined computation diverges.
- The combinator is **not** symmetric in general: simultaneous results favor `c₁`.

## Not to be confused with

- `Computation.bind`: sequences two computations (the second depends on the result of the first), rather than racing them in parallel.
- `Computation.think`: wraps a single computation in one unit of delay; it does not combine two computations.
- `Option.orElse` / `OrElse` on plain `Option`: a purely synchronous fallback with no notion of steps or divergence.