# Batch report: Failure Forensics — why 11/41 didn't ship (2026-07-31)

*Second entry in `docs/batch_reports/` (see the first entry's own note on why this directory
exists). Investigation session — diagnosis and evidence, not policy. The policy decision on
what to do about any of this belongs to the human, made from this report.*

## Part 0 — Enablement fixes (committed)

1. **REPL-death detect/recover in `authoring/cleanup.py`**, mirroring `authoring.batch.run_batch`'s
   pattern — the gap that cost `Equiv.subtypePreimage` its cleanup run in the prior session.
   Detect+recover only (no proactive per-name restart — a cleanup run is a handful of names;
   forcing a ~1-minute re-import before each would cost more than the one real death observed
   ever bought back). One test (`test_run_cleanup_detects_repl_death_and_recovers_via_repl_warmup`).
   Commit `7bc2c9b`.
2. **Backfilled `pending_safety_updates.json`** with the 8 rotations from the completion session
   that `author_task`-direct calls never queued (the completion driver called `author_task`
   directly, not `run_batch`, so `append_rotation` never fired). Reconstructed $0 from the real
   Bedrock call log for 4 of them (Monotone, DependsOn, Equiv.ofLeftInverse, IsMinBadSeq —
   detail text lost to a scratchpad-script serialization bug in the completion session); the
   other 4 (Filter.Germ.IsConstant, Graph.banana, memPartition, Multiset.Pi.cons) had intact
   detail already. The 4 reconstructed entries also had STALE queue rows left over from before
   Items 1-2 (still recording their ORIGINAL `truth_splice`/REPL-death rotation) — updated in
   place, with the old reason preserved in an `artifacts.note` history field, not silently
   overwritten. Data-only change; not committed (script, not repo code).
3. **`docs/batch_reports/`** created — first entry retroactively captures the completion
   session's final table (the exact thing lost last time when predictions/vocabulary lived only
   in chat). This file is the second entry.

## Part 1 — Per-name forensic verdict, all 11 unresolved names

| Name | Stage | Verdict | Evidence |
|---|---|---|---|
| **Monotone** | dossier_consistency | **CHECK_SUSPECT** (confirmed bug) | `check_no_real_name_leak`'s word-boundary matcher fires on the task symbol's OWN suffix: `\bMonotone\b` matches inside `VTask.Monotone` (the "." before it is a word boundary). Confirmed: reconstructed the exact rejected dossier from the Bedrock call log ($0) and found **9/9** occurrences of "Monotone" are `VTask.Monotone` — zero bare uses. The model followed instructions perfectly; the check cannot pass for any unnamespaced real name. |
| **DependsOn** | dossier_consistency | **CHECK_SUSPECT** (same bug) | Same mechanism. **14/14** occurrences of "DependsOn" preceded by "VTask." |
| **memPartition** | dossier_consistency | **CHECK_SUSPECT** (same bug) | Same mechanism. **12/12** occurrences preceded by "VTask." |
| **Equiv.ofLeftInverse** | dossier_consistency | **CHECK_SUSPECT** (different flavor) | The dossier's "Not to be confused with" section legitimately names a real, different Mathlib declaration (`Equiv.ofLeftInverse'`, the primed variant) for disambiguation — exactly what that section is prompted to do. `Equiv.ofLeftInverse` is a substring of `Equiv.ofLeftInverse'`, so the leak check fires. Design tension: the prompt asks for real nearby-object names; the check forbids any real name, unconditionally. |
| **Set.PartiallyWellOrderedOn.IsMinBadSeq** | mechanical_validation | **MODEL_MATH** (structural root cause) | All 10 proposed facts reference the bare identifier `IsBadSeq` — genuinely undefined in this task's spliced environment. Root cause: the real definition is stated in terms of a companion definition, `Set.PartiallyWellOrderedOn.IsBadSeq`, which is a SEPARATE task in this same batch (and shipped clean) with its own, disjoint task symbol. The model never had a legal way to reference it. Confirmed clean (no REPL-death contamination): 8/10 facts show `Unknown identifier 'IsBadSeq'`, 2/10 show `Unknown identifier` for local hypothesis names (`r`,`rk`,`s`,`f`) apparently copied from the real docstring's own variable names without proper binding. |
| **SimpleGraph.replaceVertex** | mechanical_validation (this session) | **INDETERMINATE — likely HARNESS-contaminated** | Three independent attempts to re-validate its fact suite against ground truth (two in a combined script, one in an isolated single-name script with a fresh server) **all** hit total REPL death (100% "Unknown environment" across every one of 16 facts) before any real signal could be obtained. Combined with the confirmed `validate_global_fact` bug below, I cannot rule out that the ORIGINAL "no facts survived" verdict was itself contaminated by undetected REPL instability. See the machine-state note below the table. |
| **Function.Embedding.setValue** | round_trip_scoring | **ENCODING_HARDNESS** | 5 repair attempts, every one exhausts 4 compile attempts. Attempt 1's error is **byte-identical every single time**: `Invalid ⟨...⟩ notation... is not an inductive type` — the candidate tries to build a `Function.Embedding` (bundled structure with an injectivity proof obligation) via anonymous-constructor syntax and fails the same way each time; later attempts spiral into increasingly complex tactic proofs with cascading type mismatches trying to route around it. |
| **Equiv.subtypePreimage** | (cleanup setup) | **HARNESS** | Direct REPL death during the cleanup runner's truth-splice setup (`error_if_any: "LeanError: Unknown environment."`, 0 attempts used) — exactly the gap Part 0.1 of this session fixes going forward. Its historical round-trip/signature-substring failures never got a fair post-Item-3 attempt this round. |
| **Filter.Germ.IsConstant** | round_trip_scoring | **ENCODING_HARDNESS** | 4/4 compile attempts fail on `Unknown identifier 'P.liftOn'`/`'P.liftOn''` — the candidate consistently reaches for `Filter.Germ`'s standard quotient-elimination combinator but can't get the right name/notation in a minimal round-trip context. |
| **Graph.banana** | round_trip_scoring | **ENCODING_HARDNESS** | 4/4 compile attempts fail on structure-literal syntax (`unexpected identifier; expected '}'` ×3, then `invalid {...} notation, expected type is not of the form (C ...)`) — difficulty constructing a `Graph` structure literal. |
| **Multiset.Pi.cons** | mechanical_validation | **INDETERMINATE — likely HARNESS-contaminated** | Same pattern as SimpleGraph.replaceVertex: an isolated single-name re-validation attempt hit total REPL death (100% "Unknown environment" across all 12 facts). See the machine-state note below. |

### A confirmed, significant check bug: `validate_global_fact` misclassifies infra failures as genuine rejections

While chasing the SimpleGraph.replaceVertex/Multiset.Pi.cons REPL deaths, I found the root cause
of why they were so damaging. `authoring/validate.py`'s three per-fact-type validators handle a
`CheckStatus.ERRORED` REPL response differently:

- `validate_casework_fact` (line 308): falls through to `ReasonCode.ERRORED` for anything that
  isn't `PASSED` or `FAILED` — correct.
- `validate_membership_fact` (line 431-437): explicitly checks `elaborate_check.status is
  CheckStatus.ERRORED` and returns `ReasonCode.ERRORED` — correct.
- `validate_global_fact` (line 525): checks only `if prop_check.status is not CheckStatus.PASSED`,
  collapsing `FAILED` (genuine non-elaboration) and `ERRORED` (infra failure) into the **same**
  `Verdict.REJECTED` / `ReasonCode.PROPOSITION_DOES_NOT_ELABORATE` — **bug**.

This matters because `authoring.orchestrate.adjudicate_proposed_facts`'s entire "row 5" retry
mechanism (retry once on `ReasonCode.ERRORED`, then flag the whole task via `task_errored` if it
persists — the correct behavior for infra flakiness, distinct from "this fact is bad") is gated
on `outcome.reason_code == ReasonCode.ERRORED`. Because `validate_global_fact` never emits that
code, a global fact whose elaboration check happens to hit a dead REPL server is **silently,
permanently dropped as if the model had proposed something invalid** — no retry, no task flag,
no visibility. Confirmed with a minimal, deterministic, non-memory-dependent repro (bogus env id
forcing `CheckStatus.ERRORED`):

```
verdict: REJECTED
reason_code: PROPOSITION_DOES_NOT_ELABORATE
detail: LeanError: Unknown environment.
BUG CONFIRMED (reason_code != ERRORED for an infra failure): True
```

**Machine-state note.** During this investigation, `AutoLeanServer` died reproducibly and
completely on essentially every REPL call issued shortly after warm-up, across two *different,
unrelated* declarations (SimpleGraph.replaceVertex and Multiset.Pi.cons), in isolated
single-name scripts with fresh servers each time. `vm_stat` at the time showed ~64MB free system
memory. This is not conclusively diagnosed as "this specific machine, right now, in real memory
distress" vs. "something more systemically fragile" — but it directly demonstrates, live, the
exact class of problem `CLAUDE.md`'s own "Known follow-ups" section already flagged (the
`max_total_memory` guard dialed up to 0.95 because this dev machine regularly sits above 80%
system memory from unrelated apps) — and shows concretely how that fragility, combined with the
`validate_global_fact` bug above, can make a definition's fact suite **look** mathematically
unworkable when it was never actually given a clean evaluation.

## Part 2 — Survivorship analysis

### 2.1/2.2 — Encoding-difficulty proxies vs. outcome (all 41 names)

Computed mechanically from the pinned type string (binder counts, bundled-return-type markers
`≃`/`↪`/`//`, universe variable count) and the real source text (anonymous-constructor `⟨⟩`
presence, `where`-structure presence) — $0, pure text analysis, no REPL.

| Group | n | avg binders | avg implicit | avg instance | frac bundled return | frac anon-ctor in source | avg universe vars |
|---|---|---|---|---|---|---|---|
| Shipped clean | 24 | 3.67 | 1.46 | 0.08 | 0.12 | 0.21 | 1.29 |
| Repaired & shipped | 6 | 5.00 | 1.67 | 0.67 | 0.17 | 0.50 | 1.50 |
| Unresolved — check bug (Monotone, DependsOn, memPartition, Equiv.ofLeftInverse) | 4 | 4.25 | 2.00 | 0.50 | 0.25 | 0.25 | 1.75 |
| Unresolved — harness/indeterminate (subtypePreimage, replaceVertex, Pi.cons) | 3 | 5.67 | 1.67 | 1.00 | 0.33 | 0.33 | 1.67 |
| Unresolved — genuine hardness/model-math (setValue, Germ.IsConstant, banana, IsMinBadSeq) | 4 | 5.25 | 2.00 | 0.50 | 0.25 | 0.50 | 2.00 |

**Plain-language read.** Every group that ever needed a repair or never shipped is more
binder-rich, more instance-heavy, and more bundled-structure-prone than the clean-shipped group
— that part of the human's concern is real: harder-to-encode definitions genuinely fail (or need
repair) more often (shipped_clean's 0.08 average instance binders vs. 0.50-1.00 everywhere else
is the sharpest single signal). **But** the 11 "unresolved" names split roughly evenly into three
very different buckets, and only 4 of 11 (36%) represent genuine encoding/model difficulty that
current mechanisms couldn't already handle. 4 of 11 (36%) are blocked by a single confirmed check
bug that has nothing to do with definitional hardness at all — those 4 names' dossiers were
followed to the letter and rejected anyway. 3 of 11 (27%) are contaminated by REPL
reliability/harness issues, indeterminate rather than genuinely hard. **The corpus is not
currently primarily hardness-filtered — it is currently more limited by check-correctness and
REPL reliability than by encoding difficulty**, though the hardness signal among the genuinely-hard
4 (and the repaired 6, which succeeded despite similarly elevated proxies) is real and will matter
more as check/harness bugs get fixed and hardness becomes the binding constraint.

### 2.3 — Round-trip failure clustering

Across every round-trip compile-exhaustion case examined (List.prev, Function.Embedding.setValue,
SimpleGraph.replaceVertex's early attempts, Equiv.subtypePreimage's early attempts,
Filter.Germ.IsConstant, Graph.banana):

- **Bundled-structure/anonymous-constructor syntax errors** (`Invalid ⟨...⟩ notation`,
  `unexpected identifier; expected '}'`/`'else'`, `invalid {...} notation`) — **4 of 7 cases**
  (Function.Embedding.setValue, SimpleGraph.replaceVertex, Equiv.subtypePreimage, Graph.banana).
  This **is** the dominant cluster, matching the hypothesis in the task text — every one of these
  four targets a bundled structure (`Embedding`, `Graph`) or requires building a term with an
  attached proof obligation, and the round-trip model's first move is almost always a
  `⟨...⟩`/structure-literal attempt that Lean rejects for a reason specific to that construct.
- **API-name-guessing failures** (`Unknown identifier`) — 1 of 7 (Filter.Germ.IsConstant, guessing
  at `P.liftOn`/`P.liftOn'`).
- **Term-level type mismatches from an otherwise-plausible tactic proof** — the remainder (List.prev,
  Function.Embedding.setValue's later attempts after its initial ⟨...⟩ failure) — the model's
  proof sketch is structurally reasonable but Lean's exact unification/case-split mechanics trip
  it up.

### 2.4 — Repair-drift check (6 repaired-and-shipped names)

Diffed each name's ORIGINAL rejected dossier (stored in the queue at first-rotation time)
against its FINAL shipped `dossier.md`. Word counts: Int.leastOfBdd 624→735, Finset.sumLexLift
745→779, OrderHom.prevFixed 610→696, Nat.findGreatest 665→607, Nat.binaryRec 677→657,
List.prev 534→544 — no group-level shrinkage pattern.

**Verdict: no content loss detected in any of the 6.** Read every diff in full (not just the
word counts, which can hide a swap). Two specific things worth naming:

- **`Nat.binaryRec`'s repair actually FIXED a real-name leak**, not just reworded: the original
  "Not to be confused with" section named the bare real declarations `Nat.binaryRec'` /
  `Nat.binaryRecFromOne`; the repaired version correctly uses `VTask.binaryRec'` /
  `VTask.binaryRecFromOne`. Same content, same disambiguating comparisons, leak removed.
- **`Nat.findGreatest`'s repair swapped one worked example for another** (`P=(·=0), n=4` →
  `P=(fun _ => True), n=0`) rather than dropping coverage — both test genuine boundary behavior
  (junk-value ambiguity vs. the `n=0` bound itself), just different boundaries; the Boundaries
  section's prose still covers the original point (junk value indistinguishable from a genuine
  witness at 0).
- Every other diff (`OrderHom.prevFixed`, `List.prev`) is a pure header-format/rewording
  artifact from Item 3's Signature-section convention change plus paraphrasing — same claims,
  same edge cases, same "Not to be confused with" comparisons, sometimes MORE worked examples
  (List.prev's final version added a 5th: the singleton self-predecessor case, absent originally).

**No back-door survivorship bias found**: the repair loop is not quietly simplifying dossiers
toward round-trip-compilability at the expense of mathematical content, at least not in these 6
observed cases.

## Part 3 — Evidence for the policy discussion

### 3.1 — Ship-with-flag counterfactual

A `ROUND_TRIP_UNVERIFIED_COMPILE` flag (mirroring the existing termination-only flag) covering
round-trip compile exhaustion specifically would let through: **Function.Embedding.setValue,
Filter.Germ.IsConstant, Graph.banana** (3 of 11) — all three are pure round_trip_scoring compile
failures with everything upstream (dossier, facts, mechanical validation) intact; nothing in their
history suggests the dossier or facts are wrong, only that the round-trip re-derivation model
couldn't compile a candidate. It would **not** ship the 4 CHECK_SUSPECT names (blocked earlier,
at dossier_consistency, never reaching round-trip), the 3 harness/indeterminate names (also
blocked earlier or contaminated), or IsMinBadSeq (blocked at mechanical_validation, before
round-trip). Gain: 3 more names shipped, all with a real, upstream-verified fact suite — the
missing signal is specifically "does an independent fresh-context model also land on this
definition," which is real evidence but not the ONLY thing task quality depends on. Loss: those 3
tasks would ship without ever having demonstrated an independent Lean re-derivation succeeds —
exactly the round-trip check's own reason for existing (contract §5).

### 3.2 — What each CHECK_SUSPECT case implies about that check's design

- **Monotone/DependsOn/memPartition** (`check_no_real_name_leak`): the check's word-boundary
  matcher operates on the RAW forbidden name string against the WHOLE dossier text, without ever
  masking out the task symbol's own text first. It cannot distinguish "the model wrote the real
  name" from "the real name happens to be a trailing substring of the task symbol the model was
  REQUIRED to use." This is a mechanical fix (mask/strip every `VTask\.\w+` occurrence before
  searching, or search only for the real name preceded by a non-`.`-non-word-boundary), not a
  design tradeoff — the check's OWN stated intent ("must use the task symbol exclusively") is
  currently self-defeating for any unnamespaced real name.
- **Equiv.ofLeftInverse** (same check, different mechanism): the check has no notion of "a
  legitimately-cited NEARBY real object, in the one section explicitly prompted to name nearby
  real objects." This is a genuine design tradeoff, not a bug: either the "Not to be confused
  with" section's own prompt instruction needs to stop asking for real nearby-object names (losing
  useful disambiguation content), or the leak check needs a carve-out scoped to that section
  specifically (risking a real leak hiding there instead).
- **`validate_global_fact`** (found via the SimpleGraph.replaceVertex/Multiset.Pi.cons
  investigation, not itself one of the 11's DIRECT causes, but load-bearing for whether their
  verdicts can be trusted): the fix is a one-line change to match the other two validators'
  already-correct pattern (check `ERRORED` specifically before falling through to `REJECTED`).

### 3.3 — Optional $1 probe (Function.Embedding.setValue at n=8 round-trip attempts)

**Skipped.** AWS credentials expired mid-session and the probe is explicitly optional per the
task's own instruction ("skip if the $1 cap or credential state makes it awkward"). Worth doing
in a future session specifically to distinguish "hard but achievable at higher n" from
"systematically unable" for setValue's `⟨...⟩`-notation failure — the fact that its FIRST compile
attempt is byte-identical across all 5 repair-loop attempts (never varying) is weak evidence
toward "systematic," but n=4 attempts per round is a thin sample to conclude that from.

### 3.4 — Recoverability, per name, for the human

| Name | (a) existing repair loop as-is | (b) policy change only | (c) check change only | (d) needs new capability |
|---|---|---|---|---|
| Monotone | No — repair loop can't fix a check that rejects the task symbol itself | — | **Yes** — fix `check_no_real_name_leak`'s word-boundary matcher | — |
| DependsOn | No, same reason | — | **Yes**, same fix | — |
| memPartition | No, same reason | — | **Yes**, same fix | — |
| Equiv.ofLeftInverse | No, same reason | Possible — relax the "Not to be confused with" instruction | Possible — carve out that section | — |
| Set.PartiallyWellOrderedOn.IsMinBadSeq | Untested this round (never reached repair — died at mechanical_validation, not a `dossier_consistency`/compile-exhaustion category the repair loop's feedback restriction covers) | — | Partial — nothing to check-fix; this is a task-design tension (companion-definition dependency under single-symbol-per-task) | Arguably (d) — no mechanism today lets a task legally reference a sibling task's symbol |
| SimpleGraph.replaceVertex | Unknown — never got a clean attempt this round | — | **Yes** — fix `validate_global_fact`'s ERRORED/FAILED conflation, which may be silently corrupting this exact name's evaluations | Also needs a healthier machine / REPL-restart-on-memory-pressure to get a trustworthy read at all |
| Function.Embedding.setValue | No — exhausted all 5 attempts on the identical error | Yes — `ROUND_TRIP_UNVERIFIED_COMPILE` flag would ship it | — | Possibly (d) — may need round-trip prompt guidance for bundled-structure-with-proof-obligation construction |
| Equiv.subtypePreimage | Untested post-fix — Part 0.1 (this session) should let it get a fair attempt now | — | — | — |
| Filter.Germ.IsConstant | Untested (never repaired — fresh phase-C rotation) | Yes — the flag would ship it | — | Possibly (d) — quotient-elimination-combinator naming guidance |
| Graph.banana | Untested (same) | Yes — the flag would ship it | — | Possibly (d) — structure-literal construction guidance |
| Multiset.Pi.cons | Untested this round (died before real signal) | — | **Yes**, same `validate_global_fact` fix as replaceVertex | Same machine-health caveat |

## Problems found, NOT fixed (this session)

1. **`validate_global_fact` misclassifies REPL-death (`CheckStatus.ERRORED`) as genuine
   non-elaboration (`ReasonCode.PROPOSITION_DOES_NOT_ELABORATE`/`REJECTED`)** — confirmed with a
   minimal deterministic repro. The other two per-fact-type validators already handle this
   correctly; this is the one outlier. Highest-priority finding of this session — it can make a
   genuinely-fine definition look mathematically unworkable.
2. **`check_no_real_name_leak`'s word-boundary matcher self-triggers on the task symbol** for
   every unnamespaced real Mathlib name (confirmed for 3/3 cases in this batch: Monotone,
   DependsOn, memPartition) — structurally unshippable under current code, regardless of dossier
   quality.
3. **REPL reliability under memory pressure** reproducibly killed two independent, unrelated
   single-name investigation scripts this session (100% "Unknown environment" across every fact
   checked, every time) — live confirmation of `CLAUDE.md`'s own already-flagged concern, and
   concrete evidence it can silently corrupt validation results via finding 1 above.
4. **`Equiv.ofLeftInverse`'s leak-check-vs-disambiguation-prompt tension** is a genuine design
   question, not a bug — needs a human call (relax the prompt, or carve out the check).
5. **Set.PartiallyWellOrderedOn.IsMinBadSeq's companion-definition dependency** — no mechanism
   today lets a task legally cite a sibling task's own definition, and this is likely to recur
   for any definition mined from a family of mutually-referencing helpers.

## Ranked opinion, next session (≤5 bullets)

1. Fix `validate_global_fact`'s `ERRORED`/`FAILED` conflation (one-line change, matches the
   other two validators' existing pattern) — this is the highest-leverage fix found this session
   and directly bears on whether SimpleGraph.replaceVertex/Multiset.Pi.cons's verdicts can be
   trusted at all.
2. Fix `check_no_real_name_leak`'s word-boundary matcher to mask the task symbol before
   searching — ships Monotone, DependsOn, memPartition through the existing repair loop with no
   policy change needed, once the check itself stops rejecting them for using the task symbol.
3. Once both checks above are fixed, re-run Equiv.subtypePreimage (now that Part 0.1's cleanup
   REPL-recovery exists), SimpleGraph.replaceVertex, and Multiset.Pi.cons for a genuinely clean
   read — on a machine with real memory headroom, not mid-investigation-session.
4. Bring `ROUND_TRIP_UNVERIFIED_COMPILE` (mirroring the termination flag) to the human as a
   concrete policy proposal, scoped specifically: it would ship exactly 3 names
   (Function.Embedding.setValue, Filter.Germ.IsConstant, Graph.banana), all upstream-verified,
   all failing only on independent round-trip re-derivation.
5. Decide `Equiv.ofLeftInverse`'s check-vs-prompt tension (relax "Not to be confused with," or
   carve out the leak check for that section) and Set.PartiallyWellOrderedOn.IsMinBadSeq's
   companion-definition-reference gap — both need a human call before any fix is attempted.

**Bottom line for the survivorship question**: of 41 names, 30 shipped. Of the 11 that didn't,
only 4 (setValue, Germ.IsConstant, banana, IsMinBadSeq) show genuine encoding/model difficulty —
and even among those, 3 are pure round-trip-compile cases with a clean upstream fact suite, not
evidence the OBJECT itself is unshippable. 7 of 11 are process artifacts (4 check bugs, 3
harness/indeterminate) with nothing to do with definitional hardness. The pipeline is not
currently primarily selecting for easy definitions — it is currently more limited by check
correctness and REPL reliability than by the model's capability to handle hard ones. That said,
the encoding-proxy signal (2.1/2.2) is real and should be watched as those process issues get
fixed and hardness becomes the binding constraint instead.
