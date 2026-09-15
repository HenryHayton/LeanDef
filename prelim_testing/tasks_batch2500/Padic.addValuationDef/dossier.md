## VTask.addValuationDef

### Object

The additive $p$-adic valuation on the field $\mathbb{Q}_p$ of $p$-adic numbers, taking values in $\mathbb{Z} \cup \{+\infty\}$ (written `WithTop ℤ`). For a nonzero $p$-adic number $x$, this is the integer exponent $v$ such that $|x|_p = p^{-v}$, i.e., the largest power of $p$ that "divides" $x$ in the $p$-adic sense. The value $+\infty$ is assigned to zero, reflecting the convention that zero is divisible by every power of $p$.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.addValuationDef : {p : ℕ} -> [hp : Fact (Nat.Prime p)] -> ℚ_[p] → WithTop ℤ
<!-- PINNED-SIGNATURE:END -->


The implicit natural number argument `p` is the prime base of the $p$-adic field. The typeclass argument `hp` supplies the proof that `p` is prime, ensuring the $p$-adic field is well-formed. The explicit argument is the $p$-adic number whose additive valuation is to be computed.

### Conventions

The additive $p$-adic valuation of zero is defined to be $+\infty$ (the top element `⊤` of `WithTop ℤ`), which is the standard convention ensuring the valuation map extends the ultrametric inequality and behaves well in algebraic identities.

### Worked examples

- Claim: `VTask.addValuationDef (0 : ℚ_[p]) = ⊤` — zero maps to the top element `⊤`.

- Claim: `VTask.addValuationDef (1 : ℚ_[p]) = 0` — the multiplicative identity has additive valuation 0, since $|1|_p = p^0 = 1$.

- Claim: For nonzero $x, y \in \mathbb{Q}_p$, `VTask.addValuationDef (x * y) = VTask.addValuationDef x + VTask.addValuationDef y` — the function is completely additive (converts products to sums), mirroring the logarithmic nature of a valuation.

- Claim: For all $x, y \in \mathbb{Q}_p$, `min (VTask.addValuationDef x) (VTask.addValuationDef y) ≤ VTask.addValuationDef (x + y)` — the ultrametric (non-Archimedean) triangle inequality holds: the valuation of a sum is at least the minimum of the two valuations.

### Boundaries

- At $x = 0$: the output is `⊤` (positive infinity), not any integer. Arithmetic in `WithTop ℤ` treats `⊤` as an absorbing element for `min` and a neutral-like element in certain sum expressions.
- For a nonzero $x$: the output is the ordinary integer-valued $p$-adic valuation of $x$, living in the `ℤ` stratum of `WithTop ℤ`.
- For $p$-adic units (elements with $|x|_p = 1$, e.g., nonzero rational integers not divisible by $p$): the valuation is $0$.
- The function is total — it is defined for every element of $\mathbb{Q}_p$ with no domain restriction.

### Not to be confused with

- The *multiplicative* $p$-adic norm $|\cdot|_p : \mathbb{Q}_p \to \mathbb{R}_{\geq 0}$, which returns a non-negative real rather than an element of `WithTop ℤ`, and maps zero to $0$ rather than $+\infty$.
- The `Padic.valuation` field on `ℚ_[p]`, which is the underlying integer-valued valuation defined only for nonzero elements (or returning a junk value at zero), before the `WithTop` extension.
- `AddValuation` as a bundled algebraic structure (a `Valuation`-type object carrying extra algebraic data), as opposed to this bare function `VTask.addValuationDef`.
