# Stage D first look — decide component, PROVISIONAL (2026-08-06)

**Not the committed selection.** Governed by `docs/preregistration_prelim_scoring.md` (committed
before any verdict). The decide component alone cannot select a base model, for a reason the
pre-registration did not anticipate — see "The headline is not the table".

## Run stats

| | |
|---|---|
| Candidates scored | **948** distinct bodies → **1,039** verdict files (dedup fan-out) |
| Wall-clock | **3.5 min**, 0.219 s/candidate |
| `env_probe_fires` / server recycles | **0** / 4 |
| Cost | **$0** — see "Where this ran" |
| Proof facts | marked `NOT_ATTEMPTED_THIS_PASS`; records cover `decide` only, so Stage E appends without rescoring |

## The headline is not the table

**The decide component reaches only 16 of 41 tasks. 25 tasks have zero decide facts at all.**
After admissibility filtering it reaches far less: the macro average is computed over **7, 8 and
3 tasks respectively** — different task sets per model, so the three numbers are not comparable
with each other even in principle.

Within that narrow reach the metric is **saturated**: 96.7% / 98.2% / 97.1%. It does not
discriminate, because a candidate that survives admissibility on an arithmetic task has almost
always got the definition right — the decide facts then confirm what admissibility already
implied.

The pre-registration's coverage fallback anticipated the *proof* component being thin
("if corpus-wide non-UNKNOWN coverage on the proof component is below 30%, the band rule reads
decide-only"). The decide component turns out to have the more severe coverage problem, and
**"decide-only" is therefore not a viable fallback** — it is a 16/41-task instrument that
saturates. That needs an amendment before selection, and it is a finding about the *corpus*
(fact-type distribution), not about the models.

## (1) Model × verified rate — decide component, provisional

| model | macro | micro | candidates | admissible | adm % | facts resolved | coverage | noncomp % | tier-4 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| goedel-prover-v2-8b | 98.2% | 98.9% | 258 | 49 | 19.0% | 523/523 | 100.0% | 3.9% | 9 |
| goedel-formalizer-v2-8b | 97.1% | 96.8% | 371 | 86 | 23.2% | 600/836 | 71.8% | 32.1% | 8 |
| qwen2.5-coder-7b-instruct | 96.7% | 97.0% | 410 | 49 | 12.0% | 197/233 | 84.5% | 2.0% | 0 |

Macro over **8 / 7 / 3 tasks** respectively. **Do not read this as a ranking.**

## (2) The funnel — where the actual signal is

| model | total | compile_error | wrong_type | sorry | name_shadowed | **admitted** |
|---|--:|--:|--:|--:|--:|--:|
| goedel-formalizer-v2-8b | 371 | 138 | 22 | **124** | 1 | **86 (23.2%)** |
| goedel-prover-v2-8b | 258 | 194 | 12 | 0 | 3 | **49 (19.0%)** |
| qwen2.5-coder-7b-instruct | 410 | **355** | 4 | 1 | 1 | **49 (12.0%)** |

Three behavioural differences that the saturated verified-rate hides entirely:

- **Goedel-Formalizer emits `sorry` in 124 of 371 candidates (33%)**; Goedel-Prover emits it
  **zero** times and Qwen once. That is a large, clean stylistic split — Formalizer will hand back
  a well-typed skeleton with the content missing, and the other two will not.
- **Qwen produces the most candidates (410, every sample extractable) and the fewest admissible
  (12%)** — 355 outright compile errors. High fluency, low Lean correctness.
- **`WRONG_TYPE` is real but small** (22 / 12 / 4). It fires most for Formalizer, consistent with
  it writing plausible-looking signatures that don't match the pin.

## (3) Per-candidate histogram (admissible only)

| model | 0% | 0–25% | 25–50% | 50–75% | 75–100% | 100% | unscored |
|---|--:|--:|--:|--:|--:|--:|--:|
| goedel-formalizer-v2-8b | 0 | 0 | 0 | 3 | 1 | **42** | 40 |
| goedel-prover-v2-8b | 0 | 0 | 0 | 1 | 0 | **30** | 18 |
| qwen2.5-coder-7b-instruct | 0 | 0 | 0 | 0 | 2 | **10** | 37 |

**Bimodal to the point of being binary**: an admissible candidate almost always scores 100% or is
unscorable. Only 7 candidates in the whole run land strictly between. "Partial credit" is not
what this instrument measures on the decide component.

The **unscored** column (40 / 18 / 37) is admissible candidates whose every decide fact came back
UNKNOWN. Only 8 / 2 / 7 of those are noncomputable, so noncomputability is *not* the main driver
— the rest are tasks whose decide facts don't evaluate for other reasons.

## (4) Candidate-level metric — the discriminating one

Fraction of **all** candidates (inadmissible included, per the pre-registration's candidate-level
denominator) that are admissible and pass every resolved fact:

| model | all-pass / total | rate |
|---|--:|--:|
| goedel-prover-v2-8b | 30 / 258 | **11.6%** |
| goedel-formalizer-v2-8b | 42 / 371 | **11.3%** |
| qwen2.5-coder-7b-instruct | 10 / 410 | **2.4%** |

This discriminates where the per-fact metric does not. **Note the band consequence**: on the
per-fact metric all three sit at ~97%, far ABOVE the 15–55% band (all skyline, no selection); on
the candidate-level metric all three sit at 2–12%, BELOW it. **Neither yields an in-band
selection**, and the two disagree about direction. Surfaced as **contested**, not resolved here.

## (5) Coverage, suspect facts, RECALLED_TARGET

**Suspect facts: 0.** No fact was failed by every admissible candidate of every model — no
truth-side defect surfaced by this pass. That is a genuine (if quiet) positive result about the
corpus.

Lowest-coverage tasks: `Nat.nthRoot` 32.8% (65/198), `Nat.clog` 70.4%, `Nat.log` 79.7%,
`Nat.ModEq` 87.5%; the remaining reached tasks are at 100%.

RECALLED_TARGET slice (first-pass names only; "harder" flags remain unrecoverable for the 19
repaired names):

| model | recalled | other |
|---|--:|--:|
| goedel-formalizer-v2-8b | 95.7% (445 facts) | 100.0% (155) |
| goedel-prover-v2-8b | 98.2% (332) | 100.0% (191) |
| qwen2.5-coder-7b-instruct | 100.0% (137) | 90.0% (60) |

Saturated everywhere; no usable signal at these denominators.

**Tier-4 fast path fired 9 / 8 / 0 times.** Qwen never once produced a definition definitionally
equal to the truth, while both Goedel models did. That is a memorization signal the verified rate
cannot see, and it is the cheapest available proxy for the verbatim/non-verbatim split the
pre-registration requires at Stage E.

## Where this ran, and why it is not a deviation

Stage D ran **on the Mac, not the EC2 box**. The AWS session token expired and refreshing it
needs an interactive MFA code. The two reasons scoring was assigned to the box — multi-worker
memory pressure and EC2-only tier 3 — apply to neither this pass (single worker) nor this
component (decide facts are kernel computation; no tactic search, no hammer). Both machines pin
the identical Mathlib commit `81a5d257c8e410db227a6665ed08f64fea08e997`, verified at pre-flight,
so the verdicts are the same computation either way. **Stage E still needs the box**, since the
early-hammer trigger can only be honoured there.

## Priority rule: invoked once

The first bounded run (`--limit-candidates 50`) returned **zero admitted of 53** — a systematic
surprise against the smoke's 6/9. Stopping there was correct and cheap. Diagnosis:

1. Alphabetically-first tasks (`DependsOn`, `Equiv.*`, `Filter.*`) are the hardest — genuine model
   failures, not a harness fault. Confirmed by re-running `Nat.clog`, which reproduced the smoke
   exactly (6/9 admitted).
2. **But it also exposed a real harness bug**: `Monotone` returned 7/7 `WRONG_TYPE` on *correct*
   candidates. The type probe `#check (name : type)` does not bind the universe variables a `def`
   auto-binds, failing with ``unknown universe level `u` ``. **32 of the 41 tasks carry universe
   variables**, so unfixed this would have manufactured false `WRONG_TYPE` across 78% of the
   corpus — and it would have read as a model failure, not a harness one. Fixed by prefixing a
   `universe` declaration; wrong types are still rejected (both directions tested).

The 62 records written before the fix were discarded and the pass re-run from scratch.
