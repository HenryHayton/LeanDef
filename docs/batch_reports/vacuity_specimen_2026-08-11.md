# Vacuity specimens — `:= True` scores 1.000 fidelity (11 Aug 2026)

Two deliberately vacuous candidates, scored through the standard pipeline
(`scoring.candidate.score_candidate_body`, same path as every other verdict in the corpus).
Verdict files: `scoring_output/vacuity_specimens/`.

```lean
def VTask.Monotone {α : Type u} {β : Type v} [Preorder α] [Preorder β] (_f : α → β) : Prop := True
def VTask.DependsOn {ι : Type u_1} {α : ι → Type u_2} {β : Type u_3}
    (_f : ((i : ι) → α i) → β) (_s : Set ι) : Prop := True
```

| | admissible | fidelity | resolution | pass | fail | unknown |
|---|---|---|---|---|---|---|
| Monotone | **true** | **1.000** | 0.857 | 6 | **0** | 1 |
| DependsOn | **true** | **1.000** | 0.714 | 5 | **0** | 2 |

Both are admissible and score perfect fidelity. Confirmed, not inferred.

## The mechanism is worse than "no fact catches them"

A discriminating fact **does** exist and **is** violated — it just cannot register.

`Monotone/monotone_unfolding` states
`∀ f, VTask.Monotone f ↔ ∀ a b, a ≤ b → f a ≤ f b`,
which is plainly **false** of `:= True`. Kernel-verified refutation against the vacuous
candidate, with the decreasing witness `fun n : ℕ => 10 - n`:

```lean
example : ¬ (∀ {α β : Type} [Preorder α] [Preorder β] (f : α → β),
             VTask.Monotone f ↔ ∀ a b : α, a ≤ b → f a ≤ f b) := by
  intro h
  have := (h (fun n : ℕ => 10 - n)).mp trivial
  have := this 0 1 (by norm_num)
  omega                                   -- PASSED
```

Same shape for `DependsOn/dependsOn_empty_constant_global` and
`dependsOn_factors_through_global`, the other two unknowns.

So the failure is in three steps:

1. the forward proof fails — **correctly**, the fact is false of this candidate;
2. no negation attempt runs in the standard scoring pipeline, so it lands **UNKNOWN**, not FAIL;
3. **fidelity excludes UNKNOWN from its denominator**, so the one fact that detects the vacuity
   is silently dropped from the score.

A vacuous candidate is therefore not merely unpunished — it is *rewarded*, because precisely the
facts it violates become invisible. Fidelity measures "of the facts we could prove, how many
held", which for a definition denoting nothing is a near-empty and flattering question.

## Implications for the near-miss gate

- **We are not short of discriminating facts here; we are short of FAIL verdicts.** Running the
  negation direction as part of standard scoring — not as a separate top-up pass — would have
  caught both specimens.
- The refuting witness is concrete and small (`fun n => 10 - n`, `0 ≤ 1`), which is exactly the
  near-miss shape: cheap to check, decisive.
- Any vacuity gate should assert `fidelity < 1.0` **or** a non-empty FAIL set for a known-vacuous
  control, rather than assuming an unknown-count is protective.
