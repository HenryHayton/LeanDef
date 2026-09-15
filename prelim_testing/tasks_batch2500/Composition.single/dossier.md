## VTask.single

### Object

The *trivial* or *coarse* composition of a positive natural number `n`: the unique composition of `n` consisting of exactly one block, namely `n` itself. In other words, it expresses `n` as the ordered sum of a single part equal to `n`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.single : (n : ℕ) -> (h : 0 < n) -> Composition n
<!-- PINNED-SIGNATURE:END -->


The first argument `n` is the natural number being composed. The second argument `h` is a proof that `n` is positive (strictly greater than zero), which is required because a composition's blocks must all be positive.

### Conventions

The positivity hypothesis `h` is required as explicit data, not inferred automatically, even though many callers obtain it from the context; any two proofs of `0 < n` give definitionally equal results.

### Worked examples

- Claim: `VTask.single 3 (by norm_num)` has blocks list `[3]`.
  ```lean
  example : (VTask.single 3 (by norm_num)).blocks = [3] := by decide
  ```

- Claim: `VTask.single 5 (by norm_num)` has length 1.
  ```lean
  example : (VTask.single 5 (by norm_num)).length = 1 := by decide
  ```

- Claim: `VTask.single 4 (by norm_num)` is its own reverse (the single-block composition is a palindrome).
  ```lean
  example : (VTask.single 4 (by norm_num)).reverse = VTask.single 4 (by norm_num) := by decide
  ```

- Claim: For `VTask.single n h`, the unique block's size (`blocksFun` at the only index) equals `n`.

- Claim: A composition `c` of `n` equals `VTask.single n h` if and only if `c.length = 1`.

### Boundaries

- The smallest valid input is `n = 1` with `h : 0 < 1`; this yields the unique composition of 1, which is `[1]`.
- The definition requires `0 < n` strictly; there is no composition of 0 in this framework, so `n = 0` is not in the domain.
- There is exactly one block and exactly one index into that block list (namely `0 : Fin 1`); the embedding maps every `i : Fin n` to itself.
- `VTask.single n h` is self-reverse for all valid `n`.

### Not to be confused with

- `Composition.ones n` — the *finest* composition, consisting of `n` blocks each of size 1, which is the opposite extreme from the coarse single-block composition.
- A `Finset.univ`-style singleton — `VTask.single` is a composition (an ordered list of block sizes summing to `n`), not a set or multiset containing a single element.
- `Composition.length` — a field of a `Composition`, not a constructor; `VTask.single` constructs a composition whose length happens to equal 1.