## VTask.contained

### Object

`VTask.contained C o` is a predicate on a set `C` of Boolean-valued functions on an index type `I`, asserting that every function in `C` has all its "support" (the indices where it takes value `true`) concentrated strictly below the ordinal level `o`, as measured by the canonical ordinal rank `ord I` assigned to each element of `I`. Informally, `C` is *contained in level `o`* if no function in `C` is "switched on" at any index whose rank is `≥ o`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.contained : {I : Type u} -> (C : Set (I → Bool)) -> [LinearOrder I] -> [WellFoundedLT I] -> (o : Ordinal.{u}) -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.contained : {I : Type u} -> (C : Set (I → Bool)) -> [LinearOrder I] -> [WellFoundedLT I] -> (o : Ordinal.{u}) -> Prop`

The implicit type argument `I` is the index type whose elements are the coordinates of the Boolean-valued functions. `C` is the set of Boolean-valued functions on `I` under scrutiny. The instance arguments `LinearOrder I` and `WellFoundedLT I` provide the well-founded linear order on `I` that allows assigning each element of `I` an ordinal rank `ord I i`. Finally, `o` is the ordinal threshold: the predicate asserts that every function in `C` is supported only on indices of rank strictly less than `o`.

### Conventions

There are no declared junk-value or edge-case conventions beyond what is logically forced: at `o = 0`, no index can have rank `< 0`, so `VTask.contained C 0` holds precisely when no function in `C` takes the value `true` at any index — equivalently, every function in `C` is the constantly-`false` function (or `C` is empty).

### Worked examples

- Claim: The empty set `∅` satisfies `VTask.contained ∅ o` for every ordinal `o`, because the universal quantification over membership in `∅` is vacuously true.

- Claim: If `C` is a set such that `VTask.contained C o` holds and `o ≤ o'`, then `VTask.contained C o'` also holds, since every rank strictly below `o` is also strictly below `o'`.

- Claim: For a singleton set `C = {f}` where `f : I → Bool` has `f i = true` only for indices `i` with `ord I i < o`, `VTask.contained C o` holds.

- Claim: The projection `π C (ord I · < o)` — the restriction of `C` to functions supported below `o` — always satisfies `VTask.contained (π C (ord I · < o)) o`.

### Boundaries

- **`o = 0`**: Since no ordinal is strictly less than `0`, `VTask.contained C 0` holds if and only if every `f ∈ C` is identically `false` (has empty support). In particular, `VTask.contained ∅ 0` holds vacuously.
- **Empty `C`**: `VTask.contained ∅ o` holds for every ordinal `o` by vacuous truth.
- **Monotonicity in `o`**: If `VTask.contained C o` holds and `o ≤ o'`, then `VTask.contained C o'` holds. The predicate is upward-monotone in the ordinal argument.
- **Equivalence with projection**: When `VTask.contained C o` holds, `C` equals its own projection to indices of rank `< o`; that is, `C = π C (ord I · < o)`.

### Not to be confused with

- **`π C (ord I · < o)`** (the projection of `C` to level `o`): This is a *set construction* (a new set of functions), not a predicate; `VTask.contained C o` is the *assertion* that `C` already equals this projection.
- **`isGood`**: A predicate on individual *products* (lists of indices) relative to `C`, asserting a maximality/independence condition; not a global condition on the set `C` itself.
- **`ord I i < o`** (a pointwise rank comparison): This is a predicate on individual indices `i ∈ I`, whereas `VTask.contained` universally quantifies this condition over all functions in `C` and all their supporting indices.