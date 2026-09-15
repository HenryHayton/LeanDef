## VTask.cast

### Object

Given a composition `c` of the natural number `m` (i.e., an ordered list of positive parts that sum to `m`) and a proof that `m = n`, `VTask.cast` produces a composition of `n` that is structurally identical to `c` — the same list of parts — but now recognised as a composition of `n` instead of `m`. This is a purely bookkeeping operation: no data changes, only the index type is rewritten along the supplied proof.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.cast : {n m : ℕ} -> (c : Composition m) -> (hmn : m = n) -> Composition n
<!-- PINNED-SIGNATURE:END -->


`{n m : ℕ}` are implicit natural numbers; `m` is the original index (the value that the blocks of `c` sum to) and `n` is the target index. `c : Composition m` is the composition being transported. `hmn : m = n` is the propositional equality witness used to rewrite the summation type.

### Conventions

When the proof `hmn` is `rfl` (i.e., `m` and `n` are definitionally equal), the result is propositionally equal to the original composition: `c.cast rfl = c`. No junk values arise because the function is total and the output carries exactly the same block data.

### Worked examples

- Claim: Casting along `rfl` returns the original composition unchanged: for any `c : Composition n`, `VTask.cast c rfl = c`.

- Claim: The result of `VTask.cast c hmn` is heterogeneously equal (`HEq`) to `c`, reflecting that the underlying data is identical even though the types differ when `m ≠ n` definitionally.

- Claim: For compositions `c₁ : Composition m` and `c₂ : Composition n`, reversing their append equals the append of the reverses cast along `add_comm n m`: `reverse (append c₁ c₂) = (append c₂.reverse c₁.reverse).cast (add_comm _ _)`.

### Boundaries

- The only "edge" input is `hmn : m = n` being `rfl`. In that case `VTask.cast c rfl` is propositionally equal (indeed definitionally equal after unfolding) to `c` itself.
- The function is total: it is defined for every composition `c` and every proof `hmn : m = n`. There are no undefined or degenerate cases.
- When `m = 0` (the unique empty composition), `VTask.cast` simply produces the unique composition of `n = 0`, which is again empty.

### Not to be confused with

- `Composition.cast_eq_cast`: a theorem relating `VTask.cast` to Lean's built-in heterogeneous `cast`; not the operation itself.
- `List.map` or `List.cast`: generic list-level casts that do not preserve the `Composition` invariants.
- `Equiv.cast` / `Eq.mpr`: universe-level or type-level casts that operate on types, not on structured combinatorial objects like compositions.