"""Orchestration (contract §8 item 3): wires the prompt templates -> `BedrockClient.send` ->
`authoring.parse` -> `authoring.validate`, implementing the §6 error-handling table exactly.

Each row of that table is a genuinely different retry shape, so this module does not have one
generic "retry loop" -- it has one function per row, composed by the per-call wrappers below:

- Rows 1-2 (JSON parse failure / schema-shape failure): `_call_llm_json` -- one retry with the
  parse error appended to the prompt, terminal (raises `AuthoringCallFailed`) on a second
  failure. Shared by the classification, dossier, and fact-proposal calls, since all three
  produce a JSON envelope `authoring.parse` can fail to make sense of the same two ways.
- Row 3 (a per-fact statement-format rejection): `_retry_rejected_facts` -- one retry, but
  batched into a SINGLE follow-up call covering every rejected fact from the original response
  at once, not one call per fact. This is a deliberate reading of "one retry ... then the fact
  is dropped" where the contract does not itself specify call-batching granularity; batching
  is cheaper and the row's own "then the fact is dropped" language already anticipates a
  per-fact outcome that a batched call still produces. Noted as a contract-silent choice in
  the implementation report this module's task produced.
- Rows 4-5 (a fact fails ground truth / errors): `adjudicate_proposed_facts` -- no LLM
  involvement at all, since both rows are about `authoring.validate`'s mechanical REPL-backed
  verdict, not the model's output shape. FALSE_OF_GROUND_TRUTH-class rejections get no retry
  (row 4); ERRORED gets exactly one re-run of validation itself, not a re-prompt of the model
  ("not charged to the model") -- persistent ERRORED flags the whole task rather than dropping
  just that fact (row 5).
- Rows 6-7 (a dossier example fails / round-trip fails): `with_one_repair_cycle` -- a generic
  "try, repair once, try again, then terminal" state machine both rows share the shape of. Row
  6 cannot be wired to anything real this session: it requires the §3.4 dossier/domain
  consistency check (executing worked examples, matching conventions prose), which is not
  listed anywhere in contract §8's implementation scope and was not built here -- see the
  implementation report's "contract gaps found" section. Row 7 (round-trip) IS wired, via
  `authoring.roundtrip.score_round_trip_first_cut` as the caller-supplied `attempt_fn`.

`CallBudget` is the "per-task call budget as configuration" contract §6 asks for -- checked
BEFORE every `BedrockClient.send()` call this module makes (fail before spending, not after).
"""

import json
import re
from dataclasses import dataclass, field

from bedrock.client import BedrockClient
from authoring import config as authoring_cfg
from authoring.facts import ProposedFact
from authoring.parse import (
    Classification,
    DossierPayload,
    FactParseRejection,
    ParseError,
    parse_classification,
    parse_dossier,
    parse_facts,
    validate_classification_against_shape,
)
from authoring.prompt_loader import load_prompt_template
from authoring.validate import DomainSpec, ReasonCode, ValidationOutcome, Verdict, validate_fact

# Real models routinely wrap JSON in a ```json (or bare ```) fence despite an explicit
# instruction not to -- observed directly in the 2026-07-28 slice run (2 of 4 real dossier
# responses fenced, 2 didn't, no other change) and already the documented reason
# `_strip_markdown_fence` below exists for Call 4's Lean-text response. Stripped defensively
# before every JSON parse attempt, the same way -- fighting the model into never fencing has a
# ~50% real-world failure rate per that observation; tolerating it costs nothing.
_JSON_FENCE_RE = re.compile(r"^```(?:json)?\s*\n(.*?)\n```\s*$", re.DOTALL)


def _strip_json_fence(text: str) -> str:
    text = text.strip()
    m = _JSON_FENCE_RE.match(text)
    return m.group(1).strip() if m else text

# Per-task LLM call budget (contract §6: "a task consumes at most a bounded number of LLM
# calls (configuration), and a task that exhausts its call budget rotates out"). A dial, not a
# commitment -- same status as every other threshold in this codebase (e.g.
# `bedrock.config.MAX_ATTEMPTS`, `miner.config`'s gate thresholds).
DEFAULT_MAX_CALLS_PER_TASK = 20


class AuthoringCallFailed(Exception):
    """A contract call (§6 rows 1-2) exhausted its one retry and is terminal for this call."""


class CallBudgetExceeded(Exception):
    """A task's LLM call budget (contract §6) would be exceeded by the next call."""


@dataclass
class CallBudget:
    max_calls: int = DEFAULT_MAX_CALLS_PER_TASK
    calls_made: int = 0

    def charge(self, n: int = 1) -> None:
        if self.calls_made + n > self.max_calls:
            raise CallBudgetExceeded(
                f"would exceed budget: {self.calls_made} call(s) made, {n} more requested, max {self.max_calls}"
            )
        self.calls_made += n


def _charge(budget: CallBudget | None) -> None:
    if budget is not None:
        budget.charge()


def _parse_llm_json_response(response, parse_fn, *, max_tokens: int):
    """Shared by the initial attempt and the one retry in `_call_llm_json`/
    `_retry_rejected_facts`: a response that hit its `max_tokens` ceiling is treated as
    malformed -- structurally a `ParseError`, feeding the SAME one-retry path everything else
    in rows 1-2 uses -- never handed to `parse_fn` as if it were complete. Confirmed necessary:
    the real 2026-07-28 slice run's dossier responses truncated mid-JSON-string at exactly the
    token ceiling every time, and `json.loads` failing on the resulting garbage was incidental,
    not something to rely on (a truncation could in principle land on a syntactically-valid-but-
    semantically-incomplete boundary). Fences are stripped before parsing either way -- see
    `_strip_json_fence`'s own docstring."""
    if response.stop_reason == "max_tokens":
        raise ParseError(
            f"response was truncated at the {max_tokens}-token limit (stop_reason=max_tokens) "
            "before it completed -- a partial response is never parsed as if it were whole"
        )
    return parse_fn(_strip_json_fence(response.text))


def _call_llm_json(client, system, user_message, *, model_id, parse_fn, budget=None, max_tokens: int = 1024):
    """Rows 1-2: send once; on `ParseError`, retry once with the error appended; raise
    `AuthoringCallFailed` if the retry also fails to parse. Returns whatever `parse_fn`
    returns."""
    _charge(budget)
    response = client.send(system=system, user_message=user_message, model_id=model_id, max_tokens=max_tokens)
    try:
        return _parse_llm_json_response(response, parse_fn, max_tokens=max_tokens)
    except ParseError as e:
        retry_user = (
            f"{user_message}\n\n"
            f"Your previous response could not be used: {e.detail}\n"
            "Respond again with corrected strict JSON only -- no markdown fences, no prose "
            "outside the JSON."
        )
        _charge(budget)
        response2 = client.send(system=system, user_message=retry_user, model_id=model_id, max_tokens=max_tokens)
        try:
            return _parse_llm_json_response(response2, parse_fn, max_tokens=max_tokens)
        except ParseError as e2:
            raise AuthoringCallFailed(f"terminal after one retry: {e2.detail}") from e2


# === Call 1 -- Regime classification ===========================================================


def run_classification_call(
    client: BedrockClient,
    model_id: str,
    *,
    pinned_signature: str,
    definition_source: str,
    docstring: str,
    mention_sidecar_excerpt: str,
    return_shape: str,
    budget: CallBudget | None = None,
    max_tokens: int | None = None,
) -> Classification:
    """`return_shape` ("value"|"prop"|"bundled", `miner.shape.classify_return_shape`'s own
    vocabulary) is mechanical truth read off the pinned type, passed to the model as a stated
    fact (§2's "Rule:" line references it directly) rather than left for the model to infer
    from the pinned signature's own text. `parse_fn` wraps `parse_classification` with
    `validate_classification_against_shape` so a response that contradicts `return_shape` (e.g.
    'casework' regime on a Prop) is a `ParseError` -- feeding the same one-retry-then-terminal
    machinery as a malformed-JSON response, not a silent pass-through."""
    template = load_prompt_template("classification")
    system, user = template.render(
        pinned_signature=pinned_signature,
        definition_source=definition_source,
        docstring=docstring,
        mention_sidecar_excerpt=mention_sidecar_excerpt,
        return_shape=return_shape,
    )
    max_tokens = max_tokens if max_tokens is not None else authoring_cfg.AUTHORING_MAX_TOKENS["classification"]

    def parse_fn(text: str) -> Classification:
        return validate_classification_against_shape(parse_classification(text), return_shape)

    return _call_llm_json(client, system, user, model_id=model_id, parse_fn=parse_fn, budget=budget, max_tokens=max_tokens)


# === Call 2 -- Dossier generation ==============================================================


def run_dossier_call(
    client: BedrockClient,
    model_id: str,
    *,
    pinned_signature: str,
    definition_source: str,
    docstring: str,
    mention_sidecar_excerpt: str,
    classification: str,
    decidability: str | None = None,
    budget: CallBudget | None = None,
    max_tokens: int | None = None,
) -> DossierPayload:
    """`decidability` (2026-07-30, `authoring.preflight.probe_decidability`'s vocabulary --
    `None` for a non-Prop task, rendered as `"not_applicable"`) governs whether the dossier's
    Prop-valued worked examples may carry an executable command; see `dossier.txt`'s own
    Worked-examples instruction."""
    template = load_prompt_template("dossier")
    system, user = template.render(
        pinned_signature=pinned_signature,
        definition_source=definition_source,
        docstring=docstring,
        mention_sidecar_excerpt=mention_sidecar_excerpt,
        classification=classification,
        decidability=decidability if decidability is not None else "not_applicable",
    )
    max_tokens = max_tokens if max_tokens is not None else authoring_cfg.AUTHORING_MAX_TOKENS["dossier"]
    return _call_llm_json(client, system, user, model_id=model_id, parse_fn=parse_dossier, budget=budget, max_tokens=max_tokens)


# === Call 3 -- Fact proposal ====================================================================


@dataclass(frozen=True)
class FactProposalResult:
    facts: list[ProposedFact]
    dropped: list[FactParseRejection] = field(default_factory=list)  # still-bad after the one retry


def _retry_rejected_facts(
    client: BedrockClient,
    model_id: str,
    system: str,
    rejections: list[FactParseRejection],
    *,
    budget: CallBudget | None = None,
    parse_fn=parse_facts,
    max_tokens: int | None = None,
) -> tuple[list[ProposedFact], list[FactParseRejection]]:
    """Row 3's one retry, batched (see module docstring). Returns `(fixed, still_bad)`.
    `parse_fn` defaults to bare `parse_facts`; `run_fact_proposal_call` passes a closure
    carrying `task_symbol`/`forbidden_name` (contract §4.4) so a "fixed" fact is held to the
    same raw-name check as the original batch."""
    max_tokens = max_tokens if max_tokens is not None else authoring_cfg.AUTHORING_MAX_TOKENS["fact_proposal"]
    listing = "\n\n".join(
        f"Fact at index {r.index} (id {r.fragment.get('id')!r}) was rejected: {r.detail}\n"
        f"Original fact JSON: {json.dumps(r.fragment)}"
        for r in rejections
    )
    retry_user = (
        "The following facts from your previous response violated the statement-format rule "
        "for their mechanism and could not be used. Respond with a corrected JSON array "
        "containing ONLY replacements for these facts (same ids, same overall shape as "
        "before).\n\n" + listing
    )
    _charge(budget)
    response = client.send(system=system, user_message=retry_user, model_id=model_id, max_tokens=max_tokens)
    try:
        fixed, still_bad = _parse_llm_json_response(response, parse_fn, max_tokens=max_tokens)
    except ParseError:
        # The whole retry response was itself unusable (malformed JSON, wrong shape, or
        # truncated at the token ceiling). This WAS the one retry (row 3), so every
        # originally-rejected fact is now terminal -- dropped, not raised.
        return [], rejections
    return fixed, still_bad


def run_fact_proposal_call(
    client: BedrockClient,
    model_id: str,
    *,
    pinned_signature: str,
    dossier_md: str,
    mention_sidecar_excerpt: str,
    classification: str,
    budget: CallBudget | None = None,
    task_symbol: str | None = None,
    forbidden_name: str | None = None,
    domain_constraint: str | None = None,
    decidability: str | None = None,
    domain_variables: list[str] | None = None,
    max_tokens: int | None = None,
) -> FactProposalResult:
    """`task_symbol`/`forbidden_name` (contract §4.4) thread through to `authoring.parse.parse_facts`
    on both the initial parse and the row-3 per-fact retry, so a raw-Mathlib-name leak is caught
    (and the offending fact dropped, not silently shipped) the same way on either path.
    `domain_constraint` (2026-07-28) threads through the same way, gating the membership
    `domain_inputs` pre-check `parse_facts` mirrors from `harness.task_schema`. `decidability`
    (2026-07-30, `authoring.preflight.probe_decidability`'s vocabulary -- `None` for a non-Prop
    task) is rendered into the prompt AND threads to `parse_facts`, so the model is told which
    mechanism to use for this Prop up front, and a fact that ignores that guidance is still
    caught mechanically rather than trusted. `domain_variables` (2026-07-30, schema v1.1.3, the
    dossier's `domain.variables`) threads to `parse_facts` the same way -- rule 5's parse-time
    mirror, gating `domain_inputs` keys to the declared set."""
    template = load_prompt_template("fact_proposal")
    system, user = template.render(
        pinned_signature=pinned_signature,
        dossier_md=dossier_md,
        mention_sidecar_excerpt=mention_sidecar_excerpt,
        classification=classification,
        decidability=decidability if decidability is not None else "not_applicable",
    )
    max_tokens = max_tokens if max_tokens is not None else authoring_cfg.AUTHORING_MAX_TOKENS["fact_proposal"]

    def _parse(text: str):
        return parse_facts(
            text, task_symbol=task_symbol, forbidden_name=forbidden_name,
            domain_constraint=domain_constraint, decidability=decidability,
            domain_variables=domain_variables,
        )

    facts, rejections = _call_llm_json(client, system, user, model_id=model_id, parse_fn=_parse, budget=budget, max_tokens=max_tokens)
    if not rejections:
        return FactProposalResult(facts=facts, dropped=[])

    fixed_facts, still_dropped = _retry_rejected_facts(
        client, model_id, system, rejections, budget=budget, parse_fn=_parse, max_tokens=max_tokens
    )
    return FactProposalResult(facts=facts + fixed_facts, dropped=still_dropped)


# === Rows 4-5 -- mechanical adjudication (no LLM involvement) ==================================


@dataclass(frozen=True)
class AdjudicationResult:
    accepted: list[ProposedFact]
    dropped: list[ValidationOutcome] = field(default_factory=list)  # no-retry drops (row 4 + siblings)
    task_errored: list[ValidationOutcome] = field(default_factory=list)  # ERRORED twice -- flags the task


def adjudicate_proposed_facts(
    server, env: int, facts: list[ProposedFact], domain: DomainSpec, pinned_name: str, *, timeout: float | None = None
) -> AdjudicationResult:
    """Runs `authoring.validate.validate_fact` over already-parsed facts and applies rows 4-5:
    a `FALSE_OF_GROUND_TRUTH`-class (or any other non-ERRORED) rejection is dropped with no
    retry (row 4 -- "this is signal about the model's mathematics"); an `ERRORED` result gets
    validation re-run exactly once ("not charged to the model" -- no LLM call happens here at
    all); if it errors again, the fact is NOT dropped -- it is reported via `task_errored` so
    the caller flags the whole task (row 5: "persistent -> task flagged, not dropped")."""
    accepted: list[ProposedFact] = []
    dropped: list[ValidationOutcome] = []
    task_errored: list[ValidationOutcome] = []
    for fact in facts:
        outcome = validate_fact(server, env, fact, domain, pinned_name, timeout=timeout)
        if outcome.reason_code == ReasonCode.ERRORED:
            outcome = validate_fact(server, env, fact, domain, pinned_name, timeout=timeout)
            if outcome.reason_code == ReasonCode.ERRORED:
                task_errored.append(outcome)
                continue
        if outcome.verdict in (Verdict.ACCEPTED, Verdict.PROVISIONALLY_VALIDATED):
            accepted.append(fact)
        else:
            dropped.append(outcome)
    return AdjudicationResult(accepted=accepted, dropped=dropped, task_errored=task_errored)


# === Call 4 -- Blind round-trip generation =====================================================

# Real models routinely wrap code in ```lean fences despite an explicit instruction not to
# (the same phenomenon `authoring.validate`'s adversarial-input tests document for proposed
# fact statements) -- stripped defensively rather than trusted away. Contract §5 does not
# specify Call 4's output format (unlike Calls 1-3, which have explicit "Output (JSON)"
# lines); this module treats it as raw text (the candidate body), not a JSON envelope, since a
# Lean definition body is code, not structured data -- principle 2's "strict JSON" rule reads
# as governing structured data output specifically. Noted as a contract-silent choice.
_LEAN_FENCE_RE = re.compile(r"^```(?:lean4?)?\s*\n(.*?)\n```\s*$", re.DOTALL)


def _strip_markdown_fence(text: str) -> str:
    text = text.strip()
    m = _LEAN_FENCE_RE.match(text)
    return m.group(1).strip() if m else text


def run_round_trip_generation_call(
    client: BedrockClient,
    model_id: str,
    *,
    pinned_signature: str,
    dossier_md: str,
    budget: CallBudget | None = None,
    max_tokens: int | None = None,
    previous_attempt: str | None = None,
    previous_error: str | None = None,
) -> str:
    """Contract §5: a fresh context, ONLY the dossier and pinned signature -- the caller is
    responsible for that information hygiene (this function takes exactly those two inputs and
    nothing else, so it cannot leak the definition source, fact suite, or mention excerpt even
    by accident).

    `previous_attempt`/`previous_error` (decided 2026-07-28, replacing the prior blind-retry
    design): when BOTH are given, the user message gets a feedback block appended -- the ONLY
    thing added is this call's OWN prior attempt and the Lean error it produced, never anything
    from outside the round-trip context (no definition source, no fact suite, no fact-failure
    detail -- the information barrier holds exactly as before, just with one more thing the
    fresh context is allowed to see about ITSELF). Either both or neither must be given; a
    caller passing just one gets a silent no-feedback prompt (backward compatible with a first
    attempt, where both are `None`) -- not asserted here since `authoring.pipeline`'s own loop
    is the only real caller and always passes both or neither together."""
    template = load_prompt_template("round_trip")
    system, user = template.render(pinned_signature=pinned_signature, dossier_md=dossier_md)
    if previous_attempt is not None and previous_error is not None:
        user = (
            f"{user}\n\n"
            "Your previous attempt is below, with the compiler's error -- fix it (restructure "
            "the recursion if the error concerns termination).\n\n"
            f"Previous attempt:\n{previous_attempt}\n\n"
            f"Compiler error:\n{previous_error}"
        )
    max_tokens = max_tokens if max_tokens is not None else authoring_cfg.AUTHORING_MAX_TOKENS["round_trip"]
    _charge(budget)
    response = client.send(system=system, user_message=user, model_id=model_id, max_tokens=max_tokens)
    return _strip_markdown_fence(response.text)


# === Rows 6-7 -- one repair cycle, then terminal ===============================================


@dataclass(frozen=True)
class RepairCycleOutcome:
    passed: bool
    attempt: int  # 1 = passed on the first try; 2 = passed after the one repair cycle
    detail: str


def with_one_repair_cycle(attempt_fn, repair_fn, *, max_attempts: int = 2) -> RepairCycleOutcome:
    """The shared shape of contract §6 rows 6 and 7: try, and on failure, repair once and try
    again; a second failure is terminal (the caller rotates to the next candidate/task, per
    "then task rotates"/"then rotate"). `attempt_fn() -> (bool, str)` and `repair_fn() -> None`
    carry the actual repair mechanics -- what changes between attempts is unspecified by the
    contract for both rows (no dossier-regeneration or round-trip-repair prompt shape is
    named), so this function owns only the shared retry-count bookkeeping, not the repair
    itself."""
    detail = ""
    for attempt in range(1, max_attempts + 1):
        passed, detail = attempt_fn()
        if passed:
            return RepairCycleOutcome(passed=True, attempt=attempt, detail=detail)
        if attempt < max_attempts:
            repair_fn()
    return RepairCycleOutcome(passed=False, attempt=max_attempts, detail=detail)
