# Task Schema v1.1

*Frozen 24 July 2026. Replaces `task_schema_v1.md` (frozen 21 July 2026), which has been
deleted — this document is fully self-contained (see the Changelog below for the complete
v1 → v1.1 delta); the pre-v1.1 text is retrievable from git history if ever needed. Changes to
this schema are versioned events (v1.2/v2 with stated rationale), never silent edits. Every
component — miner, scorer, definition-writer prompts — builds against this document.*

*Written against `docs/design/reward_structure_2026-07-21.md` (consolidated 24 July 2026)
consequential-work item 1. `harness/task_schema.py`, `harness/facts.py`, `authoring/facts.py`
were updated in the same pass as this document — see repo history for that commit.*

## Changelog: v1.1.1 → v1.1.2

- **`task_symbol` (required string), new.** Per `docs/design/llm_io_contract_v1.md` §4.4 (the
  task-symbol convention): every task carries a task-local symbol, `VTask.<base name>` (e.g.
  `VTask.clog` for `Nat.clog`), used everywhere an object identity is needed — the pinned
  signature, every fact statement, and every splice (the true definition's body, aliased under
  the symbol to build the ground-truth environment, and any candidate body, round-trip or
  real). *Rationale:* splicing a candidate under a name that already exists in the base
  (Mathlib-imported) environment fails outright — confirmed empirically against real Mathlib,
  `` `Nat.clog` has already been declared `` — which blocked round-trip scoring for any task
  pinned under its real Mathlib name (found while building the driver session's end-to-end
  test). The task symbol is guaranteed fresh (no real Mathlib declaration uses the `VTask.`
  namespace), so splicing under it never collides, and truth-side validation and candidate
  scoring become the same operation.
- **Coherence rule: `signature.name` must equal `task_symbol`.** `signature.name` keeps its
  existing role unchanged (it is what candidates and facts actually reference for splicing) —
  `task_symbol` is the schema's own explicit, named assertion that a task follows the
  convention, enforced by requiring the two fields to agree. `authoring.emit.emit_task` is the
  single producer of task.json and enforces this by construction (overwrites `signature.name`
  with `task_symbol` unconditionally), so nothing that ships through it can disagree.
- **`task_symbol` format**: `VTask\.[A-Za-z_][A-Za-z0-9_']*` — anything else fails structural
  validation.
- This is a micro-addition in name only, decided so: unlike v1.1.1's `self_cited` (optional,
  backward compatible), `task_symbol` is REQUIRED and breaks any pre-existing task.json that
  lacks it — `tests/fixtures/tasks/is_sorted_v1/task.json` was updated in the same pass to stay
  valid. `SCHEMA_VERSION`'s enforced string is left at `"1.1"` regardless, matching the v1.1.1
  precedent, not because this change is non-breaking (it is) but because the project's own
  versioning discipline for this document treats `v1.1.x` as the informal micro-revision track
  and reserves a `v1.2`/`v2` frozen restatement for changes large enough to warrant one; this
  one, while breaking, is a single field plus one coherence rule.

## Changelog: v1.1 → v1.1.1

- **`discharge.self_cited` (optional boolean), new.** Per
  `docs/design/llm_io_contract_v1.md` §4.2 (the self-citation rule): a global fact that
  restates its anchor theorem near-verbatim discharges trivially by citing that anchor, so its
  recorded tier/cost must not be read as a candidate-side difficulty estimate (candidate-side
  the citation breaks — the candidate is a fresh symbol — and the fact's true depth is unknown
  until measured). `self_cited: true` marks this on the `discharge` record, alongside the real
  integer `tier` — not as a distinct tier value, since `tier` stays pinned to integers 1–5
  (2026-07-24 Clarification, unchanged). Omitted (or `false`) means "not flagged as
  self-citing"; absence is not an error, matching every other optional field in this schema.
  This is a micro-addition, not a new schema generation: every other v1.1 rule is unchanged,
  hence "v1.1.1" rather than a v1.2 with its own full restatement.

## Changelog: v1 → v1.1

- **Provisional status slot.** New required per-fact field `validation_status`
  (`CERTIFIED | PROVISIONALLY_VALIDATED`). *Rationale:* v1's validation manifest implicitly
  required every `proof` fact to already be proved before a task could ship, which the
  adjudication ladder (reward doc §3) makes both wrong and unnecessary — a task may now ship
  with global/proof-mechanism facts the ladder hasn't resolved yet, and the reward-side ladder
  (not authoring) resolves them. `decide` facts have no provisional state: they must already be
  executed-and-passed to ship, unchanged from v1.
- **`provenance` becomes a real runtime field**, not just a schema-required-but-unread key.
  *Rationale:* the structural validator already required `provenance` on every fact in v1; the
  Python dataclasses (`harness.facts.Fact`, `authoring.facts.ProposedFact`) never actually
  carried it, so the data was validated then silently dropped by every consumer. Fixed by
  adding a `FactProvenance` dataclass to both.
- **Statement format by mechanism is now a validated rule**, not an unstated convention.
  *Rationale:* v1 fixtures had already drifted — `tests/fixtures/authoring_facts.py`'s facts
  use full runnable commands (`example : ... := by decide`) while
  `tests/fixtures/tasks/is_sorted_v1/task.json`'s facts used bare propositions — with nothing
  catching the inconsistency. v1.1 fixes the convention as: `decide`-mechanism statements are
  the full runnable command; `proof`-mechanism statements are a bare `Prop` (no `:=`). The
  `is_sorted_v1` fixture is corrected to match.
- **`anchors` ships on `global` facts** (non-empty array of fully-qualified theorem names, no
  whitespace per entry). *Rationale:* `authoring.validate.validate_global_fact` has required
  and mechanically checked anchors since it was written — resolving each one in the pinned
  environment — but v1's schema had nowhere to put them in `task.json`, so `ProposedFact.to_fact()`
  silently discarded them before a task ever shipped. They are the tier-3 explicit premises
  (reward doc §3, tier 3) and existing only in memory during authoring made them unusable at
  reward time.
- **`domain.variables` and per-fact `domain_inputs` ship.** *Rationale:* v1's `domain.constraint`
  was "a Lean-parsable predicate over the input variable(s)" but named no variables anywhere,
  and `authoring.validate.check_domain_containment` already needed a fact's concrete
  input-variable binding to check containment — that binding (`ProposedFact.domain_inputs`)
  existed only in the authoring-time dataclass, with no schema home, so it was dropped by
  `to_fact()` exactly like `anchors` was.
- **`DomainSpec.conventions` (authoring dataclass) loses its `[]` default**, and
  `ConventionPoint.point`/`.statement` become `str | None` so the schema's own `NONE_DECLARED`
  sentinel (point/statement both null) is actually representable in code, not just in JSON.
  *Rationale:* the schema has allowed the sentinel since v1; the Python dataclass never could
  hold it (`point: str` was non-optional), which is a latent bug independent of anything else
  in this revision — caught while touching this file for the other changes here.
- **New ladder-era per-fact fields, all nullable:** `discharge` (`{tier, wall_clock_s, at}` or
  `null`), `cached_script` (proof script string or `null`), `axiom_closure` (list of axiom
  names or `null`, required exactly when `cached_script` is non-null). *Rationale:* schema
  homes for the tiered ladder's outputs (reward doc §3.2, §3.3), so a fact that has been
  discharged by the ladder can say so; the ladder itself is not built in this pass (see this
  document's own "Not built yet" note below).
- **New optional task-level field `ladder_budget_override`** (an object, opaque to this
  validator beyond that). *Rationale:* reward doc §7 — per-task budget overrides, defaults live
  in ladder config, not schema.
- **`prover_budget` removed** (was: RESERVED, must be `null`). *Rationale:* superseded by
  `ladder_budget_override`, above — both were "the budget for the thing that proves facts," and
  v1's own doc said `prover_budget` would be "filled when the prover scaffold exists," which the
  adjudication ladder now is. Rather than carry two fields for the same concept, this revision
  completes the consolidation: `ladder_budget_override` is the one home for it, and
  `prover_budget` is gone from the schema, the validator, the dataclasses, and every fixture.
- **`expected_type` (membership facts) stays authoring-only, decided.** Dropped by `to_fact()`,
  never reaches a shipped `task.json` fact entry. *Rationale:* nothing at reward time needs it —
  a `decide`-mechanism membership fact's `statement` already bakes the check in full
  (`example : Monotone (...) := by decide`), and a `proof`-mechanism membership fact's
  bare-`Prop` `statement` already carries the instance's type via the term itself (e.g.
  `Monotone (fun n : ℕ => n)` — the `ℕ` is right there). `expected_type` exists solely to drive
  the authoring-time `#check ((instance) : (expected_type))` elaboration probe; once that probe
  has run, nothing downstream reads the field again.
- **Duplicated mechanism/type and `violated_property` rules across `harness/task_schema.py` and
  `authoring/validate.py` stay split, decided.** This mirrors the schema's own "status of
  structural vs. semantic validation" clarification (below) — `task_schema.py` owns structural
  shape with path-prefixed exception messages (the miner's debugging interface, per that
  module's docstring); `authoring/validate.py` owns mechanical/semantic checks with
  `ValidationOutcome`/reason-code objects (the validation-manifest's record format). Unifying
  them would mean one module importing the other across a boundary that's currently clean, to
  save a handful of duplicated lines that are each independently tested. Revisit if the
  duplication grows past this size, or if the two ever disagree on a rule (they don't today).
- **`schema_version` must be `"1.1"`.** Old `"1"` payloads are no longer accepted; this is a
  breaking versioned migration, not an additive one, consistent with every field above being
  required (not optional-with-fallback) wherever the schema doc says "required."
- **Unchanged:** fidelity/scoring semantics, tri-state adjudication, `EXCESSIVE_UNKNOWN`,
  admissibility gate and contract, `axiom_baseline`, `mutants` (still RESERVED, still `[]`),
  task-level `provenance`, `heldout`, the `instance`-representation rule, the structural/semantic
  validation split (all restated in full below, not deferred to a now-deleted document).

### Not built yet

Nothing in this revision implements ladder execution, axiom-closure *checking* (only the
schema home to *record* a closure), or cache replay. `discharge`/`cached_script`/`axiom_closure`
are homes for those outputs, populated by hand in fixtures for now; no code in this repo writes
them yet outside test fixtures.

---

## Artifact shape

One directory per task:

    tasks/<task_id>/
      dossier.md      # prose spec — the human-authoritative statement of meaning
      task.json       # everything machine-readable

**Anti-drift rule:** no information exists authoritatively in both files. The dossier owns
mathematical meaning (what the object is, conventions as prose, worked examples). task.json
owns everything machinery reads. The single deliberate overlap is the domain and its
conventions, which appear in both; the machine-readable form is authoritative for validation,
and an authoring-time consistency check confirms the prose states the same thing. See
`docs/design/llm_io_contract_v1.md` §3 for the dossier's required structure and §3.4 for this
consistency check's specification.

## task.json fields

All fields below are REQUIRED unless marked otherwise. A task missing any required field is
invalid and must be rejected by the validator.

- `task_id` (string), `schema_version` (must be `"1.1"`).
- `task_symbol` (string, **new in v1.1.2**) — `VTask.<base name>` (e.g. `VTask.clog`), the
  task-symbol convention (`docs/design/llm_io_contract_v1.md` §4.4). Must equal
  `signature.name` exactly (coherence rule, see Changelog).
- `signature`: `{ name, type, imports }` — the pinned signature candidates must inhabit. `name`
  must equal `task_symbol` (above) — never the real Mathlib name for a mined task.
- `domain`: the machine-readable scope of the specification:
  - `constraint` (string): a Lean-parsable predicate over the input variable(s), e.g.
    `"n ≥ 1"`, or `"True"` if genuinely unrestricted.
  - `variables` (array of strings) — **new in v1.1**. The names of the input variable(s) that
    `constraint` (and every fact's `domain_inputs`, below) is stated over, e.g. `["b", "n"]` for
    a two-argument signature. Each entry a non-empty string; entries unique. May be `[]` only
    when the signature genuinely takes no domain-relevant inputs.
  - `conventions` (array): junk-value / edge conventions, each `{ point, statement, note }` —
    e.g. point `"0"`, statement `"tau 0 = 0"`, note `"Mathlib convention: divisors of 0 is
    empty"`. **This field is mandatory and may not be omitted or empty.** Where an object truly
    has no meaningful conventions, the array contains exactly one sentinel entry:
    `{ "point": null, "statement": null, "note": "NONE_DECLARED: <one-sentence reason>" }`. The
    authoring LLM must always actively fill this field — silence is not an option — and every
    value it supplies here is flagged for downstream review (human or agent) via the provenance
    block.
  - **Validation rule (mechanical, at authoring time):** every fact — and, when they exist,
    every mutant divergence-witness — must lie inside `constraint` or be a stated convention
    point. Out-of-domain facts are rejected before a task ships.
- `axiom_baseline` (array of axiom names): computed at authoring time by `#print axioms` on the
  true definition. Gate rule: a candidate's axiom closure must be a subset of this baseline.
- `admissibility_contract`: `{ "single_declaration": true }` — the candidate is exactly one
  declaration of the pinned name. Stated here so the gate and any definition-writer prompt can
  never silently disagree.
- `ladder_budget_override` (object, **OPTIONAL**, new in v1.1) — per-task override of ladder
  budgets (reward doc §7). Opaque to this validator beyond "must be an object" when present;
  defaults live in ladder config, not schema. May be omitted entirely.
- `facts` (array), each:
  - `id` (string), unique within the task.
  - `type`: one of `casework | membership | global` (reward doc §2).
  - `mechanism`: one of `decide | proof`. Always declared, never implicit. `global` facts must
    have mechanism `proof`. `casework` facts must have mechanism `decide`. `membership` facts
    may have either.
  - `statement` (string) — **format now validated by mechanism, new in v1.1**:
    - mechanism `decide`: the full runnable command — either a `#`-command (`#eval ...`,
      `#check ...`) or the `example ... := by decide` form.
    - mechanism `proof`: a bare `Prop` — no `:=`, no tactic block. The ladder wraps it as a
      goal in a standard template (`theorem <fact_id> : <Prop> := by <attempt>`) at discharge
      time; the proof-script cache (reward doc §3.2) stores scripts against this bare-Prop
      statement's hash.
  - `domain_inputs` (object, string → string, **new in v1.1**) — binds this fact's concrete
    Lean-term inputs to the names declared in `domain.variables` (every key must be one of
    them). Required non-empty for every `casework` fact. Required non-empty for `membership`
    facts unless `domain.constraint` is the unrestricted `"True"` sentinel, in which case it
    may be `{}`. For `global` facts it is always permitted to be `{}` (global facts state
    behaviour over the domain in general; concrete instance bindings are what `casework` and
    `membership` facts are for).
  - `anchors` (array of strings, **new in v1.1**) — required non-empty for `type: global`
    (fully-qualified Mathlib theorem names, no whitespace per entry — the tier-3 explicit
    premises, reward doc §3, tier 3). For `casework`/`membership` facts this must be `[]`.
  - `validation_status` (`CERTIFIED | PROVISIONALLY_VALIDATED`, **new in v1.1**):
    - mechanism `decide`: must be `CERTIFIED` (decide facts have no provisional state — they
      are executed-and-passed against the ground truth before a task ships, unchanged from
      v1's validation-manifest rule).
    - mechanism `proof`: either value. `CERTIFIED` means the ladder (reward doc §3) has
      produced and kernel-checked a proof; `PROVISIONALLY_VALIDATED` means the fact is
      well-formed (elaborates, anchors resolve, in-domain) but not yet discharged — the
      reward-side ladder resolves it later.
  - `discharge` (object or `null`, **new in v1.1**) — `{ "tier": 1-5, "wall_clock_s": number,
    "at": "authoring" | "reward", "self_cited": boolean (optional, new in v1.1.1) }` when
    present. Required non-null whenever mechanism is `proof` and `validation_status` is
    `CERTIFIED`. Required `null` whenever `validation_status` is `PROVISIONALLY_VALIDATED`.
    Optional either way for `decide` facts (tier-1 certification is definitionally instant;
    recording it is not required). `self_cited`, when present, must be a boolean — see the
    Changelog's v1.1.1 entry (`docs/design/llm_io_contract_v1.md` §4.2) for what it records.
  - `cached_script` (string or `null`, **new in v1.1**) — the reconstructed proof script.
    Required non-null exactly when mechanism is `proof` and `validation_status` is `CERTIFIED`;
    required `null` when `validation_status` is `PROVISIONALLY_VALIDATED`.
  - `axiom_closure` (array of strings or `null`, **new in v1.1**) — required non-null exactly
    when `cached_script` is non-null; required `null` when `cached_script` is `null` (reward doc
    §3.3's rule stated one direction — "required whenever `cached_script` is non-null" — this
    validator enforces the converse too, for internal coherence: a closure with no script to
    close over is meaningless).
  - Membership facts additionally: `instance`, `polarity` (`accept | reject`), and for rejects
    `violated_property` (the one broken clause — the §2.2 diagnostic tag).
  - `provenance`: `{ validation_run_id, note }` — how this fact was produced and what validated
    it, now actually carried by the runtime dataclasses (`harness.facts.FactProvenance`), not
    just validated-then-dropped.
- `heldout` (boolean): whether this task is reserved for evaluation and excluded from training
  data.
- `mutants` (array): RESERVED — must be present, must be `[]` in v1.1. Populated in a later
  phase, after candidate definitions exist.
- `provenance` (task-level): `{ source: "mathlib" | "fresh", mathlib_name (optional),
  dossier_generator, validation_run_id, review_status }` — `review_status` records whether the
  LLM-populated domain/conventions block has been checked, one of
  `unreviewed | agent_reviewed | human_reviewed`.

## Scoring semantics

- Status vocabulary is per-mechanism:
  - mechanism `decide`: `PASSED | FAILED | ERRORED`.
  - mechanism `proof`: `TRUE | FALSE | UNKNOWN | ERRORED`. TRUE/FALSE are kernel-certified (the
    fact, or its negation, was proved). UNKNOWN means both attempts exhausted budget honestly.
    ERRORED means infrastructure failure. UNKNOWN and ERRORED are never folded into failure.
  - The tri-state protocol requires two independent attempts (fact, negation); this is a
    protocol requirement on the adjudication ladder (reward doc §3).
- **Fidelity** = certified-passing / (total − UNKNOWN − ERRORED). UNKNOWN and ERRORED counts are
  always reported alongside the score.
- **UNKNOWN alarm:** if UNKNOWNs exceed 10% of a candidate's proof-mechanism facts, the score
  still computes but carries flag `EXCESSIVE_UNKNOWN` with a machine-readable reason (the count,
  the facts affected). Flagged pairs are surfaced for review: the cause is either a degenerate
  candidate or a defective task, and which one is a human/agent assessment that may lead to
  repairing or pulling that task. The 10% value is a dial, not a commitment; changing it is a
  config change, not a schema change.

## Validation manifest

A task is shippable only with a recorded validation run demonstrating:
1. every `decide` fact executed TRUE against the ground-truth definition (`validation_status:
   CERTIFIED`, unchanged from v1);
2. every `proof` fact is at least `PROVISIONALLY_VALIDATED` (elaborates, in-domain, anchors
   resolve, instance elaborates where applicable) — **relaxed from v1's "every proof fact
   proved," per the Changelog's first entry**; a fact reaching `CERTIFIED` additionally carries
   a `discharge` record from the ladder;
3. every fact in-domain per the domain validation rule, and every membership-fact instance
   elaborates in the pinned environment — unchanged from v1;
4. dossier/domain consistency check passed — specified in `docs/design/llm_io_contract_v1.md` §3.4;
5. the axiom baseline was computed, not assumed — unchanged from v1.

Tasks without a manifest enter no dataset — unchanged from v1.

## Clarifications

*Clarifications resolve underspecified fields; they change no decision above. Each is dated.*

**2026-07-21 — `instance` representation.** The `instance` field of a membership fact is always
a Lean term string (e.g. `"[1, 2, 3]"`, `"⟨3, by norm_num⟩"`), never structured data. Rationale:
the fact `statement` must reference the instance as a Lean term anyway, so any second
representation would duplicate authority over the same object (anti-drift rule). The term must
elaborate in the task's pinned environment; verifying this is part of authoring-time validation
(validation manifest, item 3), alongside the domain-containment rule it naturally accompanies.

**2026-07-21 — status of structural vs. semantic validation.** The `harness/task_schema.py`
validator enforces the *structural* rules of this schema (fields, types, compatibility
constraints). Semantic rules — domain containment of facts, instance elaboration, and
everything in the validation manifest — are authoring-time checks owned by the mining/authoring
pipeline and are recorded per-task in the validation manifest. A task passing the structural
validator is well-formed, not yet shippable.

**2026-07-24 — `discharge.tier` representation.** An integer 1–5, matching the reward doc's
`Tier 1`–`Tier 5` numbering exactly (§3), not a tier name string — the mapping from number to
tier semantics lives in the reward doc, not duplicated here.

**2026-07-24 — `domain.variables` vs. `domain_inputs` under an unrestricted (`"True"`) domain.**
`domain.variables` still names the signature's input variable(s) even when `constraint` is
`"True"` — the two are independent: `variables` says what the inputs are called, `constraint`
says what (if anything) restricts them. A `casework` fact still must bind them via
`domain_inputs` regardless of whether the constraint is trivial, since `domain_inputs` also
serves as the concrete-input record for the fact itself, not only as containment-check input.
