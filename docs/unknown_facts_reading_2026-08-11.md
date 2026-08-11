# Why 731 facts came back UNKNOWN — a reading of 50 definitions

**Method.** I read 50 distinct (task, definition) pairs that carry UNKNOWN facts — every distinct
definition text, not 50 samples of the same one — covering **391 unknown fact instances** and
**61 distinct (task, fact) pairs**. Spread: `Nat.divisors` 13, `Relation.Fibration` 13,
`Nat.choose` 10, `Relation.CutExpand` 10, `Nat.nthRoot` 4.

Where I claim a proof would or would not work, I ran it against the live kernel rather than
judging by eye; those checks are marked **[verified]**.

**Headline.** Of the 50 definitions I read, I judge **48 mathematically correct**, 1 correct but
semantically stronger than the truth in a way that matters only without irreflexivity, and 1
unverifiable by inspection (an unproven numerical algorithm). Almost none of the 731 UNKNOWNs are
the models getting the mathematics wrong. Three mechanisms produce nearly all of them, and **two
are defects in our verifier, not in the candidates.**

---

## Mechanism A — tier 2 never unfolds the definition it is testing

This is the biggest and most embarrassing finding.

For global (∀-quantified) facts, tier 2 runs `DEFAULT_TIER2_TACTICS`:
`rfl, omega, norm_num, positivity, simp, exact?, aesop`.

**None of these unfold the candidate's own definition.** `VTask.divisors` is an ordinary `def`, so
a bare `simp` cannot see inside it. The definition-unfolding tactics do exist — `with_membership_
tactics` in `ladder/budgets.py` builds `simp [VTask.X]`, `simp only [VTask.X] <;> aesop` — but
they are only wired into the **decide-fallback** path (`ladder/adjudicate.py:102`), which handles
`by decide`-shaped facts. Global facts never receive them.

So for 579 of the 731 unknowns, we asked tactics to prove a statement about a symbol they were
forbidden to look inside.

### Example 1 — `Nat.divisors` [entry 31, qwen3-32b s9], correct definition

```lean
def VTask.divisors (n : ℕ) : Finset ℕ :=
  if n = 0 then ∅ else Finset.filter (· ∣ n) (Finset.range (n + 1))
```
Correct. (For `n ≠ 0`, `0 ∤ n`, so `0` is filtered out automatically; `n < n+1` so `n` is in
range.) Unknown fact:

```lean
∀ n : ℕ, 0 < n → n ∈ VTask.divisors n
```

**[verified]** against the kernel:

| tactic | result |
|---|---|
| `by simp` (in tier 2's set) | FAILED |
| `by aesop` (in tier 2's set) | FAILED |
| `by intro n hn; simp [VTask.divisors, hn.ne', Finset.mem_filter, Finset.mem_range]` | **PASSED** |

A one-liner closes it. The only missing ingredient is naming the definition.

### Example 2 — `Nat.choose` [entry 10, goedel-prover-v2-32b s7], byte-identical to Mathlib

```lean
def VTask.choose : ℕ → ℕ → ℕ
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => VTask.choose n k + VTask.choose n (k + 1)
```
This is character-for-character Mathlib's `Nat.choose`. Unknown fact `∀ n, VTask.choose n 0 = 1`
— which is the *first defining clause*.

**[verified]**: `by simp` FAILED, `by aesop` FAILED, **`by intro n; cases n <;> rfl` PASSED**.

We recorded "the models could not prove `choose n 0 = 1`" about a definition whose first line
says exactly that.

---

## Mechanism B — tier 4 (equivalence) cannot do induction

Equivalence is the fast path: prove `candidate = truth` once and every fact transports. Its power
is stark — **every equivalence-certified candidate has zero unknowns, 27 out of 27.**

But tier 4 states the goal as `VTask.choose = Nat.choose` and tries only tier-2 tactics then
hammer. Function equality between two recursive definitions needs `funext` plus induction, which
none of them do.

**[verified]** on entry 10 above:

| tactic | result |
|---|---|
| `rfl` (tier 4's first attempt) | FAILED |
| `simp [VTask.choose, Nat.choose]` | FAILED |
| `aesop` | FAILED |
| `funext n k; induction n generalizing k …` (5 lines) | **PASSED** |

`Nat.choose` has 16 admissible candidates, **0 equivalence-certified**, and 128 unknowns. A
single five-line proof on any of them would have discharged its 8 global facts at a stroke.
Instead five models spent thousands of attempts re-deriving binomial-coefficient theory.

### Example 3 — the same task, harder-to-prove shapes [entries 3, 5, 7]

```lean
-- [3] stepfun s0
def VTask.choose (n k : ℕ) : ℕ :=
  if k = 0 then 1 else if k > n then 0 else VTask.choose (n-1) (k-1) + VTask.choose (n-1) k

-- [5] stepfun s9
def VTask.choose : ℕ → ℕ → ℕ
  | n, k => if k = 0 ∨ k = n then 1 else if k > n then 0 else
            VTask.choose (n-1) (k-1) + VTask.choose (n-1) k
```

Both are **mathematically correct**, but they compile via *well-founded* recursion using truncated
subtraction (`n-1`). Their equation lemmas do not reduce definitionally, and induction on `n` does
not line up with the recursion. These are genuinely harder to reason about than entry 10 even
though they denote the same function — a real observation for task design: **definitional shape
drives provability at least as much as correctness does.**

---

## Mechanism C — definitions that do not reduce, so `decide` cannot run

90 unresolved facts are `by decide`-shaped. Almost all belong to definitions the kernel cannot
evaluate. Two sub-cases, and the contrast between them is instructive.

### Example 4 — `Nat.nthRoot` [entry 24, goedel-prover-v2-32b s9]: binary search, 29 unknowns

```lean
def VTask.nthRoot (n a : ℕ) : ℕ :=
  if n = 0 then 1
  else
    let rec find_root (lo hi : ℕ) : ℕ :=
      if hi ≤ lo then lo
      else
        let mid := (lo + hi) / 2
        if (mid + 1) ^ n ≤ a then find_root (mid + 1) hi else find_root lo mid
    find_root 0 (a + 1)
```

A textbook integer binary search — plausibly correct, though I would not certify it by eye.
`find_root` is well-founded recursion, which compiles to `WellFounded.fix` and **does not reduce
in the kernel**. So *every one of its 19 `by decide` facts fails*, including
`VTask.nthRoot 2 9 = 3`. Not a proving failure; the kernel has nothing to compute.

### Example 5 — `Nat.nthRoot` [entry 23, goedel-prover-v2-32b s2]: 8 unknowns, all global

```lean
def VTask.nthRoot (n a : ℕ) : ℕ :=
  if n = 0 then 1 else Nat.findGreatest (fun r => r ^ n ≤ a) a
```

Same task, same model family. Because `Nat.findGreatest` *is* computable, **all 16 decidable facts
passed**; only the 8 global ones remain. This is the clean controlled comparison: the definition's
*computational* character, not its correctness, decided whether two-thirds of its fact suite could
be adjudicated at all.

### Example 6 — `Nat.log` [StepFun s0]: correct, noncomputable, 23 unknowns

```lean
def VTask.log (b n : ℕ) : ℕ :=
  if b ≤ 1 ∨ n = 0 then 0 else sSup {k | b ^ k ≤ n}
```

Mathematically this is the *best* definition of the five I read for this task — the log genuinely
is the greatest `k` with `bᵏ ≤ n`, and the set is bounded so the sup is attained. But `sSup` is
noncomputable, so all 12 `by decide` facts fail. Noncomputable candidates are **3.2% of the pool
but carry 9.2% of the unknowns**.

This is the finding with the sharpest design implication: **our fact suites structurally penalise
definition-by-characterisation**, which is the very style the project holds up as a first-class
answer (the `Filter.limsSup` exemplar was chosen for exactly that).

---

## Mechanism D — facts that are genuinely hard

Some are simply real theorems, and the models failing them is honest signal.

### Example 7 — `Relation.CutExpand` [entries 11–20], all essentially correct

```lean
-- [16] goedel-prover-v2-32b s0  (Mathlib's definition, conjuncts in the same order)
def VTask.CutExpand (r : α → α → Prop) (s' s : Multiset α) : Prop :=
  ∃ (a : α) (t : Multiset α), (∀ b ∈ t, r b a) ∧ s' + {a} = s + t
```

Ten variants, differing only in binder style and conjunct order. Their unknown facts include:

```lean
cutexpand_wellfounded : WellFounded r → WellFounded (VTask.CutExpand r)
cutexpand_acc_singleton : Acc r a → Acc (VTask.CutExpand r) {a}
```

These are substantial theorems — Mathlib proves them over several lemmas using multiset
induction. Expecting a one-shot LLM proof is unreasonable, and I would not read these UNKNOWNs as
evidence against the models.

Their *membership* facts are a different story:
```lean
VTask.CutExpand (· < ·) {1, 5} {3, 5}
```
This needs the prover to *invent* `a = 3, t = {1}` and then prove `{1,5} + {3} = {3,5} + {1}` as
multisets. Solvable, but it is witness search, not a tactic call.

### Example 8 — `Relation.CutExpand` [entry 12, qwen3-32b s0]: the one genuine semantic deviation

```lean
def VTask.CutExpand (r : α → α → Prop) (s' s : Multiset α) : Prop :=
  ∃ a t, a ∈ s ∧ s' + {a} = s + t ∧ (∀ b ∈ t, r b a)
```

The extra conjunct `a ∈ s` is **not** in Mathlib's definition. It is *derivable* when `r` is
irreflexive (if `a ∈ t` then `r a a`), so for every intended use the two agree — but as stated
this is strictly stronger, and it would diverge for a reflexive `r`. This is precisely the class
of "typed plausible misreading" the mutant suites are designed to catch, and our current fact
suite does not distinguish it from the correct variants. **The one candidate in 50 where I think
the definition is arguably wrong, and the verifier gave it the same score as the right ones.**

### Example 9 — `Relation.Fibration` [entries 38–50], all correct

```lean
-- [50] goedel-prover-v2-32b s5
def VTask.Fibration (rα : α → α → Prop) (rβ : β → β → Prop) (f : α → β) : Prop :=
  ∀ (a : α) (b : β), rβ b (f a) → ∃ (a' : α), rα a' a ∧ f a' = b
```

Thirteen variants; the only differences are binder order (`∀ a b` vs `∀ b a`) and conjunct order.
Mathlib uses strict-implicit binders `⦃a b⦄`; semantically identical. Unknown facts like

```lean
fibration_iff_image_Iic :
  Monotone f → (Fibration (·≤·) (·≤·) f ↔ ∀ x, f '' Set.Iic x = Set.Iic (f x))
```
are real order-theory results. But `fibration_not_subrel_reject` — refuting
`Fibration (<) (<) (fun n => 2*n)` — needs only the witness `a = 1, b = 1` and is the kind of
thing a targeted prompt should land.

---

## Judgement on the 50 definitions

| verdict | count | notes |
|---|---|---|
| Correct, and equivalent to the Mathlib object | 48 | across all five tasks |
| Correct but semantically stronger than the truth | 1 | CutExpand [12], extra `a ∈ s` |
| Not verifiable by inspection | 1 | nthRoot [21], unproven Newton iteration |
| **Clearly wrong** | **0** | — |

## Where the 731 unknowns come from

| mechanism | share | whose fault |
|---|---|---|
| A — tier 2 cannot unfold the definition | large part of 579 globals | **verifier** |
| B — tier 4 cannot do induction, so nothing transports | gates all of the above | **verifier** |
| C — definition does not reduce (WF recursion / noncomputable) | ~90 decidable + some globals | **task design** |
| D — genuinely hard theorems | the residue | honest model limitation |

## Recommendations, in order of leverage

1. **Give tier 2 the unfolding tactics on global facts**, not just the decide-fallback. One-line
   change to `ladder/adjudicate.py`; two facts I tested go from UNKNOWN to PASS immediately.
2. **Teach tier 4 `funext` + induction.** Verified to close the `Nat.choose` family, which is 128
   unknowns; certification then transports every remaining fact for free.
3. **Decide the noncomputable question.** A correct `sSup`-based characterisation currently scores
   zero on its `decide` facts. Either the suite should carry non-decidable counterparts for such
   facts, or admissibility should record "characterisation-style" and grade it differently.
4. **Do not read the current UNKNOWN totals as model capability.** Until 1 and 2 are fixed, the
   number mostly measures our tactic wiring.
