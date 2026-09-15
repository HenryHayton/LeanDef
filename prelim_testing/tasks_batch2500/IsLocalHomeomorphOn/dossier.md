## VTask.IsLocalHomeomorphOn

### Object

A predicate on a function `f : X → Y` and a subset `s ⊆ X` that holds exactly when `f` is a *local homeomorphism on `s`*: for every point `x` belonging to `s`, there exists an open partial homeomorphism `e` (a homeomorphism between two open subsets, one in `X` and one in `Y`) whose source contains `x` and which agrees with `f` everywhere on its source. Intuitively, every point of `s` has an open neighbourhood on which `f` restricts to a homeomorphism onto an open subset of `Y`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsLocalHomeomorphOn : {X : Type u_1} -> {Y : Type u_2} -> [TopologicalSpace X] -> [TopologicalSpace Y] -> (f : X → Y) -> (s : Set X) -> Prop
<!-- PINNED-SIGNATURE:END -->


The first argument `f` is the continuous map under scrutiny. The second argument `s` is the subset of the domain `X` on which local homeomorphicity is required; the condition is imposed only at points of `s` and not at any point outside it.

### Conventions

No junk-value or edge-case conventions are declared for this predicate: it is a universally quantified statement over `s`, so when `s` is empty the condition holds vacuously, and this is simply the standard behaviour of universal quantification over an empty set rather than a special convention.

### Worked examples

- Claim: `VTask.IsLocalHomeomorphOn f s` is monotone in `s` in the sense that if it holds on a larger set `t` and `s ⊆ t`, then it holds on `s`.

- Claim: If `f : X → Y` is a full local homeomorphism (i.e., `IsLocalHomeomorph f` holds), then `VTask.IsLocalHomeomorphOn f s` holds for every subset `s` of `X`.

- Claim: The identity map on any topological space `X` satisfies `VTask.IsLocalHomeomorphOn id s` for any subset `s`, since every point is covered by the identity partial homeomorphism on all of `X`.

- Claim: `VTask.IsLocalHomeomorphOn f Set.univ` is equivalent to `f` being a local homeomorphism everywhere (i.e., `IsLocalHomeomorph f`).

### Boundaries

- When `s = ∅`, the predicate holds for every function `f`, because the universal quantification over an empty set is vacuously true.
- When `s = Set.univ`, `VTask.IsLocalHomeomorphOn f Set.univ` is equivalent to `IsLocalHomeomorph f`, i.e., the global notion of local homeomorphism.
- The predicate requires the chart `e` to satisfy `f = e` (as functions, agreeing on the entire source of `e`), not merely that `f` and `e` agree at the single point `x`; the neighbourhood on which they agree is the full source of `e`, which is open.
- A local homeomorphism on `s` is in particular continuous on `s` and maps each neighbourhood filter `𝓝 x` (for `x ∈ s`) to `𝓝 (f x)`.
- The predicate is not symmetric in `s`: enlarging `s` makes the condition strictly harder to satisfy, while restricting to a subset (`mono`) preserves it.

### Not to be confused with

- `IsLocalHomeomorph f`: the global version, requiring every point of the whole space `X` to have a chart; equivalent to `VTask.IsLocalHomeomorphOn f Set.univ`.
- `IsOpenEmbedding`: an open embedding is a homeomorphism onto an open subset globally, which is strictly stronger than being a local homeomorphism on a set.
- `ContinuousOn f s`: a much weaker condition; `VTask.IsLocalHomeomorphOn f s` implies `ContinuousOn f s` but not conversely.