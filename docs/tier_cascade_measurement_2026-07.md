# Tier cascade measurement, 2026-07-27 (Ladder worker, Session B)

60 real theorem statements ("mentions") drawn from `miner/output/mention_names.jsonl` for the
slice's ten definitions — Nat.clog, Nat.choose, Nat.ModEq, Monotone, Function.Bijective,
Relation.Map, Function.extend, Nat.findGreatest, Nat.divisors, DependsOn — 6 each (60/10, an
even split; the smallest-supply definition, Nat.ModEq, has exactly 6 mentions, so this is the
maximum even split the corpus supports). Statements taken as-is: the mined `statement_text`,
mechanically converted from `theorem <name> (binders) : T` to the bare-Prop canonical form
(schema v1.1 §3.1) as `∀ binders, T` (or bare `T` when there are no binders) — no namespace
`open`s, no manual fix-ups. Each statement runs elaboration probe → tier 2 → tier 3 (real
hammer, on the box) — no tier 4 (no candidates here, only truth-side statements) and no tier 5.

## Pre-registered predictions (written before running; the human explicitly waived registering
their own for this run — calibration framing)

- **Elaboration rate: ~50% (30/60).** Many mentions are theorems ABOUT the target definitions
  declared in files with `variable`/`section`-scoped implicit arguments (type classes, ambient
  ring/field parameters) that the mined `statement_text` doesn't carry — the exact
  "context-stripped real Mathlib statement" failure mode `docs/ec2_runbook.md`'s own smoke test
  already documented (2/7 failed elaboration there). Expect the concrete, Nat-only definitions
  (Nat.clog, Nat.findGreatest, Nat.divisors) to elaborate at a much higher rate than the
  abstract/generic ones (DependsOn, Relation.Map, Function.Bijective), which lean heavily on
  ambient type parameters.
- **Tier-2 discharge rate of elaborated statements: ~65%.** Every statement in this sample IS a
  real, already-proved Mathlib theorem — `exact?`/`aesop`'s library search is expected to find
  the statement's own source lemma (or an equivalent) directly and often, for anything that
  elaborates cleanly.
- **Tier-3 incremental discharge (of the tier-2 residual): ~20%.** Hammer's premise-selection
  route searches the same library tier 2's `exact?` already searched, so expect a real but
  modest increment — mostly goals needing a short multi-step combination tier 2's fixed tactic
  set can't assemble but hammer's ATP search can.
- **Self-citation rate (of certified facts): ~75%.** Given every statement is itself a real
  theorem, expect most tier-2/tier-3 successes to be the ladder finding and citing that exact
  source theorem (or a trivial restatement of it) rather than a genuinely independent proof —
  the atlas-poisoning risk this measurement exists to quantify, not suppress.

## Actuals

Raw output: `ladder/output/measurement_output.jsonl` (60 records) and
`ladder/output/measurement_cache.jsonl` (5 cache entries, one per certified fact), both synced
back from the box.

| Measurement | Predicted | Actual |
|---|---|---|
| Elaboration rate | ~50% (30/60) | **8.3% (5/60)** |
| Tier-2 discharge of elaborated | ~65% | **100% (5/5)** |
| Tier-3 incremental (of tier-2 residual) | ~20% | **no data — zero residual reached tier 3** |
| Self-citation rate (of certified facts) | ~75% | **100% (5/5)** |

The elaboration rate missed the prediction by a wide margin — not because the prediction's
*mechanism* was wrong, but because it badly underestimated the mechanism's severity. Manually
inspecting the `DOES_NOT_ELABORATE` statements confirms the failure is genuine, systematic
context-stripping, not a bug in the bare-Prop conversion: e.g. `Nat.clog_of_left_le_one`'s
canonical statement is `∀ {b : ℕ} (hb : b ≤ 1) (n : ℕ), clog b n = 0` — bare `clog`, needing
`Nat.clog` and thus the enclosing `namespace Nat` this mention's source file supplies but the
mined text doesn't; `Pi.mulSingle_mono`'s is `Monotone (Pi.mulSingle i : f i → ∀ i, f i)` — `i`
and `f` are free, declared as file-scoped `variable`s never captured per-mention. Every
inspected failure fits one of these two patterns (bare namespace self-reference, or a missing
`variable`/`section` binder) — exactly `docs/ec2_runbook.md`'s own "context-stripped real
Mathlib statement" finding, just far more pervasive across this sample than its 2/7 suggested.

Because tier 2 discharged every statement that DID elaborate, the tier-3 (hammer) leg of the
cascade never ran on real measurement data — zero wall-clock spent there, no incremental-rate
number to report. This is itself informative (see below), not a gap in execution.

### Per-territory table

| Definition | Elaborates | Certified (tier 2) | Self-cited |
|---|---|---|---|
| Nat.clog | 0/6 | 0/6 | — |
| Nat.choose | 3/6 | 3/6 | 3/3 |
| Nat.ModEq | 1/6 | 1/6 | 1/1 |
| Monotone | 0/6 | 0/6 | — |
| Function.Bijective | 0/6 | 0/6 | — |
| Relation.Map | 0/6 | 0/6 | — |
| Function.extend | 0/6 | 0/6 | — |
| Nat.findGreatest | 0/6 | 0/6 | — |
| Nat.divisors | 1/6 | 1/6 | 1/1 |
| DependsOn | 0/6 | 0/6 | — |
| **Total** | **5/60** | **5/60** | **5/5** |

7 of the 10 definitions contributed zero elaborating statements at all. The 3 that did
(Nat.choose, Nat.ModEq, Nat.divisors) are exactly the more concrete, Nat-arithmetic-flavored
territory the prediction expected to do relatively better — directionally correct even though
the absolute rate was far lower everywhere, including there.

### Wall-clock / cost accounting

Total measured wall-clock across all 60 statements: **16.4 seconds** (not the 1.5–2.5 hours
estimated going in). The estimate assumed most statements would reach real tactic/hammer search;
instead 55/60 short-circuited at the elaboration probe (a single fast `#check`, milliseconds
each) and never reached tier 2 at all. The 5 that did elaborate cost 0.01s–12.3s each (tier 2's
`exact?` dominates the one slow case — a cold library-search-index build, consistent with
Session A's own finding that `exact?`'s discrimination tree is built once per environment and
reused). Box time actually billed for this session (start to planned stop) is accounted for in
the final report, not here — this section is the measurement's own compute cost, which is a
small fraction of the session's total box time (most of which went to the earlier tier 3/4
verification work, Part 1/2).

### Retry-flip count

**Not instrumented this run** — `TierAttempt` records the tactic, status, and elapsed time, but
`harness.repl.run_checked`'s internal retry-on-timeout behavior isn't surfaced as a separate
count on the returned result, so there is no way to tell from `Adjudication`/`TierAttempt`
records alone whether a given attempt's reported outcome took one try or two. Flagged as a real
instrumentation gap (not attempted to fix this session — out of scope, and moot for this
specific run regardless, since zero attempts here approached their timeout budget).

### Self-citation

**5/5 certified facts (100%) were self-citations** — in every case, `exact?` closed the goal by
citing the statement's own source theorem (confirmed via a supplementary `by exact?` probe
parsing the `Try this: exact <term>` suggestion and checking it names the fact's own
`theorem_name`). This is the expected, worst-case-for-signal outcome the task's framing warned
about: since every sampled statement IS a real, already-proved Mathlib theorem, a tier-2/tier-3
"success" here demonstrates the ladder can *find a proof that already exists in the library it
searches*, not that it can independently re-derive the mathematical content. n=5 is too small to
generalize the *rate*, but the *direction* (100%, not "mostly independent") is unambiguous on
this data and consistent with the concern as stated.

### What this implies for ladder budgets and the fact-selection dial

1. **Fact selection cannot use raw "mentions" verbatim as anchor facts without solving the
   context-stripping problem first.** At an 8.3% standalone-elaboration rate, a fact suite built
   naively from mined mentions would be almost entirely `DOES_NOT_ELABORATE` — not a signal
   about proof difficulty, a signal about missing `variable`/`namespace` context the miner's
   current mention-extraction doesn't capture per-mention. This is a miner/authoring-pipeline
   gap, not a ladder gap; the ladder correctly and honestly reports `DOES_NOT_ELABORATE` for
   every one of these, which is the CORRECT behavior — the bug (if it's fixed as one) belongs
   upstream, in what gets captured per mention.
2. **Self-citation is real and needs a design answer before mentions-as-facts is viable at
   all**, independent of point 1: even fixing context-stripping wouldn't fix this — reusing a
   library's own existing theorem as a fact literally asks "can you find the theorem that's
   already sitting in the library," which every general-purpose tactic that does library search
   (`exact?`, `aesop`, hammer's premise selection) will trivially answer yes to. Facts drawn
   this way measure library-search competence, not the candidate-vs-truth distinction the
   verifier exists to make.
3. **Tier-3 budget defaults are unvalidated by this run** — zero real data on hammer's
   incremental contribution, since nothing reached it. The tier-3 budget dials
   (`tier3_wall_clock_s`, `tier3_premise_count`) remain exactly as Session A set them, informed
   by nothing beyond the standalone tier-3 correctness tests (Part 1) — a genuine measurement
   gap for a future run to close, ideally with a sample that elaborates at a much higher rate
   (either hand-authored facts, or mentions with reconstructed context).
4. **The pilot's own pre-registered measurement #1** (reward doc §11: "tier discharge cascade,
   truth-side... → tier-2 tactic-set tuning; hammer adoption depth") is what this run most
   directly informs, and its answer is blunt: the tactic-set tuning question is currently
   downstream of a data-supply problem, not a tactic-selection problem.
