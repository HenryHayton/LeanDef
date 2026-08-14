## VTask.IsSaddlePointOn

### Object

A pair `(a, b)` is called a **saddle point** of a two-variable function `f : E → F → β` on the product set `X × Y` if the value `f a b` simultaneously minimises `f(·, b)` over `X` and maximises `f(a, ·)` over `Y`—that is, `a` is a "best response" against `b` from the left, and `b` is a "best response" against `a` from the right. Concretely, this means: for every `x ∈ X` and every `y ∈ Y`, the inequality `f a y ≤ f x b` holds. Geometrically, the value `f a b` is a minimax point: it is at least as large as any `f a y` (with `y ∈ Y`), and at most as large as any `f x b` (with `x ∈ X`).

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsSaddlePointOn : {E : Type u_1} -> {F : Type u_2} -> {β : Type u_3} -> (X : Set E) -> (Y : Set F) -> (f : E → F → β) -> [Preorder β] -> (a : E) -> (b : F) -> Prop
<!-- PINNED-SIGNATURE:END -->


```
VTask.IsSaddlePointOn : {E : Type u_1} -> {F : Type u_2} -> {β : Type u_3} -> (X : Set E) -> (Y : Set F) -> (f : E → F → β) -> [Preorder β] -> (a : E) -> (b : F) -> Prop
```

`X` is the admissible set for the first (row) player's strategies; `Y` is the admissible set for the second (column) player's strategies. `f` is the payoff function evaluated at a row strategy and a column strategy. The `Preorder` instance provides the ordering used to compare payoff values. `a` is the proposed row strategy forming the candidate saddle point, and `b` is the proposed column strategy.

### Conventions

Membership of the candidate point `(a, b)` in the sets `X × Y` is **not required**. The predicate merely demands the inequality `f a y ≤ f x b` for all `x ∈ X` and all `y ∈ Y`; whether `a ∈ X` or `b ∈ Y` is left unconstrained and must be tracked separately by the user if needed.

### Worked examples

- Claim: For `f : ℝ → ℝ → ℝ` defined by `f x y = x - y`, the pair `(0, 0)` is a saddle point of `f` on `{x : ℝ | x ≥ 0} × {y : ℝ | y ≥ 0}` because `0 - y ≤ x - 0` for all non-negative `x` and `y`.

- Claim: For the constant function `f x y = c`, every pair `(a, b)` is a saddle point on any sets `X` and `Y`, because `c ≤ c` holds trivially.

- Claim: If `(a, b)` and `(a', b')` are both saddle points of `f` on `X × Y` with `a' ∈ X` and `b ∈ Y`, then `(a, b')` is also a saddle point of `f` on `X × Y` (saddle-point interchangeability / swap_left).

- Claim: When `β` is a complete linear order and `a ∈ X`, `b ∈ Y`, `(a, b)` is a saddle point of `f` on `X × Y` if and only if the supremum of `f a y` over `Y` equals the infimum of `f x b` over `X` (minimax equality).

### Boundaries

- **Empty sets**: If `X = ∅` or `Y = ∅`, the universal quantification over that set is vacuously true, so `VTask.IsSaddlePointOn ∅ Y f a b` and `VTask.IsSaddlePointOn X ∅ f a b` both hold for any `a`, `b`, and `f`.
- **Candidate outside the domain**: The predicate places no constraint requiring `a ∈ X` or `b ∈ Y`. A pair `(a, b)` with one or both components outside their respective sets can still be a saddle point.
- **Non-antisymmetric preorders**: Because `β` only needs to be a preorder (not necessarily a partial order), the value `f a b` need not be uniquely determined by the saddle-point inequalities.

### Not to be confused with

- **`IsSaddlePoint` (global saddle point)**: The version without restricted domains, asserting the saddle-point inequalities over all of `E` and `F` rather than subsets `X` and `Y`.
- **`IsMinOn` / `IsMaxOn`**: One-sided extremality conditions; `VTask.IsSaddlePointOn` captures both directions simultaneously.
- **Nash equilibrium**: In game theory, Nash equilibrium generalises saddle points to non-zero-sum games; a saddle point of `f` on `X × Y` corresponds to a Nash equilibrium of the zero-sum game with payoff `f`, but only when both players are restricted to pure strategies.