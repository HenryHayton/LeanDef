## VTask.find

### Object

`VTask.find` computes the **least natural number satisfying a given decidable predicate**, given a proof that at least one such number exists. More precisely, if `p : ℕ → Prop` is a predicate for which we can decide truth at each natural number, and `H` witnesses that some natural number satisfies `p`, then `VTask.find H` is the unique natural number `n` such that `p n` holds and no smaller natural number satisfies `p`.

### Signature

<!-- PINNED-SIGNATURE:BEGIN -->
VTask.find : {p : ℕ → Prop} -> [DecidablePred p] -> (H : ∃ n, p n) -> ℕ
<!-- PINNED-SIGNATURE:END -->


`{p : ℕ → Prop}` is the predicate being searched; it is an implicit argument inferred from context. `[DecidablePred p]` is the typeclass instance asserting that the truth of `p` at each natural number can be decided algorithmically; it is synthesised automatically. `H : ∃ n, p n` is an explicit proof that there is at least one witness — this is necessary to guarantee termination of the search and that the result is well-defined.

### Conventions

The result is guaranteed to satisfy `p` (this is `find_spec`): the value returned actually meets the predicate. The result is minimal: no natural number strictly smaller than `VTask.find H` satisfies `p` (this is `find_min`). Equivalently, any natural number satisfying `p` is at least as large as `VTask.find H` (this is `find_min'`). The definition is **protected**, so it cannot be invoked as plain `find` even when the relevant namespace is open; it must always be fully qualified.

### Worked examples

- Claim: For the predicate `p n ↔ 3 ≤ n`, the least witness is `3`.
  ```lean
  example : VTask.find (p := fun n => 3 ≤ n) ⟨3, le_refl 3⟩ = 3 := by native_decide
  ```

- Claim: For the predicate `p n ↔ n % 5 = 0 ∧ 7 ≤ n`, the least witness is `10`.
  ```lean
  example : VTask.find (p := fun n => n % 5 = 0 ∧ 7 ≤ n) ⟨10, by decide, by decide⟩ = 10 := by native_decide
  ```

- Claim: If `p` is a predicate implied by `q` (i.e., `∀ n, q n → p n`), then `VTask.find hp ≤ VTask.find hq` (monotonicity of the minimum witness under predicate weakening).

- Claim: If two decidable predicates `p` and `q` are logically equivalent (i.e., `∀ n, p n ↔ q n`), then `VTask.find hp = VTask.find hq`.

### Boundaries

- The function is **only defined** (i.e., well-typed) when a proof `H : ∃ n, p n` is provided; without such a witness the minimum does not exist as a total function and the definition cannot be applied.
- If `p 0` holds, then `VTask.find H = 0`, since `0` is the smallest natural number and it already satisfies `p`.
- The function does not produce any junk value for an uninhabited predicate; the existential hypothesis in the signature rules this case out entirely at the type level.
- The `DecidablePred p` instance is required for computation; if this instance is not available or is classical, the value is still well-defined but may not reduce definitionally.

### Not to be confused with

- `Nat.findGreatest`: finds the **greatest** natural number up to a bound satisfying a predicate, not the least one.
- `PNat.find`: the analogous construction for **positive** natural numbers `ℕ+`, whose minimum is `1`, not `0`.
- `Nat.rfind`: a **partial** (monadic) search over a `Bool`-valued function that may fail to terminate, whereas `VTask.find` always terminates given its existential hypothesis.