## 1. Object

`VTask.greatestOfBdd` computes the **greatest integer satisfying a decidable predicate**, given an explicit upper bound and a witness that the predicate holds somewhere. It returns not just the greatest value but a proof certificate: the value satisfies the predicate, and every other integer satisfying the predicate is at most this value. In other words, it produces the maximum element of the (non-empty, bounded-above) set `{z : ℤ | P z}`.

## 2. Signature

```
VTask.greatestOfBdd : {P : ℤ → Prop} -> [DecidablePred P] -> (b : ℤ) -> (Hb : ∀ (z : ℤ), P z → z ≤ b) -> (Hinh : ∃ z, P z) -> { ub // P ub ∧ ∀ (z : ℤ), P z → z ≤ ub }
```

- `P : ℤ → Prop` — the predicate whose greatest satisfying integer is sought (implicit).
- `[DecidablePred P]` — typeclass requirement that `P` is computably decidable at every integer.
- `b : ℤ` — an explicit upper bound: a known integer that is guaranteed to be at least as large as any integer satisfying `P`.
- `Hb : ∀ (z : ℤ), P z → z ≤ b` — proof that `b` is indeed an upper bound for `{z | P z}`.
- `Hinh : ∃ z, P z` — proof that the predicate holds for at least one integer (non-emptiness witness).
- **Returns** `{ ub // P ub ∧ ∀ (z : ℤ), P z → z ≤ ub }` — a dependent pair consisting of the greatest satisfying integer `ub` together with a proof that `P ub` holds and that `ub` is an upper bound for `{z | P z}`.

## 3. Conventions

There are no junk-value or edge-case conventions to declare for this definition: it is a total function whose inputs are constrained by proof obligations (`Hb` and `Hinh`) that rule out degenerate cases entirely. Any valid call is guaranteed to return a well-defined greatest element.

## 4. Worked Examples

- Claim: For `P z := z ≤ 3`, upper bound `b = 5`, the returned value coerces to `3` and satisfies `P`.

- Claim: For `P z := (z = -2 ∨ z = 0 ∨ z = 1)`, upper bound `b = 1`, the greatest satisfying integer is `1`.

- Claim: For `P z := z ≤ 0`, with upper bound `b = 0`, the returned subtype value `ub` satisfies `ub = 0` and `P 0` holds and every `z` with `P z` satisfies `z ≤ ub`.

- Claim: The value returned by `VTask.greatestOfBdd` is independent of which upper bound is supplied: if `Hb` and `Hb'` are two different upper bounds for the same predicate and the same inhabitation proof, the coerced integer results are equal (this corresponds to `coe_greatestOfBdd_eq`).

## 5. Boundaries

- **Negative integers are fully supported**: `P` can be satisfied only at negative integers; the result will be a negative integer.
- **Single-element support set**: If `P` holds at exactly one integer, that integer is both the witness and the greatest element.
- **Tight upper bound**: The function works correctly even when `b` is exactly the greatest satisfying value (i.e., `b` itself satisfies `P`).
- **Loose upper bound**: The function works correctly when `b` is strictly larger than the greatest satisfying value; the returned `ub` will be strictly less than `b`.
- **The upper bound `b` need not satisfy `P`**: Only the existence proof `Hinh` is needed for inhabitation; `b` is used solely to bound the search.
- **Bound independence**: As guaranteed by `coe_greatestOfBdd_eq`, different choices of upper bound for the same predicate and inhabitation proof yield the same integer result.

## 6. Not to be confused with

- **`leastOfBdd`** — the analogous function returning the *least* (minimum) integer satisfying a decidable, bounded-below, inhabited predicate; `VTask.greatestOfBdd` is its "mirror image" obtained by negation.
- **`exists_greatest_of_bdd`** — a non-computable existence theorem asserting that a greatest element exists; `VTask.greatestOfBdd` is its computable counterpart that actually constructs the witness.
- **`sSup` on sets of integers** — the conditionally-complete-lattice supremum; related by `csSup_eq_greatestOfBdd` but defined abstractly and not necessarily computable.
