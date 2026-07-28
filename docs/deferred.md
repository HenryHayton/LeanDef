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
- **Bare-alias candidate bodies (e.g. `body = Nat.clog` verbatim) trip the admissibility
  shadowing check rather than being scored as memorization** — decide handling.
  **Trigger:** mini-trial design.
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
- **Parse-time mirror for rule 5 (`domain_inputs` keys ⊆ `domain.variables`).** `harness.
  task_schema._validate_fact` rejects a fact whose `domain_inputs` key isn't one of the task's
  declared `domain.variables`; `authoring.parse.parse_facts` doesn't check this — it would need
  the dossier's `domain.variables` threaded into `parse_facts` (not just `domain_constraint`,
  which the 2026-07-28 enforcement session already added for the membership non-emptiness rule).
  **Trigger:** the first `emit` rotation or review flag showing a fact with a wrong/unknown
  domain-variable key in a real batch.
- **Cross-retry duplicate-id detection (rule 12).** `authoring.parse.parse_facts` only dedupes
  fact ids WITHIN one response; a fact from the original fact-proposal response and a fact from
  its row-3 retry response can share an id undetected until `emit_task`'s schema validation.
  Would need the original response's ids carried into the retry's `parse_facts` call.
  **Trigger:** the first real duplicate-id occurrence in a real batch (used deliberately as the
  test vehicle for the 2026-07-28 emit-rotation `round_trip_score`-preservation fix, so it's a
  known, exercised gap, not a hypothetical one).
