## Object

`VTask.piecewise s f g` is the **piecewise-defined dependent function** that agrees with `f` at every point belonging to the set `s`, and with `g` at every point not belonging to `s`. In other words, it is the function whose value at a point `i` is determined by asking whether `i ∈ s`: if yes, it returns `f i`; if no, it returns `g i`. This is the standard construction that "glues" two functions together along a set boundary.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piecewise : {α : Type u} -> {β : α → Sort v} -> (s : Set α) -> (f g : (i : α) → β i) -> [(j : α) → Decidable (j ∈ s)] -> (i : α) -> β i
<!-- PINNED-SIGNATURE:END -->


The implicit argument `α` is the common domain type, and `β` is the (possibly dependent) codomain family. The argument `s` is the set that serves as the dividing region: points inside it are handled by `f`, points outside it by `g`. The arguments `f` and `g` are the two dependent functions to be glued — `f` is used on `s`, and `g` is used on the complement of `s`. The instance argument `[∀ j, Decidable (j ∈ s)]` provides the computational ability to decide membership in `s` at each point, which is necessary to define the function by cases. The final argument `i` is the point at which the piecewise function is being evaluated.

## Conventions

When both branches agree — i.e., `f` and `g` are the same function — `VTask.piecewise s f f` is definitionally equal to `f` regardless of what `s` is. No special junk values are defined; the function is total.

## Worked examples

- Claim: For the universal set, `VTask.piecewise Set.univ f g = f` (the piecewise function on all of the domain reduces to `f` everywhere).

- Claim: For the empty set, `VTask.piecewise ∅ f g = g` (the piecewise function on the empty set reduces to `g` everywhere, since no point belongs to `∅`).

- Claim: On a singleton `{x}`, the piecewise function equals `g` updated at `x` with the value `f x` — that is, it equals `Function.update g x (f x)`. This follows from `piecewise_singleton`.

- Claim: If `f = g`, then `VTask.piecewise s f f = f` for any `s` — the two branches being equal makes the choice of `s` irrelevant.

- Claim: For `s = Set.Iic 0` (the non-positive reals) and scalar functions on `ℝ`, the piecewise function at `−1` equals `f (−1)` since `−1 ∈ Set.Iic 0`, and at `1` equals `g 1` since `1 ∉ Set.Iic 0`.

## Boundaries

- **Universal set**: `VTask.piecewise Set.univ f g = f`, because every point satisfies membership and `g` is never invoked.
- **Empty set**: `VTask.piecewise ∅ f g = g`, because no point satisfies membership and `f` is never invoked.
- **Same function**: `VTask.piecewise s f f = f` for any `s`, since both branches return the same value.
- **Singleton set `{x}`**: the piecewise function coincides with `Function.update g x (f x)` — it is `g` everywhere except at `x`, where it takes the value `f x`.
- **Dependent codomain**: the construction works for families `β : α → Sort v`, not just simple function types, so each value `VTask.piecewise s f g i` lives in `β i`.

## Not to be confused with

- `Function.update g x v` — updates a single point `x` in `g` to value `v`; `piecewise` generalises this to an entire set rather than one point.
- `Set.indicator` — a related but non-dependent construction that multiplies a function by the characteristic function of a set (defined only for additive/zero structures); piecewise is more general, providing an arbitrary fallback function `g` rather than zero.
- `Set.ite s t t'` — the set-level analogue that forms the "if-then-else" of two *sets* based on `s`, not of two *functions*.