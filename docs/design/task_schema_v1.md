# Task Schema v1

*Frozen 21 July 2026. Changes to this schema are versioned events (v2 with stated
rationale), never silent edits. Every component — miner, scorer, definition-writer
prompts — builds against this document.*

## Artifact shape

One directory per task:

    tasks/<task_id>/
      dossier.md      # prose spec — the human-authoritative statement of meaning
      task.json       # everything machine-readable

**Anti-drift rule:** no information exists authoritatively in both files. The
dossier owns mathematical meaning (what the object is, conventions as prose,
worked examples). task.json owns everything machinery reads. The single
deliberate overlap is the domain and its conventions, which appear in both; the
machine-readable form is authoritative for validation, and an authoring-time
consistency check confirms the prose states the same thing.

## task.json fields

All fields below are REQUIRED unless marked otherwise. A task missing any
required field is invalid and must be rejected by the validator.

- `task_id` (string), `schema_version` (must be "1").
- `signature`: `{ name, type, imports }` — the pinned signature candidates must
  inhabit.
- `domain`: the machine-readable scope of the specification:
  - `constraint` (string): a Lean-parsable predicate over the input variable(s),
    e.g. "n ≥ 1", or "True" if genuinely unrestricted.
  - `conventions` (array): junk-value / edge conventions, each
    `{ point, statement, note }` — e.g. point "0", statement "tau 0 = 0",
    note "Mathlib convention: divisors of 0 is empty". **This field is
    mandatory and may not be omitted or empty.** Where an object truly has no
    meaningful conventions, the array contains exactly one sentinel entry:
    `{ "point": null, "statement": null, "note": "NONE_DECLARED: <one-sentence
    reason>" }`. The authoring LLM must always actively fill this field —
    silence is not an option — and every value it supplies here is flagged
    for downstream review (human or agent) via the provenance block.
  - **Validation rule (mechanical, at authoring time):** every fact — and, when
    they exist, every mutant divergence-witness — must lie inside `constraint`
    or be a stated convention point. Out-of-domain facts are rejected before a
    task ships.
- `axiom_baseline` (array of axiom names): computed at authoring time by
  `#print axioms` on the true definition. Gate rule: a candidate's axiom
  closure must be a subset of this baseline.
- `admissibility_contract`: `{ "single_declaration": true }` — the candidate is
  exactly one declaration of the pinned name. Stated here so the gate and any
  definition-writer prompt can never silently disagree.
- `facts` (array), each:
  - `id` (string), unique within the task.
  - `type`: one of `casework | membership | global` (reward doc §2).
  - `mechanism`: one of `decide | proof`. Always declared, never implicit.
    `global` facts must have mechanism `proof`. `casework` facts must have
    mechanism `decide`. `membership` facts may have either.
  - `statement` (string): the Lean proposition, stated in terms of the pinned
    name.
  - Membership facts additionally: `instance`, `polarity` (`accept | reject`),
    and for rejects `violated_property` (the one broken clause — the §2.2
    diagnostic tag).
  - `provenance`: how this fact was produced and what validated it (free-form
    string plus `validation_run_id`).
- `heldout` (boolean): whether this task is reserved for evaluation and
  excluded from training data.
- `mutants` (array): RESERVED — must be present, must be `[]` in v1. Populated
  in a later phase, after candidate definitions exist.
- `prover_budget`: RESERVED — must be present, must be `null` in v1. Filled
  when the prover scaffold exists.
- `provenance` (task-level): `{ source: "mathlib" | "fresh", mathlib_name
  (optional), dossier_generator, validation_run_id, review_status }` —
  `review_status` records whether the LLM-populated domain/conventions block
  has been checked, one of `unreviewed | agent_reviewed | human_reviewed`.

## Scoring semantics

- Status vocabulary is per-mechanism:
  - mechanism `decide`: `PASSED | FAILED | ERRORED`.
  - mechanism `proof`: `TRUE | FALSE | UNKNOWN | ERRORED`. TRUE/FALSE are
    kernel-certified (the fact, or its negation, was proved). UNKNOWN means
    both attempts exhausted budget honestly. ERRORED means infrastructure
    failure. UNKNOWN and ERRORED are never folded into failure.
  - The tri-state protocol requires two independent attempts (fact, negation);
    this is a protocol requirement on the future prover scaffold.
- **Fidelity** = certified-passing / (total − UNKNOWN − ERRORED). UNKNOWN and
  ERRORED counts are always reported alongside the score.
- **UNKNOWN alarm:** if UNKNOWNs exceed 10% of a candidate's proof-mechanism
  facts, the score still computes but carries flag
  `EXCESSIVE_UNKNOWN` with a machine-readable reason (the count, the facts
  affected). Flagged pairs are surfaced for review: the cause is either a
  degenerate candidate or a defective task, and which one is a human/agent
  assessment that may lead to repairing or pulling that task. The 10% value
  is a dial, not a commitment; changing it is a config change, not a schema
  change.

## Validation manifest

A task is shippable only with a recorded validation run demonstrating:
1. every `decide` fact executed TRUE against the ground-truth definition;
2. every `proof` fact proved of the ground-truth definition under the
   production budget;
3. every fact in-domain per the domain validation rule;
4. dossier/domain consistency check passed;
5. the axiom baseline was computed, not assumed.
Tasks without a manifest enter no dataset.

## v1 clarifications

*Clarifications resolve underspecified fields; they change no frozen decision.
Each is dated. Anything that would alter a decision above requires v2.*

**2026-07-21 — `instance` representation.** The `instance` field of a
membership fact is always a Lean term string (e.g. `"[1, 2, 3]"`,
`"⟨3, by norm_num⟩"`), never structured data. Rationale: the fact `statement`
must reference the instance as a Lean term anyway, so any second
representation would duplicate authority over the same object (anti-drift
rule). The term must elaborate in the task's pinned environment; verifying
this is part of authoring-time validation (validation manifest, item 3),
alongside the domain-containment rule it naturally accompanies.

**2026-07-21 — status of structural vs. semantic validation.** The
`harness/task_schema.py` validator enforces the *structural* rules of this
schema (fields, types, compatibility constraints). Semantic rules — domain
containment of facts, instance elaboration, and everything in the validation
manifest — are authoring-time checks owned by the mining/authoring pipeline
and are recorded per-task in the validation manifest. A task passing the
structural validator is well-formed, not yet shippable.
