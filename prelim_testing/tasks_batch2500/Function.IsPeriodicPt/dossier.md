## VTask.IsPeriodicPt

### Object

A point `x` is a **periodic point of period `n`** of a self-map `f : α → α` if applying `f` exactly `n` times to `x` returns `x`. Formally, `x` is periodic of period `n` when the `n`-fold iterate of `f` fixes `x`. Note that the period `n` is allowed to be zero; no positivity requirement is built into the definition, though many theorems impose `0 < n` explicitly.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsPeriodicPt : {α : Type u_1} -> (f : α → α) -> (n : ℕ) -> (x : α) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsPeriodicPt : {α : Type u_1} -> (f : α → α) -> (n : ℕ) -> (x : α) -> Prop`

The implicit type argument `α` is the ambient type on which the dynamical system lives. The argument `f` is the self-map whose dynamics are being studied. The natural number `n` is the candidate period — the number of times `f` is composed with itself. The argument `x` is the point being tested for periodicity.

### Conventions

Every point is considered periodic of period 0 for any map, because the 0-fold iterate is the identity, so `f^[0] x = x` holds trivially for all `x`. Concretely, `VTask.IsPeriodicPt f 0 x` is always true.

### Worked examples

- Claim: Every point is a periodic point of period 0 for any map, i.e., `VTask.IsPeriodicPt f 0 x` holds for all `f` and `x`.

- Claim: The identity function on any type makes every point periodic of every period `n`, i.e., `VTask.IsPeriodicPt id n x` holds for all `n` and `x`.

- Claim: For `f : ℤ → ℤ` defined by `f x = -x`, the point `3` is periodic of period 2, because `f(f(3)) = f(-3) = 3`.

- Claim: `VTask.IsPeriodicPt f n x` if and only if the minimal period of `x` under `f` divides `n`.

### Boundaries

- **Period 0**: `VTask.IsPeriodicPt f 0 x` is unconditionally true for every `f` and every `x`, since the 0-fold iterate is the identity map.
- **Fixed points**: Any fixed point of `f` (a point where `f x = x`) is a periodic point of every period `n ≥ 0`, because all iterates return to `x`.
- **Divisibility**: A point periodic of period `n` is also periodic of period `k·n` for any natural number `k`, since `f^[k·n] x = (f^[n])^[k] x = x`.
- **Minimal period**: The smallest positive `n` for which `x` is periodic is the minimal period. For `n > 0`, `x` is periodic of period `n` exactly when the minimal period of `x` divides `n`.
- **n = 1**: Period-1 points are precisely the fixed points of `f`.

### Not to be confused with

- `Function.minimalPeriod f x`: The *smallest positive* period of `x` under `f`, a natural number rather than a predicate.
- `Function.periodicPts f`: The *set* of all points that are periodic for some positive period, i.e., points `x` with `∃ n > 0, VTask.IsPeriodicPt f n x`.
- `Function.ptsOfPeriod f n`: The *set* of points periodic of period exactly `n`, defined as `{x | VTask.IsPeriodicPt f n x}`; `VTask.IsPeriodicPt f n x` is the membership predicate for this set.
