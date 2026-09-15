## Object

`VTask.SuperpolynomialDecay l k f` is the proposition that the function `f` decays faster than any polynomial power of `k` along the filter `l`. Concretely, it says that for every natural number `n`, the product `k(a)^n · f(a)` tends to `0` as `a` tends to `l`. This captures the idea that `f` is eventually smaller in magnitude than `C / k^n` for any fixed `n` and any constant `C > 0`, generalising the classical notion of a Schwartz-class or rapidly-decaying function.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.SuperpolynomialDecay : {α : Type u_1} -> {β : Type u_2} -> [TopologicalSpace β] -> [CommSemiring β] -> (l : Filter α) -> (k f : α → β) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.SuperpolynomialDecay : {α : Type u_1} -> {β : Type u_2} -> [TopologicalSpace β] -> [CommSemiring β] -> (l : Filter α) -> (k f : α → β) -> Prop`

The type `α` is the domain of the functions (e.g. the positive reals or the natural numbers). The type `β` is the codomain, which must carry both a topology (so that the notion of "tends to 0" is meaningful) and a commutative semiring structure (so that powers and products are defined). The argument `l` is the filter along which decay is measured — typically a neighbourhood filter at infinity or at some limit point. The argument `k` is the "gauge" or "weight" function whose powers are used to test the decay rate. The argument `f` is the function whose decay is being asserted.

## Conventions

No special junk-value or edge conventions are declared for this definition: it is a universally-quantified Prop whose meaning is fully determined for every input by the standard interpretation of the topological limit, and no inputs are restricted or given exceptional default values.

## Worked examples

- Claim: The zero function `fun _ : ℝ => (0 : ℝ)` has superpolynomial decay with respect to any gauge `k` along any filter `l`, because `k(a)^n * 0 = 0` tends to `0` trivially.

- Claim: For the filter `Filter.atTop` on `ℕ` and the gauge `k a = (1 : ℝ) / (a + 1)`, the function `f a = 1 / (a + 1)` has superpolynomial decay, because `(1/(a+1))^(n+1)` tends to `0` along `atTop` for every `n`.

- Claim: If `VTask.SuperpolynomialDecay l k f` and `VTask.SuperpolynomialDecay l k g` both hold (in a topological semiring), then `VTask.SuperpolynomialDecay l k (fun a => f a + g a)` holds as well, because a sum of sequences tending to `0` tends to `0`.

- Claim: If `VTask.SuperpolynomialDecay l k f` holds and `m : ℕ`, then for every `n : ℕ` the function `fun a => k a ^ n * (k a ^ m * f a)` tends to `0` at `l`, witnessing that `fun a => k a ^ m * f a` also has superpolynomial decay.

## Boundaries

- When `n = 0`, the condition reduces to `Tendsto (fun a => f a) l (𝓝 0)`, so superpolynomial decay implies ordinary convergence to `0`.
- If `l` is the `⊥` filter (the filter containing every set), then every tendsto statement is vacuously true, so `VTask.SuperpolynomialDecay ⊥ k f` holds for any `k` and `f`.
- If `l` is the principal filter of a single point, the tendsto condition is just evaluation, so the property places a pointwise constraint on `f` at that point.
- The definition does not require `k` to be small or tending to `0`; it is meaningful even when `k` grows, though in that regime the condition on `f` becomes very strong.
- No positivity or ordering is required of `β`; the notion of "decay" is purely topological (convergence to the zero element).

## Not to be confused with

- **Polynomial decay** (`∃ n, Tendsto (fun a => k a ^ n * f a) l (𝓝 0)`): that requires only a single `n` to work, whereas superpolynomial decay requires all `n`.
- **Tendsto f l (𝓝 0)** (plain convergence to zero): this is the special case `n = 0` of superpolynomial decay, but it is strictly weaker.
- **Asymptotics.IsLittleO**: a Bachmann–Landau `o`-notation statement, which quantifies over a single comparison function rather than all polynomial powers of a gauge.