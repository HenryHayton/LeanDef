# Verifier Architecture: Updated Design Report

*Status: working design, post n=1 probe. Stuff on reward structure is superseeded by the dedicated reward plan from the 21st july 2026 this is from 20 July 2026.*

## 1. Purpose and framing

The project builds a mechanical signal for **definitional faithfulness**: given an informal dossier describing a mathematical object and a candidate Lean 4 definition, measure whether the definition denotes the intended object. The Lean kernel certifies type-correctness only; faithfulness is the missing property, and this verifier operationalizes it. The eventual use is twofold: evaluation of definition-writing systems, and (in the computable fragment, where the economics permit) a reward signal for training one.

A **task** consists of: the informal dossier; a pinned signature (name and type, body as the hole); a fact suite; a mutant battery; and, for tasks outside the decidable fragment, a set of proof obligations. A candidate supplies the body. The verifier splices the candidate under the pinned name in a warm Mathlib REPL environment (LeanInteract, pinned toolchain) and scores it.

## 2. The three scoring layers

**Layer 0 — admissibility.** The candidate must compile against the pinned signature with no `sorry` (detected as a REPL warning — proven in Step 0), no new axioms, no shadowing of the pinned name, and no tampering with dependencies. Where the task carries proof obligations, the same gate applies to the candidate's submitted proofs. Admissibility is the anti-cheating gate; it produces no score, only a pass/fail on eligibility.

**Layer 1 — fidelity (facts).** Facts are concrete propositions stated in terms of the pinned name. Fidelity is the fraction of the fact suite certified for the candidate. Two fact mechanisms exist, and a task may carry either or both:

- *Decidable facts*, checked by `decide` against the warm environment: pointwise values (`tau 6 = 4`) and bounded windows (`∀ n < 100, tau n = ref n`). Millisecond-scale, deterministic, kernel-pure, zero completeness gap. These remain the backbone wherever the object's content survives restriction to checkable finite instances.
- *Proof-obligation facts*, for objects whose content does not finitize (topologies, compactness-like concepts, general algebraic structure): general statements, including unbounded universals, adjudicated by a flagship LLM prover (accessed via the company Amazon Bedrock account) attempting to prove the fact and, independently, its negation. Every successful proof is kernel-checked; the model only ever finds proofs, it never certifies anything.

**Layer 2 — separation (mutants).** Each mutant is a plausibly wrong definition (boundary slip, dropped condition, flipped relation, wrong-object confusion). The true fact suite is run against every mutant; a good suite fails each of them. Separation is the audit that keeps fidelity honest: a mutant surviving the full suite is a certified blind spot — a misreading the facts cannot distinguish from the truth. Separation per task is also the quality-control metric that makes mined tasks trustworthy at scale without hand inspection.

## 3. Established empirical findings (n=1 probe, tau)

The splice-score pipeline works end to end: true candidate 10/10, warm-environment `decide` checks sub-second, hand-written definition verified against Mathlib's divisor count. Three design findings came out of the probe and are now baked into the plan. First, inequality-phrased refuting facts (`tau 6 ≠ 3`) are dropped: they leak free passes to constant candidates (junk scored 3/10 entirely from `≠` facts) and are strictly dominated by exact-value facts as mutant-catchers. Second, structurally uniform objects produce undiagnostic mutants — every crude mutation of tau shifts all outputs, so all mutants fail all facts and separation collapses into a copy of fidelity; mutant generation should therefore be biased toward boundary/degenerate-input perturbations, where survivors (and therefore information) live. Third, surviving edge mutants split into two kinds — fact-coverage holes (patch the window) and dossier underspecification, e.g. conventions at n = 0 (patch the prose); the pipeline should route survivors to a human rather than auto-patch, since distinguishing the two is a judgment call.

## 4. Scoring semantics

**Tri-state adjudication for obligation facts.** For each obligation, the prover attempts the fact and its negation under a fixed budget. Prove the fact → kernel-certified TRUE. Prove the negation → kernel-certified FALSE. Neither → UNKNOWN, reported as its own category and never folded into failure. Soundness is absolute (the kernel checks every proof); incompleteness is confined to the visible UNKNOWN rate. Decidable facts have no UNKNOWN state.

**Rules for the prover layer.** The prover never sees the true definition or ground-truth answers — only the candidate and the fact statement. Identical model version, scaffold, and attempt budget for every candidate on every fact within an experiment; the exact Bedrock model ID is pinned and recorded alongside the Lean/Mathlib pins. The prover lives in evaluation and task authoring only; it is never part of a training loop, whose reward must come from the decidable layer. Batch invocation should be used for evaluation runs where available.

**Separation gating.** Separation is credited only to candidates above a fidelity floor, so that degenerate candidates cannot collect separation credit they did not earn.

**Reporting split.** Results on the decidable fragment (kernel-pure, deterministic) are reported separately from results involving the prover layer (kernel-sound but incomplete, with UNKNOWN rates). These are different claims and are kept unmixed.

## 5. The miner and the LLM's role in task authoring

The miner harvests candidate objects from Mathlib and assembles tasks automatically: facts generated by running the true definition as its own oracle; mutants generated by structured perturbation biased toward boundaries and degenerate inputs; dossiers generated by reverse-translation with spot-checking.

**Fact-mechanism selection is made per object by an LLM at mining time.** The model inspects the harvested definition and decides which fact types make sense: decidable pointwise/window facts where the object is computable and its content finitizes; obligation facts where it does not; a mixture where finite instances carry partial content (e.g. finite-instance checks as a cheap pre-filter alongside general obligations). Decide checks remain the default wherever they make sense — the LLM's job is to recognize when they do.

Two safeguards keep this judgment from becoming load-bearing in the wrong way. First, decidability claims are verified mechanically, not trusted: every generated decidable fact is actually executed against the true definition during mining, so a wrong "this is decidable" call fails loudly at authoring time and costs nothing downstream. Second, obligation statements are validated by running the prover against the *true* definition at authoring time; obligations the prover cannot discharge for the ground-truth object are rejected or simplified, which calibrates task difficulty and bounds the UNKNOWN rate before any candidate is ever scored. In both cases the LLM proposes and the machinery disposes; soundness never rests on the model's judgment.

Mined tasks are quality-controlled by their own separation audit: a task whose fact suite kills too few of its mutants is flagged or discarded. This also automatically detects concepts that have escaped the method's jurisdiction (a compactness-like object yields finite facts that separate nothing, scoring near-zero separation and self-flagging as vacuous).

## 6. Cost model

The verifier's viability as more than a report card depends on the inner loop staying flat. Decidable facts: ~10–70 ms per check against the warm environment, bounded and predictable — compatible with reward-function use. Obligation facts: seconds to minutes per attempt with timeout-shaped variance — compatible with offline evaluation and authoring-time validation only. This asymmetry is why the prover is architecturally confined to the outer loops, and why the decidable layer is retained as the primary mechanism rather than a legacy one: wherever both mechanisms are available, milliseconds-and-deterministic wins.

## 7. Open questions

Window sizes for bounded `decide` facts (pending timing of `∀ n < N` agreement checks at N = 100/500/1000, which also settles whether `native_decide` and its compiler-trust extension are needed at all). The exact fidelity floor for separation gating. The held-out status of fact suites relative to any future trained candidate-producer (currently assumed held out; must be stated in the schema). Prover budget per obligation. Whether obligation-carrying tasks admit partial credit across obligations or score them as a block.

## 8. Build order

Unchanged in sequence, extended in scope: (1) complete the mutant battery run on tau and analyze the survivor tail; (2) freeze the task schema, now including the obligations field, tri-state scoring semantics, separation gating, and pinned-model metadata; (3) build the decidable-fragment miner with LLM fact-mechanism selection and mechanical validation; (4) stand up the prover scaffold against Bedrock (tri-state, budget parity) for authoring-time validation first, candidate evaluation second; (5) first mined-task evaluation runs, reported with the decidable/prover split.
