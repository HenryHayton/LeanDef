"""The top-level authoring pipeline driver (contract §8's last consequential-work item, per
the orchestration session's report: "no top-level `author_task(...)` pipeline driver was
built... left as the natural next step").

`author_task` CHAINS the stations built across the prior sessions -- `authoring.mentions`,
`authoring.orchestrate`'s per-call functions and `with_one_repair_cycle`, `authoring.consistency`,
`authoring.roundtrip`, `authoring.emit`, `authoring.task_symbol` -- in contract order. It does
not reimplement any of their logic; every retry/repair/error-classification rule it appears to
apply is really just the composition of what those stations already do.

**Task-symbol convention (contract §4.4)**, resolving this driver's own reported finding: every
task authors under a task-local symbol, `VTask.<base name>` (`authoring.task_symbol.task_symbol_for`),
never the real Mathlib name. The pinned signature, every fact statement, and every splice --
both the TRUE definition's body (aliased under the symbol to build a fresh ground-truth
environment: `def VTask.clog : T := Nat.clog`, via `harness.scoring.splice_candidate`, the same
splice machinery round-trip already used) and the round-trip candidate body -- use the symbol.
Because both splices originate independently from the SAME untouched `base_env` (never chained
onto each other), neither can collide with the real declaration OR with each other -- this is
what makes `round_trip_base_env` (the prior session's workaround) unnecessary; it has been
retired. `authoring.parse.parse_facts`'s `forbidden_name` check enforces that the model never
writes the real name into a fact statement in the first place.

Three genuine driver-layer decisions, documented where they're made below because the contract
is silent on all three:

1. **`discharge`/`cached_script`/`axiom_closure` are always `null`.** No ladder exists (schema
   doc's own "Not built yet" note, unchanged this session); every accepted fact this driver
   emits is either `mechanism: decide` (schema-mandated `CERTIFIED`, tier-1 certification never
   recorded per schema doc's own "recording it is not required") or `mechanism: proof`
   (`PROVISIONALLY_VALIDATED` -- `authoring.validate`'s global/proof-mechanism validators never
   return `ACCEPTED`, only `PROVISIONALLY_VALIDATED` at best, confirmed by reading both
   validators, not assumed). `validation_status` is therefore fully determined by
   `fact.mechanism` alone -- no verdict needs threading through from `AdjudicationResult`.
2. **Round-trip retry policy (revised 2026-07-28, replacing the original blind-single-repair
   design)**: the round-trip stage's third real attempt against `Nat.clog` (2026-07-28) failed
   twice, byte-for-byte the same request both times (confirmed by diffing the two logged
   request bodies), on a genuinely fixable Lean termination-checker issue -- exactly the
   failure mode blind repair can never recover from. The policy now distinguishes two failure
   kinds, matching `docs/design/llm_io_contract_v1.md` §5's updated text: a COMPILE failure
   (fails admissibility) gets up to `authoring.config.ROUND_TRIP_MAX_COMPILE_ATTEMPTS` (4) total
   attempts, each retry carrying the PREVIOUS attempt's code and Lean error verbatim as feedback
   (`ladder.tier3`-style "give it what actually happened," not blind resampling) -- the
   information barrier still holds, since only the round-trip's own prior attempt/error is
   shown, never the definition source, fact suite, or fact-failure detail. If every one of the
   4 attempts fails and every failure was PURELY a termination-checker error (never any other
   admissibility reason, and never mixed), the task ships anyway with a
   `ROUND_TRIP_FLAG_UNVERIFIED_TERMINATION_ONLY` flag -- termination-checking a fuel/measure-
   based recursion is a genuinely separate, sometimes very hard problem from whether the
   dossier determines the object, and failing only on it should not indict the task the way a
   dossier-quality failure would. A FACT failure (compiles, but the fact suite doesn't pass)
   gets NO retry at all: the stage ends immediately and the task rotates, flagged for review --
   retrying against a fact failure would optimize the definition toward the facts rather than
   the dossier, which is exactly the information-barrier violation the round-trip check exists
   to catch, not something to paper over with another attempt.
3. **`self_restatement` (contract §4.2) is collected and reported in the batch review, not
   projected into a shipped `discharge.self_cited`.** Since `discharge` is always `null` (point
   1), there is currently nowhere in a shipped task.json for it to land; see
   `authoring.facts.ProposedFact.self_restatement`'s own docstring.
4. **Every type-conditional required-field rule `harness.task_schema._validate_fact` enforces is
   mirrored at parse time (2026-07-28)**, not just discovered at `emit_task`. The real
   2026-07-28 `Nat.clog` run rotated at `emit` after all 6 real LLM calls: 15/15 casework facts
   had reached that point with an empty `domain_inputs` (silently defaulted by
   `authoring.parse`, never checked by `authoring.validate`'s casework path, and never mentioned
   as required by the fact-proposal prompt's casework rule text) and the schema validator
   rejected the first one it saw. `authoring.parse.parse_facts` now rejects (per-fact, feeding
   the existing batched row-3 retry -- see its own docstring) any fact missing a rule
   `harness.task_schema` would reject it for: non-empty `domain_inputs` for casework and
   domain-constrained membership, non-empty `anchors` for global, empty `anchors` for
   non-global. The principle: no fact may reach `emit` missing anything `emit` will reject for.

No station's public interface was broken to build this driver -- `authoring.parse.parse_facts`
and `authoring.orchestrate.run_fact_proposal_call` both gained new OPTIONAL keyword parameters
(`task_symbol`/`forbidden_name`, and as of 2026-07-28 `domain_constraint`), backward compatible
with every existing caller. One adaptation was made to a non-code artifact:
`authoring/prompts/dossier.txt` specifies a parseable Worked-Examples convention (a `Claim: ...`
bullet + optional fenced command) -- without it, `authoring.consistency` check (b) had nothing
reliable to extract.
"""

import json
import uuid
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable

from lean_interact import AutoLeanServer, Command

from authoring import config as authoring_cfg
from authoring.consistency import (
    ConsistencyCheckResult,
    ConventionMatchResult,
    check_dossier_consistency,
    check_round_trip_recalls_target,
    inject_pinned_signature,
)
from authoring.composition import enforce as enforce_composition
from authoring.emit import emit_task
from authoring.fact_validation import _schema_status as schema_status, validate_fact
from authoring.facts import DomainSpec, ProposedFact
from authoring.mentions import DEFAULT_MENTION_CAP, render_mention_excerpt
from authoring.orchestrate import (
    AuthoringCallFailed,
    CallBudget,
    CallBudgetExceeded,
    FactParseRejection,
    run_classification_call,
    run_dossier_call,
    run_fact_proposal_call,
    run_round_trip_generation_call,
    with_one_repair_cycle,
    adjudicate_proposed_facts,
)
from authoring.parse import Classification, DossierPayload
from authoring.roundtrip import RoundTripScore, score_round_trip_first_cut
from authoring.task_symbol import task_symbol_for
from authoring.validate import ValidationOutcome
from bedrock.client import BedrockClient, BedrockClientError
from harness import config as cfg
from harness.admissibility import _parse_axioms  # internal helper, reused deliberately -- see
# `_compute_axiom_baseline`'s own note; not duplicated, not made public API here.
from harness.facts import Fact, FactProvenance
from harness.repl import run_checked
from harness.results import CheckStatus
from harness.scoring import splice_candidate, splice_real_name
from harness.signature import PinnedSignature
from harness.task_schema import TaskSchemaError
from miner.harvest import MentionRecord

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "output"


# === Driver inputs ==============================================================================


@dataclass(frozen=True)
class DefinitionInput:
    """Everything about ONE definition the pipeline needs, beyond infrastructure. Assembling
    this from a real corpus (mining output, Mathlib source lookup) is out of scope for this
    driver -- no existing station does it, and building one wasn't asked for; callers (the
    end-to-end test, a future batch script) supply it via `PipelineConfig.resolve_definition`.

    `name` is the REAL Mathlib name (e.g. `"Nat.clog"`) -- used to build the truth-splice alias
    and as `authoring.parse.parse_facts`'s `forbidden_name`, never written into a statement
    itself. The task symbol every statement/splice actually uses is derived from it
    mechanically (`authoring.task_symbol.task_symbol_for`), not stored here.
    """

    name: str
    signature_dict: dict  # schema shape: {name, type, imports} -- 'name' is informational only;
    # the driver always splices/pins under the computed task symbol, never this value.
    definition_source: str
    docstring: str
    return_shape: str  # "value" | "prop" | "bundled" (miner.shape.classify_return_shape's own
    # vocabulary) -- mechanical truth read off the real pinned type, NOT something the
    # classification call infers from prose (2026-07-30, docs/design/llm_io_contract_v1.md §2
    # enforcement). Required, not defaulted: a caller that has no real corpus to read this from
    # has no business authoring a task at all, so there is no honest default to fall back to.
    decidability: str | None = None  # authoring.preflight.probe_decidability's vocabulary
    # ("decidable"|"undecidable"|"indeterminate") -- unlike return_shape, genuinely optional:
    # None is the correct, common value for every non-Prop task, not a caller oversight, so
    # this is defaulted rather than required (2026-07-30, docs/design/llm_io_contract_v1.md §4.1).
    mention_records: list[MentionRecord] = field(default_factory=list)


@dataclass(frozen=True)
class PipelineConfig:
    client: BedrockClient
    authoring_model_id: str
    flagship_model_id: str
    server: AutoLeanServer
    base_env: int
    resolve_definition: Callable[[str], DefinitionInput]
    output_dir: Path = DEFAULT_OUTPUT_DIR
    batch_review_dir: Path = DEFAULT_OUTPUT_DIR
    max_calls_per_task: int = authoring_cfg.AUTHORING_MAX_CALLS_PER_TASK
    mention_cap: int = DEFAULT_MENTION_CAP
    check_timeout: float | None = None
    heldout: bool = False


# === Driver outputs ==============================================================================


@dataclass(frozen=True)
class StageRecord:
    stage: str
    status: str  # "ok" | "flagged" | "rotated"
    detail: str = ""
    calls_made: int = 0


@dataclass(frozen=True)
class TaskResult:
    definition_name: str
    outcome: str  # "SHIPPED" | "ROTATED"
    rotated_at_stage: str | None
    stage_records: list[StageRecord]
    parser_rejected_facts: list[FactParseRejection] = field(default_factory=list)
    validation_dropped_facts: list[ValidationOutcome] = field(default_factory=list)
    task_errored_facts: list[ValidationOutcome] = field(default_factory=list)
    convention_flags: list[ConventionMatchResult] = field(default_factory=list)
    self_restatement_fact_ids: list[str] = field(default_factory=list)
    calls_made: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    task_dir: Path | None = None
    round_trip_score: RoundTripScore | None = None
    round_trip_flags: list[str] = field(default_factory=list)  # e.g.
    # [ROUND_TRIP_FLAG_UNVERIFIED_TERMINATION_ONLY, ROUND_TRIP_FLAG_RECALLED_TARGET] -- LIST,
    # not a single value (renamed from `round_trip_flag: str | None` 2026-07-29): the two flags
    # are orthogonal conditions that can both fire across a single round-trip attempt sequence
    # (see `_author_task_inner`'s round-trip block for exactly how) -- see
    # `_is_termination_only_failure`'s and `authoring.consistency.check_round_trip_recalls_target`'s
    # own docstrings for what each means and why it exists. Confirmed safe to rename cleanly,
    # not a backward-compat concern: grepped every emitted `task.json` (committed and
    # scratchpad) plus `authoring/emit.py` itself for `round_trip_flag` before this rename --
    # zero hits anywhere; this field has never been part of a shipped artifact. No home in the
    # emitted task.json's schema-validated `provenance` object was found for it either
    # (`harness.task_schema._validate_task_provenance` is permissive about extra keys, but
    # nothing in the schema DOCUMENT sanctions one -- adding a key that merely happens to pass
    # validation is exactly "inventing a schema field silently," which an earlier session's
    # task explicitly said not to do) -- lives only in `TaskResult` and the batch review for
    # now; a real open question for whoever next revises schema v1.1, not resolved here.


# === Internal helpers ============================================================================


def _render_classification(c: Classification) -> str:
    return f"regimes={c.regimes}, difficulty={c.difficulty}, rationale={c.rationale!r}"


def _summarize_consistency_failure(result: ConsistencyCheckResult) -> str:
    parts = []
    if not result.signature_injection_ok:
        parts.append(f"signature check: {result.signature_detail}")
    if not result.real_name_leak_ok:
        parts.append(result.real_name_leak_detail)
    for c in result.worked_example_checks:
        if c.kind in ("EXECUTION_FAILED", "MALFORMED_NO_WORKED_EXAMPLES"):
            parts.append(f"worked example ({c.kind}) {c.claim!r}: {c.detail}")
    return "; ".join(parts) if parts else "consistency check failed for an unspecified reason"


# Round-trip ships anyway (flagged) when every compile-failure attempt was PURELY a
# termination-checker error. Markers below are drawn from three real, independently-observed
# Lean error texts (2026-07-28): the real slice run's own failure ("fail to show termination
# for... failed to infer structural recursion:... Could not find a decreasing measure.... Please
# use `termination_by`..."), plus two deliberately-provoked cases confirming Lean's termination
# diagnostics come in more than one shape -- a `termination_by` clause present but wrong
# ("failed to prove termination, possible solutions:... Use `decreasing_by`...") reads
# completely differently from the "no termination_by at all" case, so a single fixed phrase
# would have missed it. "termination" alone (case-insensitive) already covers all three
# observed cases; the rest are redundant-but-safe backstops for phrasing this session hasn't
# seen. None of Lean's other admissibility-failure vocabulary (sorry, axiom, name-shadowing)
# plausibly contains any of these words, so this is not just convenient -- it doesn't fire on
# an unrelated failure by coincidence either, as far as this session's evidence shows.
_TERMINATION_ERROR_MARKERS = (
    "termination",
    "decreasing measure",
    "structural recursion",
    "decreasing_by",
)


# `RoundTripScore.admissibility_detail` is built (in `authoring.roundtrip
# .score_round_trip_first_cut`) as `f"{verdict.failure.value}: {verdict.detail}"` when the
# failure came from a real `check_admissibility` verdict -- `"compile_error: ..."` specifically
# for `AdmissibilityFailure.COMPILE_ERROR` (never "sorry:"/"new_axiom:"/"name_shadowed:"), and
# with NO such prefix at all for a splice-level `ERRORED` (an infrastructure hiccup, not the
# model's code -- deliberately excluded from the termination-only carve-out below by this same
# prefix check, since it isn't a "compile error" in the sense this policy means).
ROUND_TRIP_FLAG_UNVERIFIED_TERMINATION_ONLY = "UNVERIFIED_TERMINATION_ONLY"

# Round-trip ships anyway (flagged) when the candidate body itself references the task's real
# Mathlib name (decided 2026-07-29, after a real round-trip attempt against `Nat.clog` returned
# the literal text `Nat.clog b n`). Detection is not a failure: a clean round-trip pass on a
# recalled body is not evidence the dossier alone determines the object (the model may simply
# have recalled the real answer from pretraining, not derived it) -- the check abstains where
# it cannot measure, the same shape as the termination-only flag above. See
# `authoring.consistency.check_round_trip_recalls_target` for the detection mechanism.
ROUND_TRIP_FLAG_RECALLED_TARGET = "RECALLED_TARGET"

# Round-trip ships anyway (flagged) when every compile attempt was exhausted and the failures
# were NOT purely termination-related -- the general compile-exhaustion case the two flags above
# don't cover. Adopted 31 July 2026 as a corpus-hardness decision, not a loosening: these tasks'
# dossiers and fact suites already passed every upstream check, so the only thing unverified is
# whether a fresh-context model can re-derive the definition in Lean. The 2026-07-31 failure
# forensics found these failures cluster hard on bundled return types (`≃`, `↪`, structures) --
# i.e. the flag marks definitions that are HARDER TO ENCODE, exactly the population the corpus
# most needs to retain rather than silently filter out. Third instance of this codebase's
# abstain-when-you-cannot-measure pattern (see the two flags above); the flag is data for the
# mini-trial, never a defect marker. Rendered to humans as "harder" -- see `render_batch_review`.
ROUND_TRIP_FLAG_UNVERIFIED_COMPILE = "ROUND_TRIP_UNVERIFIED_COMPILE"

# Human-facing labels for round-trip flags. The mechanical constant stays the schema//code name;
# only the batch review (and anything else showing a human a flag) uses these.
ROUND_TRIP_FLAG_LABELS = {
    ROUND_TRIP_FLAG_UNVERIFIED_COMPILE: "harder",
}


def render_round_trip_flag(flag: str) -> str:
    """`harder (ROUND_TRIP_UNVERIFIED_COMPILE)` for a flag with a human label; the bare constant
    otherwise. One helper so every human-facing surface renders flags identically."""
    label = ROUND_TRIP_FLAG_LABELS.get(flag)
    return f"{label} ({flag})" if label else flag


def _is_termination_only_failure(admissibility_detail: str) -> bool:
    if not admissibility_detail.startswith("compile_error:"):
        return False
    lowered = admissibility_detail.lower()
    return any(marker in lowered for marker in _TERMINATION_ERROR_MARKERS)


def _count_log_lines(log_path: Path) -> int:
    if not log_path.exists():
        return 0
    with log_path.open(encoding="utf-8") as f:
        return sum(1 for _ in f)


def _token_totals_since(log_path: Path, start_line: int) -> dict:
    totals = {"input_tokens": 0, "output_tokens": 0}
    if not log_path.exists():
        return totals
    with log_path.open(encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i < start_line or not line.strip():
                continue
            record = json.loads(line)
            usage = (record.get("response") or {}).get("usage") or {}
            totals["input_tokens"] += usage.get("input_tokens", 0)
            totals["output_tokens"] += usage.get("output_tokens", 0)
    return totals


def _compute_axiom_baseline(server: AutoLeanServer, env: int, task_symbol: str, *, timeout: float | None) -> list[str]:
    """`#print axioms <task_symbol>` against the truth-splice environment (schema doc: "computed
    at authoring time by `#print axioms` on the true definition" -- `task_symbol` in `env` IS
    the true definition, aliased there by the truth splice). Reuses
    `harness.admissibility._parse_axioms` (an internal helper, not public API) rather than
    duplicating its two regexes -- both live in this same project, not a third-party boundary."""
    timeout = timeout if timeout is not None else cfg.DECIDE_TIMEOUT
    check = run_checked(server, Command(cmd=f"#print axioms {task_symbol}", env=env), timeout=timeout)
    if check.status is not CheckStatus.PASSED or check.raw_response is None:
        return []
    info_messages = [m.data for m in check.raw_response.messages if m.severity == "info"]
    for data in info_messages:
        parsed = _parse_axioms(data)
        if parsed is not None:
            return sorted(parsed)
    return []


# === author_task ==================================================================================


def author_task(definition_name: str, config: PipelineConfig) -> TaskResult:
    """Author one task for `definition_name`, end to end. Never raises: every failure mode --
    a station's own terminal exception, budget exhaustion, an unexpected error -- is caught and
    turned into a `TaskResult(outcome="ROTATED", ...)` carrying the full stage-by-stage record,
    since `author_batch`'s whole contract depends on a single task never taking the batch down
    with it.

    `budget`/`log_start_line` are created HERE, not inside `_author_task_inner`, specifically so
    this function's own `except` branch can still report real spend on a crash that happens
    deep inside a station -- `budget` is a mutable object `_author_task_inner` charges as it
    goes, so even if an exception cuts the inner call short, `budget.calls_made` at the moment
    of the crash is exactly how many calls were actually made, and `_token_totals_since` reads
    directly from the log rather than from any state the crash might have skipped past. Before
    this, an unexpected-error rotation silently reported zero calls/tokens even when a real,
    billed Bedrock call had just succeeded moments earlier (confirmed 2026-07-28: a genuine
    classification call spent 1773+257 tokens, then crashed in response parsing, and the
    resulting `TaskResult` claimed 0 calls / 0 tokens)."""
    budget = CallBudget(max_calls=config.max_calls_per_task)
    log_start_line = _count_log_lines(config.client.log_path)
    try:
        return _author_task_inner(definition_name, config, budget, log_start_line)
    except Exception as e:  # noqa: BLE001 -- the batch-mode safety net; see docstring.
        tokens = _token_totals_since(config.client.log_path, log_start_line)
        return TaskResult(
            definition_name=definition_name,
            outcome="ROTATED",
            rotated_at_stage="unexpected_error",
            stage_records=[StageRecord(stage="unexpected_error", status="rotated", detail=f"{type(e).__name__}: {e}", calls_made=budget.calls_made)],
            calls_made=budget.calls_made,
            input_tokens=tokens["input_tokens"],
            output_tokens=tokens["output_tokens"],
        )


def _make_rotate(
    definition_name: str, config: PipelineConfig, budget: CallBudget,
    stage_records: list[StageRecord], log_start_line: int,
) -> Callable[..., "TaskResult"]:
    """Factory for the `_rotate` closure `_author_task_inner`/`_author_from_dossier` each need --
    identical shape, different `stage_records` list, so a factory avoids duplicating the body
    (2026-07-30, extracted for `authoring.cleanup`'s re-run-downstream-of-a-repaired-dossier
    path, which needs `_author_from_dossier`'s own rotation bookkeeping to work exactly the same
    way as a normal run's, not a reimplementation of it)."""

    def _rotate(stage: str, detail: str, **partial) -> TaskResult:
        stage_records.append(StageRecord(stage=stage, status="rotated", detail=detail, calls_made=budget.calls_made))
        tokens = _token_totals_since(config.client.log_path, log_start_line)
        return TaskResult(
            definition_name=definition_name,
            outcome="ROTATED",
            rotated_at_stage=stage,
            stage_records=list(stage_records),
            parser_rejected_facts=partial.get("parser_rejected", []),
            validation_dropped_facts=partial.get("validation_dropped", []),
            task_errored_facts=partial.get("task_errored", []),
            convention_flags=partial.get("convention_flags", []),
            self_restatement_fact_ids=partial.get("self_restatement", []),
            calls_made=budget.calls_made,
            input_tokens=tokens["input_tokens"],
            output_tokens=tokens["output_tokens"],
            # `round_trip_score`/`round_trip_flags` (2026-07-28 fix): a rotation that happens
            # AFTER round-trip scoring already ran (currently only `emit`'s `TaskSchemaError`
            # branch) must not discard that result -- confirmed lost in the real 2026-07-28
            # clog run, where a fully-passing round trip was recorded as `None` because the
            # `emit`-stage rotation never threaded it through.
            round_trip_score=partial.get("round_trip_score"),
            round_trip_flags=partial.get("round_trip_flags", []),
        )

    return _rotate


def _author_task_inner(definition_name: str, config: PipelineConfig, budget: CallBudget, log_start_line: int) -> TaskResult:
    stage_records: list[StageRecord] = []
    run_id = f"{definition_name}-{uuid.uuid4().hex[:8]}"
    _rotate = _make_rotate(definition_name, config, budget, stage_records, log_start_line)

    # --- lookup ---------------------------------------------------------------------------
    try:
        definition_input = config.resolve_definition(definition_name)
    except Exception as e:  # noqa: BLE001 -- caller-supplied resolver; one bad name must not sink the batch
        return _rotate("lookup", f"{type(e).__name__}: {e}")
    stage_records.append(StageRecord("lookup", "ok", calls_made=budget.calls_made))

    task_symbol = task_symbol_for(definition_input.name)
    pinned_signature = f"{task_symbol} : {definition_input.signature_dict['type']}"
    signature_obj = PinnedSignature(name=task_symbol, type_sig=definition_input.signature_dict["type"])

    # --- mention retrieval ------------------------------------------------------------------
    mention_excerpt = render_mention_excerpt(definition_input.mention_records, cap=config.mention_cap)
    stage_records.append(StageRecord("mention_retrieval", "ok", calls_made=budget.calls_made))

    # --- Truth splice (contract §4.4): alias the real definition under the task symbol -------
    # `def VTask.clog : T := Nat.clog` -- the SAME splice machinery (harness.scoring.splice_candidate)
    # round-trip candidates use, off the SAME untouched base_env, so this can never collide with
    # the real declaration (a fresh VTask.* name) or with a later candidate splice (independent,
    # also off base_env, never chained onto this one).
    truth_splice = splice_real_name(
        config.server, config.base_env, signature_obj, definition_input.name, timeout=config.check_timeout
    )
    if truth_splice.status is not CheckStatus.PASSED:
        return _rotate("truth_splice", truth_splice.detail or "truth-side splice under the task symbol failed")
    truth_env = truth_splice.env
    stage_records.append(StageRecord("truth_splice", "ok", calls_made=budget.calls_made))

    # --- Call 1: classification --------------------------------------------------------------
    try:
        classification = run_classification_call(
            config.client, config.authoring_model_id,
            pinned_signature=pinned_signature, definition_source=definition_input.definition_source,
            docstring=definition_input.docstring, mention_sidecar_excerpt=mention_excerpt,
            return_shape=definition_input.return_shape, budget=budget,
        )
    except (AuthoringCallFailed, CallBudgetExceeded, BedrockClientError) as e:
        return _rotate("classification", f"{type(e).__name__}: {e}")
    stage_records.append(StageRecord("classification", "ok", calls_made=budget.calls_made))
    classification_text = _render_classification(classification)

    # --- Call 2: dossier + §3.4 consistency check, one repair cycle -------------------------
    holder: dict = {}

    def dossier_attempt():
        note = holder.get("failure_note")
        classification_input = (
            classification_text if note is None else
            f"{classification_text}\n\nNOTE: your previous dossier attempt failed a mechanical "
            f"check and must be corrected: {note}"
        )
        try:
            payload = run_dossier_call(
                config.client, config.flagship_model_id,
                pinned_signature=pinned_signature, definition_source=definition_input.definition_source,
                docstring=definition_input.docstring, mention_sidecar_excerpt=mention_excerpt,
                classification=classification_input, decidability=definition_input.decidability,
                budget=budget,
            )
        except (AuthoringCallFailed, CallBudgetExceeded, BedrockClientError) as e:
            holder["last_failure_kind"] = "call"
            holder["failure_note"] = None
            return False, f"{type(e).__name__}: {e}"

        # Mechanical signature injection (contract §3.4(c), 2026-07-31): the model never wrote
        # the pinned signature itself (dossier.txt's own prompt), so it's inserted here, once,
        # before the dossier is used for anything else -- see authoring.consistency's own note.
        payload = replace(payload, dossier_md=inject_pinned_signature(payload.dossier_md, pinned_signature))
        holder["payload"] = payload
        consistency = check_dossier_consistency(
            config.server, truth_env, pinned_signature, payload.dossier_md, payload.domain,
            timeout=config.check_timeout, forbidden_name=definition_input.name,
        )
        holder["consistency"] = consistency
        if consistency.passed:
            return True, "ok"
        holder["last_failure_kind"] = "consistency"
        detail = _summarize_consistency_failure(consistency)
        holder["failure_note"] = detail
        return False, detail

    def dossier_repair():
        return None  # feedback carried via `holder["failure_note"]`, read on the next attempt

    dossier_outcome = with_one_repair_cycle(dossier_attempt, dossier_repair)
    if not dossier_outcome.passed:
        stage = "dossier" if holder.get("last_failure_kind") == "call" else "dossier_consistency"
        return _rotate(stage, dossier_outcome.detail)
    stage_records.append(StageRecord("dossier", "ok", calls_made=budget.calls_made))
    dossier_payload: DossierPayload = holder["payload"]
    consistency_result: ConsistencyCheckResult = holder["consistency"]
    stage_records.append(
        StageRecord(
            "dossier_consistency", "ok" if not consistency_result.flags else "flagged",
            detail=f"{len(consistency_result.flags)} convention-prose flag(s)", calls_made=budget.calls_made,
        )
    )

    return _author_from_dossier(
        definition_name, config, budget, log_start_line, stage_records, run_id,
        definition_input, task_symbol, pinned_signature, signature_obj, truth_env,
        mention_excerpt, classification_text, dossier_payload, consistency_result,
    )


def _author_from_dossier(
    definition_name: str, config: PipelineConfig, budget: CallBudget, log_start_line: int,
    stage_records: list[StageRecord], run_id: str,
    definition_input: DefinitionInput, task_symbol: str, pinned_signature: str, signature_obj: PinnedSignature,
    truth_env: int, mention_excerpt: str, classification_text: str,
    dossier_payload: DossierPayload, consistency_result: ConsistencyCheckResult,
) -> TaskResult:
    """Everything downstream of a dossier that has already passed `dossier_consistency`: fact
    proposal -> mechanical validation -> round-trip -> emit. Factored out of `_author_task_inner`
    (2026-07-30) so `authoring.cleanup`'s repair loop can re-run this EXACT chain against a
    revised dossier -- fresh facts, fresh round-trip, fresh emit, never grafting old facts onto
    a new dossier -- without reimplementing any of its retry/flag logic. `stage_records` is
    APPENDED TO, not replaced: the caller passes in whatever stage history already exists
    (lookup/mention_retrieval/truth_splice/classification/dossier/dossier_consistency for a
    normal run; the cleanup repair loop's own history for a re-run), so a `TaskResult`'s
    `stage_records` always reads as one continuous story regardless of which caller built it."""
    _rotate = _make_rotate(definition_name, config, budget, stage_records, log_start_line)

    # --- Call 3: fact proposal ----------------------------------------------------------------
    try:
        proposal = run_fact_proposal_call(
            config.client, config.authoring_model_id,
            pinned_signature=pinned_signature, dossier_md=dossier_payload.dossier_md,
            mention_sidecar_excerpt=mention_excerpt, classification=classification_text, budget=budget,
            task_symbol=task_symbol, forbidden_name=definition_input.name,
            domain_constraint=dossier_payload.domain.constraint,
            decidability=definition_input.decidability,
            domain_variables=dossier_payload.domain.variables,
            reject_topup=True,
        )
    except (AuthoringCallFailed, CallBudgetExceeded, BedrockClientError) as e:
        return _rotate("fact_proposal", f"{type(e).__name__}: {e}", convention_flags=consistency_result.flags)
    stage_records.append(
        StageRecord(
            "fact_proposal", "ok",
            detail=f"{len(proposal.facts)} proposed, {len(proposal.dropped)} format/name-dropped",
            calls_made=budget.calls_made,
        )
    )

    topup = proposal.reject_topup
    if topup is not None and topup.needed:
        # Measured on the 50-task run: the reject floor of 2 was stated as "hard" in the prompt
        # and only 15 of 29 suites met it, 7 with ZERO reject facts, while the mechanically
        # enforced decide cap held 29/29. So the floor gets ONE focused re-ask. It never discards
        # the task -- a suite still short after the top-up ships anyway, because the floor of 2 is
        # not yet known to be the right number and deleting the evidence would prevent finding out.
        stage_records.append(
            StageRecord(
                "reject_topup", "ok" if topup.met_after else "still_short",
                detail=f"{topup.before} -> {topup.after} reject facts; {topup.detail}",
                calls_made=budget.calls_made,
            )
        )

    # --- Mechanical validation against ground truth (contract §6 rows 4-5) -------------------
    try:
        adjudication = adjudicate_proposed_facts(
            config.server, truth_env, proposal.facts, dossier_payload.domain, task_symbol,
            timeout=config.check_timeout,
        )
    except Exception as e:  # noqa: BLE001 -- REPL/infra issues here must not sink the batch
        return _rotate(
            "mechanical_validation", f"{type(e).__name__}: {e}",
            parser_rejected=proposal.dropped, convention_flags=consistency_result.flags,
        )
    if not adjudication.accepted:
        return _rotate(
            "mechanical_validation", "no facts survived mechanical validation",
            parser_rejected=proposal.dropped, validation_dropped=adjudication.dropped,
            task_errored=adjudication.task_errored, convention_flags=consistency_result.flags,
        )
    stage_records.append(
        StageRecord(
            "mechanical_validation", "ok",
            detail=(
                f"{len(adjudication.accepted)} accepted, {len(adjudication.dropped)} dropped, "
                f"{len(adjudication.task_errored)} errored"
            ),
            calls_made=budget.calls_made,
        )
    )

    self_restatement_ids = [f.id for f in adjudication.accepted if f.self_restatement]

    # --- Suite composition, enforced (11 Aug 2026) --------------------------------------------
    # The prompt calls the decide cap and reject floor "hard", but a prompt only asks. The
    # 3-task calibration proved asking insufficient: 10 decide facts against a cap of 6 on one
    # task, a 6-fact suite against a floor of 8 on another.
    comp = enforce_composition(adjudication.accepted)
    surviving = comp.kept
    stage_records.append(
        StageRecord(
            "composition", "ok" if comp.ok else "violations",
            detail=(f"{len(surviving)} kept, {comp.trimmed_decide} decide trimmed to cap"
                    + (f"; {'; '.join(comp.violations)}" if comp.violations else "")),
            calls_made=budget.calls_made,
        )
    )

    # --- Fact validation ladder (schema v1.2) --------------------------------------------------
    # Replaces "validated against ground truth" as a claim made without running the kernel. Five
    # checks against the TRUTH splice: restatement rejection, anchor-must-be-a-theorem, negation
    # (a fact false of the truth is quarantined, which is how the two known defective facts are
    # caught), full-ladder discharge, and witness validation on reject facts. See
    # `authoring.fact_validation`.
    validations = {}
    validated_facts = []
    for f in surviving:
        # `pinned_signature` here is the RENDERED STRING, not an object -- reading `.imports`
        # off it raised AttributeError inside the per-task try, which rotated every task at
        # `unexpected_error` AFTER its three Bedrock calls had already been paid for. The
        # imports live on the resolved definition input.
        v = validate_fact(config.server, truth_env, f, task_symbol, definition_input.name,
                          imports=definition_input.signature_dict.get("imports"))
        validations[f.id] = v
        if v.ships:
            validated_facts.append((f, v))
    quarantined = [fid for fid, v in validations.items() if not v.ships]
    stage_records.append(
        StageRecord(
            "fact_validation", "ok",
            detail=(f"{len(validated_facts)} ship "
                    f"({sum(1 for _, v in validated_facts if v.status == 'CERTIFIED')} certified), "
                    f"{len(quarantined)} rejected/quarantined"),
            calls_made=budget.calls_made,
        )
    )

    fact_list: list[Fact] = [
        f.to_fact(
            validation_status=schema_status(v.status),
            anchors_resolved=v.anchors_resolved,
            cached_script=v.winning_script,
            axiom_closure=v.axiom_closure,
            # Schema: a CERTIFIED proof fact must carry a discharge record. The ladder has the
            # evidence (which tier won, with what script); without projecting it here the task
            # fails emit at the first proof fact -- decide facts are unaffected, which is why
            # the failure surfaced only at facts[6].
            # Schema shape (harness.task_schema._validate_discharge): tier, wall_clock_s and
            # `at` are all REQUIRED once discharge is non-null.
            discharge=({"tier": v.tier, "wall_clock_s": v.wall_clock_s, "at": "authoring",
                        "script": v.winning_script,
                        "self_cited": bool(getattr(f, "self_restatement", False))}
                       if v.status == "CERTIFIED" and f.mechanism == "proof" else None),
            provenance=FactProvenance(
                validation_run_id=run_id,
                note=(f"authored by {config.authoring_model_id}; "
                      f"{v.status.lower()} by the v1.2 kernel validation ladder"),
            ),
        )
        for f, v in validated_facts
    ]

    # --- Call 4: blind round-trip generation + scoring -----------------------------------------
    # Splices under `task_symbol` into the SAME untouched `base_env` the truth splice used --
    # an independent splice, not chained onto `truth_env`, so it cannot collide with the truth
    # alias declared there.
    #
    # Retry policy (decided 2026-07-28, replacing the prior blind-single-repair design -- see
    # module docstring, decision 2, and `docs/design/llm_io_contract_v1.md` §5): a COMPILE
    # failure (fails admissibility) gets up to `ROUND_TRIP_MAX_COMPILE_ATTEMPTS` total attempts,
    # each retry carrying the previous attempt's code and Lean error as feedback. A FACT failure
    # (compiles, but the fact suite doesn't pass) is immediately terminal -- no retry at all,
    # regardless of which attempt number produced it.
    rt_attempts: list[tuple[str, RoundTripScore]] = []  # (body, score), one entry per real attempt
    rt_call_failure_detail: str | None = None
    recalled_target = False  # set the moment ANY attempt's body names the real Mathlib name

    for _ in range(authoring_cfg.ROUND_TRIP_MAX_COMPILE_ATTEMPTS):
        if rt_attempts:
            prev_body, prev_score = rt_attempts[-1]
            feedback_kwargs = {"previous_attempt": prev_body, "previous_error": prev_score.admissibility_detail}
        else:
            feedback_kwargs = {}
        try:
            body = run_round_trip_generation_call(
                config.client, config.authoring_model_id,
                pinned_signature=pinned_signature, dossier_md=dossier_payload.dossier_md, budget=budget,
                **feedback_kwargs,
            )
        except (CallBudgetExceeded, BedrockClientError) as e:
            rt_call_failure_detail = f"{type(e).__name__}: {e}"
            break

        # Checked BEFORE scoring (2026-07-29): detection doesn't skip scoring -- a recalled body
        # still gets scored for the record (the score may be legitimately high, which is exactly
        # the problem the flag exists to mark) -- it skips only the RETRY decision below.
        if check_round_trip_recalls_target(body, definition_input.name):
            recalled_target = True

        score = score_round_trip_first_cut(
            config.server, config.base_env, signature_obj, body, fact_list, check_timeout=config.check_timeout,
        )
        rt_attempts.append((body, score))
        if recalled_target:
            # No feedback resend, no further attempts, regardless of pass/fail/compile state --
            # "detection is not a failure" (decided 2026-07-29): once the model has named the
            # real target, more attempts can't make the signal any more trustworthy.
            break
        if score.passed:
            break
        if score.admissible:
            # Compiled, but the fact suite failed -- immediately terminal (decided 2026-07-28):
            # retrying against a fact failure would optimize the definition toward the facts
            # rather than the dossier, defeating the information barrier the round-trip check
            # exists to enforce. A compiled-but-fact-failing attempt IS the check working as
            # intended, not a defect to route around.
            break
        # else: a compile failure -- loop continues (with feedback) up to the attempt cap.

    if rt_call_failure_detail is not None:
        return _rotate(
            "round_trip_generation", rt_call_failure_detail,
            parser_rejected=proposal.dropped, validation_dropped=adjudication.dropped,
            task_errored=adjudication.task_errored, convention_flags=consistency_result.flags,
            self_restatement=self_restatement_ids,
        )

    last_body, last_score = rt_attempts[-1]
    round_trip_flags: list[str] = []
    if recalled_target:
        round_trip_flags.append(ROUND_TRIP_FLAG_RECALLED_TARGET)

    scoring_detail = ""
    if not last_score.passed:
        if last_score.admissible:
            detail = (
                "compiled but failed the fact suite (no retry, per policy): "
                f"failing decide facts: {last_score.failing_decide_fact_ids}; "
                f"failing global facts: {last_score.failing_global_fact_ids}"
            )
            if recalled_target:
                # Never rotated once recall is detected (decided 2026-07-29) -- ships anyway,
                # flagged; the fact-suite result is not evidence either way for a recalled body.
                scoring_detail = f"shipped despite fact-suite failure ({detail}) -- round-trip candidate recalled the real Mathlib name, see RECALLED_TARGET flag"
            else:
                return _rotate(
                    "round_trip_scoring", detail,
                    parser_rejected=proposal.dropped, validation_dropped=adjudication.dropped,
                    task_errored=adjudication.task_errored, convention_flags=consistency_result.flags,
                    self_restatement=self_restatement_ids,
                )
        else:
            # Every attempt was a compile failure. Since 31 July 2026 a FULLY EXHAUSTED attempt
            # cap always ships (flagged) rather than rotating -- the only question is which
            # flag: `UNVERIFIED_TERMINATION_ONLY` when every failure was purely Lean's
            # termination checker (the narrower, older carve-out), otherwise the general
            # `ROUND_TRIP_UNVERIFIED_COMPILE`. Recall is orthogonal and stacks: `RECALLED_TARGET`
            # was already appended above, so an exhausted+recalled run carries both, exactly as
            # termination-only+recall already did. A run that stopped EARLY without recall (a
            # budget or infrastructure cut-off) has not established compile exhaustion at all
            # and still rotates.
            summary = "; ".join(f"attempt {i + 1}: {s.admissibility_detail}" for i, (_, s) in enumerate(rt_attempts))
            exhausted = len(rt_attempts) == authoring_cfg.ROUND_TRIP_MAX_COMPILE_ATTEMPTS
            recall_note = " -- round-trip candidate also recalled the real Mathlib name, see RECALLED_TARGET flag" if recalled_target else ""
            if exhausted and all(_is_termination_only_failure(s.admissibility_detail) for _, s in rt_attempts):
                round_trip_flags.append(ROUND_TRIP_FLAG_UNVERIFIED_TERMINATION_ONLY)
                scoring_detail = f"shipped after {len(rt_attempts)} compile attempt(s), all termination-only{recall_note}"
            elif exhausted:
                round_trip_flags.append(ROUND_TRIP_FLAG_UNVERIFIED_COMPILE)
                scoring_detail = f"shipped after {len(rt_attempts)} compile attempt(s) failing ({summary}) -- reconstruction unverified, see {ROUND_TRIP_FLAG_UNVERIFIED_COMPILE} flag{recall_note}"
            elif recalled_target:
                # Recall stopped the loop early, so the cap was never exhausted -- ships on the
                # recall flag alone (decided 2026-07-29).
                scoring_detail = f"shipped despite {len(rt_attempts)} compile attempt(s) failing ({summary}) -- round-trip candidate recalled the real Mathlib name, see RECALLED_TARGET flag"
            else:
                return _rotate(
                    "round_trip_scoring", f"exhausted {len(rt_attempts)} compile attempt(s): {summary}",
                    parser_rejected=proposal.dropped, validation_dropped=adjudication.dropped,
                    task_errored=adjudication.task_errored, convention_flags=consistency_result.flags,
                    self_restatement=self_restatement_ids,
                )
    elif recalled_target:
        scoring_detail = "passed, but round-trip candidate recalled the real Mathlib name -- score is not evidence, see RECALLED_TARGET flag"

    stage_records.append(StageRecord("round_trip_generation", "ok", calls_made=budget.calls_made))
    stage_records.append(
        StageRecord(
            "round_trip_scoring",
            "ok" if (last_score.passed and not round_trip_flags) else "flagged",
            detail=scoring_detail,
            calls_made=budget.calls_made,
        )
    )
    round_trip_score: RoundTripScore = last_score

    # --- Emit -----------------------------------------------------------------------------
    try:
        axiom_baseline = _compute_axiom_baseline(
            config.server, truth_env, task_symbol, timeout=config.check_timeout
        )
        emitted = emit_task(
            config.output_dir / definition_name,
            task_id=definition_name,
            task_symbol=task_symbol,
            signature=definition_input.signature_dict,
            domain=dossier_payload.domain,
            axiom_baseline=axiom_baseline,
            facts=fact_list,
            dossier_md=dossier_payload.dossier_md,
            heldout=config.heldout,
            provenance={
                "source": "mathlib",
                "mathlib_name": definition_input.name,
                "dossier_generator": config.flagship_model_id,
                "validation_run_id": run_id,
                "review_status": "unreviewed",
            },
        )
    except TaskSchemaError as e:
        return _rotate(
            "emit", str(e),
            parser_rejected=proposal.dropped, validation_dropped=adjudication.dropped,
            task_errored=adjudication.task_errored, convention_flags=consistency_result.flags,
            self_restatement=self_restatement_ids,
            round_trip_score=round_trip_score, round_trip_flags=round_trip_flags,
        )
    stage_records.append(StageRecord("emit", "ok", calls_made=budget.calls_made))

    tokens = _token_totals_since(config.client.log_path, log_start_line)
    return TaskResult(
        definition_name=definition_name,
        outcome="SHIPPED",
        rotated_at_stage=None,
        stage_records=stage_records,
        parser_rejected_facts=proposal.dropped,
        validation_dropped_facts=adjudication.dropped,
        task_errored_facts=adjudication.task_errored,
        convention_flags=consistency_result.flags,
        self_restatement_fact_ids=self_restatement_ids,
        calls_made=budget.calls_made,
        input_tokens=tokens["input_tokens"],
        output_tokens=tokens["output_tokens"],
        task_dir=emitted.task_dir,
        round_trip_score=round_trip_score,
        round_trip_flags=round_trip_flags,
    )


# === author_batch =================================================================================


def author_batch(
    names: list[str], config: PipelineConfig, *, stop_after_first_failure: bool = False
) -> tuple[list[TaskResult], Path]:
    """Sequential, continue-on-rotation (decided 26 July 2026: "a failed task NEVER halts the
    batch"). `stop_after_first_failure` exists for future use, default `False`, per the same
    decision. Writes the human-readable batch review file and returns `(results, review_path)`.
    """
    results: list[TaskResult] = []
    for name in names:
        result = author_task(name, config)
        results.append(result)
        if stop_after_first_failure and result.outcome == "ROTATED":
            break
    review_path = _write_batch_review(results, config.batch_review_dir)
    return results, review_path


def render_batch_review(results: list[TaskResult]) -> str:
    shipped = [r for r in results if r.outcome == "SHIPPED"]
    rotated = [r for r in results if r.outcome == "ROTATED"]
    lines = [
        "# Authoring batch review", "",
        f"Generated: {datetime.now(UTC).isoformat()}",
        f"Tasks: {len(results)} ({len(shipped)} shipped, {len(rotated)} rotated)", "",
        "## Per-task outcomes", "",
    ]
    for r in results:
        header = f"### {r.definition_name} -- {r.outcome}"
        if r.rotated_at_stage:
            header += f" (rotated at `{r.rotated_at_stage}`)"
        lines.append(header)
        lines.append(f"- calls made: {r.calls_made}; tokens: {r.input_tokens} in / {r.output_tokens} out")
        if r.task_dir is not None:
            lines.append(f"- task dir: `{r.task_dir}`")
        if r.round_trip_flags:
            # Flag(s) and score always rendered together (decided 2026-07-29) -- a reader must
            # never be able to see one without the other, since a flag is precisely what marks
            # an otherwise-normal-looking score as non-evidence.
            lines.append(
                f"- **round-trip flag(s): {', '.join(render_round_trip_flag(f) for f in r.round_trip_flags)}**"
            )
            if r.round_trip_score is not None:
                lines.append(
                    f"  - round-trip score (context only while a flag is set, not independent "
                    f"evidence): passed={r.round_trip_score.passed}, admissible={r.round_trip_score.admissible}"
                )
            if ROUND_TRIP_FLAG_UNVERIFIED_TERMINATION_ONLY in r.round_trip_flags:
                lines.append(
                    "    - `UNVERIFIED_TERMINATION_ONLY`: shipped without a verified round-trip "
                    "reconstruction (every compile attempt failed ONLY on Lean's termination "
                    "checker; any other failure mode still rotates the task instead)"
                )
            if ROUND_TRIP_FLAG_RECALLED_TARGET in r.round_trip_flags:
                lines.append(
                    "    - `RECALLED_TARGET`: the round-trip candidate body referenced the "
                    "task's real Mathlib name -- a clean pass above is not evidence the dossier "
                    "alone determines the object (the model may simply have recalled the real "
                    "definition's name from pretraining rather than derived it)"
                )
            if ROUND_TRIP_FLAG_UNVERIFIED_COMPILE in r.round_trip_flags:
                lines.append(
                    "    - **harder** (`ROUND_TRIP_UNVERIFIED_COMPILE`): dossier and fact suite "
                    "passed every upstream check, but every round-trip compile attempt failed -- "
                    "the reconstruction demands more Lean fluency than the round-trip model has. "
                    "Retained deliberately as corpus-hardness signal, NOT a defect"
                )
        if r.parser_rejected_facts:
            lines.append("- facts rejected at the parser layer (statement-format/raw-name, after the one retry):")
            for d in r.parser_rejected_facts:
                lines.append(f"  - index {d.index} (id {d.fragment.get('id')!r}): {d.reason_code} -- {d.detail}")
        if r.validation_dropped_facts:
            lines.append("- facts dropped by mechanical validation (no retry):")
            for d in r.validation_dropped_facts:
                lines.append(f"  - `{d.fact_id}`: {d.reason_code} -- {d.detail}")
        if r.task_errored_facts:
            lines.append("- facts flagged ERRORED (persistent infrastructure failure; task flagged, not silently dropped):")
            for d in r.task_errored_facts:
                lines.append(f"  - `{d.fact_id}`: {d.detail}")
        if r.convention_flags:
            lines.append("- dossier/domain consistency flags (§3.4(a), non-blocking):")
            for f in r.convention_flags:
                lines.append(f"  - point {f.point!r}: {f.detail}")
        if r.self_restatement_fact_ids:
            lines.append(
                "- self-restatement declarations (§4.2 -- discharge tier/cost for these facts "
                "must not be read as a candidate-side estimate):"
            )
            for fact_id in r.self_restatement_fact_ids:
                lines.append(f"  - `{fact_id}`")
        else:
            lines.append("- self-restatement declarations: none")
        if r.outcome == "ROTATED":
            lines.append("- stage-by-stage record (full where-it-died reconstruction):")
            for sr in r.stage_records:
                lines.append(f"  - `{sr.stage}`: {sr.status} -- {sr.detail} (calls so far: {sr.calls_made})")
        lines.append("")
    return "\n".join(lines)


def _write_batch_review(results: list[TaskResult], batch_review_dir: Path) -> Path:
    batch_review_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    path = batch_review_dir / f"batch_review_{timestamp}.md"
    path.write_text(render_batch_review(results), encoding="utf-8")
    return path
