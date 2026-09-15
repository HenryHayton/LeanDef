## Object

`VTask.restricted n p` is the finite set of all partitions of the natural number `n` in which **every part satisfies the predicate `p`**. Concretely, a partition of `n` is a multiset of positive integers whose sum is `n`; this object retains exactly those partitions all of whose constituent parts pass the test `p`.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.restricted : (n : ℕ) -> (p : ℕ → Prop) -> [DecidablePred p] -> Finset n.Partition
<!-- PINNED-SIGNATURE:END -->


```
VTask.restricted : (n : ℕ) -> (p : ℕ → Prop) -> [DecidablePred p] -> Finset n.Partition
```

The first argument `n` is the integer being partitioned. The second argument `p` is the part-condition: a predicate on natural numbers that each part of an accepted partition must satisfy. The instance argument `[DecidablePred p]` is a computability witness ensuring that membership in the resulting `Finset` can be decided algorithmically.

## Conventions

The predicate `p` is tested against each individual part (a positive integer) of the partition; the **sum** of the partition itself is not tested against `p`. Parts that appear with multiplicity must each individually satisfy `p`. When `p` is the always-true predicate, `VTask.restricted n p` equals the full `Finset` of all partitions of `n`.

## Worked examples

- Claim: Every element of `VTask.restricted 4 (· % 2 = 1)` (partitions of 4 into odd parts) consists only of odd parts, namely {1+1+1+1} and {3+1} and {1+3} — but as multisets these collapse; the two distinct ones are [1,1,1,1] and [3,1].

- Claim: The size of `VTask.restricted 0 p` is 1 for any decidable `p`, because the unique partition of 0 is the empty partition whose (vacuous) part condition is satisfied.

- Claim: `VTask.restricted n (fun _ => False)` contains exactly one element when `n = 0` (the empty partition trivially satisfies the vacuous condition) and is empty for `n > 0` (every non-empty partition has at least one part, which would fail the always-false predicate).

- Claim: The generating function `PowerSeries.mk (fun n => #(VTask.restricted n p))` equals the infinite product `∏' i, if p (i+1) then ∑' j : ℕ, X^((i+1)*j) else 1`, as stated by `powerSeriesMk_card_restricted_eq_tprod`.

## Boundaries

- **n = 0**: The only partition of 0 is the empty partition. Since it has no parts, the universal condition `∀ i ∈ parts, p i` holds vacuously. Hence `VTask.restricted 0 p` is always a singleton regardless of `p`.
- **p = fun _ => True**: All parts satisfy the condition, so `VTask.restricted n (fun _ => True)` equals the full set of partitions of `n`.
- **p = fun _ => False**: For `n > 0`, every partition has at least one part, which fails `False`, so the finset is empty. For `n = 0`, see the vacuous case above.
- **p restricts to prime parts, parts not divisible by m, etc.**: These produce combinatorially interesting subsets, related to Glaisher-type bijections, as witnessed by the `card_restricted_eq_card_countRestricted` theorem.

## Not to be confused with

- `Nat.Partition.countRestricted n m`: counts partitions of `n` into parts each appearing fewer than `m` times — a *frequency* restriction, not a part-value restriction.
- The full `Finset.univ : Finset n.Partition`: the unrestricted set of all partitions of `n`, which equals `VTask.restricted n (fun _ => True)`.
- `VTask.restricted n p` with `p` applied to the *number of parts* rather than each *part value*: this definition tests each individual part, not the total count or any global statistic of the partition.