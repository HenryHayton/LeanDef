# Deferred

A running list of known, deliberately-not-yet-done items. Each entry has a **trigger**: the
specific event or milestone that makes it time to act. An entry is not a priority ranking and
not a promise of when it'll happen — it's a tripwire, so that when the trigger fires, the item
gets picked up rather than re-discovered from scratch. Remove an entry once it's actioned;
don't leave it checked off in place.

- **`docs/decidability_bias_survey.md` line ~137 prover-retry phrasing.** Describes retry cost
  in terms of "a prover agent's retry," pre-dating the adjudication ladder.
  **Trigger:** the next edit of that doc.
- **Sonnet 5 re-pin.** `AUTHORING_MODEL_ID` / `FLAGSHIP_MODEL_ID` (`bedrock/config.py`) are
  pinned to `eu.anthropic.claude-sonnet-4-6`; `eu.anthropic.claude-sonnet-5` is catalogued
  in-region (`eu-west-1`) but not yet entitled to the account.
  **Trigger:** Bedrock entitlement for `eu.anthropic.claude-sonnet-5` lands.
- **Flagship-model residue comparison.** Pre-registered follow-up: re-run the hammer-failed
  residue with a flagship-class model for comparison
  (`docs/design/reward_structure_2026-07-21.md` §6).
  **Trigger:** the pilot (§11 of that doc) shows a fat residue of hammer-failed facts that the
  pinned model also cannot close.
- **Stub-fixture parity with the real Bedrock response shape.** `tests/test_bedrock_client.py`'s
  `_success_body()` fixture doesn't model prompt-caching `usage` fields or `stop_details`,
  which the real Bedrock response carries (confirmed 2026-07-24).
  **Trigger:** the next `bedrock/`-touching task that edits its tests.
- **Archived τ probe → schema-v1 golden fixture.** `archive/n1_tau/` is the one worked example
  from the n=1 probe; converting it into a golden fixture under the frozen task schema would
  give the harness a known-answer regression test.
  **Trigger:** task schema v1.1 lands.
- **Self-host the premise-selection server** (`hanwenzhu/lean-premise-server`). The EC2 hammer
  box currently uses the public default (`http://leanpremise.net`, per the LeanHammer README —
  documented as intended for individual use); self-hosting is a separate repo with its own
  setup, materially more complex than using the default (`docs/ec2_runbook.md` Phase D).
  **Trigger:** before the first real training round; until then the public server is used for
  search only — cached-script replay (reward doc §3.2) has no server dependency, so nothing
  downstream of a certified proof depends on the public server staying up.
- **Elastic IP or SSM Session Manager for stable EC2 box addressing.** The hammer box's public
  IP changes on every stop/start (`docs/ec2_runbook.md`), requiring a re-fetch (and a security-
  group rule update) every session.
  **Trigger:** if IP-refetch friction becomes a recurring cost (e.g. once sessions on this box
  become frequent enough that the manual re-fetch/re-authorize steps add up).
- **Two unexplained non-elaborating miner candidates.** `Tactic.NormNum.SquarefreeHelper`
  (`Data/Nat/Squarefree.lean`) and `SimpleGraph.ErdosStone.filter`
  (`Combinatorics/SimpleGraph/Extremal/ErdosStoneSimonovits.lean`) scan and qualify correctly
  (confirmed against the real source — not `_root_.`, not a `/-!` phantom, not a universe-
  annotation or `noncomputable section`/`public section` desync, not the dotted-namespace bug
  below — every class diagnosed so far) but `#check` still fails for both under their
  correctly-scanned name. Other declarations from the same two files elaborate fine, ruling out
  a whole-file import problem; root cause not established
  (`miner/output/non_elaborator_characterization.jsonl`, class `unexplained_correctly_scanned`).
  **Trigger:** the next miner scan-layer task (another parser-bug fix, another non-elaborator
  sweep, or a full-corpus mine into new territory).
- **`miner.scan` mis-tracks dotted multi-component `namespace A.B.C` declarations.** Lean treats
  `namespace A.B.C` as opening three nested namespaces (closable either as three separate
  `end`s or via a combined `end A.B` etc.), but the scanner's namespace stack pushes it as ONE
  opaque frame — correct for name *qualification* (string-joining one frame gives the same
  result as joining three), but wrong for stack *depth*, so a source file that closes such a
  namespace with multiple partial `end`s (e.g. `namespace Order.Frame.MinimalAxioms ... end
  MinimalAxioms ... end Order.Frame`, the real shape in `Order/CompleteBooleanAlgebra.lean`,
  `Order/Disjointed.lean`, `Order/Grade.lean`) desyncs the stack depth for whatever follows.
  Found while investigating the `noncomputable section`/`public section` fix (2026-07-24
  follow-up); confirmed harmless there — all 6 scanned candidates from the 3 affected files
  still elaborate correctly (`elaborates=True`), and only one (`disjointed`) is in the 727
  eligible set, unaffected — but the underlying stack-depth bug is real and could corrupt a
  future candidate's qualified name in a file shaped differently. Not fixed (out of scope for
  that task — it isn't a section-modifier variant).
  **Trigger:** the next miner scan-layer task, or any non-elaborator investigation that
  reproduces a namespace-tracking symptom not already covered by the fixed bug classes.
- **DONE (2026-08-05) — Bare-alias candidate bodies are now SCORED, not rejected.** The
  trigger (mini-trial design) fired at Stage B. `check_admissibility` unioned each declaration's
  `name` and `full_name`, and `full_name` resolves to the alias TARGET for a body that is a bare
  reference to an existing constant (`def VTask.choose := Nat.choose` reports
  `name='VTask.choose', full_name='Nat.choose'`), inventing a phantom second declaration.
  **Resolution: score them.** These are the memorization population the run exists to measure,
  not tampering, and excluding them would misclassify a verbatim-correct answer as inadmissible.
  Measured incidence: **5 of 1040** extractable prelim candidates, of which four are
  verbatim-correct `Nat.choose` — i.e. concentrated precisely on the `RECALLED_TARGET` slice the
  results table reports on, so the misclassification was not merely rare but biased. A
  declaration now counts as the pinned one when EITHER field names it; a second declaration, or
  a single declaration of some other name, still fails exactly as before.
- **Mined "mentions" have a very low standalone-elaboration rate (measured: 8.3%, 5/60) because
  the miner doesn't capture per-mention `variable`/`section`/`namespace` context.** Confirmed by
  manual inspection (`docs/tier_cascade_measurement_2026-07.md`): every inspected failure is
  either a bare namespace self-reference (e.g. `clog` needing `Nat.clog`) or a free variable from
  a file-scoped `variable` declaration the mined `statement_text` doesn't carry. Fact selection
  cannot use raw mentions verbatim as anchor facts until this is solved (either the miner
  captures the enclosing context per mention, or authoring-time synthesis reconstructs it).
  **Trigger:** the next fact-selection/authoring task that wants to draw real Mathlib mentions
  as anchor or global-fact candidates directly.
- **Self-citation: reusing a library's own existing theorem as a fact trivially passes via
  library-search tactics.** Measured 100% (5/5) on the tier-cascade run's certified facts —
  `exact?`/hammer found and cited the statement's own source theorem every time it discharged
  one. n=5 is too small to trust the *rate*, but the *mechanism* is structural: any fact that IS
  a real existing Mathlib theorem will be found by anything that searches Mathlib. Needs a
  design answer (mutation, non-verbatim restatement, or excluding raw mentions as fact sources
  entirely) before mentions-as-facts is viable, independent of the context-stripping issue above.
  **Trigger:** same as the context-stripping entry above — whichever fact-selection task
  revisits using mined mentions directly.
- **Retry-on-timeout usage isn't instrumented per attempt.** `TierAttempt` records status/
  elapsed/detail but not whether the underlying `run_checked` call needed its retry budget —
  `docs/tier_cascade_measurement_2026-07.md`'s "retry-flip count" ask couldn't be answered from
  existing records. Would need `run_checked`/`CheckResult` to surface an attempt count.
  **Trigger:** the next measurement or reliability review that specifically wants retry-rescue
  data (moot for any run where nothing approaches its timeout budget, as this one didn't).
- **`ladder.tier4`'s per-fact scoping is narrower than the reward doc's tier 4** (candidate-level
  whole-suite transfer, reward doc §3) — this session's `adjudicate_fact` only offers tier 4 as
  one more per-fact fallback when the caller supplies `truth_env`/`candidate_name`/`truth_name`;
  a single tier-4 success does not transfer the rest of the candidate's fact suite, since that
  needs a round-level driver this session doesn't build (`ladder/adjudicate.py`'s own docstring
  flags this).
  **Trigger:** the round-driver/training-loop task that actually runs candidates through the
  full ladder across a fact suite, not one fact at a time.
- **DONE (2026-07-30) — Parse-time mirror for rule 5 (`domain_inputs` keys ⊆ `domain.variables`).**
  Its own trigger fired for real: the 41-name batch's Gate 1 (`Nat.clog`, 2026-07-30 re-run,
  post-reducibility-fix) rotated at `emit_task` because a monotonicity-probing membership fact
  needed two values of `n` and, with no schema-sanctioned way to say so, the model invented
  keys `n1`/`n2` — caught only after the task's full round-trip spend was gone. Fixed in the
  same build session that found it: `authoring.parse.parse_facts` now threads `domain.variables`
  through and rejects (per-fact) any undeclared `domain_inputs` key, mirroring
  `harness.task_schema._validate_domain_inputs` exactly, with feedback naming the fix (schema
  v1.1.3's new list-valued `domain_inputs` — `"n": ["8", "9"]` — rather than a new key per
  point). See `docs/design/task_schema_v1_1.md`'s v1.1.3 changelog entry for the full design.
- **Cross-retry duplicate-id detection (rule 12).** `authoring.parse.parse_facts` only dedupes
  fact ids WITHIN one response; a fact from the original fact-proposal response and a fact from
  its row-3 retry response can share an id undetected until `emit_task`'s schema validation.
  Would need the original response's ids carried into the retry's `parse_facts` call.
  **Trigger:** the first real duplicate-id occurrence in a real batch (used deliberately as the
  test vehicle for the 2026-07-28 emit-rotation `round_trip_score`-preservation fix, so it's a
  known, exercised gap, not a hypothetical one).
- **Dossier convention-point parsing is looser than the schema, the same bug class in reverse.**
  Found during the 2026-07-28 parser-vs-schema strictness sweep (the session that made
  `expected_type` optional): `harness.task_schema._validate_conventions` requires a non-sentinel
  convention entry's `point` AND `statement` to both be non-empty strings (the NONE_DECLARED
  sentinel path requires BOTH null, no partial state); `authoring.parse._parse_convention_entry`
  only rejects a JSON-shape violation (wrong type) and the case where BOTH are null without a
  `NONE_DECLARED:`-prefixed note -- it silently accepts a MIXED entry (e.g. `point: null,
  statement: "some prose"`), which then fails `emit_task`'s schema validation. Confirmed live:
  `parse_dossier` accepts `{"point": null, "statement": "...", "note": "..."}`;
  `harness.task_schema._validate_conventions` rejects the identical payload with "field 'point'
  must be a non-empty string, got None". Not fixed this session (out of the fix session's
  explicit scope, which was about the parser being STRICTER than schema, not looser).
  **Trigger:** the first `emit` rotation whose `TaskSchemaError` names `domain.conventions`, or
  the next authoring-pipeline task that revisits dossier/domain parsing.
- **Recursor-class pseudo-gate: revisit if eliminator/recursor-shaped definitions appear at
  meaningful scale in wider harvests** (trigger: full-corpus or widened-mine selection run);
  decide then between a real coded gate, a curation policy, or admitting the class with a
  different task design. Cross-ref `miner/output/excluded_recursor_class.json`.
- **Richness metric blind spot: dependent binders/arrows inflate richness for
  proof-infrastructure definitions** (`Nat.leRec` ranked 2). Trigger: same as above. Evidence:
  batch-50 preflight + 29 July 2026 characterization report.
- **Namespace-relative sibling references: how a task names OTHER real Mathlib declarations.**
  A mined definition's `definition_source` is shown to the model exactly as it appears in
  Mathlib — i.e. written *inside* its enclosing namespace, so sibling declarations appear
  unqualified. The task environment splices only the task's own symbol at the root namespace, so
  those bare names do not resolve. Confirmed concretely (31 July 2026, $0 REPL probe against
  `Set.PartiallyWellOrderedOn.IsMinBadSeq`, whose definition reads `¬IsBadSeq r s g`):
  bare `IsBadSeq` → `Unknown identifier`; fully-qualified
  `Set.PartiallyWellOrderedOn.IsBadSeq` → **resolves**; the companion's own task symbol
  `VTask.IsBadSeq` → `Unknown identifier` (each task splices only itself, so a sibling task's
  symbol is never in scope); a realistic global fact using the qualified companion → **elaborates
  cleanly**; and the dossier leak check correctly **permits** the qualified companion, since it is
  a genuinely different declaration from the task's target. So no capability is missing — the
  machinery already supports everything such a task needs.
  **Mitigated, not solved**: `authoring/prompts/fact_proposal.txt` now tells the model that
  statements elaborate at the root namespace and that any other Mathlib declaration must be
  fully qualified, with this exact case as the worked example. That is guidance, not a
  guarantee. The open design question is whether the pipeline should instead *mechanically*
  help — e.g. supply the enclosing namespace as an explicit input field, qualify the source
  text before showing it, or `open` the namespace in the spliced environment (which risks
  collisions and changes what "the task environment" means for every task). This will recur
  for any definition mined from a family of mutually-referencing helpers, which is extremely
  common in Mathlib.
  **Trigger:** the second `mechanical_validation` rotation whose dropped facts are dominated by
  `Unknown identifier` on a sibling name (the first is IsMinBadSeq, 31 July 2026), or the
  pilot-100 mine, whichever comes first.
- **Dossier "Not to be confused with" sections should name neighbour objects anonymously.**
  Today those sections name real Mathlib declarations (`Nat.log`, `Int.greatestOfBdd`, ...) to
  disambiguate the target. For a model with memorized Mathlib those names are localization
  landmarks: being told the object is "not `Nat.log`, which rounds down" narrows the search to
  `Nat.clog` without the model ever reasoning from the specification. The section should instead
  describe the neighbour behaviourally and anonymously -- e.g. "a floor logarithm rounds down:
  floor-log 2 9 = 3" -- preserving the disambiguation while removing the landmark. Measured
  2026-08-03 (prelim testing Stage 2, report §4): **9 of the 41 dossiers name another batch
  task's target**; 0 name their own (the leak check already forbids that). Accepted as-is for
  prelim testing, since the exposure is identical across all models compared and identical to
  what the pipeline's own round-trip check already saw -- it biases the absolute numbers, not
  the ranking. **Trigger:** the next dossier-prompt revision, or pilot-100 authoring, whichever
  comes first.
- **Retry DeepSeek-Prover-V2 and Herald under a different tokenizer/vLLM configuration.** Both
  were excluded from the 2026-08-03 prelim field as *excluded-unmeasured*, not as failures: under
  vLLM 0.26.0 their output arrives byte-corrupted (raw BPE artifacts for space/newline; latin1-
  rendered UTF-8) and the content ignores the prompt, returning memorised benchmark or web text.
  One bounded rescue was attempted for DeepSeek (`--tokenizer-mode slow`, one sample) and failed
  identically. Notably both are non-Qwen-family, while all three models that decode cleanly are
  Qwen-derived -- so the suspicion is vLLM 0.26's detokenizer for these tokenizer types rather
  than anything in this repo. **Untried options:** `--tokenizer-mode slow` for Herald (never
  reached, it failed earlier on a context-length mismatch); pinning vLLM <= 0.25; or serving via
  transformers directly to isolate vLLM. **Trigger:** a contested prelim winner (where a missing
  prover-family baseline would change the conclusion), or a write-up that needs the standard
  DeepSeek-Prover baseline for comparability.
- **`authoring.roundtrip` still splices candidates through the un-laddered path.** Stage A
  (2026-08-04) gave the candidate splice the two rescues the truth side already had —
  `_root_.` qualification and the `noncomputable` retry — via
  `harness.scoring.splice_candidate_body`. `authoring/roundtrip.py:74-75` was deliberately NOT
  migrated: it still calls `signature.splice(body)` + `splice_candidate` directly, so a
  round-trip body needing either rescue fails to compile through no fault of the body. The
  round-trip check decides whether an authored task ships, so this is a live authoring gap.
  **Tested and NOT the explanation for the "harder" flags** (this is the interesting part):
  the obvious hypothesis was that batch-41's six `ROUND_TRIP_UNVERIFIED_COMPILE` names failed
  for want of exactly these rescues. Probed directly against live Mathlib (2026-08-04) — all
  six alias-splice cleanly on the plain path, needing neither rescue. The mechanism also rules
  itself out a priori: the self-reference collision requires the real declaration to be
  reachable *bare*, i.e. top-level unnamespaced (`Monotone`, `DependsOn`), and all six are
  namespaced (`Equiv.*`, `Function.Embedding.*`, `Filter.Germ.*`, `SimpleGraph.*`, `Graph.*`).
  So the six remain genuine corpus-hardness signal, and the roundtrip gap is a real but
  separate defect that has not yet been shown to have cost anything.
  **Trigger:** the next authoring/round-trip task.

- **Tranche B mining territory: `CategoryTheory`, `AlgebraicGeometry`, `AlgebraicTopology`,
  `Condensed`, `RepresentationTheory`, `MeasureTheory`, `Probability`, `Geometry/Manifold`.**
  Excluded from the batch-5 widening (11 Aug 2026) on the expectation of near-total attrition at
  the dependency-vocabulary and self-containment gates -- heavy abstract infrastructure whose
  dossiers are not self-containable at the current depth standard. Batch 5's own round-2 exclusion
  table supports this: `Algebra/Homology` (501 blocked refs), `CategoryTheory/Subfunctor` (375),
  `Algebra/Category` (193) and `AlgebraicTopology/*` (156) were the highest-count vocabulary
  rejections and were declined on exactly that ground.
  **Trigger:** the eligible pool falling short of a stage-2 need after the current 2,609 are
  consumed, or a strata need only this territory supplies (e.g. the `MeasurableSet` predicate
  layer for measure-theoretic tasks).
- **Richness blind-spot counters: MEASURED AND DECLINED, not open.** The recorded trigger
  ("revisit if recurring at scale in a wider harvest") fired with batch 5 and was answered:
  `blind_disjoint_binders` 14, `blind_heyting` 5, `blind_cond` 1 -- 20 of 2,609 eligible (0.8%)
  across a 4.8x-larger corpus. They do NOT recur at scale. The counters remain recorded as
  per-candidate metadata, excluded from `richness_total`, the preference score and every gate,
  with a load-bearing test asserting that exclusion.
  **Re-open only if:** a future harvest shows materially higher incidence, or a stage-2 failure
  mode is traced to one of these notations being invisible to the richness metric.
- **`mention_count` values are not comparable across batches 4 and 5.** The batch-5 rewrite of
  `compute_mention_counts` changed matching from `grep -F` substring to identifier-token, which
  corrects a systematic overcount for every name that prefixes a longer sibling. Cached batch-4
  `VerifiedDef` records retain their old (inflated) values unless re-verified. Harmless today --
  the field gates nothing -- but any future analysis that compares this metric across batches must
  re-derive it rather than trust the stored values.
  **Trigger:** the first analysis or gate proposal that reads `mention_count` quantitatively.
