## VTask.Balanced

### Object
A subset `A` of a module (or vector space) `E` over a seminormed ring `𝕜` is called **balanced** if, for every scalar `a` in `𝕜` with `‖a‖ ≤ 1`, the scalar multiple `a • A = {a • x | x ∈ A}` is entirely contained in `A`. Intuitively, a balanced set is one that "shrinks into itself" under any contraction by a scalar of norm at most one; it is a fundamental notion in topological vector space theory.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.Balanced : (𝕜 : Type u_1) -> {E : Type u_3} -> [SeminormedRing 𝕜] -> [SMul 𝕜 E] -> (A : Set E) -> Prop
<!-- PINNED-SIGNATURE:END -->


The first argument `𝕜` is the scalar field (or ring), required to carry a seminorm (via a `SeminormedRing` instance) so that the condition `‖a‖ ≤ 1` is meaningful. The second implicit argument `E` is the type of the ambient module or space. The `SMul 𝕜 E` instance provides the scalar multiplication used to form `a • A`. The final argument `A` is the subset of `E` being tested for the balanced property.

### Conventions
There are no declared junk-value or boundary conventions for this definition: the property is a universally quantified implication over all scalars of norm at most one, which is well-formed for any set, including the empty set and the whole space, with no exceptional cases requiring special treatment.

### Worked examples

- Claim: The singleton set `{0}` in any module over a seminormed ring is balanced, since `a • 0 = 0` for all scalars `a`.

- Claim: In `ℝ` as a module over itself, the closed interval `Set.Icc (-1 : ℝ) 1` is balanced: for any `a : ℝ` with `|a| ≤ 1` and any `x ∈ [-1, 1]`, we have `|a * x| ≤ |a| * |x| ≤ 1 * 1 = 1`, so `a • x ∈ [-1, 1]`.

- Claim: The open ball `Metric.ball (0 : E) r` (for `r > 0`) in a normed space is balanced, since scaling by a scalar of norm at most one cannot increase the norm.

- Claim: The set `{x : ℝ | 1 < ‖x‖}` (the complement of the closed unit ball in ℝ) is **not** balanced, because `0 • x = 0` is not in this set even though `0 ∈ 𝕜` has `‖0‖ ≤ 1`.

### Boundaries

- **Empty set**: The empty set is vacuously balanced — the condition `a • ∅ ⊆ ∅` holds trivially since `a • ∅ = ∅`.
- **Whole space**: The whole space `Set.univ` is balanced, since any scalar multiple of the whole space is contained in it.
- **The scalar `a = 0`**: The condition requires `0 • A ⊆ A`; since `0 • x = 0` for all `x`, this forces `0 ∈ A` whenever `A` is nonempty. Thus, a nonempty balanced set must contain the origin.
- **Seminormed vs normed**: The definition works for any seminormed ring, not just fields; in particular, the norm may fail to be strictly positive, but the condition is still well-posed.
- **Scalars of norm exactly 1**: The condition includes `‖a‖ = 1`, so a balanced set must be stable under all isometric scalar multiplications (e.g., multiplication by `−1` in `ℝ`, meaning balanced sets are symmetric about the origin in real vector spaces).

### Not to be confused with

- **Convex sets**: Convexity requires stability under convex combinations of points, while balancedness requires stability under scalar scaling. A set can be balanced without being convex or vice versa.
- **Absorbing sets**: An absorbing set is one that can be scaled up to contain any given point, a dual concept to balancedness; a set may be absorbing but not balanced.
- **Absolutely convex (balanced convex) sets**: These are sets that are simultaneously balanced and convex; they are strictly more constrained than either property alone.
