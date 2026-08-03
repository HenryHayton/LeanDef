## 1. Object

`VTask.strongDownwardInduction` is a recursion/induction principle for finsets that proceeds **downward by cardinality**. Given a bound `n` and a step function `H`, it produces a value of type `p s` for every finset `s` whose cardinality is at most `n`, by starting at finsets of cardinality exactly `n` and working downward: to define `p s`, one is allowed to assume that `p t` has already been defined for every strict superset `t` of `s` with `t.card ≤ n`. The principle can be used both to define data and to prove propositions.

## 2. Signature

```
VTask.strongDownwardInduction : {α : Type u_1} -> {p : Finset α → Sort u_4} -> {n : ℕ} -> (H : (t₁ : Finset α) → ({t₂ : Finset α} → t₂.card ≤ n → t₁ ⊂ t₂ → p t₂) → t₁.card ≤ n → p t₁) -> (s : Finset α) -> s.card ≤ n → p s
```

- `α` : the (implicit) type of elements of the finsets.
- `p` : the motive — a type family indexed by `Finset α`, in any `Sort` (so it can be data or a proposition).
- `n` : the (implicit) cardinality bound; induction is carried out only for finsets of cardinality `≤ n`.
- `H` : the step function. Given any finset `t₁` together with a way to obtain `p t₂` for every strict superset `t₂ ⊆·` of `t₁` with `t₂.card ≤ n`, and a proof that `t₁.card ≤ n`, `H` must produce `p t₁`.
- `s` : the finset at which the value is to be computed.
- `s.card ≤ n` : the cardinality hypothesis, confirming that `s` falls within the induction regime.
- **Returns** a term of type `p s`.

## 3. Conventions

There are no junk-value or out-of-domain edge conventions to declare: the function is genuinely total on all inputs satisfying the stated types, and there is no convention assigning special meaning to boundary inputs beyond what the step function `H` naturally produces.

## 4. Worked examples

- Claim: When `p` is the constant `True` predicate and `H` always produces `trivial`, `VTask.strongDownwardInduction H s hs` produces a term of type `True` for any finset `s` with `s.card ≤ n`.

- Claim: Applying `VTask.strongDownwardInduction` with `n = 0` and any finset `s` satisfying `s.card ≤ 0` (i.e., `s = ∅`) asks `H` to produce `p ∅` without any inductive hypothesis (since no strict superset of `∅` can have cardinality `≤ 0`), so the result equals `H ∅ (fun h _ => absurd h (by omega)) (by omega)` (a call to `H` with an vacuous hypothesis supplier).

- Claim: The unfolding equation holds — for any `s` and step function `H`, `VTask.strongDownwardInduction H s` equals `H s (fun ht _ => VTask.strongDownwardInduction H _ ht)` as a function of the cardinality hypothesis. (This is the `strongDownwardInduction_eq` theorem in the neighborhood.)

## 5. Boundaries

- **Cardinality exactly `n`**: When `s.card = n`, the inductive hypothesis supplier handed to `H` covers strict supersets of `s` with cardinality `≤ n`. Since any strict superset of `s` has strictly greater cardinality than `s`, and cardinality `≤ n = s.card`, there can be no such superset. Therefore the inductive hypothesis is vacuously available and `H` receives an empty collection of recursive calls — it is in effect a base case.
- **Cardinality `0`** (empty finset): If `n = 0` as well, the situation is as above with `s = ∅`. If `n > 0`, then `s = ∅` has strict supersets of cardinality `≤ n`, so the inductive hypothesis is non-trivial.
- **`n = 0` with non-empty `s`**: The cardinality hypothesis `s.card ≤ 0` forces `s = ∅`, so no other case arises.
- The recursion is well-founded by the measure `n - s.card`, which strictly decreases as one moves to strict supersets within the bound.

## 6. Not to be confused with

- **`Finset.strongDownwardInductionOn`**: The flipped version of the same principle where the finset argument comes before the step function (method-call style), rather than after it.
- **`Finset.strongInduction` / `strongInductionOn`**: The *upward* analogue — induction on finsets proceeding from larger finsets down to smaller ones by looking at strict *subsets*, rather than the downward-by-cardinality direction used here.
- **`Nat.strongRecOn` / strong recursion on `ℕ`**: A plain strong recursion on natural numbers; `VTask.strongDownwardInduction` applies the same well-founded idea but to finsets ordered by the strict superset relation, not to naturals.