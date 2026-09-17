## Object

`VTask.ContinuousAt f x` is the proposition that a function `f : X → Y` between topological spaces is **continuous at the point `x`**: that is, for every open neighbourhood `V` of `f x` in `Y`, there exists an open neighbourhood `U` of `x` in `X` such that `f(U) ⊆ V`. Equivalently, the images of sets containing `x` eventually land in any prescribed neighbourhood of `f x`, i.e., `f` maps the neighbourhood filter of `x` into the neighbourhood filter of `f x`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ContinuousAt : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (f : X → Y) -> (x : X) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.ContinuousAt : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (f : X → Y) -> (x : X) -> Prop
```

The implicit type arguments `X` and `Y` are the domain and codomain types, respectively. The instance arguments supply the topological structures on `X` and `Y` that give meaning to neighbourhoods. The explicit argument `f` is the function whose continuity is being examined. The explicit argument `x` is the particular point in `X` at which continuity is being asserted.

## Conventions

There are no declared junk-value or boundary conventions for this definition: `VTask.ContinuousAt f x` is a well-formed proposition for every `f` and every `x` as long as topological-space instances are available; there is no regime where the definition silently adopts a fallback value.

## Worked examples

- Claim: The identity function on any topological space is continuous at every point.

- Claim: Any constant function `fun _ => c` between topological spaces is continuous at every point, because the image of every filter under a constant function is the principal filter at `c`, which is coarser than the neighbourhood filter of `c`.

- Claim: The function `f : ℝ → ℝ` defined by `f x = x ^ 2` is continuous at every real number `x₀`, since polynomial functions are continuous everywhere on `ℝ`.

- Claim: If `f : X → Y` and `g : Y → Z` are both continuous at `x` and `f x` respectively, then `g ∘ f` is continuous at `x`.

## Boundaries

- If `X` or `Y` carries the discrete topology, then every function into or out of it is continuous at every point, because singleton sets are open and neighbourhoods are just all supersets of the point.
- If `Y` carries the indiscrete topology, every function `f : X → Y` is continuous at every point, since the only neighbourhoods of any point in `Y` are the whole space.
- `VTask.ContinuousAt f x` does **not** imply that `f` is continuous at any other point; continuity at a single point is a strictly local condition.
- A function that is continuous at `x` need not be continuous on any open set containing `x`; the condition is point-wise.
- The negation, `¬ VTask.ContinuousAt f x`, means there exists a neighbourhood of `f x` whose preimage is not a neighbourhood of `x`, i.e., `f` has an essential discontinuity at `x`.

## Not to be confused with

- **`Continuous f`**: global continuity — asserts `VTask.ContinuousAt f x` for *every* `x`, not just at a single specified point.
- **`ContinuousWithinAt f s x`**: continuity at `x` restricted to a subset `s`, using the relative (subspace) neighbourhood filter of `x` within `s`, which is weaker than full continuity at `x`.
- **`Tendsto f (𝓝 x) (𝓝 y)`**: the bare filter-convergence statement; it coincides with `VTask.ContinuousAt f x` only when `y = f x`, so using it with a different target point `y ≠ f x` is a distinct (and stronger or incomparable) condition.
