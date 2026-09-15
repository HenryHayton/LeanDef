## Object

The **dynamical entourage** `dynEntourage T U n` is a binary relation on a set `X` that tracks when two points remain close under repeated application of a transformation. Given a transformation `T : X → X`, an entourage (a binary relation capturing a notion of "closeness") `U` on `X`, and a non-negative integer `n`, the dynamical entourage declares two points `x` and `y` to be related if and only if `T^k(x)` and `T^k(y)` are `U`-close for every time step `k` satisfying `0 ≤ k < n`. In other words, it is the entourage of pairs that stay `U`-close over the entire time window `{0, 1, …, n-1}`.

This construction is central to the definition of dynamical covers and topological entropy: a set of points is `(T, U, n)`-separated if no two distinct points lie in the same dynamical entourage ball, and dually such balls form the basic neighborhoods for dynamical covers.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.dynEntourage : {X : Type u_1} -> (T : X → X) -> (U : SetRel X X) -> (n : ℕ) -> SetRel X X
<!-- PINNED-SIGNATURE:END -->


`VTask.dynEntourage : {X : Type u_1} -> (T : X → X) -> (U : SetRel X X) -> (n : ℕ) -> SetRel X X`

The implicit type argument `X` is the ambient space on which the dynamics take place. The first explicit argument `T` is the transformation being iterated. The second explicit argument `U` is the base entourage (a binary relation on `X`) encoding the desired notion of closeness at each individual time step. The third explicit argument `n` is the length of the time window: pairs are required to remain `U`-close at every integer time `k` with `0 ≤ k < n`. The result is a new binary relation (entourage) on `X`.

## Conventions

When `n = 0` the time window `{k : k < 0}` is empty, so there are no conditions to satisfy, and every pair `(x, y)` belongs to `dynEntourage T U 0`. The dynamical entourage at time zero is therefore the universal relation on `X`, regardless of `T` and `U`.

## Worked examples

- Claim: For `n = 0`, `dynEntourage T U 0` is the universal relation: every pair belongs to it, since there are no time steps to check.

- Claim: A pair `(x, y)` belongs to `dynEntourage T U n` if and only if for every `k < n`, the pair `(T^[k] x, T^[k] y)` belongs to `U`. In particular, for `n = 1` the condition reduces to `(x, y) ∈ U` alone (only `k = 0` is checked, giving `(T^[0] x, T^[0] y) = (x, y)`).

- Claim: `dynEntourage T U n` is anti-monotone in `n`: enlarging the time window can only shrink (or preserve) the set of close pairs, since more conditions must be satisfied. Formally, `dynEntourage T U (n + 1) ⊆ dynEntourage T U n`.

- Claim: `dynEntourage T U n` is monotone in `U`: if `U ⊆ V` then `dynEntourage T U n ⊆ dynEntourage T V n`, because every pair satisfying the stricter closeness condition also satisfies the looser one.

- Claim: If `T` is uniformly continuous and `U` is an entourage of a uniform space structure on `X`, then `dynEntourage T U n` is also an entourage of that uniform space.

## Boundaries

- **`n = 0`**: The intersection is over an empty index set, so `dynEntourage T U 0` equals the universal relation `univ` on `X × X`. Every pair of points is "0-close".
- **`n = 1`**: Only `k = 0` is checked; since `T^[0]` is the identity, `dynEntourage T U 1 = U`.
- **`U = univ`**: `dynEntourage T univ n = univ` for all `n`, since every pair is always `univ`-close.
- **Antitone in `n`**: Adding more time steps can only make the dynamical entourage smaller; the sequence `dynEntourage T U 0 ⊇ dynEntourage T U 1 ⊇ dynEntourage T U 2 ⊇ …` is decreasing.
- **Composition**: `(dynEntourage T U n) ○ (dynEntourage T V n) ⊆ dynEntourage T (U ○ V) n`, meaning composing two dynamical entourages refines into the dynamical entourage of the composed base relation.

## Not to be confused with

- **`ball x (dynEntourage T U n)`**: The *ball* of a point `x` in the dynamical entourage — this is a subset of `X` (all points `y` with `(x, y) ∈ dynEntourage T U n`), not the relation itself.
- **`IsDynCoverOf T F U n s`**: A predicate asserting that `s` is a dynamical cover of `F` with respect to `T`, `U`, and `n`; it *uses* `dynEntourage` but is a separate notion.
- **The uniform entourage `U` itself**: `dynEntourage T U 1` coincides with `U`, but for `n ≥ 2` the dynamical entourage is strictly smaller in general, encoding time-dependent proximity rather than instantaneous closeness.