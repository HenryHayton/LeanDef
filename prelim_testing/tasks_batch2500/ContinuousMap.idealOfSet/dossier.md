## VTask.idealOfSet

### Object

Given a topological semiring `R` and a subset `s` of a topological space `X`, `VTask.idealOfSet R s` is the ideal in the ring of continuous functions `C(X, R)` consisting precisely of those continuous functions `f : X → R` that vanish on the complement of `s` — that is, `f(x) = 0` for every `x ∉ s`. Intuitively, this is the "support-contained-in-s" ideal: members are continuous functions whose support (the set where they are nonzero) is contained in `s`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.idealOfSet : {X : Type u_1} -> (R : Type u_2) -> [TopologicalSpace X] -> [Semiring R] -> [TopologicalSpace R] -> [IsTopologicalSemiring R] -> (s : Set X) -> Ideal C(X, R)
<!-- PINNED-SIGNATURE:END -->


The first explicit argument `R` is the coefficient semiring, which must be equipped with a topology making it a topological semiring. The implicit argument `X` is the underlying topological space on which the continuous functions are defined. The final argument `s` is a subset of `X`; functions in the ideal are required to be zero at every point outside `s`.

### Conventions

No special junk-value or boundary conventions are declared for this definition: it is genuinely total and well-defined for every choice of `s`, including `s = ∅` (yielding the zero ideal) and `s = Set.univ` (yielding the whole ring `C(X, R)` as an ideal).

### Worked examples

- Claim: The zero function `0 : C(X, R)` belongs to `VTask.idealOfSet R s` for every `s`.

- Claim: If `f : C(X, R)` has support contained in `s` (i.e., `∀ x ∉ s, f x = 0`), then `f ∈ VTask.idealOfSet R s`.

- Claim: When `s = ∅`, the ideal `VTask.idealOfSet R ∅` contains only the zero function, because every point of `X` lies in the complement of `∅`, so every member must vanish everywhere; by continuity and the Hausdorff-like separation this forces the function to be identically zero.

- Claim: When `s = Set.univ`, every continuous function `f : C(X, R)` belongs to `VTask.idealOfSet R Set.univ`, since the complement of `Set.univ` is empty and the universal quantification `∀ x ∈ ∅, f x = 0` is vacuously true.

### Boundaries

- **`s = ∅`**: The complement of `∅` is all of `X`, so every member of the ideal must vanish on all of `X`. The ideal thus equals the zero ideal `{0}`.
- **`s = Set.univ`**: The complement of `Set.univ` is `∅`, so the vanishing condition is vacuous. The ideal is all of `C(X, R)`, which as an ideal of itself equals the unit ideal.
- **`s₁ ⊆ s₂`**: Enlarging `s` can only shrink (or leave equal) the complement, so `VTask.idealOfSet R s₁ ≤ VTask.idealOfSet R s₂` as ideals — more functions qualify when the complement is smaller.
- **Open vs. closed `s`**: The definition places no topological restriction on `s` itself; it is valid for arbitrary subsets, whether open, closed, or neither.

### Not to be confused with

- **`Ideal.vanishingIdeal`** (or a "vanishing ideal of a set"): That construction collects functions vanishing *on* `s` itself, not on the complement of `s` — the roles of `s` and `sᶜ` are swapped.
- **`ContinuousMap.compactSupport` submodule**: A related but distinct object requiring the support to be compact, not merely contained in a given set.
- **`idealOfSet` for a closed set in C*-algebra theory**: In C*-algebra contexts one often constructs ideals from *closed* subsets via vanishing on the set (not its complement); `VTask.idealOfSet` uses the complement and imposes no closedness assumption.
