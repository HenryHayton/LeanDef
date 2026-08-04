# Pre-registration — Prelim scoring and base-model selection

Committed 2026-08-06, before any candidate verdict has been computed. Governs the analysis of the
4 Aug prelim samples. Deviations require a dated amendment stating what changed and why.

**Scope.** This round measures **fidelity only**. The corpus carries no mutants (schema v1.1
reserves the field); separation is not computable and is not claimed. Fidelity-only is exactly
the metric a vacuous definition can pass; this limitation is accepted for base selection — the
band rule concerns headroom, not candidate certification — and is mitigated only by admissibility
+ decide-fact kills. `heldout` is `false` corpus-wide; no held-out slice is reported.

**The field.** Three models measured: Goedel-Prover-V2-8B, Goedel-Formalizer-V2-8B,
Qwen2.5-Coder-7B-Instruct. Kimina-Prover-Distill-7B, Herald, and DeepSeek-Prover-V2 are
**excluded-unmeasured**, shared cause: vLLM 0.26 detokenizer corruption (4 of 7 candidates
affected; the Qwen-family-only hypothesis is retired). No Kimina number is reported anywhere.

**Primary metric.** Per-fact verified fraction, **macro-averaged over tasks** (mean of per-task
fractions); pooled micro-average reported alongside. PASS includes tier-4 equivalence-certified
facts (fast-path share reported per model, not discounted). Denominators exclude UNKNOWN and
ERROR; per-task coverage reported alongside every fraction.

**Verdict semantics.** Decide-mechanism facts: PASS / FAIL / ERROR — FAIL requires kernel-certified
refutation; `Decidable`-synthesis failure is UNKNOWN; machinery failure is ERROR. Proof-mechanism
facts: PASS / UNKNOWN / ERROR — a tactic failing to prove is never evidence against a candidate.
Proof-fact UNKNOWN means "could not test", never "failed"; UNKNOWN rates are reported per model
and per verbatim/non-verbatim slice, and a differential UNKNOWN pattern is itself a headline
result, with the early-hammer trigger attached (see Amendments). Infra errors: one retry, then
ERROR, excluded-and-reported. `NOT_ATTEMPTED_THIS_PASS` marks proof facts pending the
proof-component pass and is excluded from all metrics.

**Temperature.** Pooled (0.7 + 1.0) primary; split reported.

**Components.** Decide-mechanism (196 facts, kernel-certified truth-side) and proof-mechanism
(275 facts, provisionally validated, never kernel-certified truth-side except the pilot-certified
side ledger) reported separately in every table, then combined. **Coverage fallback:** if
corpus-wide non-UNKNOWN coverage on the proof component is below 30%, the band rule reads
decide-only, proof supplementary; between 30–60%, combined governs with a decide-only sensitivity
check — a flipped winner is surfaced as **contested**, not resolved silently.

**Selection rule.** The model whose primary metric lies **closest to the middle of the 15–55%
band (35%)** is selected as training base — *not* the highest scorer; above-band models become
the reported skyline. Tie-break: trainability (tokenizer/family compatibility with the training
stack, context length, license).

**Suspect facts.** Any fact FAILED by every admissible candidate of every model is flagged
suspect, excluded from all denominators, and listed for truth-side inspection.

**Candidate accounting.** Dedup by normalized hash; verdicts fan out to all samples sharing a
hash, with provenance recorded. Extraction recomputed from `completion` with the current
extractor; stored flags untrusted. The funnel (unextractable → COMPILE_ERROR → WRONG_TYPE →
SORRY/NEW_AXIOM/NAME_SHADOWED → admissible-partial → all-facts-pass) reported per model;
inadmissible candidates score zero facts but remain in candidate-level denominators. Bare-alias
candidates are **scored, not excluded** (deferred-ledger trigger fired; resolution recorded).
Known differential-coverage mechanism, on record before results: noncomputable candidates cannot
evaluate decide facts (correctly UNKNOWN), so they are judged on proof facts only; smoke incidence
~48% of adjudications on the clog sample. Per-model noncomputable-emission rate (model-written or
splice-added) reported alongside coverage.

**Committed report views:** (1) per-candidate fact-pass histogram per model; (2) model × task
heatmap, mean and best-of-10 per cell, with counts of all-10-fail tasks and sometimes-succeeds
tasks; (3) the funnel; (4) decide/proof split + coverage; (5) distinct-answers-per-task.
`RECALLED_TARGET` and "harder" slices carry the caveat that "harder" is **inferred** for the
repaired population (source: 31 Jul closing report; flags for the 19 repaired names
unrecoverable).

## Amendments (2026-08-06, pre-commit, from the truth-side pilot)

1. Tier-2 discharge on authored facts cleared the pre-registered **≥60% no-hammer threshold**
   (15/20 sampled; membership stratum the sole weakness). **Tier 3 does not run in the prelim by
   default.** These discharge rates are properties of the **Mathlib-anchored corpus construction**
   (facts mined as short anchored restatements; `exact?` resolves anchors on the truth splice) and
   **must not be extrapolated** to candidate-side coverage or to unanchored corpora.
2. The tier-2 set is extended with `with_membership_tactics` (definition-unfolding shape; adopted
   after recovering 4/5 pilot residue facts; appended after the pinned set so prior discharge
   behavior is unchanged), applied uniformly to all candidates in the proof-component pass.
   Sampled truth-side discharge after extension: **19/20**.
3. **Early-hammer trigger:** if the proof-component pass shows non-verbatim candidates with
   materially elevated UNKNOWN rates relative to verbatim candidates (the anchor-lookup failure
   mode), tier 3 is enabled for the proof component **before selection is finalized**, recorded as
   a further amendment.

## Not claimed

No separation/anti-gaming property; no candidate-level certification; no claim of proof-fact truth
beyond provisional validation (except the pilot-certified side-ledger facts, kernel-proved
truth-side); no comparison involving excluded models; no transfer of truth-side discharge rates to
any other population.
