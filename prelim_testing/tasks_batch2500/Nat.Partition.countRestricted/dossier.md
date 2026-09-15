## VTask.countRestricted

### Object

`VTask.countRestricted n m` is the finite set (a `Finset`) of all partitions of the natural number `n` in which every part appears **strictly fewer than `m` times**. More precisely, a partition of `n` belongs to this set if and only if, for each part value that appears in the partition, its multiplicity (the number of times it occurs) is less than `m`.

For example, when `m = 2` every part may appear at most once, so the resulting set is exactly the set of partitions of `n` into **distinct** parts. When `m = 1` no part may appear even once, so the set is empty (for `n > 0`) or contains only the empty partition (for `n = 0`). When `m = 0` the condition "count < 0" is vacuously false for any part that appears, so again the set is empty for `n > 0`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.countRestricted : (n m : ℕ) -> Finset n.Partition
<!-- PINNED-SIGNATURE:END -->


The first argument `n` is the natural number being partitioned; all partitions in the returned finset sum to `n`. The second argument `m` is the **multiplicity bound**: each part of any partition in the set must appear strictly fewer than `m` times.

### Conventions

When `m = 0`, the condition `count i < 0` is never satisfied for any part `i` that actually appears, so `VTask.countRestricted n 0` is the empty finset for every `n > 0`; for `n = 0` it contains only the unique empty partition (which trivially satisfies the vacuous condition). When `m = 1`, parts may appear zero times but not one or more times, which forces the finset to be empty for `n > 0` and a singleton for `n = 0`.

### Worked examples

- Claim: `VTask.countRestricted 0 m` is always a singleton `{∅}` for any `m ≥ 1`, since the only partition of 0 is the empty partition and it trivially satisfies the count restriction.

- Claim: `VTask.countRestricted n 2` equals `distincts n`, the finset of partitions of `n` into distinct parts, for every `n`.

- Claim: `VTask.countRestricted 4 2` contains the partitions of 4 into distinct parts: `{4}`, `{3,1}`, and `{2,1,1}` is excluded (1 appears twice), so the members are `{4}`, `{3,1}`, `{2+2}` is excluded (2 appears twice). Thus the partitions are exactly `{4}` and `{3,1}`, giving cardinality 2.

- Claim: `VTask.countRestricted 3 3` contains every partition of 3 (since with bound 3 every part may appear up to twice), which are `{3}`, `{2,1}`, `{1,1,1}` — here `{1,1,1}` has part 1 appearing 3 times, which is not < 3, so it is **excluded**; the members are `{3}` and `{2,1}`, giving cardinality 2.

### Boundaries

- **`m = 0`**: The condition `count i < 0` is never true, so the finset is empty for `n > 0` and equals the singleton `{∅}` for `n = 0` (the empty partition vacuously satisfies the condition).
- **`m = 1`**: Only parts with multiplicity 0 are allowed — impossible for any part that actually occurs — so the finset is empty for `n > 0` and `{∅}` for `n = 0`.
- **`m = 2`**: Recovers exactly `distincts n`, the partitions of `n` into pairwise distinct parts (proven as `countRestricted_two`).
- **Large `m`**: Once `m` exceeds `n`, the multiplicity bound is never binding (no part of a partition of `n` can appear more than `n` times), so `VTask.countRestricted n m` equals the full set of all partitions of `n`.
- **`n = 0`**: The unique partition of 0 is the empty partition, which trivially satisfies any count condition, so the result is always the singleton `{∅}` for every `m ≥ 1`.

### Not to be confused with

- **`distincts n`** — the special case `VTask.countRestricted n 2`; it is the finset of partitions into *distinct* parts, i.e., with every multiplicity strictly less than 2.
- **`restricted n p`** — the finset of partitions of `n` whose parts all satisfy a predicate `p`; it filters on which *values* may appear, not on how many times a value may appear.
- **`Nat.Partition.parts`** — the underlying multiset of parts of a single partition, not a finset of partitions; `countRestricted` is a finset whose *elements* are partitions.
