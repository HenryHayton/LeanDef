"""The rotation cleanup runner (2026-07-30): repairs `agent_fixable` entries from
`authoring/output/pending_safety_updates.json` (`authoring.rotation_queue`) by revising the
dossier and re-running the pipeline downstream of it, bounded by a per-name attempt cap and a
per-run dollar budget.

**Why the dossier specifically**: every `AGENT_FIXABLE` category (dossier-leak, signature-
substring, round-trip compile exhaustion) traces back to the same upstream artifact -- the
dossier is what the model wrote the leaking/mismatched Signature section from, and it's also
the ONLY thing the round-trip call ever sees, so a round-trip compile exhaustion is at least as
plausibly a dossier-clarity problem as a round-trip-model problem. One repair mechanism, not
one per category.

**Guardrails (each is load-bearing -- see the session report for why each exists):**

1. **The checks are never weakened.** `check_dossier_consistency` and the full downstream
   pipeline (`authoring.pipeline._author_from_dossier`) run UNCHANGED -- this module imports
   them, never reimplements or loosens them. A revised dossier either passes the real check or
   it doesn't.
2. **The information barrier holds.** `_author_from_dossier`'s own round-trip stage is the same
   fresh-context-only call every normal run uses; nothing here special-cases a cleanup re-run.
3. **Repair feedback is compile-errors-and-mechanical-check-failures ONLY.** `_feedback_text`
   below is the only place repair feedback is constructed; it reads `StageRecord.detail` for
   `dossier_consistency` (a mechanical check summary) or `round_trip_scoring`/
   `round_trip_generation` specifically when the detail text is a COMPILE failure (starts with
   `"exhausted"` or is a single compile-error string) -- never a `mechanical_validation`
   rotation (fact-validation outcomes) and never a round-trip FACT-suite failure (`"compiled
   but failed the fact suite"` -- the candidate's own fact score). Anything else encountered
   mid-loop is not feedback-eligible and ends the loop immediately (`escalate_to_human`), rather
   than looping blind or leaking forbidden information.
4. **The repair call never sees a round-trip candidate body.** Only reachable via
   `_feedback_text`'s own restriction above -- `RoundTripScore.splice.raw_response.pp` (the
   candidate's literal body) is never read by this module at all.
5. **`not_agent_fixable` entries are never attempted.** `run_cleanup` filters to
   `category == AGENT_FIXABLE` before doing anything.

**Infra-failure exemption (2026-07-31, `_run_dossier_call_with_infra_retry`).** A dossier call
that fails on response-shape/infra grounds (malformed JSON, a null-field parse error -- Bedrock
variance, not a real check failure) gets one extra retry that does NOT consume an attempt slot
out of `MAX_REPAIR_ATTEMPTS`; only two CONSECUTIVE infra failures escalate (labeled `"infra"` in
the repair log), same as any lone infra failure always did before this existed. Distinguishing
this from a genuine mechanical-check failure matters because, before the fix, an infra blip on
attempt 1 of 5 silently threw away the other 4 attempts' worth of real repair budget.
"""

import time
import uuid
from dataclasses import dataclass, field, replace
from pathlib import Path

from authoring import config as authoring_cfg
from authoring.consistency import check_dossier_consistency, inject_pinned_signature
from authoring.mentions import render_mention_excerpt
from authoring.orchestrate import AuthoringCallFailed, CallBudget, run_classification_call, run_dossier_call
from authoring.parse import DossierPayload
from authoring.pipeline import (
    PipelineConfig,
    StageRecord,
    TaskResult,
    _author_from_dossier,
    _count_log_lines,
    _render_classification,
    _summarize_consistency_failure,
    _token_totals_since,
)
from authoring.rotation_queue import (
    AGENT_FIXABLE,
    STATUS_ESCALATE_TO_HUMAN,
    STATUS_PENDING,
    STATUS_REPAIRED_AND_SHIPPED,
    DEFAULT_QUEUE_PATH,
    load_queue,
    save_queue,
)
from authoring.task_symbol import task_symbol_for
from bedrock.client import BedrockClientError
from harness.results import CheckStatus
from harness.scoring import splice_candidate
from harness.signature import PinnedSignature

MAX_REPAIR_ATTEMPTS = 5
DEFAULT_RUN_BUDGET_USD = 4.0

# Rotation stages/details eligible as repair feedback -- see module docstring guardrail 3.
_COMPILE_FAILURE_PREFIXES = ("exhausted",)  # round_trip_scoring's compile-exhaustion detail

# Infra-classified dossier-call failures (2026-07-31): malformed JSON, null-field parse errors
# -- Bedrock response-shape variance, not a real mechanical-check failure -- `AuthoringCallFailed`
# (contract §6 rows 1-2, raised only after `run_dossier_call`'s own internal one retry already
# failed) and `BedrockClientError` (transport-level). Before this existed, either one propagated
# straight out of `repair_one`'s attempt loop to the outer catch-all and escalated the WHOLE
# name immediately -- burning every remaining attempt in `MAX_REPAIR_ATTEMPTS` on what was often
# a one-off Bedrock hiccup, not a real defect in the dossier.
_INFRA_FAILURE_EXCEPTIONS = (AuthoringCallFailed, BedrockClientError)


class _InfraFailure(Exception):
    """Two CONSECUTIVE infra-classified dossier-call failures within one repair attempt (see
    `_run_dossier_call_with_infra_retry`) -- as opposed to a lone one, which is now retried
    transparently and does not reach here at all."""


def _feedback_text(result: TaskResult) -> str | None:
    """`None` means "not feedback-eligible" -- the caller must stop, not loop blind."""
    if result.outcome != "ROTATED":
        return None
    stage = result.rotated_at_stage
    detail = result.stage_records[-1].detail if result.stage_records else ""
    if stage == "dossier_consistency":
        return detail
    if stage in ("round_trip_generation", "round_trip_scoring") and detail.strip().startswith(_COMPILE_FAILURE_PREFIXES):
        return detail
    return None


def _task_cost(input_tokens: int, output_tokens: int) -> float:
    from bedrock import config as bedrock_cfg

    return input_tokens / 1000 * bedrock_cfg.PRICE_PER_1K_INPUT_TOKENS_USD + output_tokens / 1000 * bedrock_cfg.PRICE_PER_1K_OUTPUT_TOKENS_USD


def _run_dossier_call_with_infra_retry(client, model_id, *, pinned_signature, definition_source,
                                        docstring, mention_sidecar_excerpt, classification,
                                        decidability, budget) -> DossierPayload:
    """One EXTRA retry, on top of `run_dossier_call`'s own internal one (contract §6 rows 1-2),
    reserved for a dossier call that fails on response-shape/infra grounds -- see
    `_INFRA_FAILURE_EXCEPTIONS`'s own note. This retry does NOT consume a `repair_one` attempt
    slot (`MAX_REPAIR_ATTEMPTS`) -- it happens entirely within one iteration of that loop.
    Raises `_InfraFailure` only if BOTH this call and its retry fail on infra grounds; any other
    exception (a real `CallBudgetExceeded`, for instance) propagates unchanged, since that is
    never an infra blip worth retrying."""
    call_kwargs = dict(
        pinned_signature=pinned_signature, definition_source=definition_source, docstring=docstring,
        mention_sidecar_excerpt=mention_sidecar_excerpt, classification=classification,
        decidability=decidability, budget=budget,
    )
    try:
        return run_dossier_call(client, model_id, **call_kwargs)
    except _INFRA_FAILURE_EXCEPTIONS as e1:
        try:
            return run_dossier_call(client, model_id, **call_kwargs)
        except _INFRA_FAILURE_EXCEPTIONS as e2:
            raise _InfraFailure(
                f"two consecutive infra failures: {type(e1).__name__}: {e1}; then {type(e2).__name__}: {e2}"
            ) from e2


@dataclass
class CleanupResult:
    name: str
    status: str
    attempts_used: int
    spend_usd: float
    shipped_task_dir: str | None = None


def repair_one(entry: dict, config: PipelineConfig) -> CleanupResult:
    """Repair a single `AGENT_FIXABLE` queue entry in place (mutates `entry["repair_log"]`/
    `entry["status"]`) and returns a summary. Never raises: any unexpected failure becomes an
    `escalate_to_human` entry with the exception recorded, same "one bad name must not sink the
    run" contract every other station in this package follows."""
    name = entry["name"]
    log_start_line = _count_log_lines(config.client.log_path)
    try:
        definition_input = config.resolve_definition(name)
        task_symbol = task_symbol_for(definition_input.name)
        pinned_signature = f"{task_symbol} : {definition_input.signature_dict['type']}"
        signature_obj = PinnedSignature(name=task_symbol, type_sig=definition_input.signature_dict["type"])
        mention_excerpt = render_mention_excerpt(definition_input.mention_records, cap=config.mention_cap)

        truth_cmd = signature_obj.splice(definition_input.name)
        truth_splice = splice_candidate(config.server, config.base_env, truth_cmd, timeout=config.check_timeout)
        if truth_splice.status is not CheckStatus.PASSED:
            entry["repair_log"].append({
                "attempt_n": 0, "what_was_changed": "n/a (re-splicing the truth side to set up the repair)",
                "check_result": "fail", "error_if_any": truth_splice.detail or "truth_splice failed during cleanup setup",
            })
            entry["status"] = STATUS_ESCALATE_TO_HUMAN
            tokens = _token_totals_since(config.client.log_path, log_start_line)
            return CleanupResult(name, STATUS_ESCALATE_TO_HUMAN, 0, _task_cost(tokens["input_tokens"], tokens["output_tokens"]))
        truth_env = truth_splice.env

        budget = CallBudget(max_calls=authoring_cfg.AUTHORING_MAX_CALLS_PER_TASK * MAX_REPAIR_ATTEMPTS)
        classification = run_classification_call(
            config.client, config.authoring_model_id,
            pinned_signature=pinned_signature, definition_source=definition_input.definition_source,
            docstring=definition_input.docstring, mention_sidecar_excerpt=mention_excerpt,
            return_shape=definition_input.return_shape, budget=budget,
        )
        classification_text = _render_classification(classification)

        feedback = entry["rotation_reason"]
        for attempt_n in range(1, MAX_REPAIR_ATTEMPTS + 1):
            classification_input = (
                f"{classification_text}\n\nNOTE: an earlier authoring attempt for this exact task "
                f"failed a mechanical check and must be corrected this time: {feedback}"
            )
            try:
                payload = _run_dossier_call_with_infra_retry(
                    config.client, config.flagship_model_id,
                    pinned_signature=pinned_signature, definition_source=definition_input.definition_source,
                    docstring=definition_input.docstring, mention_sidecar_excerpt=mention_excerpt,
                    classification=classification_input, decidability=definition_input.decidability,
                    budget=budget,
                )
            except _InfraFailure as e:
                entry["repair_log"].append({
                    "attempt_n": attempt_n, "what_was_changed": "n/a (infra retry exhausted)",
                    "check_result": "fail (infra)", "error_if_any": str(e),
                })
                entry["status"] = STATUS_ESCALATE_TO_HUMAN
                tokens = _token_totals_since(config.client.log_path, log_start_line)
                return CleanupResult(name, STATUS_ESCALATE_TO_HUMAN, attempt_n, _task_cost(tokens["input_tokens"], tokens["output_tokens"]))
            # Same mechanical injection pipeline.py's own dossier_attempt performs -- see
            # authoring.consistency's note; the repair loop generates a fresh dossier per
            # attempt, so this must run every time, not just once per name.
            payload = replace(payload, dossier_md=inject_pinned_signature(payload.dossier_md, pinned_signature))
            consistency = check_dossier_consistency(
                config.server, truth_env, pinned_signature, payload.dossier_md, payload.domain,
                timeout=config.check_timeout, forbidden_name=definition_input.name,
            )
            if not consistency.passed:
                detail = _summarize_consistency_failure(consistency)
                entry["repair_log"].append({
                    "attempt_n": attempt_n, "what_was_changed": "revised dossier",
                    "check_result": "fail (dossier_consistency)", "error_if_any": detail,
                })
                feedback = detail
                continue

            run_id = f"{name}-cleanup{attempt_n}-{uuid.uuid4().hex[:8]}"
            stage_records = [StageRecord("cleanup_dossier_revision", "ok", detail=f"attempt {attempt_n}")]
            result = _author_from_dossier(
                name, config, budget, log_start_line, stage_records, run_id,
                definition_input, task_symbol, pinned_signature, signature_obj, truth_env,
                mention_excerpt, classification_text, payload, consistency,
            )

            if result.outcome == "SHIPPED":
                entry["repair_log"].append({
                    "attempt_n": attempt_n, "what_was_changed": "revised dossier",
                    "check_result": "pass -- shipped", "error_if_any": None,
                })
                entry["status"] = STATUS_REPAIRED_AND_SHIPPED
                tokens = _token_totals_since(config.client.log_path, log_start_line)
                return CleanupResult(
                    name, STATUS_REPAIRED_AND_SHIPPED, attempt_n,
                    _task_cost(tokens["input_tokens"], tokens["output_tokens"]), str(result.task_dir),
                )

            next_feedback = _feedback_text(result)
            downstream_detail = result.stage_records[-1].detail if result.stage_records else ""
            if next_feedback is None:
                entry["repair_log"].append({
                    "attempt_n": attempt_n, "what_was_changed": "revised dossier",
                    "check_result": f"fail ({result.rotated_at_stage}, not feedback-eligible -- stopping, see guardrails)",
                    "error_if_any": downstream_detail,
                })
                entry["status"] = STATUS_ESCALATE_TO_HUMAN
                tokens = _token_totals_since(config.client.log_path, log_start_line)
                return CleanupResult(name, STATUS_ESCALATE_TO_HUMAN, attempt_n, _task_cost(tokens["input_tokens"], tokens["output_tokens"]))

            entry["repair_log"].append({
                "attempt_n": attempt_n, "what_was_changed": "revised dossier",
                "check_result": f"fail ({result.rotated_at_stage})", "error_if_any": downstream_detail,
            })
            feedback = next_feedback

        entry["status"] = STATUS_ESCALATE_TO_HUMAN
        tokens = _token_totals_since(config.client.log_path, log_start_line)
        return CleanupResult(name, STATUS_ESCALATE_TO_HUMAN, MAX_REPAIR_ATTEMPTS, _task_cost(tokens["input_tokens"], tokens["output_tokens"]))

    except Exception as e:  # noqa: BLE001 -- one bad name must not sink the cleanup run
        entry["repair_log"].append({
            "attempt_n": len(entry["repair_log"]) + 1, "what_was_changed": "n/a",
            "check_result": "fail (unexpected error)", "error_if_any": f"{type(e).__name__}: {e}",
        })
        entry["status"] = STATUS_ESCALATE_TO_HUMAN
        tokens = _token_totals_since(config.client.log_path, log_start_line)
        return CleanupResult(name, STATUS_ESCALATE_TO_HUMAN, len(entry["repair_log"]), _task_cost(tokens["input_tokens"], tokens["output_tokens"]))


@dataclass
class CleanupRunResult:
    results: list[CleanupResult] = field(default_factory=list)
    total_spend_usd: float = 0.0
    stopped_reason: str | None = None  # None if every eligible entry was attempted


def run_cleanup(
    config: PipelineConfig, *,
    queue_path: Path = DEFAULT_QUEUE_PATH,
    run_budget_usd: float = DEFAULT_RUN_BUDGET_USD,
    credentials_check=None,
) -> CleanupRunResult:
    """Iterate every `AGENT_FIXABLE` + `pending` entry in `queue_path`, repairing each in turn
    (`repair_one`), persisting the queue file after every single name (not batched -- a crash
    mid-run must not lose already-recorded repair_log entries). Stops before spending past
    `run_budget_usd` (checked before each name, using the running total so far) or, if
    `credentials_check` is supplied, before starting a name once credentials are no longer
    live -- matching `authoring.batch.run_batch`'s own per-item credential-check convention."""
    entries = load_queue(queue_path)
    eligible_idxs = [i for i, e in enumerate(entries) if e["category"] == AGENT_FIXABLE and e["status"] == STATUS_PENDING]

    run_result = CleanupRunResult()
    for idx in eligible_idxs:
        if credentials_check is not None and not credentials_check():
            run_result.stopped_reason = f"credentials expired before {entries[idx]['name']}"
            break
        if run_result.total_spend_usd >= run_budget_usd:
            run_result.stopped_reason = f"budget ceiling (${run_budget_usd}) reached before {entries[idx]['name']}"
            break

        result = repair_one(entries[idx], config)
        run_result.results.append(result)
        run_result.total_spend_usd += result.spend_usd
        save_queue(entries, queue_path)

    return run_result
