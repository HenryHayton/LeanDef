## Object

A cardinal `c` is a **strong pre-limit** if it is closed under the powerset (exponential) operation: whenever `x < c`, the cardinal `2^x` (the cardinality of the power set of a set of size `x`) is also strictly less than `c`. Informally, no cardinal strictly below `c` can "jump out" of the interval `[0, c)` via the powerset operation.

The prefix "pre" signals that `0` is included: the empty cardinal trivially satisfies the condition (there is no `x < 0` to check). The stronger notion `IsStrongLimit` additionally requires `c > 0`, excluding `0`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsStrongPrelimit : (c : Cardinal.{u_1}) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsStrongPrelimit : (c : Cardinal.{u_1}) -> Prop`

The sole argument `c` is the cardinal being tested for the strong pre-limit property.

## Conventions

The cardinal `0` is declared a strong pre-limit by convention: the universal quantifier `∀ x < 0` is vacuously true, so `IsStrongPrelimit 0` holds without any nontrivial content.

## Worked examples

- Claim: `VTask.IsStrongPrelimit 0` holds, because there is no cardinal strictly less than `0` to serve as a counterexample.

- Claim: The first infinite cardinal `ℵ₀` is a strong pre-limit, because for every finite cardinal `n`, `2^n` is also finite and hence still less than `ℵ₀`.

- Claim: A successor cardinal such as `ℵ₁` is **not** a strong pre-limit, because `2^{ℵ₀}` is at least `ℵ₁`, violating the closure requirement (there exists `x = ℵ₀ < ℵ₁` with `2^x ≥ ℵ₁`).

- Claim: If `o` is a successor ordinal, then `VTask.IsStrongPrelimit (preBeth o)` is false, because `IsStrongPrelimit (preBeth o) ↔ IsSuccPrelimit o` and successor ordinals are not successor-pre-limits.

## Boundaries

- **`c = 0`**: Satisfies `IsStrongPrelimit` vacuously; this is a deliberate convention so that `IsStrongPrelimit` is the "pre" (zero-inclusive) version of the strong limit notion.
- **Successor cardinals**: Never strong pre-limits. If `c = κ⁺` for some `κ`, then `x = κ < c` but `2^κ ≥ c`.
- **Every strong pre-limit is a successor-pre-limit** (i.e., is not a successor cardinal), as closure under powersets implies, in particular, that the cardinal is a limit or zero.
- **`ℵ₀`**: Is a strong pre-limit, since finite powersets are finite.
- The definition makes no universe restriction beyond the ambient universe of cardinals; `c` ranges over all cardinals in universe `u_1`.

## Not to be confused with

- **`IsStrongLimit`**: The same closure condition with the additional requirement `c > 0`; equivalently, `IsStrongLimit c ↔ IsStrongPrelimit c ∧ c ≠ 0`.
- **`IsSuccPrelimit` / `IsLimit`**: Weaker: only requires that `c` is not a successor cardinal (closed under the successor operation), with no condition on powersets.
- **`IsPrelimit` / `IsWeakLimit`**: Sometimes used for cardinals closed under `· + 1` (ordinal successor) but not necessarily under powersets; a strong pre-limit is always a (weak) pre-limit but not vice versa.