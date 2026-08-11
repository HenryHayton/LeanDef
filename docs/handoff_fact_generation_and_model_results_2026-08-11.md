# Handoff: fact generation, and what the 32B scoring run actually showed

**Date:** 11 August 2026. **Audience:** planning session with no prior context on this run.
**Pins:** Lean v4.32.0, Mathlib commit `81a5d257c8e410db227a6665ed08f64fea08e997`.

Everything below is either **measured** (a number from the scored corpus, or a kernel check I
ran) or **inferred** (my reading, marked as such). Where a figure I reported earlier turned out to
be wrong, the correction is stated explicitly rather than quietly replaced.

---

# PART 1 — What the models did

## 1.1 The run

Three 32B base models, 41 tasks × 10 samples each, zero exemplars, one prompt held fixed across
models. Candidates are definitions filling a pinned signature; the fact suites were authored
earlier by Sonnet 4.6 against ground truth.

| model | samples | adm/100 | reach | newly cracked | verbatim | med tok |
|---|---|---|---|---|---|---|
| qwen3-32b | 410 | **28.0** | 20/41 | 7 | 11 | 4,420 |
| goedel-prover-v2-32b | 410 | 20.5 | 20/41 | 7 | 11 | 1,506 |
| stepfun-formalizer-32b | 409 | 4.2 | 6/41 | 0 | 5 | 1,989 |

"Newly cracked" = tasks no 8B model ever solved (of 26). Admissible candidates total **216**
(qwen 115, goedel 84, stepfun 17).

StepFun's collapse is a task-mismatch, not incompetence: 216 of its 409 samples emitted a
`theorem` instead of a `def` — its trained task is statement autoformalization.

## 1.2 Fact adjudication, whole corpus

3,045 fact instances across admissible candidates.

| stage | count |
|---|---|
| tier 1 `decide` | 936 |
| tier 2 pinned tactics | 553 |
| tier 3 LeanHammer | 29 |
| tier 4 equivalence | 544 |
| tier 5 LLM provers | 252 |
| **UNKNOWN** | **731** |
| **FAIL** | **0** |

**Resolution 76.0%. Fidelity ≈ 1.000 for all three models** — and that number is close to
meaningless, for reasons in §1.4.

## 1.3 Tier-5 head-to-head (the interesting comparison)

These are facts *nothing else could close*. Each model attacked a hash-assigned, direction-blind
share of the residue.

| model | scripts checked | certified | hit rate | axiom-rejected | truncation |
|---|---|---|---|---|---|
| **DeepSeek V3.2** | 449 | **111** | **24.7%** | 0 | 0% |
| Sonnet 4.6 | 100 | 58 | 58%\* | 0 | 57% |
| Goedel-Prover-V2-32B | 1,650 | 38 | 2.3% | 11 | 32% |
| Goedel-Prover-V2-8B | 3,872 | 36 | 0.9% | 10 | 22% |
| Qwen3-Coder-480B | 226 | 9 | 4.0% | 0 | 0% |

\* Sonnet's rate is on a filtered subset — only 100 of its 284 scripts reached checking.

**DeepSeek certified more than both Goedel arms combined, with one attempt per goal** (no pass@k),
100% parseable output, zero errors, in minutes. It is the clear recommendation for the tier-5
backend.

Two secondary findings:

- **The axiom audit earned its keep.** It rejected 21 kernel-accepted proofs — 11 from Goedel-32B,
  10 from Goedel-8B, **0 from DeepSeek, Sonnet, or Qwen**. The prover-trained models attempt
  proofs that typecheck but smuggle a nonstandard axiom (typically `sorryAx`). The general models
  don't.
- **Qwen3-Coder-480B underperformed badly** (4.0%) despite being the largest model tested. Its
  output was clean; its proofs were just wrong. Coding-specialised ≠ proof-specialised.

**Operational note:** Sonnet failed to complete a stage three times for infrastructure reasons
(daily Bedrock token quota, expired credentials). 89% of its output tokens on 10 Aug were spent on
replies truncated at a 4,096-token cap — every truncated call bills the full budget. DeepSeek and
Qwen run in `eu-west-2` (neither is available in `eu-west-1`) via the Bedrock **Converse** API;
the existing Anthropic-format client cannot talk to them.

## 1.4 Why fidelity ≈ 1.000 is not evidence of faithfulness

**Zero FAIL verdicts exist in the entire corpus.** Forward facts can only return PASS or UNKNOWN —
a fact that is *false* of a candidate simply fails to prove, which is indistinguishable from
"automation too weak". FAIL requires proving the **negation**.

Negation coverage as it stands:

- 730 of 731 unknowns got a tier-2/3 negation attempt (push_neg + hammer, 20s) → **1 refutation**
- DeepSeek then attempted the negation of **all 731** → **0 refutations**, 100% script yield
- Sonnet's negation attempts produced 4 usable scripts, ever

Every refutation this project has produced — three, total — indicted the **fact**, not a
candidate. Two facts are now quarantined, both missing an `n ≠ 0` side condition:

- `Nat.log/log_lt_of_lt_pow`
- `Nat.divisors/divisors_mem_iff` — *kernel-confirmed false of the real `Nat.divisors`*

So the honest statement is: **no candidate has ever been shown unfaithful, and the instrument
currently cannot show one.** Fidelity divides by a denominator containing only facts we could
prove true; it cannot come out below 1.0.

---

# PART 2 — Verifier defects found (all verified against the kernel)

## 2.1 Tier 2 never unfolds the definition it is testing

For global (∀-quantified) facts, tier 2 runs `DEFAULT_TIER2_TACTICS` = `rfl, omega, norm_num,
positivity, simp, exact?, aesop`. **None unfold the candidate's own `def`.** The unfolding tactics
exist (`with_membership_tactics` in `ladder/budgets.py` → `simp [VTask.X]`, `simp only [VTask.X]
<;> aesop`) but are wired only into the decide-fallback path (`ladder/adjudicate.py:102`).

**Verified**, on a correct `Nat.divisors` candidate, fact `∀ n, 0 < n → n ∈ VTask.divisors n`:

| tactic | result |
|---|---|
| `by simp` (in tier 2's set) | FAILED |
| `by aesop` (in tier 2's set) | FAILED |
| `by intro n hn; simp [VTask.divisors, hn.ne', Finset.mem_filter, Finset.mem_range]` | **PASSED** |

And on a `Nat.choose` candidate that is *character-for-character Mathlib's definition*, fact
`∀ n, VTask.choose n 0 = 1` — literally its own first clause: `simp` FAILED, `aesop` FAILED,
`by intro n; cases n <;> rfl` **PASSED**.

579 of the 731 unknowns are global facts attacked by tactics forbidden to look inside the symbol
under test.

## 2.2 Tier 4 (equivalence) cannot do induction

Equivalence is decisive when it lands: **all 27 equivalence-certified candidates have zero
unknowns, and all 544 of their facts resolved via tier 4.** Conversely **all 731 unknowns sit in
the 189 non-certified candidates**, without exception.

But tier 4 states the goal as `VTask.X = Mathlib.X` and tries only tier-2 tactics then hammer.
Function equality between two recursive definitions needs `funext` + induction.

**Verified** on the byte-identical `Nat.choose` candidate:

| tactic | result |
|---|---|
| `rfl` (tier 4's first attempt) | FAILED |
| `simp [VTask.choose, Nat.choose]` | FAILED |
| `aesop` | FAILED |
| `funext n k; induction n generalizing k …` (5 lines) | **PASSED** |

`Nat.choose` has 16 admissible candidates, **0 certified**, 128 unknowns. One five-line proof on
any of them would have discharged its 8 global facts at a stroke.

## 2.3 The truth countercheck was too weak (now fixed)

`llm_prover.py check --direction negation` certified FAIL from any kernel-accepted negation,
without checking the truth survives the same attack. Its countercheck used a generic
`push_neg/simp_all/aesop` ladder, which **cannot rediscover a counterexample witness**.

**Verified** on `Nat.divisors/divisors_mem_iff`: generic ladder returns `False` (never guesses
`n=0, d=1`); the model's own four-line script, ported to the truth, returns `True` instantly. The
same defective fact therefore produced spurious FAILs on three separate runs.

**Fixed**: the countercheck now ports the model's refutation script to the truth and tries that
first, keeping the ladder as fallback. Corpus FAIL count is now 0, which is the honest state.

## 2.4 Definitions that do not reduce kill every `decide` fact

90 unresolved facts are `by decide`-shaped, nearly all belonging to definitions the kernel cannot
evaluate. Two sub-cases:

- **Noncomputable** — e.g. `VTask.log b n = sSup {k | b^k ≤ n}`, mathematically the best `Nat.log`
  definition in the corpus; `sSup` is noncomputable, so all 12 of its decide facts fail.
- **Well-founded recursion** — e.g. a binary-search `nthRoot`; compiles to `WellFounded.fix`,
  which does not reduce, so all 19 of its decide facts fail.

Controlled comparison, same task and model family: the binary-search `nthRoot` has **29 unknowns
including all 19 decidable facts**; a `Nat.findGreatest`-based `nthRoot` has **8, all global** —
its 16 decidable facts all passed. Noncomputable candidates are **3.2% of the pool carrying 9.2%
of the unknowns**.

**This penalises definition-by-characterisation**, the style the project explicitly values (the
`Filter.limsSup` exemplar was chosen for exactly that).

## 2.5 Tier-2 wins record no winning tactic

`script` is empty for all 553 tier-2 wins. Since `exact?` (a Mathlib-wide search) is in that
tactic set, "closed by citing its own anchor theorem" is currently undetectable at scoring time
and had to be reconstructed by hand.

---

# PART 3 — What is wrong with the fact suites

## 3.1 Composition today

471 distinct facts across 41 tasks, ~11.5 per task:

| type / mechanism | distinct | share |
|---|---|---|
| `casework` / decide | 104 | 22% |
| `membership` / decide | 92 | 20% |
| **decidable subtotal** | **196** | **41.6%** |
| `global` / proof | 242 | 51% |
| `membership` / proof | 33 | 7% |

Badly skewed by definition style: `Nat.choose` has 21 decidable of 31 (68%); Prop-valued tasks
like `Relation.Fibration` have almost none.

## 3.2 Tautological facts — measured, 13.1% floor

Some "genuine theorem" facts merely restate the definition. Example, from `Relation.Map`:

```lean
def VTask.Map r f g := fun c d => ∃ a b, r a b ∧ f a = c ∧ g b = d

map_apply_iff_global : VTask.Map r f g c d ↔ ∃ a b, r a b ∧ f a = c ∧ g b = d
map_apply_unfold     : (the same statement, ℕ-instantiated)
```

**Verified**: `Iff.rfl` closes it. Any candidate written in that shape passes for free; a correct
candidate written differently could fail. It rewards syntactic conformity, not correctness.

Audit of all 275 proof-mechanism facts, testing `rfl`/`Iff.rfl` against the **truth**:

| | count | share |
|---|---|---|
| SUBSTANTIVE | 239 | 86.9% |
| RESTATEMENT | 33 | 12.0% |
| ANCHORED_TO_DEFINITION | 3 | 1.1% |

This is a **floor**, not an estimate: `rfl`-closure is sufficient evidence of restatement, not
necessary. An earlier n=5 study (`docs/tier_cascade_measurement_2026-07.md`) using
"`exact?` cites its own anchor" found **100%**.

### Corrected resolution figures

An earlier figure I gave — "1,046 of 1,687 genuine theorem facts resolved, 62.0%" — was inflated
by these. Corrected, splitting by discriminating power:

| stage | **discriminating** | restatement |
|---|---|---|
| tier 2 | 425 | 128 |
| tier 3 | 29 | 0 |
| tier 4 equivalence | 162 | 50 |
| tier 5 DeepSeek | 100 | 11 |
| tier 5 Sonnet | 54 | 4 |
| tier 5 Goedel-32B | 35 | 3 |
| tier 5 Goedel-8B | 34 | 2 |
| tier 5 Qwen | 8 | 1 |
| **UNKNOWN** | **613** | 28 |
| **TOTAL** | **1,460** | **227** |

**Resolution on discriminating facts: 58.0%**, not 62.0%. Restatements resolve at **87.7%** versus
58.0% — they are 13.5% of instances but 23% of resolutions. Tier 2 is worst affected: 128 of its
553 wins (23%) are tautologies.

## 3.3 How the tautologies got in

Facts are **authored**, not copied — the prompt forbids verbatim reproduction and requires a fresh
statement citing Mathlib **anchors**. Three things then combined:

1. **Mathlib genuinely contains definitional lemmas.** `Relation.map_apply` is a real, named,
   used lemma, proved there by `Iff.rfl` because it is unfolding API. A fact faithfully derived
   from it inherits that triviality. Nothing malfunctioned.
2. **Anchors are not required to be theorems.** `map_apply_unfold` is anchored to `Relation.Map` —
   the definition itself.
3. **The mitigation existed and was discarded.** The prompt instructs the model to set
   `self_restatement: true` for near-verbatim anchor restatement *and* for "a Prop-valued task's
   own definitional unfolding". But `authoring/facts.py:115` marks it
   **"authoring-time-only: never reaches a shipped task.json fact entry"**, because its schema home
   is `discharge.self_cited` and `discharge` is null for every shipped fact. The signal is computed
   and thrown away before scoring can use it.

This was a **known, logged risk**: `docs/deferred.md` carries a "self-citation" entry concluding it
"needs a design answer … before mentions-as-facts is viable."

## 3.4 Validation checks truth, never discriminating power

`validation_status: PROVISIONALLY_VALIDATED, "validated against ground truth"` asks *is this fact
TRUE of the real object?* It never asks *could this fact ever be FALSE of a plausible misreading?*

Worse, it does not appear to have run the kernel: two shipped facts are **false of the truth**
(§1.4), and both carry that status.

## 3.5 Zero mutants exist

**No task has any mutant suite — 0 across all 41.** The schema supports them and
`harness/scoring.py` reads them. **Separation has never been measured.** Every number in this
document is fidelity only.

## 3.6 Near-miss / reject facts are thin and unlabelled

Facts asserting an object is *not* in the extension — the only thing that can catch a vacuous
definition:

| | count |
|---|---|
| reject-shaped facts (`¬`, `∉`, `≠`) | 88 of 471 (18.7%) |
| explicitly labelled `polarity: reject` | **46** |
| tasks with ≥1 | 24 of 41 |
| **tasks with none** | **17** |

The 17 with none include **`Monotone`** and **`DependsOn`**, both Prop-valued. Every `Monotone`
fact asserts some function *is* monotone. **Inference, not yet verified:** `def VTask.Monotone
(_ : α → β) : Prop := True` would be admissible and pass every fact — fidelity 1.000. This is the
vacuity failure the reward doc names first, apparently live in the corpus.

## 3.7 A reading of 50 definitions

I read 50 distinct (task, definition) pairs carrying unknowns — 391 unknown instances, 61 distinct
(task, fact) pairs, across `Nat.divisors` 13, `Relation.Fibration` 13, `Nat.choose` 10,
`Relation.CutExpand` 10, `Nat.nthRoot` 4. My judgement:

| | count |
|---|---|
| Correct and equivalent to the Mathlib object | **48** |
| Correct but semantically **stronger** than the truth | 1 |
| Not verifiable by inspection | 1 |
| **Clearly wrong** | **0** |

The one deviation: a `CutExpand` variant adding `a ∈ s`, which is derivable under irreflexivity
but strictly stronger without it — precisely the "typed plausible misreading" mutants exist to
catch, and the suite scored it identically to the correct variants.

**Definitional shape drives provability at least as much as correctness does.** Three `Nat.choose`
candidates are correct but use well-founded recursion with truncated subtraction (`n-1`); their
equation lemmas do not reduce and induction does not align with the recursion. They are far harder
to reason about than the structurally-recursive form denoting the same function.

Full detail: `docs/unknown_facts_reading_2026-08-11.md`.

---

# PART 4 — Design proposals

Ordered by leverage. (1)–(4) are cheap and unambiguous; (5) is the structural change; (6)–(7)
need an operator decision.

### 1. Validation must *prove* each fact of the truth
Discharge every fact against the real Mathlib object at authoring time; a fact that cannot be
proved ships as `UNVALIDATED`. Also attempt the **negation** — that is how both defective facts
were eventually caught, months late.

### 2. Ship `self_restatement`, backed by a mechanical check
The model already computes it and it is discarded. Ship it, and independently reject facts closed
by `rfl`/`Iff.rfl` against the truth. **Require anchors to resolve to theorems, not definitions.**

### 3. Record the winning tactic on tier-2 wins
Makes "closed by `exact?` citing its own anchor" measurable at scoring time.

### 4. Give tier 2 the unfolding tactics on global facts, and teach tier 4 `funext` + induction
Both verified to convert UNKNOWN → PASS on real corpus examples. These target the 613 remaining
discriminating unknowns directly and cost no new generation spend.

### 5. Near-miss objects as a **gate** — the structural change

Not perturbed *definitions* (a perturbed definition usually fails many facts at once, so it does
not isolate which fact discriminates). Instead: **objects the definition should NOT accept**,
with facts of the form `¬ VTask.P(witness)`. A group definition is pinned down by a monoid that
isn't a group.

**Generation rule:** for a definition that is a conjunction `P₁ ∧ … ∧ Pₙ`, emit **one near-miss
per condition** — an object satisfying every `Pⱼ` for `j ≠ i` and violating `Pᵢ`. Every defining
clause then has a fact that fires if a candidate drops it.

Why this is the right mechanism:

- **It kills vacuity**, which nothing currently does (§3.6).
- **Refutation is usually cheap** — `¬P(concrete witness)` on a concrete carrier is often `decide`
  or two lines of `simp`, i.e. kernel computation. This sidesteps the disproof machinery entirely,
  which matters because refuting a false *global* fact has never once succeeded. Separation becomes
  measurable now.
- **It is how mathematicians pin down definitions** — via non-examples.

**Make it a gate:** a Prop-valued task shipping with zero reject facts fails authoring validation,
the way a task with no fact supply does. Also set `polarity` on all of them (42 of the current 88
are unlabelled and cannot be selected on).

**Honest limitation:** ~70% of the batch-5 eligible pool is value-typed, where the near-miss idea
degrades to wrong-value and boundary facts. Full strength lands on the Prop-valued and bundled
minority — which is also where the hardest definitions live.

### 6. Prune interior decidable facts; keep boundary ones

Consider what actually kills `choose 10 3 = 120`. A plausible misreading (boundary shifted, side
condition dropped, inequality flipped) is wrong at the **boundary** and computes the interior
correctly. Killing an interior spot-check needs an artificial piecewise mutant. Whereas
`choose 0 0 = 1` and `choose 4 5 = 0` are killed by realistic misreadings.

So: **keep boundary and degenerate-case checks, drop interior arithmetic spot-checks.** This also
reduces the computability penalty on noncomputable definitions for free.

**Important asymmetry:** decidable facts are weak on the *truth* side but the **strongest** thing
available on the *mutant/reject* side, where `decide` refutes instantly. 35 of the current 88
reject facts are decide-mechanism. Prune decidables from positive suites; lean on them for kills.

### 7. Report fidelity per fact class, not one weighted number

Operator proposal was to weight decidable facts at half. Reasonable, but a single weighted number
hides composition, and composition varies enormously (68% decidable for `Nat.choose`, ~0% for
`Fibration`). Prefer reporting fidelity per class — decidable / membership / global — and deriving
a headline if one is needed. Then a model passing only arithmetic spot-checks is visibly different
from one proving global theorems.

### 8. One line in the negation prompt

The current prompt says "typically: `push_neg`, then exhibit a concrete counterexample witness".
Add: **try small/boundary values first** (`0`, `1`, empty, the boundary) before attempting a proof.
That is exactly how the one real counterexample in the corpus was found.

---

# PART 5 — Open questions for planning

1. **Should a correct noncomputable definition score better than it does?** Operator view: yes.
   Options: emit a proof-mechanism counterpart for each decidable fact; or record definition style
   and report separately. Doing nothing keeps penalising definition-by-characterisation.

2. **Can all facts be refuted by counterexample? No.** Three classes resist it: infinite witnesses
   (`WellFounded (CutExpand r)`); type-quantified facts (refuting requires *choosing* a type and a
   relation); and `↔` facts. This argues for biasing generation toward facts whose negation is
   constructible — currently a small minority.

3. **Do models do enough counterexample checking? Unknown — there are no positive controls.**
   DeepSeek produced 731 negation scripts at 100% yield and landed zero, but nearly every fact it
   was asked to refute is *true* of its candidate (48/50 definitions read are correct), so zero is
   the correct answer. We have never handed a model a fact genuinely false of its candidate and
   checked whether it finds the witness. The one time a real counterexample existed, DeepSeek found
   it immediately and repeatedly. **Near-miss facts and mutants would provide exactly these
   positive controls.**

4. **Equivalence is the gold standard while a reference exists.** For this corpus we have the
   truth, and `candidate = Mathlib.X` resolves everything when it lands (27/27). Mutants and
   near-misses matter because the eventual target — novel definitions with no reference — has no
   truth to compare against. They are a rehearsal for the reference-free setting, not the best
   available test today.

5. **Re-mine the two quarantined facts** with their `n ≠ 0` hypotheses restored
   (`scoring_output/suspect_facts.json`).

---

# Appendix — artifacts

| file | contents |
|---|---|
| `scoring_output/smoke32b_scores/` | per-candidate verdict tree, 3,045 fact verdicts |
| `scoring_output/fact_discrimination_audit.json` | the 275-fact restatement audit |
| `scoring_output/suspect_facts.json` | 2 quarantined defective facts |
| `docs/unknown_facts_reading_2026-08-11.md` | the 50-definition reading, with worked examples |
| `docs/tier_cascade_measurement_2026-07.md` | earlier n=5 self-citation measurement (100%) |
| `docs/deferred.md` | self-citation and context-stripping entries, with triggers |
| `scripts/audit_fact_discrimination.py` | reproducible restatement audit |
| `scripts/llm_prover.py` | tier 5, both directions, Bedrock + Converse + vLLM backends |
