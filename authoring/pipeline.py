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
2. **Round-trip repair carries no failure feedback into the retry** (unlike the dossier's
   repair, which does) -- matching the contract's own wording difference: row 6 says "with the
   failure shown," row 7 (round-trip) does not. The round-trip repair is a second, independent,
   equally-blind attempt.
3. **`self_restatement` (contract §4.2) is collected and reported in the batch review, not
   projected into a shipped `discharge.self_cited`.** Since `discharge` is always `null` (point
   1), there is currently nowhere in a shipped task.json for it to land; see
   `authoring.facts.ProposedFact.self_restatement`'s own docstring.

No station's public interface was broken to build this driver -- `authoring.parse.parse_facts`
and `authoring.orchestrate.run_fact_proposal_call` both gained new OPTIONAL keyword parameters
(`task_symbol`/`forbidden_name`), backward compatible with every existing caller. One adaptation
was made to a non-code artifact: `authoring/prompts/dossier.txt` specifies a parseable
Worked-Examples convention (a `Claim: ...` bullet + optional fenced command) -- without it,
`authoring.consistency` check (b) had nothing reliable to extract.
"""

import json
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable

from lean_interact import AutoLeanServer, Command

from authoring import config as authoring_cfg
from authoring.consistency import ConsistencyCheckResult, ConventionMatchResult, check_dossier_consistency
from authoring.emit import emit_task
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
from harness.scoring import splice_candidate
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


# === Internal helpers ============================================================================


def _render_classification(c: Classification) -> str:
    return f"regimes={c.regimes}, difficulty={c.difficulty}, rationale={c.rationale!r}"


def _summarize_consistency_failure(result: ConsistencyCheckResult) -> str:
    parts = []
    if not result.signature_substring_ok:
        parts.append(f"signature check: {result.signature_detail}")
    if not result.real_name_leak_ok:
        parts.append(result.real_name_leak_detail)
    for c in result.worked_example_checks:
        if c.kind in ("EXECUTION_FAILED", "MALFORMED_NO_WORKED_EXAMPLES"):
            parts.append(f"worked example ({c.kind}) {c.claim!r}: {c.detail}")
    return "; ".join(parts) if parts else "consistency check failed for an unspecified reason"


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


def _author_task_inner(definition_name: str, config: PipelineConfig, budget: CallBudget, log_start_line: int) -> TaskResult:
    stage_records: list[StageRecord] = []
    run_id = f"{definition_name}-{uuid.uuid4().hex[:8]}"

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
        )

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
    truth_cmd = signature_obj.splice(definition_input.name)
    truth_splice = splice_candidate(config.server, config.base_env, truth_cmd, timeout=config.check_timeout)
    if truth_splice.status is not CheckStatus.PASSED:
        return _rotate("truth_splice", truth_splice.detail or "truth-side splice under the task symbol failed")
    truth_env = truth_splice.env
    stage_records.append(StageRecord("truth_splice", "ok", calls_made=budget.calls_made))

    # --- Call 1: classification --------------------------------------------------------------
    try:
        classification = run_classification_call(
            config.client, config.authoring_model_id,
            pinned_signature=pinned_signature, definition_source=definition_input.definition_source,
            docstring=definition_input.docstring, mention_sidecar_excerpt=mention_excerpt, budget=budget,
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
                classification=classification_input, budget=budget,
            )
        except (AuthoringCallFailed, CallBudgetExceeded, BedrockClientError) as e:
            holder["last_failure_kind"] = "call"
            holder["failure_note"] = None
            return False, f"{type(e).__name__}: {e}"

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

    # --- Call 3: fact proposal ----------------------------------------------------------------
    try:
        proposal = run_fact_proposal_call(
            config.client, config.authoring_model_id,
            pinned_signature=pinned_signature, dossier_md=dossier_payload.dossier_md,
            mention_sidecar_excerpt=mention_excerpt, classification=classification_text, budget=budget,
            task_symbol=task_symbol, forbidden_name=definition_input.name,
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

    # mechanism alone determines validation_status -- see module docstring, decision 1.
    fact_list: list[Fact] = [
        f.to_fact(
            validation_status="CERTIFIED" if f.mechanism == "decide" else "PROVISIONALLY_VALIDATED",
            provenance=FactProvenance(
                validation_run_id=run_id,
                note=f"authored by {config.authoring_model_id}, validated against ground truth",
            ),
        )
        for f in adjudication.accepted
    ]

    # --- Call 4: blind round-trip generation + first-cut scoring, one repair cycle -----------
    # Splices under `task_symbol` into the SAME untouched `base_env` the truth splice used --
    # an independent splice, not chained onto `truth_env`, so it cannot collide with the truth
    # alias declared there.
    rt_holder: dict = {}

    def round_trip_attempt():
        try:
            body = run_round_trip_generation_call(
                config.client, config.authoring_model_id,
                pinned_signature=pinned_signature, dossier_md=dossier_payload.dossier_md, budget=budget,
            )
        except (CallBudgetExceeded, BedrockClientError) as e:
            rt_holder["last_failure_kind"] = "call"
            return False, f"{type(e).__name__}: {e}"

        score = score_round_trip_first_cut(
            config.server, config.base_env, signature_obj, body, fact_list, check_timeout=config.check_timeout,
        )
        rt_holder["score"] = score
        rt_holder["body"] = body
        if score.passed:
            return True, "ok"
        rt_holder["last_failure_kind"] = "scoring"
        detail = (
            f"admissible={score.admissible} ({score.admissibility_detail}); "
            f"failing decide facts: {score.failing_decide_fact_ids}; "
            f"failing global facts: {score.failing_global_fact_ids}"
        )
        return False, detail

    def round_trip_repair():
        return None  # no failure feedback carried into the retry -- see module docstring, decision 2

    rt_outcome = with_one_repair_cycle(round_trip_attempt, round_trip_repair)
    if not rt_outcome.passed:
        stage = "round_trip_generation" if rt_holder.get("last_failure_kind") == "call" else "round_trip_scoring"
        return _rotate(
            stage, rt_outcome.detail,
            parser_rejected=proposal.dropped, validation_dropped=adjudication.dropped,
            task_errored=adjudication.task_errored, convention_flags=consistency_result.flags,
            self_restatement=self_restatement_ids,
        )
    stage_records.append(StageRecord("round_trip_generation", "ok", calls_made=budget.calls_made))
    stage_records.append(StageRecord("round_trip_scoring", "ok", calls_made=budget.calls_made))
    round_trip_score: RoundTripScore = rt_holder["score"]

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
