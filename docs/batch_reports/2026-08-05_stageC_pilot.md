# Stage C pilot — tier-2 discharge calibration (2026-08-05)

Statement of record for the C→C2 trigger. Run on the EC2 box (`~/verifier-lean`, Hammer-enabled
project, Lean v4.32.0 / Mathlib `81a5d257c8e4…`), tiers 1–2 only, against the **truth splice**.

## Headline

| | |
|---|---|
| Facts selected | 20, across **20 distinct tasks** |
| **Elaborated** | **20/20 (100%)** |
| **Tier-2 discharged** | **15/20 = 75.0%** of elaborated |
| Trigger read | **≥60% → "no hammer for prelim"** (reported, not acted on) |
| Total wall-clock | **23.9 s** for all 20 |
| Cache entries written | 15 (first entries ever — the cache was empty) |
| Server recycles / env-probe fires | 1 / 0 |

**Tier 3 did not run.** It is not merely disabled by budget: `ladder.adjudicate.adjudicate_fact`
calls the hammer unconditionally and Hammer *is* installed on this box, so the pilot driver calls
the elaboration probe and `adjudicate_tier2` directly. The tier-3 code path is never reached.

## Read the 75% carefully — it understates the corpus

The sample deliberately **over-samples the hard stratum**. Membership facts are 12% of the
corpus's proof facts (33 of 275) but 30% of this sample (6 of 20), because a stratum that never
appears cannot be measured.

| Fact type | Discharged | Corpus share |
|---|---|---|
| `global` | **14/14 = 100%** | 242 / 275 (88%) |
| `membership` | **1/6 = 17%** | 33 / 275 (12%) |

Corpus-weighted: `0.88 × 100% + 0.12 × 17%` ≈ **90%**.

So the honest statement is: **the trigger reads "no hammer" on the sampled 75%, and the
corpus-wide rate is probably nearer 90%** — the conclusion is robust in the direction that
matters, and a convenience sample of global facts would have reported ~100% and been useless for
calibration. The stratification is the reason this number can be trusted at all.

## The real finding: membership facts are a different problem

All five non-discharges are membership facts, and they are the *only* five:

- `Pi.Lex/lex_accept_pivot0` (7.4 s)
- `Relation.CutExpand/cutexpand_empty_source_reject` (0.6 s)
- `Relation.Fibration/fibration_not_subrel_reject` (0.2 s)
- `Relation.Map/map_lt_accept` (0.1 s)
- `Set.PartiallyWellOrderedOn.IsBadSeq/isbadseq_mem_const_lt_accept` (4.5 s)

These are facts of the form "this specific element is/is not in the object", on Prop-valued
relational definitions. They elaborate fine — the tactic set simply doesn't close them. Three of
the five failed in under a second, i.e. the ladder exhausted quickly rather than timing out,
which suggests a **missing tactic class rather than an insufficient budget**. That is a cheaper
fix than the hammer and worth trying before C2 is ever considered.

**Confound, stated rather than buried**: Prop-valued tasks show 3/8 versus 12/12 for value-typed,
but the membership picks were drawn from Prop-valued tasks, so type and Prop-ness are not
separated by this sample. Do not report the Prop/value split as an independent effect.

## Per-tactic cost (every attempt, winners and losers)

| tactic | attempts | total | mean | max | wins |
|---|--:|--:|--:|--:|--:|
| `exact?` | 11 | 12.46 s | 1.133 s | 7.17 s | **6** |
| `norm_num` | 20 | 5.21 s | 0.260 s | 2.93 s | **9** |
| `simp` | 11 | 4.81 s | 0.437 s | 2.90 s | 0 |
| `rfl` | 20 | 0.25 s | 0.013 s | 0.03 s | 0 |
| `omega` | 20 | 0.21 s | 0.011 s | 0.03 s | 0 |
| `aesop` | 5 | 0.20 s | 0.041 s | 0.12 s | 0 |
| `positivity` | 11 | 0.07 s | 0.007 s | 0.02 s | 0 |

**Only `norm_num` and `exact?` ever win**, and together they are 76% of the wall-clock. The four
non-winning tactics cost 0.73 s across all 20 facts combined, so there is **no case for trimming
the ladder on cost grounds** — they are free insurance. `exact?`'s 7.17 s maximum is the
library-search index building once per environment, consistent with Session A's finding.

Budget note: the per-fact ceiling is 300 s and the slowest fact here took 7.4 s. **The current
budgets are not the binding constraint** on this population.

## Corpus finding: authored facts elaborate

**20/20 elaborated.** The prior from `docs/tier_cascade_measurement_2026-07.md` was 5/60 (8.3%),
but that measured *mined mention* statements stripped of their `variable`/`namespace` context.
Authored facts carry their own context by construction. This closes the open question of whether
the ladder's near-total elaboration failure would recur on the real corpus: **it does not**, and
the earlier number should not be quoted as a property of the ladder.

## Truth-side debt: first payment

15 proof scripts now exist where the corpus had none — all 275 proof facts are
`PROVISIONALLY_VALIDATED` with `cached_script: null`. Written to
`scoring_output/pilot_script_ledger.jsonl` (fact id → tactic → script) and to the previously
non-existent `ladder/output/proof_script_cache.jsonl`. **`task.json` was not mutated**; folding
these back into the corpus is a separate, deliberate step after prelim.

---

## Amendment (2026-08-06): what the 14/14 actually measures

**The global-fact successes are anchor LOOKUP, not proving ability.** Global facts were mined as
short restatements anchored to existing Mathlib theorems. On the truth splice the task symbol is
defeq to the real definition, so `exact?` finds the anchor theorem on the shelf. The 14/14 is
evidence the facts are **well-anchored**, not evidence the ladder can construct hard proofs.
Membership facts failed precisely because they are bespoke concrete claims with no library twin.

### Standing caveat — do not extrapolate this number

**Tier-2 discharge measured on Mathlib-anchored facts must not be extrapolated to unanchored
corpora.** On never-formalized definitions (the future `Def_Wiki` / `Def_ArXiv` credible core)
there is no shelf, `exact?` is likely useless, and the hammer — which *constructs* proofs rather
than finding them — is the designated tool. **Re-pilot on the first fresh-source batch before
budgeting its certification.** The hammer is parked for the prelim, not deleted.

### Membership-tactic experiment: 4/5 recovered, extension adopted

The pilot's five non-discharges were re-run with definition-unfolding tactics
(`scripts/membership_tactic_probe.py`):

| fact | outcome |
|---|---|
| `Pi.Lex/lex_accept_pivot0` | recovered — `simp [VTask.Lex, Pi.Lex]` |
| `Relation.CutExpand/cutexpand_empty_source_reject` | recovered — `simp [VTask.CutExpand, Relation.CutExpand]` |
| `Relation.Map/map_lt_accept` | recovered — `simp [VTask.Map, Relation.Map]` |
| `Set.PartiallyWellOrderedOn.IsBadSeq/…` | recovered — `simp [VTask.IsBadSeq, …IsBadSeq]` |
| `Relation.Fibration/fibration_not_subrel_reject` | **still UNKNOWN** |

**4/5, every one via the same shape, in ~0.6 s for all five combined.** The membership gap was
never a proof-search deficiency — the pinned tactic set simply never unfolded the definition.
Both names must be unfolded: the splice is `@[reducible] def VTask.X := _root_.Real`, so naming
only the task symbol can resolve to the alias without reaching the real body.

Adopted uniformly as `ladder.budgets.with_membership_tactics`, **appended** after the pinned set
so cheap-first ordering is preserved and nothing already discharging changes behaviour.

The survivor is a **negated** higher-order claim (`¬ VTask.Fibration …`), which needs a
counterexample exhibited rather than a goal simplified — a genuinely different shape, and a fair
thing for the ladder not to get.

### Revised discharge estimate

| | sampled | corpus-weighted |
|---|--:|--:|
| Pilot as run | 15/20 = 75% | ~90% |
| **With the membership extension** | **19/20 = 95%** | **~98%** |

`0.88 × 100% + 0.12 × 83% ≈ 98%`. The "no hammer for prelim" trigger is not marginal.

### Required Stage E view (build it with Stage E)

**Proof-fact UNKNOWN rate split by verbatim vs non-verbatim candidates** (dedup hash vs the real
definition is a cheap verbatim proxy). On a *candidate* splice the anchor theorem only applies if
the candidate unfolds to match the truth — so `exact?` works for memorizers and may fail on
correct-but-rephrased candidates. Proof-fact UNKNOWNs would then correlate with **phrasing, not
wrongness**, flattering memorizers if unwatched.

**If non-verbatim correct candidates drown in UNKNOWNs at Stage E, that is the trigger that
reopens the hammer early** — not truth-side coverage. Stage D is untouched by any of this:
decide facts are kernel computation, indifferent to phrasing and to proof search entirely, which
is exactly why the decide component is the pre-registered clean backbone.
