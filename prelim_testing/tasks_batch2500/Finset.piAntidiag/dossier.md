## Object

`VTask.piAntidiag s n` is the finite set of all functions `f : ι → μ` that simultaneously satisfy two conditions: (1) the *support* of `f` is contained in `s` — meaning `f i = 0` whenever `i ∉ s` — and (2) the sum of all values `∑ i ∈ s, f i` equals `n`. It is thus a finite analogue of the set of ways to distribute a total "weight" `n` across the index set `s`, with nothing assigned outside `s`. This generalises the classical integer antidiagonal (pairs summing to `n`) to arbitrary finite index sets and suitably structured additive monoids.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.piAntidiag : {ι : Type u_1} -> {μ : Type u_2} -> [DecidableEq ι] -> [AddCommMonoid μ] -> [Finset.HasAntidiagonal μ] -> [DecidableEq μ] -> (s : Finset ι) -> (n : μ) -> Finset (ι → μ)
<!-- PINNED-SIGNATURE:END -->


`VTask.piAntidiag : {ι : Type u_1} -> {μ : Type u_2} -> [DecidableEq ι] -> [AddCommMonoid μ] -> [Finset.HasAntidiagonal μ] -> [DecidableEq μ] -> (s : Finset ι) -> (n : μ) -> Finset (ι → μ)`

The type `ι` is the index type whose elements label the "slots" into which weight is distributed. The type `μ` is the value type, which must be a commutative additive monoid equipped with a decidable antidiagonal structure (so that the finite set of ways to split any element is computable). The instance `DecidableEq ι` allows membership tests in `s`. The argument `s` is the *support constraint*: the finite set of indices on which functions may be nonzero. The argument `n` is the *sum constraint*: the total that the function values must add up to.

## Conventions

For any index `i` that lies outside `s`, every function `f` in `VTask.piAntidiag s n` satisfies `f i = 0`; values outside `s` are forced to the zero of `μ` and are not free variables of the distribution problem.

## Worked examples

- Claim: Every `f` in `VTask.piAntidiag {0, 1} 3` satisfies `f 0 + f 1 = 3` and `f i = 0` for `i ∉ {0, 1}` (over `ℕ`).

- Claim: `VTask.piAntidiag (∅ : Finset ℕ) (0 : ℕ)` equals `{0}`, the singleton containing only the zero function, since the zero function has empty support and sums to zero.

- Claim: `VTask.piAntidiag (∅ : Finset ℕ) (1 : ℕ)` equals `∅`, because no function with empty support can sum to a nonzero value.

- Claim: When `ι = Fin 2` and `s = Finset.univ`, `VTask.piAntidiag Finset.univ n` over `ℕ` is in natural bijection with `Nat.antidiagonalTuple 2 n` (the set of pairs of naturals summing to `n`).

## Boundaries

- When `s = ∅`: the only function with empty support is the zero function. The set equals `{0}` if `n = 0`, and `∅` otherwise.
- When `n = 0`: every function in the result must sum to zero. Over `ℕ` (or any ordered additive monoid where sums of nonneg terms vanish only when all terms vanish), the only such function with support in `s` is the zero function, so the result is `{0}`.
- When `s` is a singleton `{i}`: the result is in bijection with the set of `μ`-values equal to `n`, i.e., it contains exactly one function assigning `n` to `i` and `0` elsewhere, provided `n` itself is the unique value (which it is for a singleton antidiag).
- The result is always a `Finset`, so it is finite even when `ι` or `μ` is infinite, because the support constraint and the `HasAntidiagonal` instance ensure only finitely many possibilities arise.

## Not to be confused with

- `Finset.antidiagonal n`: the set of *pairs* `(a, b) : μ × μ` with `a + b = n`; `piAntidiag` generalises this from pairs to arbitrary finite index sets.
- `Nat.antidiagonalTuple k n`: the set of `k`-tuples of naturals summing to `n`; `piAntidiag` generalises this to arbitrary `μ` and sparse index sets rather than `Fin k`.
- `Finset.piFinset` (or `Fintype.piFinset`): the Cartesian product of finsets indexed by `ι`, which imposes no sum constraint and no support constraint.