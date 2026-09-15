## Object

`VTask.normFromBounded` constructs a genuine *ring norm* on a commutative ring `R` from a function `f : R → ℝ` that is already "almost a norm": it vanishes at zero, is nonneg­ative, is subadditive, respects negation, is multiplicatively bounded (i.e., `f(xy) ≤ c · f(x) · f(y)` for some real constant `c`), and has trivial kernel (the only element sent to `0` is `0` itself). The output is a bundled `RingNorm R` — the Mathlib type encoding all ring-norm axioms — whose underlying seminorm is the supremum-based construction `seminormFromBounded' f`, and whose extra "non-degeneracy" axiom is supplied by the trivial-kernel hypothesis.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.normFromBounded : {R : Type u_1} -> [CommRing R] -> {f : R → ℝ} -> {c : ℝ} -> (f_zero : f 0 = 0) -> (f_nonneg : 0 ≤ f) -> (f_mul : ∀ (x y : R), f (x * y) ≤ c * f x * f y) -> (f_add : ∀ (a b : R), f (a + b) ≤ f a + f b) -> (f_neg : ∀ (x : R), f (-x) = f x) -> (f_ker : f ⁻¹' {0} = {0}) -> RingNorm R
<!-- PINNED-SIGNATURE:END -->


The implicit argument `R` is the commutative ring being normed. The implicit argument `f` is the candidate function from `R` to the non-negative reals. The implicit real constant `c` is the multiplicative bounding constant for `f`. The explicit argument `f_zero` is a proof that `f` vanishes at the ring's zero element. The argument `f_nonneg` is a proof that `f` takes only non-negative values. The argument `f_mul` is a proof of the multiplicative bound: for every pair `x, y` in `R`, `f(x · y) ≤ c · f(x) · f(y)`. The argument `f_add` is a proof of subadditivity: `f(a + b) ≤ f(a) + f(b)` for all `a, b`. The argument `f_neg` is a proof that `f` is even with respect to negation: `f(-x) = f(x)` for all `x`. The argument `f_ker` is a proof that the zero-set of `f` is exactly the singleton `{0}`, i.e., `f` has trivial kernel.

## Conventions

No special junk-value or boundary conventions are declared: all arguments are genuine mathematical hypotheses, and the function is only called when all six conditions are satisfied. There are no out-of-domain inputs whose output is defined by convention rather than mathematics.

## Worked examples

- Claim: For the absolute value `|·| : ℤ → ℝ` with `c = 1`, `VTask.normFromBounded` produces a `RingNorm ℤ` satisfying `(norm : ℤ → ℝ) 3 = 3`.
  (Because `seminormFromBounded' |·|` coincides with `|·|` on `ℤ`, the resulting ring norm evaluates to the usual absolute value.)

- Claim: For any `f` satisfying the six hypotheses, the resulting ring norm satisfies `‖0‖ = 0`, i.e., the norm of the zero element is zero.
  (This follows directly from `f_zero` together with the construction of the seminorm.)

- Claim: For any `f` satisfying the six hypotheses, if `f x = 0` then `x = 0`, because the trivial-kernel condition `f_ker` is built into the `RingNorm` structure's `eq_zero_of_map_eq_zero'` field.

- Claim: For any `f` satisfying the six hypotheses, the resulting ring norm is non-negative: for every `x : R`, `0 ≤ VTask.normFromBounded ... x`.
  (Inherited from `seminormFromBounded_nonneg`.)

## Boundaries

- The multiplicative bounding constant `c` is not required to be positive or even non-negative; however, the bound `f(xy) ≤ c · f(x) · f(y)` becomes vacuous or paradoxical for negative `c` since `f` is non-negative, so in practice `c` will be positive.
- If `c = 0` and `f` is not identically zero, the bound `f(xy) ≤ 0` combined with non-negativity forces `f(xy) = 0` for all `x, y`, which conflicts with the trivial-kernel assumption unless the ring has very special structure; the definition itself does not restrict `c`.
- The trivial-kernel hypothesis `f_ker` is strictly stronger than what is required for a seminorm: without it, the same inputs yield only a `RingSeminorm`, not a `RingNorm`.
- The value `seminormFromBounded' f 1` is guaranteed to be at most `1`; if `f` is not identically zero, it equals exactly `1`.

## Not to be confused with

- `RingSeminorm.seminormFromBounded` (or the underlying `seminormFromBounded'`): produces only a *semi*norm, without the non-degeneracy/trivial-kernel condition; the present definition adds that final axiom.
- `RingNorm` (the type itself): the bundled structure that `VTask.normFromBounded` *produces*, not a construction from raw data.
- A `NormedRing` or `NormedCommRing` instance: those are typeclasses equipping a ring with a norm satisfying `‖xy‖ ≤ ‖x‖ · ‖y‖` (sub-multiplicativity with `c = 1`), whereas `VTask.normFromBounded` allows an arbitrary bounding constant `c`.