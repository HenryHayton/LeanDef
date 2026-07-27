# LLM I/O Contract v1 — Authoring Pipeline

*Drafted 25 July 2026 against task schema v1.1 and the consolidated reward-structure doc. Specifies every LLM interaction in task authoring: inputs, required output shapes, validation coupling, and failure handling. This document also supplies the first specification of three mechanisms previously named but unspecified: the dossier structure (§3), the blind round-trip check (§5), and the dossier/domain consistency check (§3.4). The orchestration layer implements this contract; the contract does not describe implementation.*

## 1 · Principles

1. **The LLM proposes; the machine validates; the human reviews batches.** No LLM output enters a task without passing mechanical validation, and no batch ships without a human-readable review.
2. **All structured output is strict JSON** — no markdown fences, no prose outside the JSON envelope, schema-v1.1 field names. A response that fails to parse gets exactly one retry with the parse error appended (§6); malformed-on-retry is terminal for that call.
3. **Every call is logged** via the Bedrock client's provenance log; every accepted artifact carries `provenance.validation_run_id` linking it to the validation pass that admitted it.
4. **Retrieval grounding**: every generation call's input includes the definition's Mathlib neighborhood from the mention sidecar (mentioning-theorem names and statements, capped and ranked by relevance). Instructions direct the model to cite existing Mathlib vocabulary rather than invent parallel notions.

## 2 · Call 1 — Regime classification

**Input:** pinned signature; true definition source; docstring; the mention-sidecar excerpt.
**Output (JSON):** `{regimes: [casework|membership|global, ...], difficulty: 1-5, rationale: <2 sentences>, expected_fact_mix: {casework: n, membership: n, global: n}}`. (Vocabulary note: `casework`, matching `Fact.type` everywhere — not `decidable`, which names a mechanism.)
**Rules:** Prop-valued definitions must not receive `casework` (it collapses into membership — settled by the Monotone fixture work). Order/Data-Set-population definitions are expected to classify global-leaning (batch-4 composition finding); a classification fighting that prior is not an error but is surfaced in the batch review.
**Validation:** mechanical — regimes consistent with the definition's return type (checker inspects the pinned signature).

## 3 · Call 2 — Dossier generation

**Input:** pinned signature; true definition source; docstring; mention-sidecar excerpt; the classification from Call 1.
**Output:** the dossier as markdown, inside a JSON envelope `{dossier_md: "..."}`, with the machine-readable `domain` object (constraint, variables, conventions per schema v1.1) as a sibling field `{domain: {...}}` produced in the same call — one call, two artifacts, so prose and machine forms cannot drift at birth.

### 3.1 Dossier structure (required sections, fixed order)
1. **Object** — what the definition denotes, informally, in terms a mathematician who has never seen Mathlib would accept.
2. **Signature** — the pinned signature restated with each argument's meaning.
3. **Conventions** — prose mirror of `domain.conventions`, one prose sentence per convention point (or the NONE_DECLARED reason). Junk-value behaviour goes here (e.g. "divisors 0 = ∅ by Mathlib convention").
4. **Worked examples** — at least 2 where the regime admits them; each carries a concrete claim AND, for casework regimes, a runnable Lean command asserting it. Executable examples are executed during validation; a dossier whose example fails execution is rejected outright.
5. **Boundaries** — edge cases and the behaviour at them.
6. **Not to be confused with** — 1–3 nearby objects/misreadings, one line each (this section is mutant material and seeds the fact suite's rejection side).

### 3.2 Root of authority
The dossier is the root of authority: facts and mutants are valid only within its declared domain. It never quotes the Lean definition body (the round-trip check depends on this — §5).

### 3.3 Prohibitions
No invented domain restrictions for total definitions (settled by the Nat.clog fixture work). No copying the definition body or its distinctive implementation choices into prose.

### 3.4 Dossier/domain consistency check (specified here, resolving the dangling v1 reference)
Mechanical where possible, LLM-assisted where not: (a) every `domain.conventions` entry must have a matching prose sentence in §3 of the dossier (matcher: statement substring or note keywords; failures flag, not reject); (b) executable worked examples are executed against the true definition; (c) a checker confirms the raw pinned-signature string appears verbatim as a substring within the dossier's Signature section (which otherwise wraps it in explanatory prose — whole-section equality is not the check). Failures of (b) and (c) reject; (a) flags for the batch review.

## 4 · Call 3 — Fact proposal

**Input:** the dossier (as authority); pinned signature; mention-sidecar excerpt (the mined mentioning theorems — the primary feedstock for global facts); classification. NOT the definition source — facts are proposed from the dossier, same information barrier as the round-trip. **Named contingency:** if the first slice's review shows casework quality suffering without sight of the implementation, the definition body may be admitted into the casework-proposal call only, keeping the barrier intact for globals and the dossier; this is a one-dial change requiring slice evidence.
**Output (JSON):** array of fact objects in schema v1.1 shape: `id, type, mechanism, statement, instance?, polarity?, violated_property?, anchors?, domain_inputs, expected_type?` — exactly the `ProposedFact` surface.

### 4.1 Per-type rules
- **Casework** (`mechanism: decide`): statement is the full runnable command. Both sides of every boundary named in dossier §5 probed where feasible.
- **Membership**: instance + polarity; rejection-polarity facts required (at least one per suite where the regime admits it) with `violated_property` naming what fails; instances drawn from or consistent with dossier examples.
- **Global** (`mechanism: proof`): statement is a bare Prop (no `:=`, no tactic block). Shape is enforced at the **parser layer** (§8) before any REPL call — a proof-mechanism statement containing `:=` or `by` is rejected with a format code and gets the one format retry; this is deliberately a strict superset of the schema-level rule (which checks only `:=`) — defense-in-depth against tactic-block leakage, and the asymmetry is intentional: nothing that clears the parser can fail the schema check. Statements that pass shape but fail to elaborate come back `PROPOSITION_DOES_NOT_ELABORATE` (the code the global validator actually produces — `MALFORMED_UNPARSEABLE_STATEMENT` is a casework/membership-path code and does not fire for globals). `anchors` non-empty, fully-qualified, resolvable — anchor quality matters: the specific theorems the fact derives from, not a namespace dump.

### 4.2 The self-citation rule
A global fact that restates its anchor theorem near-verbatim is permitted but must be marked by the model (`self_restatement: true`). Recording: self-citation lives as an optional boolean `self_cited` on the discharge record, alongside the real integer tier — NOT as a tier value, since `discharge.tier` is schema-pinned to integers 1–5 (this requires a one-field schema addition, queued in §8). Rationale: truth-side, such a fact discharges trivially by citing the anchor, so its recorded tier/cost must not be used as a candidate-side estimate — candidate-side the citation breaks (fresh symbol) and true depth is unknown until measured. Mechanical detection (discharge proof is `exact <anchor>` or trivially equivalent) activates when ladder execution exists; until then the model's declaration is collected and carried.

### 4.3 Suite-level rules
Fact ids unique; suite covers the dossier's boundaries; no fact may quantify over objects outside the declared domain; per-suite size guidance by difficulty (configuration, not contract).

## 5 · Call 4 — Blind round-trip check (specified here)

**Mechanism:** a fresh LLM context (no conversation history) receives ONLY the dossier and the pinned signature — not the true definition, not the fact suite, not the mention sidecar — and is asked to write the definition body.
**Pass criterion — first cut (pre-ladder):** the round-trip definition is spliced as a candidate and must pass admissibility plus every casework and decide-mechanism membership fact; global facts are checked structurally (statement elaborates against the round-trip candidate) but not proof-scored, since ladder execution does not yet exist. Implementation note: today's `run_facts` deliberately raises on proof-mechanism facts rather than skipping — so the first cut is implemented by the orchestration layer partitioning the suite (proof facts withheld from `run_facts`; a new spliced-candidate elaboration check, which has no existing precedent, run on them separately — §8 item). **Full criterion (activates when the ladder worker lands):** the complete suite under authoring ladder budgets, equivalence-tier success recorded when it occurs but not required. The first-cut/full distinction is recorded per task so early tasks can be re-scored under the full criterion later.
**Interpretation of failure:** a round-trip failure indicts the *task*, not the round-trip model — either the dossier underdetermines the object or the facts test things the dossier does not state. The task is flagged for repair (dossier revision or fact revision), one repair cycle permitted, then terminal for the batch (rotates to the next candidate definition).
**Information hygiene:** the round-trip context must never contain the definition source; the orchestration layer enforces this structurally (separate call path), not by prompt discipline alone.
**Side value:** the round-trip candidate is the first non-verbatim definition each fact suite meets; its ladder run is recorded as candidate-side discharge evidence feeding the pilot's tier-cascade and cost measurements.

## 6 · Error handling (single table of record)

| Failure | Handling |
|---|---|
| JSON parse failure | one retry with parse error appended; then terminal for the call |
| Schema-shape failure (missing field etc.) | one retry with the validator's reason code + offending fragment; then terminal |
| `MALFORMED_UNPARSEABLE_STATEMENT` (casework/membership) or parser-layer format rejection (global shape) or `PROPOSITION_DOES_NOT_ELABORATE` (global elaboration) | one retry citing the format rule for that mechanism; then the fact is dropped (suite may still ship if coverage rules hold) |
| Fact fails ground truth (`FALSE_OF_GROUND_TRUTH` etc.) | NO retry — this is signal about the model's mathematics, logged to the batch review; fact dropped |
| `ERRORED` (infrastructure) | not charged to the model; validation re-run once; persistent → task flagged, not dropped |
| Dossier executable example fails | dossier rejected, one regeneration with the failure shown; then task rotates |
| Round-trip failure | per §5: one repair cycle, then rotate |

Retries are per-call, never compound; a task consumes at most a bounded number of LLM calls (configuration), and a task that exhausts its call budget rotates out — the authoring analogue of the funded-channel invariant.

## 7 · Batch review (human gate, unchanged in spirit)

Every authoring batch produces a human-readable review: per-task outcomes, dropped facts with reason codes, flagged consistency items, self-citation rates, dossier §6 contents (misreading material), call/token/dollar totals. The standing rule applies: the human reads it before the batch is accepted.

## 8 · Consequential work (the implementation session's scope)

1. Parser layer: LLM JSON → `ProposedFact`/`DomainSpec` (does not exist; first construction of these objects outside test fixtures). Includes the cheap statement-shape pre-checks per §4.1 (proof statements must not contain `:=`/`by`; decide statements must be runnable-command-shaped) with their own format reason codes, applied before any REPL call.
2. Task emitter: validated artifacts → task.json + dossier.md per schema v1.1 Artifact shape (validator exists, writer does not).
3. Prompt templates as versioned files; orchestration over bare `BedrockClient.send` including the retry table above (client correctly raises on malformed; orchestration owns retries).
4. Mention-sidecar retrieval helper: cap + relevance ranking over the per-definition mention list (§1.4) — new work; the sidecar persists full unranked lists today.
5. Round-trip first-cut scoring path (§5): suite partitioning so proof-mechanism facts never reach `run_facts` (which raises on them by design), plus the new spliced-candidate elaboration check for withheld global facts — no existing code does this (the global validator elaborates against the true environment only).
6. Schema v1.1.1 micro-addition: optional boolean `self_cited` on the discharge record (§4.2), one versioned changelog line, validator updated in the same pass.
7. Housekeeping riding along: fix the dangling "unchanged from v1" reference in task_schema_v1_1.md §validation-manifest (point at §3.4 here); fix curation.yaml's stale "top-N" comment wording.

**Sequencing note:** nothing in this contract's implementation depends on ladder execution; the two places that reference it (§4.2 mechanical self-citation detection, §5's full round-trip criterion) are explicitly staged to activate at the ladder-worker milestone, with first-cut behaviour defined above. The first slice runs on the first-cut definitions.
