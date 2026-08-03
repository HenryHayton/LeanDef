## 1. Object

Given a decidable predicate `P` on the integers, an explicit lower bound `b` (together with a proof that every integer satisfying `P` is at least `b`), and a proof that `P` holds somewhere, `VTask.leastOfBdd` computes the **least integer satisfying `P`** and packages it as a dependent pair: the integer `lb` together with proofs that `P lb` holds and that `lb` is a lower bound for `{z | P z}`.

This is a fully computable analogue of the classical existence result for bounded-below, inhabited subsets of ℤ: it produces an actual witness rather than a bare existence proof.

## 2. Signature

```
VTask.leastOfBdd : {P : ℤ → Prop} -> [DecidablePred P] -> (b : ℤ) -> (Hb : ∀ (z : ℤ), P z → b ≤ z) -> (Hinh : ∃ z, P z) -> { lb // P lb ∧ ∀ (z : ℤ), P z → lb ≤ z }
```

- `P : ℤ → Prop` — the predicate whose least satisfier we seek (implicit, inferred from context).
- `[DecidablePred P]` — a typeclass argument supplying a decision procedure for `P`; required for computability.
- `b : ℤ` — an explicit lower bound; does **not** need to be the tightest possible bound.
- `Hb : ∀ (z : ℤ), P z → b ≤ z` — proof that `b` is indeed a lower bound: every `z` with `P z` satisfies `b ≤ z`.
- `Hinh : ∃ z, P z` — proof that `P` is satisfied by at least one integer.
- **Return value** `{ lb // P lb ∧ ∀ (z : ℤ), P z → lb ≤ z }` — a subtype containing the least satisfier `lb`, along with proofs that `P lb` holds and that no smaller integer satisfies `P`.

## 3. Conventions

The lower bound `b` need not itself satisfy `P`, and it need not be the tightest available lower bound; any valid lower bound suffices. Although the bound `b` affects the internal search (the search starts from `b`), the resulting integer `lb` is uniquely determined by `P` alone and is independent of which valid lower bound was supplied — two calls with different bounds `b` and `b'` but the same `P` and `Hinh` will always produce the same coerced integer (as guaranteed by `coe_leastOfBdd_eq`).

## 4. Worked examples

- Claim: For the predicate `P z := 3 ≤ z` with lower bound `b = 0`, `VTask.leastOfBdd 0 (·) ⟨3, le_refl 3⟩` yields a subtype whose underlying value is `3`.

- Claim: For the predicate `P z := z = -2 ∨ z = 5` with lower bound `b = -10`, the returned `lb` satisfies `P lb` (it equals `-2`) and for every `z` with `P z` we have `-2 ≤ z`.

- Claim: The coercion of `VTask.leastOfBdd b Hb Hinh` to `ℤ` equals `sInf {z | P z}` when `P` is viewed as a set (this is the content of `csInf_eq_leastOfBdd`).

- Claim: The result satisfies `IsLeast {z | P z} (VTask.leastOfBdd b Hb Hinh : ℤ)`, meaning it is simultaneously a member of the set and a lower bound for it.

## 5. Boundaries

- **Tightness of bound**: If `b` itself satisfies `P`, the search terminates immediately and `lb = b`. Otherwise the search advances upward from `b` until it finds the first satisfier.
- **Negative integers**: The function handles negative lower bounds and negative least satisfiers correctly; it works over all of ℤ, not just ℕ.
- **Single-element satisfying set**: If exactly one integer satisfies `P`, that integer is returned.
- **Bound independence**: Changing the lower bound `b` to any other valid lower bound `b'` does not change the value of `lb`; only the internal search range shifts.
- **Non-constructive proofs not accepted**: The `[DecidablePred P]` instance is mandatory; classical proofs of decidability are accepted via `Classical.decPred` but the function always terminates for any computable decision procedure.

## 6. Not to be confused with

- `Int.greatestOfBdd` — the dual operation, returning the **greatest** integer satisfying a predicate that is bounded above, rather than the least.
- `Nat.find` — finds the least *natural number* satisfying a decidable predicate; `VTask.leastOfBdd` generalises this to integers with an arbitrary lower bound.
- `csInf` (conditional infimum) — the lattice-theoretic infimum of a set of integers; `VTask.leastOfBdd` is the computable version that also returns membership and minimality proofs, and its coercion equals `sInf` of the corresponding set.