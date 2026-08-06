# Session handoff — prelim scoring, pilot, Stage D/E, pre-tuning experiment (2026-08-04 → 08-07)

Written for a planning agent with no prior context on this session. Everything below is measured
unless explicitly flagged as inference. Statement of record for the prelim round; supersedes
earlier first-look numbers where they differ (Stage E was incomplete when those were written).

---

## 0. One-paragraph summary

Three open models were scored against the 41-task corpus. **Admissibility, not fidelity, is the
discriminating signal** — verified rates are saturated (~97–99%) among candidates that clear the
gate, while admission rates differ 2× across models. The corpus turns out to measure **recall of
short famous definitions** rather than construction: 26 of 41 tasks have no admissible candidate
from any model, and every survivor is a one-line `Prop`, a Mathlib alias, or a short arithmetic
wrapper. A separate 8-cell prompt experiment (3,280 generations) established that
**Goedel-Formalizer's 33% `sorry` rate is not prompt-addressable** — four instruction strengths ×
two scaffolds all fail — but that instructions *do* improve the quality of non-punting attempts
(+6.8 pts conditional admissibility). Prompting buys quality-within-reach, not reach.

---

## 1. The measured field

| model | candidates | admissible | **adm %** | survivors | decide fid | proof fid | proof cov | noncomp % | tier-4 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Goedel-Formalizer-V2-8B | 371 | 86 | **23.2%** | 34 | 96.8% | 100% | 63.6% | **32.1%** | 13 |
| Goedel-Prover-V2-8B | 258 | 49 | **19.0%** | 19 | 98.9% | 100% | 64.5% | 3.9% | 10 |
| Qwen2.5-Coder-7B-Instruct | 410 | 49 | **12.0%** | 9 | 97.0% | 100% | 67.0% | 2.0% | 0 |

`survivor` = admissible, no FAIL, ≥1 PASS, nothing unresolved. 1,039 candidate records total.

**Proof fidelity is 100% by construction** and carries no information: proof facts may only be
PASS/UNKNOWN/ERROR (a tactic failing to prove is never evidence against a candidate). The
informative proof-side number is **coverage** (63.6–67.0%), i.e. how much could be tested at all.

### Excluded models

| model | reason | measured? |
|---|---|---|
| Kimina-Prover-Distill-7B | vLLM 0.26 detokenizer corruption | **No** |
| Herald-7B | same | **No** |
| DeepSeek-Prover-V2-7B | same | **No** |
| Kimina-Autoformalizer-7B | task mismatch (emits statements, not definitions) | Yes, twice |

**4 of 7 candidates lost to one infrastructure bug**, 3 never measured. `docs/deferred.md` carries
untried fixes (`--tokenizer-mode slow`, pin vLLM ≤0.25, serve via transformers). Its trigger
("a contested prelim winner") has fired. Recovering these is the cheapest way to expand the field.

---

## 2. The funnel — where the actual signal is

| model | total | compile_error | wrong_type | `sorry` | name_shadowed | **admitted** |
|---|--:|--:|--:|--:|--:|--:|
| Goedel-Formalizer | 371 | 138 | 22 | **124** | 1 | **86 (23.2%)** |
| Goedel-Prover | 258 | 194 | 12 | **0** | 3 | **49 (19.0%)** |
| Qwen2.5-Coder | 410 | **355** | 4 | 1 | 1 | **49 (12.0%)** |

**Compile rate ≠ admission rate.** `sorry`, `WRONG_TYPE` and `NAME_SHADOWED` all compile; the gate
rejects them afterwards. Compiled: Formalizer **63%**, Prover **25%**, Qwen **13%**.

### Failure taxonomy (per-candidate share)

| category | Formalizer | Prover | Qwen |
|---|--:|--:|--:|
| admitted | 23% | 19% | 12% |
| `sorry` (explicit "I can't") | **33%** | 0% | 0% |
| wrong type | 6% | 5% | 1% |
| syntax (not valid Lean) | **5%** | 14% | **25%** |
| type error (dependent-type confusion) | 13% | **24%** | 15% |
| invented/misremembered name | 4% | 12% | **25%** |
| structure/anonymous-ctor misuse | 4% | 6% | 6% |
| missing typeclass instance | 7% | 5% | 3% |
| termination/recursion | 0% | 2% | 4% |

Three distinct behavioural profiles, each traceable to training:

- **Goedel-Formalizer** — barely a syntax problem (5%). Largest bucket is `sorry`: a well-typed
  skeleton with the content declined. Emits miniF2F boilerplate (`import Aesop`,
  `set_option maxHeartbeats 0`) — a *formalizer*, trained where `sorry` is the correct output and
  a downstream prover fills the body.
- **Goedel-Prover** — **never** emits `sorry` (0/258). Dominant failure is a plain type error.
  Most Lean-literate by syntax; doesn't know when it doesn't know. Separately, **22% of its
  compile errors are truncation** at the 8192-token cap (60 samples hit it) — its admissibility is
  understated and it is the only model materially affected.
- **Qwen2.5-Coder** — 25% syntax + 25% invented names. Writes correct *programs* in a language
  that demands correct *proofs* (e.g. a well-formed upward search that Lean rejects for
  termination). No wrong prior to unlearn — its failures are honest attempts at the actual task.

Type errors are **not** "didn't write a definition" — they are dependent-type failures: families
vs functions (`α ι` where `α i` was needed), propositions vs proofs (`⟨a, p a⟩` supplying the
statement where a proof is required), `Prop` vs `Type` (`Fact (DecidablePred p)`).

---

## 3. Corpus findings (these constrain everything downstream)

### 3.1 26 of 41 tasks have no admissible candidate from any model

Tasks with ≥1 survivor: Formalizer 6/41, Prover 7/41, Qwen 3/41. Union across models: 15/41.

**Never solved by anyone**: `Equiv.*` (4), `Finset.strong*`, `Multiset.*`, `Nat.binaryRec`,
`Nat.bitCasesOn`, `Nat.evenOddRec`, `OrderHom.prevFixed`, `List.prev`, `SimpleGraph.replaceVertex`,
`Matroid.map`, `Int.leastOfBdd`, `Int.greatestOfBdd`, `Function.extend`, `Graph.banana`,
`memPartition`, `Pi.Lex`, `Filter.comk`, `Function.Bijective`, `Function.Embedding.setValue`.

Coherent category: **bundled structures, dependent eliminators, and anything with real algorithmic
content.** What succeeds: `Nat.*` arithmetic near a Mathlib primitive, and short relational `Prop`s.

### 3.2 The corpus measures recall, not construction

Of 116 survivors: **22 (19%) literally name the real Mathlib target** (`VTask.choose := Nat.choose`,
`VTask.divisors := n.divisors`, `VTask.log := Nat.log b n`, `VTask.findGreatest := …`).
`names_target` and `equivalence_certified` coincide **21/22 times** — so tier-4 equivalence
certification is an effective memorization detector, available for free.

The other 94 aren't better, only less blatant: they *recite* rather than *name*. Against real
Mathlib, `IsBadSeq`, `Fibration` and `DependsOn` survivors are character-identical modulo binder
style. **Not one long or algorithmic definition succeeded anywhere.**

Median survivor body: 54 chars. Real Mathlib bodies for these objects: 60–80 chars. So short
bodies are *not* evidence of thinness — the corpus is made of one-liners. The selection criteria
(structural richness) admit conceptually rich but textually trivial definitions.

### 3.3 The instrument is biased against characterization-shaped mathematics

Two independent gates delete it:

- **Length floor.** Only 16 of 680 eligibles (2.4%) are characterization-flavoured
  (`sInf`/`sSup`/`Classical`/`.choose`/`Nat.find`); only 3 clear a 60-char floor. Characterizations
  are compact by nature — `sInf { a | ∀ᶠ n in f, n ≤ a }` is 29 chars.
- **Richness counter.** Logical structure lives *inside* the set-builder where the counter cannot
  see it. `OrderHom.lfp` (canonical Knaster–Tarski) scores `richness_total = 1`.

Mirrored on the scoring side: a noncomputable candidate cannot evaluate decide facts (correctly
UNKNOWN), so **definition-by-characterization goes unscored while algorithm-by-reduction scores
cleanly.** Observed live: for `Nat.clog`, Formalizer wrote `sInf {k | n ≤ b^k}` (the honest
characterization, penalised) while Prover wrote a `Nat.log` wrapper (scored cleanly).

Recorded requirement on pilot-100: a characterization stratum with shape-aware gates (floor waived,
richness assessed inside the set-builder). Full writeup:
`docs/batch_reports/2026-08-07_characterization_gate_bias.md`.

### 3.4 Suspect facts: 0

No fact was failed by every admissible candidate of every model. No truth-side defect surfaced.

---

## 4. Ladder calibration (Stage C pilot + Stage E)

### Pilot (20 stratified proof facts, truth-splice, tiers 1–2)

| | |
|---|---|
| elaborated | **20/20 (100%)** |
| tier-2 discharged | **15/20 = 75%** |
| by fact type | `global` **14/14 (100%)**, `membership` **1/6 (17%)** |
| corpus-weighted estimate | **~90%** (global is 88% of corpus proof facts) |
| winning tactics | `norm_num` ×9, `exact?` ×6 — **nothing else ever won** |
| wall-clock | 23.9 s for all 20 |

**The 14/14 is anchor lookup, not proving ability.** Global facts were mined as short restatements
anchored to existing Mathlib theorems; on the truth splice `exact?` finds the anchor on the shelf.
**Do not extrapolate to unanchored corpora** (`Def_Wiki`/`Def_ArXiv`) — there is no shelf there, and
the hammer becomes the designated tool. Re-pilot before budgeting fresh-source certification.

**Membership extension** (definition-unfolding tactics, `simp [<task symbol>, <real name>]`)
recovered **4/5** of the pilot residue in ~0.6 s total. Adopted as
`ladder.budgets.with_membership_tactics`, appended after the pinned set. Revised estimate: 19/20
sampled, ~98% corpus-weighted. Both names must be unfolded — the splice is
`@[reducible] def VTask.X := _root_.Real`, so naming only the task symbol may not reach the body.

### Hammer (tier 3) shakedown

| check | result |
|---|---|
| **soundness** — false statement must not be proved | **PASS** (rejected at kernel) |
| reprove tier-2 successes, cache off | **4/4**, ~1.1 s each |
| pilot residue (`¬ VTask.Fibration …`) | still UNKNOWN even with hammer |
| explicit anchor premises vs none | **no difference** — closes the 23 Jul comparison, negatively |

Hammer emits portable scripts (`simp_all only [Nat.log_zero_left]`), not `by hammer`, so cache
replay re-runs a cheap tactic rather than an ATP search.

### Per-tier discharge cascade (Stage E, real data)

| model | tier1 | tier2 | tier3 | tier4 | equivalence | total |
|---|--:|--:|--:|--:|--:|--:|
| Goedel-Formalizer | 323 | 217 | **110** | 0 | 381 | 1031 |
| Goedel-Prover | 329 | 124 | **66** | 0 | 276 | 795 |
| Qwen2.5-Coder | 191 | 155 | **107** | 0 | 453 |

The hammer does real work: **283 facts certified by tier 3** that the cheap tiers could not get.
Tier 4 never fires *inside* `adjudicate_fact` (it needs caller-supplied truth env); the
`equivalence` column is the separate fast path in `scoring.candidate`.

Stage E: 1,039/1,039 records, **990 proof PASS / 540 UNKNOWN**, `env_probe_fires=0`, 41 recycles,
155.9 min at 75.4 s/candidate.

### 4.1 The anchor-lookup bias is real and measured

| model | UNKNOWN, verbatim candidates | UNKNOWN, non-verbatim |
|---|--:|--:|
| Goedel-Formalizer | **0/123 = 0.0%** | **258/585 = 44.1%** |
| Goedel-Prover | **0/88 = 0.0%** | **153/343 = 44.6%** |
| Qwen2.5-Coder | n/a (no equivalence hits) | 129/391 = 33.0% |

Candidates the kernel proved definitionally equal to the truth have their proof facts discharged
**100% of the time**. Correct-but-rephrased candidates fail to resolve **~44%** of the time. The
hammer ran unconditionally and **reduced but did not eliminate** this. Caveat: "non-verbatim"
lumps genuinely-wrong candidates with correct-but-rephrased ones, so 44% is an upper bound on the
phrasing effect. **A metric built on proof-fact coverage will flatter memorization.**

---

## 5. Pre-tuning prompt experiment (8 cells × 41 tasks × 10 samples = 3,280 generations)

Model: Goedel-Formalizer-V2-8B only. Temp 0.7 fixed. L40S, concurrency 32, ~2 h, **~$2**.
Factors: anti-sorry instruction (S0 / S-B commit-under-uncertainty / S-C role-reframe / S-A plain
prohibition) × reasoning scaffold (R0 none / R1 prose-first). Common base in all cells: 3 worked
exemplars, signature-conformance instruction, mechanical per-task notation glossary.

### Headline table (admissibility scoring; no facts run)

| cell | extract | `sorry`/extracted | **adm/100** | **adm \| non-sorry** | compile_err | exemplar copy | tasks | med tok |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| S0_R0 (control) | 92.9% | **36.2%** | 20.0 | **33.7%** | 74 | 16.8% | 13 | 753 |
| SB_R0 | 91.7% | 38.0% | 20.7 | 36.5% | 68 | 14.9% | 14 | 720 |
| SC_R0 | **98.5%** | 40.6% | **22.4** | 38.3% | 60 | 19.0% | 14 | 685 |
| SA_R0 | 92.7% | 40.3% | **22.4** | **40.5%** | 68 | 13.9% | 14 | 709 |
| S0_R1 | 96.6% | 40.9% | 18.8 | 32.9% | 48 | 23.4% | 13 | 708 |
| SB_R1 | 95.1% | 42.1% | 20.7 | 37.6% | 61 | 16.6% | 13 | 717 |
| SC_R1 | 97.1% | 43.5% | 20.0 | 36.4% | 62 | 16.8% | 13 | 693 |
| SA_R1 | — | — | 18.0 | 31.0% | 57 | — | 13 | — |

### Finding 1 — `sorry` is NOT prompt-addressable

```
R0 arm:  S0 36.2%  →  S-B 38.0%  →  S-C 40.6%  →  S-A 40.3%
R1 arm:  S0 40.9%  →  S-B 42.1%  →  S-C 43.5%
```

**Every instruction makes it worse; the control is best.** Four phrasings, two scaffolds, ~3,300
samples. This is a floor, not a dial.

**Mechanism, measured.** Think-block analysis:

| cell | think-block mentions completeness | punt rate \| mentioned | punt \| not mentioned |
|---|--:|--:|--:|
| S0_R0 (no instruction) | **47.2%** | 62.8% | 12.4% |
| SB_R0 | 46.0% | 68.2% | 12.3% |
| SC_R0 | 48.3% | 67.2% | 15.8% |

The model raises completeness in ~47% of think-blocks **with no instruction at all**, and adding
one does not change that rate. The instruction never enters the deliberation. And the miniF2F
boilerplate is reproduced verbatim *in the cell that says the prover does not exist*. **It is
recall of an output format, not a choice** — which is exactly what SFT overwrites and prompting
cannot touch.

### Finding 2 — instructions DO improve non-punting attempts

```
adm | non-sorry:  S0 33.7%  →  S-B 36.5%  →  S-C 38.3%  →  S-A 40.5%     (+6.8 pts, monotone)
adm/100:          20.0      →  20.7       →  22.4       →  22.4
```

More instruction ⇒ fewer, better attempts (median tokens fall 753 → 685). Reading the `sorry`
column alone would have missed this entirely.

### Finding 3 — the R1 prose scaffold is counterproductive

Worse on both metrics in every comparison (`adm/100` 18.0–20.7 vs 20.0–22.4). Median tokens *fall*
while an extra prose block is requested — **prose displaces reasoning rather than adding to it**.
Recommend dropping it.

### Finding 4 — exemplar contamination (most actionable defect)

**14–23% of extractable samples answer with an exemplar instead of the task**, across 21 of 41
tasks. Of 69 cases in the control cell: **15 byte-identical, 54 re-derived** (different
factorisation API, `Nat.ceilDiv` for the manual ceiling, disjunction split into nested ifs). The
model has taken the exemplar to *be* the task — a salience failure, not a copy reflex.

Concentrated on previously-zero-survivor tasks (`replaceVertex`, `prevFixed`, `List.prev`,
`IsMinBadSeq`, `memPartition`). By exemplar: `ceilRoot` 36, `limsSup` 31, `LocallyLinear` 2 —
first and last dominate.

Net effect of exemplars: compile errors **−9.1 pts**, `name_shadowed` **+12.8 pts**, admitted
**23.2% → 21.5%** — i.e. **net slightly negative**. They teach Lean form and simultaneously supply
a fallback.

### Finding 5 — prompting does not extend reach

| | |
|---|---|
| tasks with ≥1 admissible, any cell | 13–14 of 41 |
| union across all 8 cells | 15/41 |
| prelim baseline (same model) | 15/41 |
| **net new tasks unlocked** | **1** (`Filter.Germ.IsConstant`) |
| lost | 1 (`memPartition`) |

3,280 generations across eight conditions moved coverage by one task. **The ceiling is not
prompt-addressable.**

---

## 6. Infrastructure changed this session (all committed, 1,033 tests pass)

| change | why it mattered |
|---|---|
| **Stage A splice parity** (`_root_.` + `noncomputable` retries on the candidate path) | both protections existed only truth-side; both convert correct candidates into `COMPILE_ERROR`, differentially by output style |
| **Tier-1 decide semantics** | `run_checked` returns FAILED for *any* error; tier 1 called all of them kernel refutations. Now content-classified: kernel-false → FAIL, missing/stuck `Decidable` → UNKNOWN, everything else → ERROR. Default inverted (unrecognised ⇒ ERROR, never FAIL) |
| **Declaration-verbatim splice + `WRONG_TYPE`** | 1040/1040 field candidates are declarations, not bodies; the old body-splice produced garbage for all of them. Pinned type now enforced by kernel (`#check (name : type)`, **not** `example := name`, which fails every noncomputable candidate) |
| **Universe-aware type probe** | `#check` does not bind universe variables a `def` auto-binds; **32/41 tasks** carry them. Unfixed this manufactured false `WRONG_TYPE` across 78% of the corpus |
| **Decide-fallback** (new, 2026-08-07) | an UNKNOWN decide fact escalates to tier 2 with the membership extension. Verified live: `off=unknown → on=certified`. Tier 2 only finds proofs, so this can never manufacture a FAIL |
| **Pass-aware resume + `NOT_ATTEMPTED_THIS_PASS`** | a Stage D record otherwise looked complete and Stage E would silently skip it |
| **Stage D/E merge** | Stage E would have overwritten Stage D's decide verdicts, reverting them while leaving the file self-consistent |
| **Stale-env detection** | `AutoLeanServer` self-heals, so `is_alive()` is True while every pre-restart env id is dead. One restart poisoned 70 tests; over a long run it would silently ERROR everything |
| **Shared Mathlib test fixture** | 12 module-scoped servers → 1; suite 14 min → 5:21. Recycle keyed on **growth from measured baseline** (warm Mathlib is **5.7 GB**, not the 2.5 GB in CLAUDE.md — a flat 5 GB cap fired on every test) |
| **`scripts/reap_repls.py`** | orphaned REPLs reparent to launchd; `_kill_stray_children` cannot reap them. Six reached 15.8 GB and forced a hard restart |

---

## 7. Open items

**Blocking / urgent**
- **AWS box `i-009b37b6b652f67dc` may still be running** ($0.564/hr). Credentials expired mid-session; needs MFA to stop. **Stop, do not terminate** — terminate destroys the Hammer build and premise cache.
- **RunPod key was pasted into chat — rotate it.** Pod `1cldonwktoqim5` terminated; 0 pods remaining.

**Decided but not built**
- Exemplar follow-up cells: (a) no exemplars, (b) reframed exemplars ("illustrative, never your task"), (c) one exemplar vs three. ~15 min / ~$0.25 each. **Precondition** for keeping exemplars in the permanent architecture.
- Fact scoring on the two best pre-tuning cells (admissibility only so far — "admissible" means well-typed and complete, not correct).
- Recover the 3 detokenizer-corrupted models.
- `authoring/roundtrip.py` still uses the un-laddered splice path (`docs/deferred.md`); tested and confirmed *not* the cause of the "harder" flags.

**Recorded requirements**
- Pilot-100 needs a characterization stratum with shape-aware gates.
- Fidelity needs a companion **resolution rate** — 1.0 from 9 of 29 facts is not 1.0 from 29 of 29.
- Runbook: record GPU type at pod start (the prelim's A40 was unrecoverable from our records; the runbook says A100, which was never used).

---

## 8. Recommendations

1. **Do not select a base model on fidelity.** It is saturated and computed over non-comparable task sets. The discriminating metrics are admission rate, survivor rate, and the failure profile.
2. **The `sorry` behaviour is a fine-tuning target, not a prompt target** — established at ~$2. The thing to overwrite is an output format, the easiest class for SFT to move.
3. **Fix exemplar contamination before anything is frozen into a permanent prompt.** At 14–23% on hard tasks it would be baked into every future run and would read as model failure (`name_shadowed`), not prompt defect.
4. **Drop the R1 scaffold.**
5. **Qwen2.5-Coder is the cleanest training base despite scoring worst** (12% admission): its failures are pure capability (syntax, invented names), with no wrong prior to unlearn. Both specialists carry inherited pathologies — Prover writes `theorem … := by sorry` for definition tasks, Formalizer writes signature-then-`sorry`. This is a judgement call, not a measurement; the counter-argument is that Formalizer's higher ceiling may be worth the unlearning cost.
6. **The corpus is the binding constraint, not the models.** 26/41 tasks unsolved by anything, every survivor a recited one-liner, no mutants (so separation is not computable). Corpus work will move the needle further than model work.
