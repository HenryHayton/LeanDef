## Object

`VTask.IsPrincipal op o` is the property that an ordinal `o` is **principal** (also called *indecomposable*) with respect to a binary operation `op` on ordinals. Concretely, this means that the initial segment `{x : Ordinal | x < o}` is closed under `op`: whenever both operands are strictly below `o`, so is their image under `op`. By convention, `0` is counted as principal even though the usual notion of indecomposability would exclude it.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsPrincipal : (op : Ordinal.{u_1} → Ordinal.{u_1} → Ordinal.{u_1}) -> (o : Ordinal.{u_1}) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsPrincipal : (op : Ordinal.{u_1} → Ordinal.{u_1} → Ordinal.{u_1}) -> (o : Ordinal.{u_1}) -> Prop`

The first argument `op` is the binary operation on ordinals with respect to which principality is being tested. The second argument `o` is the ordinal being tested for principality.

## Conventions

Ordinal `0` is declared principal under every operation. This breaks the usual set-theoretic convention (where a principal ordinal is typically required to be positive), but it is adopted here for definitional simplicity: the statement `∀ a b, a < 0 → b < 0 → op a b < 0` is vacuously true.

## Worked Examples

- Claim: `VTask.IsPrincipal (· + ·) 0` holds, since no ordinals are strictly less than `0`, making the closure condition vacuously satisfied.

- Claim: `VTask.IsPrincipal (· + ·) ω` holds, because the sum of any two natural numbers (ordinals below `ω`) is again a natural number, hence strictly less than `ω`.

- Claim: `VTask.IsPrincipal (· + ·) (ω ^ ω)` holds, since `ω ^ ω` is an epsilon-number-like fixed point for ordinal addition: it equals `ω ^ ω` and every ordinal below it can be added to another such ordinal without reaching `ω ^ ω`.

- Claim: `¬ VTask.IsPrincipal (· + ·) 2` holds, because `1 < 2` and `1 < 2` but `1 + 1 = 2`, which is not strictly less than `2`.

- Claim: The supremum of a set of ordinals each principal under `op` is itself principal under `op`.

## Boundaries

- **`o = 0`**: Principal by convention (vacuously, since no ordinals are strictly less than `0`).
- **`o = 1`**: Principal under any operation, because the only ordinal below `1` is `0`, and `op 0 0` must be compared to `1`; this depends on `op`.
- **Suprema**: If every member of a (possibly empty) set `s` of ordinals is principal under `op`, then `sSup s` is principal under `op`. In particular the empty supremum (`sSup ∅ = 0`) is covered by the convention.
- **Swapping arguments**: `VTask.IsPrincipal (Function.swap op) o ↔ VTask.IsPrincipal op o`, so principality is symmetric in how `op` is presented.
- **Characterisation for addition**: An ordinal `o` is principal under `(· + ·)` if and only if `o = 0` or `o` is a power of `ω`.
- **Characterisation for multiplication**: An ordinal `o` is principal under `(· * ·)` if and only if `o ≤ 2` or `o` is of the form `ω ^ (ω ^ α)` for some ordinal `α`.

## Not to be confused with

- **`Ordinal.IsInitial`**: A stronger structural condition (being an initial ordinal / cardinal); every initial ordinal `≥ ω` is principal under addition, multiplication, and ordinal exponentiation, but `IsPrincipal` is weaker and does not require `o` to be a cardinal.
- **`Set.IsInductive` or closure under a single unary operation**: `VTask.IsPrincipal` requires closure under a *binary* operation for *all pairs* below `o`, not just iteration from a single starting point.
- **Epsilon numbers / fixed points of `ω ^·`**: While epsilon numbers satisfy principality under multiplication and addition, `VTask.IsPrincipal` is a general predicate that applies to any binary operation, not specifically to the structure of epsilon numbers.