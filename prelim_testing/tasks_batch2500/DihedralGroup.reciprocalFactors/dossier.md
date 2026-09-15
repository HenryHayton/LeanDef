## Object

`VTask.reciprocalFactors n` produces a list of natural numbers, each representing the index of a dihedral group, such that the direct product of those dihedral groups has commuting probability exactly `1/n`. In other words, it encodes a recipe — as a finite list of dihedral-group indices — whose product witnesses that every positive rational of the form `1/n` is realised as the commuting probability of some finite group.

## Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.reciprocalFactors : (n : ℕ) -> List ℕ
<!-- PINNED-SIGNATURE:END -->


`(n : ℕ) -> List ℕ`

The single argument `n` is the denominator of the target commuting probability `1/n`. The returned list contains the indices of the dihedral groups whose direct product achieves that commuting probability. Specifically, if `k` appears in the list, it designates the dihedral group `DihedralGroup k`.

## Conventions

When `n = 0`, the function returns the sentinel list `[0]`. This is a junk value: the notion of commuting probability `1/0` is mathematically undefined (or interpreted as `0` in the surrounding framework), so the output has no geometric meaning for `n = 0`.

## Worked examples

- Claim: `VTask.reciprocalFactors 1 = []` — for `n = 1` the target probability is `1/1 = 1`, achieved by the trivial group, which corresponds to an empty product, hence the empty list.

- Claim: `VTask.reciprocalFactors 2 = [3]` — since 2 is even, the even-case rule applies, prepending `3` and recursing on `2/2 = 1`; the recursion returns `[]`, giving `[3]`. The dihedral group `DihedralGroup 3` (the symmetry group of a triangle, isomorphic to `S₃`) alone has commuting probability `1/2`.

- Claim: `VTask.reciprocalFactors 4 = [3, 3]` — 4 is even, so prepend `3` and recurse on `4/2 = 2`; 2 is even, so prepend `3` and recurse on `2/2 = 1`, giving `[]`. The result is `[3, 3]`, meaning `DihedralGroup 3 × DihedralGroup 3` has commuting probability `1/4`.

- Claim: `VTask.reciprocalFactors 3 = [3, 3]` — 3 is odd (and ≠ 1), so the odd-case rule gives first element `3 % 4 * 3 = 1 * 3 = 3`, then recurses on `3/4 + 1 = 0 + 1 = 1`, which returns `[]`. The result is `[3, 3]`.

- Claim: `VTask.reciprocalFactors 5 = [5, 3]` — 5 is odd, first element is `5 % 4 * 5 = 1 * 5 = 5`, recurse on `5/4 + 1 = 1 + 1 = 2`; 2 is even, prepend `3`, recurse on `1`, get `[]`. Result is `[5, 3]`.

## Boundaries

- At `n = 0`: the output is the sentinel `[0]`. This is purely a junk/default value with no mathematical interpretation as a commuting-probability witness.
- At `n = 1`: the output is the empty list `[]`, corresponding to the trivial group (empty direct product), which has commuting probability 1.
- For even `n ≥ 2`: the first element of the list is always `3` (the index of the dihedral group `DihedralGroup 3 ≅ S₃`).
- For odd `n ≥ 3`: the first element is `n % 4 * n`, which equals `n` when `n ≡ 1 (mod 4)` and equals `3n` when `n ≡ 3 (mod 4)`.
- The recursion always terminates because the argument strictly decreases toward 0 or 1.

## Not to be confused with

- `DihedralGroup n`: the actual group of symmetries of a regular `n`-gon; `VTask.reciprocalFactors` returns *indices* that label such groups, not the groups themselves.
- `commProb`: the commuting probability function on a group; `VTask.reciprocalFactors` constructs the *witness* groups whose commuting probability equals `1/n`, but does not compute commuting probability itself.
- A prime factorisation of `n`: the list returned is not a factorisation of `n` into primes; its entries are dihedral-group indices and may repeat or follow a different pattern entirely.