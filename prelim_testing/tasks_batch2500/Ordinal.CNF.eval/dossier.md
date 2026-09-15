## VTask.eval

### Object

`VTask.eval b f` computes the value of an ordinal polynomial (or "base-`b` expansion") encoded by a finitely-supported function `f : Ordinal →₀ Ordinal`. Concretely, if `f` assigns coefficient `c_i` to exponent `e_i` (with only finitely many nonzero coefficients), then `VTask.eval b f` returns the ordinal

$$b^{e_0} \cdot c_0 + b^{e_1} \cdot c_1 + \cdots + b^{e_k} \cdot c_k$$

where the exponents are visited in **decreasing** order. This is the natural evaluation map turning a Cantor normal form (CNF) coefficient record into the ordinal it represents.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.eval : (b : Ordinal.{u_1}) -> (f : Ordinal.{u_1} →₀ Ordinal.{u_1}) -> Ordinal.{u_1}
<!-- PINNED-SIGNATURE:END -->


`VTask.eval : (b : Ordinal.{u_1}) -> (f : Ordinal.{u_1} →₀ Ordinal.{u_1}) -> Ordinal.{u_1}`

The first argument `b` is the **base** of the expansion — the ordinal that is raised to successive powers. The second argument `f` is a **finitely-supported function** from ordinals to ordinals encoding the expansion: for each ordinal exponent `e`, `f e` is the corresponding coefficient; all but finitely many values of `f` are zero.

### Conventions

When the support of `f` is empty (i.e. `f` is the zero finsupp), the sum is empty and `VTask.eval b f` returns `0`, regardless of the base `b`. In particular, `VTask.eval 0 0 = 0`.

### Worked examples

- Claim: For the zero finsupp, `VTask.eval b 0 = 0` for any base `b`.
  ```lean
  example (b : Ordinal) : VTask.eval b 0 = 0 := by simp [VTask.eval]
  ```

- Claim: For the finsupp that maps exponent `1` to coefficient `3` (and everything else to `0`), `VTask.eval ω f = ω * 3`, because the only term is `ω^1 * 3`.

- Claim: For a finsupp `f` with `f 2 = 1`, `f 1 = 0`, `f 0 = 1` (and all others zero), `VTask.eval ω f = ω^2 + 1`, since the terms are `ω^2·1 + ω^0·1`.

- Claim: For a finsupp `f` whose only nonzero value is `f 0 = c`, `VTask.eval b f = c` for any `b`, because `b^0 = 1` and `1 * c = c`.

### Boundaries

- **Base `b = 0`**: For exponents `p > 0`, `0^p = 0`, so all higher-order terms vanish. Only the coefficient at exponent `0` survives (since `0^0 = 1` in ordinal arithmetic). Thus `VTask.eval 0 f = f 0`.
- **Base `b = 1`**: Every power `1^p = 1`, so `VTask.eval 1 f` collapses to the ordinal sum of all coefficients (in decreasing exponent order), which is generally not the same as the arithmetic sum.
- **Empty support**: `VTask.eval b 0 = 0` regardless of `b`.
- **Coefficient zero at an exponent**: Because `f` is a finsupp, any exponent with coefficient `0` is not in the support and contributes nothing to the sum — there is no "phantom" term.
- **Single-term finsupp**: `VTask.eval b (single e c) = b^e * c`.

### Not to be confused with

- **`Ordinal.CNF b o`**: This produces the finsupp encoding of the CNF of an ordinal `o` in base `b`; `VTask.eval` goes in the opposite direction, from the encoding back to the ordinal.
- **`Ordinal.CNFRec`**: A recursion principle for CNF; it manipulates the structure of the normal form rather than evaluating a pre-built finsupp.
- **Finsupp.sum**: The general summation over a finsupp, which does not impose any ordering on the terms; `VTask.eval` specifically sums in decreasing exponent order, which matters for non-commutative ordinal addition.
