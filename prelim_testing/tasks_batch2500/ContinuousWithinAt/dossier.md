## VTask.ContinuousWithinAt

### Object

Given topological spaces X and Y, a function f : X → Y, a subset s of X, and a point x in X, `VTask.ContinuousWithinAt f s x` is the proposition that f is continuous at x relative to s. Concretely, this means that as x′ approaches x while staying inside s, the values f(x′) approach f(x) in Y. In the language of filters, the image of the neighbourhood filter of x within s (the filter of sets that contain all points of s near x) converges to the neighbourhood filter of f(x).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.ContinuousWithinAt : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (f : X → Y) -> (s : Set X) -> (x : X) -> Prop
<!-- PINNED-SIGNATURE:END -->


`{X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (f : X → Y) -> (s : Set X) -> (x : X) -> Prop`

The two universe-polymorphic types X and Y are the domain and codomain, both inferred implicitly. The two typeclass arguments supply the topological structure on X and Y respectively; they are also inferred. The explicit argument `f` is the function whose continuity is being tested. The explicit argument `s` is the subset of X that restricts the approach direction — only points of s that are near x are used when testing convergence. The explicit argument `x` is the basepoint at which continuity is assessed; it need not itself belong to s.

### Conventions

When x is not a limit point of s (i.e., the neighbourhood filter of x within s is the principal filter on {x} or coarser), the tendsto condition is satisfied vacuously, so `VTask.ContinuousWithinAt f s x` holds for every function f. In particular, if x is isolated from s in X, the predicate is always true regardless of f.

### Worked examples

- Claim: `VTask.ContinuousWithinAt (fun x : ℝ => x ^ 2) (Set.Icc 0 1) 0` holds, because the squaring function on ℝ is continuous everywhere, hence in particular at 0 within [0, 1].

- Claim: For any function `f : X → Y` and any point `x : X`, `VTask.ContinuousWithinAt f ∅ x` holds, because the neighbourhood filter of x within the empty set is the bottom filter, and every filter map of ⊥ tends to any target filter.

- Claim: If `f : X → Y` is globally continuous, then for every subset s and every point x, `VTask.ContinuousWithinAt f s x` holds, since global continuity at x implies relative continuity with respect to any subset.

- Claim: The identity function `id : ℝ → ℝ` satisfies `VTask.ContinuousWithinAt id s x` for every `s` and every `x`, because id is continuous.

### Boundaries

- **x ∉ s**: The predicate still makes sense and can hold. Continuity within s at x only requires f(x′) → f(x) for x′ ∈ s approaching x; the value of f at x itself is always used as the target, regardless of membership.
- **s = ∅**: As noted in conventions, `VTask.ContinuousWithinAt f ∅ x` is vacuously true for every f and x.
- **s = univ**: `VTask.ContinuousWithinAt f Set.univ x` is equivalent to ordinary continuity of f at x (`ContinuousAt f x`), because the within-filter `𝓝[univ] x` coincides with `𝓝 x`.
- **Discrete topology on X**: Every function out of a discrete space is continuous within at everywhere, since every point is isolated.
- **Non-Hausdorff Y**: The definition is meaningful and non-trivial even when Y is not Hausdorff; limits need not be unique in that setting.

### Not to be confused with

- **`ContinuousAt f x`** — continuity at x without any subset restriction; corresponds to the special case s = univ of `VTask.ContinuousWithinAt`.
- **`ContinuousOn f s`** — continuity of f at *every* point of s within s simultaneously; this is the universal quantification `∀ x ∈ s, VTask.ContinuousWithinAt f s x`.
- **`Continuous f`** — global continuity of f, requiring continuity at every point of X with no subset restriction.
