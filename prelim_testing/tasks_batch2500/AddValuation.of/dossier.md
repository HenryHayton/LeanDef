## Object

An *additive valuation* on a ring `R` valued in a linearly ordered additive commutative monoid-with-top `Γ₀`. An additive valuation is a function `v : R → Γ₀` satisfying the axioms that make it an additive analogue of the classical (multiplicative) valuation: it sends `0` to `⊤` (the largest element, representing "infinite valuation"), sends `1` to `0` (the additive identity), is ultrametric on addition (the value of a sum is at least the minimum of the values of the summands), and is a monoid homomorphism for multiplication (turns products into sums). `VTask.of` is a convenience constructor that builds such an `AddValuation` directly from the raw function and the four proof obligations, without requiring the user to work with the equivalent multiplicative picture.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.of : {R : Type u_3} -> {Γ₀ : Type u_4} -> [Ring R] -> [LinearOrderedAddCommMonoidWithTop Γ₀] -> (f : R → Γ₀) -> (h0 : f 0 = ⊤) -> (h1 : f 1 = 0) -> (hadd : ∀ (x y : R), min (f x) (f y) ≤ f (x + y)) -> (hmul : ∀ (x y : R), f (x * y) = f x + f y) -> AddValuation R Γ₀
<!-- PINNED-SIGNATURE:END -->


`VTask.of : {R : Type u_3} -> {Γ₀ : Type u_4} -> [Ring R] -> [LinearOrderedAddCommMonoidWithTop Γ₀] -> (f : R → Γ₀) -> (h0 : f 0 = ⊤) -> (h1 : f 1 = 0) -> (hadd : ∀ (x y : R), min (f x) (f y) ≤ f (x + y)) -> (hmul : ∀ (x y : R), f (x * y) = f x + f y) -> AddValuation R Γ₀`

`R` is the ring being valued and `Γ₀` is the target linearly ordered additive commutative monoid with top element. The `Ring R` and `LinearOrderedAddCommMonoidWithTop Γ₀` arguments supply the algebraic structures on these types. The argument `f` is the underlying set-theoretic function from ring elements to valuation values. The proof `h0` witnesses that `f` sends `0` to `⊤` (the additive valuation of zero is infinity). The proof `h1` witnesses that `f` sends `1` to `0` (the additive valuation of the multiplicative identity is the additive identity). The proof `hadd` witnesses the ultrametric (non-archimedean) triangle inequality for addition: the valuation of a sum is bounded below by the minimum of the two valuations. The proof `hmul` witnesses that `f` is multiplicative: the valuation of a product equals the sum of the valuations.

## Conventions

The resulting `AddValuation` evaluates on any ring element `r` by applying `f` directly: `(VTask.of f h0 h1 hadd hmul) r = f r`.

## Worked examples

- Claim: `(VTask.of f h0 h1 hadd hmul) r = f r` for any compatible `f` and `r` (the apply lemma `of_apply` holds by definition).

- Claim: The `p`-adic additive valuation on ℤ, sending `0` to `⊤` and a nonzero integer `n` to its `p`-adic exponent (as an element of `ℕ∞`), can be packaged via `VTask.of` by supplying the four proof obligations directly, yielding an `AddValuation ℤ ℕ∞`.

- Claim: For a trivial valuation on a field `k` sending `0` to `⊤` and every nonzero element to `0 : WithTop ℕ`, constructing it via `VTask.of` requires checking that `min 0 0 ≤ 0` (for the add axiom on nonzero inputs), `⊤` dominates any min involving `⊤` (for zero inputs), and that `0 + 0 = 0` (for the mul axiom).

## Boundaries

- The constructor is well-defined for any ring and any `LinearOrderedAddCommMonoidWithTop`; there is no domain restriction.
- When `f` sends every element to `⊤` except the multiplicative identity (which must go to `0`), the axioms force a degenerate structure — but as long as the four proofs are supplied, `VTask.of` accepts it.
- The `hadd` inequality goes in the direction `min (f x) (f y) ≤ f (x + y)`, i.e., the valuation of the sum is *at least* the minimum (in additive conventions, higher value means "more divisible"); equality holds when the two valuations differ.
- There is no injectivity or surjectivity requirement on `f`.

## Not to be confused with

- `AddValuation.ofValuation`: converts a multiplicative `Valuation R (Multiplicative Γ₀ᵒᵈ)` into an `AddValuation`; `VTask.of` instead takes raw data without any reference to the multiplicative world.
- `Valuation.mk` (the analogous constructor for multiplicative valuations): uses a multiplicative monoid-with-zero target and sends `0` to `0` rather than `⊤`.
- The coercion `AddValuation.toFun`: this extracts the underlying function from an existing `AddValuation`, whereas `VTask.of` *builds* an `AddValuation` from a function.