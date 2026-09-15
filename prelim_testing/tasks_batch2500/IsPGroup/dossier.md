## Object

A *p-group* (for a natural number `p` and a group `G`) is a group in which every element has order equal to some power of `p`; that is, for every element `g` in `G`, there exists a non-negative integer `k` such that raising `g` to the `p^k`-th power yields the identity.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.IsPGroup : (p : ℕ) -> (G : Type u_1) -> [Group G] -> Prop
<!-- PINNED-SIGNATURE:END -->


`VTask.IsPGroup : (p : ℕ) -> (G : Type u_1) -> [Group G] -> Prop`

The first argument `p` is the prime (or more generally, natural number) that is to serve as the base of the power. The second argument `G` is the group being tested — the type carrying the group structure. The instance argument `[Group G]` supplies the group operations on `G`.

## Conventions

The definition makes no primality assumption on `p`; it is stated for any natural number, though the interesting and classical theory applies when `p` is a prime. When `p = 0`, every element must satisfy `g ^ 0 ^ k = 1` for some `k`; since `0 ^ k = 0` for `k ≥ 1` and `0 ^ 0 = 1`, the condition is trivially satisfied only when the group is trivial or one interprets the edge cases carefully — see Boundaries. When `G` is the trivial group, the condition is vacuously true for every `p`.

## Worked examples

- Claim: The trivial group `PUnit` satisfies `VTask.IsPGroup p PUnit` for every `p`, because there are no non-identity elements to check.

- Claim: Any finite group whose cardinality equals `p ^ n` for some `n` satisfies `VTask.IsPGroup p G`; for instance, `ZMod (p ^ n)` (as an additive group) is a `p`-group when `p` is prime.

- Claim: The Prüfer `p`-group (the union of cyclic groups `ℤ / p^n ℤ`) satisfies `VTask.IsPGroup p` for the prime `p`, as every element lies in some finite cyclic layer.

- Claim: A quotient of a `p`-group by a normal subgroup is again a `p`-group: if `VTask.IsPGroup p G` holds and `H` is a normal subgroup, then `VTask.IsPGroup p (G ⧸ H)` holds.

## Boundaries

- **`p = 1`**: Every element satisfies `g ^ 1 ^ k = g ^ 1 = 1` only if `g = 1`, so `VTask.IsPGroup 1 G` holds if and only if `G` is the trivial group.
- **`p = 0`**: For `k = 0`, `0 ^ 0 = 1`, so the witness `k = 0` gives `g ^ 1 = g`, which works only if every element equals 1. For `k ≥ 1`, `0 ^ k = 0`, so `g ^ 0 = 1` holds trivially. Thus `VTask.IsPGroup 0 G` holds for every group `G` (each element is witnessed by `k = 1`).
- **Trivial group**: The predicate is vacuously true for any `p`, since there are no elements to check beyond the identity, and the identity satisfies the condition with `k = 0`.
- **Infinite `p`-groups**: The definition is not restricted to finite groups; infinite `p`-groups (such as the Prüfer group) are accommodated.
- **Non-prime `p`**: The definition is well-formed but the rich structural theory (Sylow theorems, nilpotency, etc.) requires `p` to be prime.

## Not to be confused with

- **`Sylow p G`**: The Sylow `p`-subgroup type, which packages a specific maximal `p`-subgroup of `G`, rather than asserting that `G` itself is a `p`-group.
- **`p`-primary component / `p`-torsion subgroup**: The subgroup of elements whose order is a power of `p` inside a larger group, as opposed to asserting that every element of the whole group has `p`-power order.
- **`Fingroup` cardinality conditions**: Conditions stating that the cardinality of `G` is a power of `p`, which coincide with `VTask.IsPGroup p G` for finite groups but differ conceptually from the element-order definition used here.