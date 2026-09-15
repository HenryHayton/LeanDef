## Object

`VTask.seminormFromBounded` takes a function `f : R → ℝ` on a commutative ring together with a real constant `c` and five hypotheses certifying that `f` behaves like a bounded sub-multiplicative seminorm (vanishes at zero, is nonneg, satisfies `f(xy) ≤ c·f(x)·f(y)`, is subadditive, and is even), and produces a genuine bundled `RingSeminorm R`. The underlying function of the resulting seminorm is not `f` itself but a derived normalization of `f` — concretely the function `seminormFromBounded' f` — that is guaranteed to satisfy the strict ring-seminorm axioms (sub-multiplicativity `‖xy‖ ≤ ‖x‖·‖y‖`, rather than just the weaker bounded condition).

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.seminormFromBounded : {R : Type u_1} -> [CommRing R] -> {f : R → ℝ} -> {c : ℝ} -> (f_zero : f 0 = 0) -> (f_nonneg : 0 ≤ f) -> (f_mul : ∀ (x y : R), f (x * y) ≤ c * f x * f y) -> (f_add : ∀ (a b : R), f (a + b) ≤ f a + f b) -> (f_neg : ∀ (x : R), f (-x) = f x) -> RingSeminorm R
<!-- PINNED-SIGNATURE:END -->


VTask.seminormFromBounded : {R : Type u_1} -> [CommRing R] -> {f : R → ℝ} -> {c : ℝ} -> (f_zero : f 0 = 0) -> (f_nonneg : 0 ≤ f) -> (f_mul : ∀ (x y : R), f (x * y) ≤ c * f x * f y) -> (f_add : ∀ (a b : R), f (a + b) ≤ f a + f b) -> (f_neg : ∀ (x : R), f (-x) = f x) -> RingSeminorm R

The implicit type argument `R` is the commutative ring being seminormed, with its `CommRing` instance supplied implicitly. The implicit `f` is the raw real-valued function on `R` that serves as the raw data, and `c` is the bounding constant in the sub-multiplicativity hypothesis. The explicit argument `f_zero` is a proof that `f` vanishes at zero. The argument `f_nonneg` states that `f` is everywhere nonneg. The argument `f_mul` states the weak sub-multiplicativity bound `f(xy) ≤ c · f(x) · f(y)` for all `x, y`. The argument `f_add` states that `f` is subadditive under addition. The argument `f_neg` states that `f` is even, i.e., `f(-x) = f(x)` for all `x`.

## Conventions

The value at zero of the resulting seminorm is always `0`, inherited directly from `f_zero`. The resulting seminorm's kernel (the set of elements mapping to `0`) coincides exactly with the kernel of the original function `f`. When `f` is the zero function the resulting seminorm is also the zero seminorm. The normalization step ensures the result at `1` is at most `1`; if `f` itself is nonzero the resulting seminorm evaluates to exactly `1` at `1`.

## Worked examples

- Claim: For any commutative ring `R`, applying `VTask.seminormFromBounded` to the identically-zero function (with any `c`) yields the zero `RingSeminorm`.

- Claim: If `f : R → ℝ` already satisfies the exact sub-multiplicativity `f(xy) ≤ f(x)·f(y)` with `c = 1` and `f(1) ≤ 1`, then for every `x`, `(VTask.seminormFromBounded ...) x = f x`.

- Claim: The resulting `VTask.seminormFromBounded ...` satisfies `(VTask.seminormFromBounded f_zero f_nonneg f_mul f_add f_neg) 0 = 0`.

- Claim: For the result `s := VTask.seminormFromBounded f_zero f_nonneg f_mul f_add f_neg`, one has `s (-x) = s x` for all `x : R`, reflecting the `neg'` axiom.

## Boundaries

When `f` is identically zero, all hypotheses are trivially satisfied for any `c`, and the resulting seminorm is the zero seminorm. The bounding constant `c` is allowed to be negative or zero; the construction still type-checks and produces a valid `RingSeminorm`, though the sub-multiplicativity hypothesis `f(xy) ≤ c · f(x) · f(y)` combined with non-negativity of `f` forces `f` to be identically zero in such cases. The value of the seminorm at `1` is at most `1` regardless of `f` and `c`. There is no restriction that `c ≥ 1` or that `f` be continuous.

## Not to be confused with

- `seminormFromBounded'` (the plain function `R → ℝ` obtained by the normalization procedure, without the bundled `RingSeminorm` structure — `VTask.seminormFromBounded` wraps this into a `RingSeminorm`).
- `RingSeminorm.mk` (a generic constructor for ring seminorms that requires the strict sub-multiplicativity `f(xy) ≤ f(x)·f(y)` directly, rather than the weaker bounded form `f(xy) ≤ c·f(x)·f(y)`).
- `normFromBounded` (a potential variant that produces a norm rather than a seminorm, requiring additional nondegeneracy hypotheses).