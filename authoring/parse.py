"""LLM JSON -> authoring objects: strict-JSON parsing of the four contract calls' outputs into
`Classification` / `DossierPayload` / `ProposedFact` objects, per
`docs/design/llm_io_contract_v1.md` §8 item 1.

This is the first construction of `ProposedFact`/`DomainSpec` outside test fixtures. Nothing
here talks to Bedrock or the Lean REPL -- it is a pure function of response text in, typed
object (or `ParseError`) out. `authoring.orchestrate` is the only caller that matters in
production; tests call these functions directly with hand-written JSON strings.

**Two distinct failure shapes, matching the contract's error table (§6) exactly:**

- Malformed JSON, or a whole-envelope shape violation (wrong type at the top level, a required
  field missing or wrong-typed) -- raises `ParseError`. This is a **whole-call** failure: the
  contract's rows 1-2 both get "one retry [...] then terminal for the call," and both are
  handled identically by `authoring.orchestrate`'s single retry wrapper, so this module does
  not distinguish "not JSON at all" from "valid JSON, wrong shape" in the exception type --
  only in `ParseError.detail`'s wording, which is what actually reaches the retry prompt.
- A per-fact statement-shape violation inside an otherwise well-formed facts array (§4.1's
  parser-layer pre-check: proof statements must not contain `:=`/`by`; decide statements must
  be runnable-command-shaped) -- does NOT raise. `parse_facts` returns it as a
  `FactParseRejection` alongside the facts that did parse cleanly. This is deliberate: the
  contract's row 3 ("the fact is dropped, suite may still ship") is a **per-fact** outcome, and
  a whole-call `ParseError` would incorrectly discard every fact in the batch over one bad
  statement.
"""

import json
import re
from dataclasses import dataclass

from authoring.facts import ConventionPoint, DomainSpec, ProposedFact
from authoring.validate import ReasonCode

REGIMES = frozenset({"casework", "membership", "global"})
FACT_TYPES = frozenset({"casework", "membership", "global"})
MECHANISMS = frozenset({"decide", "proof"})
POLARITIES = frozenset({"accept", "reject"})

# Mirrors harness.task_schema._validate_statement_format's decide-mechanism check exactly (the
# parser layer's decide-side pre-check is not a stricter superset the way the proof-mechanism
# check is -- contract §4.1 only calls out the proof side as deliberately stricter).
def _looks_like_decide_command(statement: str) -> bool:
    stripped = statement.strip()
    return stripped.startswith("#") or ":= by decide" in stripped

# Word-boundary match so a `by` embedded inside a longer identifier (e.g. a hypothetical
# `dividedByZero`) is not treated as a tactic-block keyword -- only a standalone `by` token
# (surrounded by non-identifier characters, e.g. spaces) counts. `:=` has no such ambiguity,
# so it's checked with a plain substring test.
_STANDALONE_BY_RE = re.compile(r"(?<![A-Za-z0-9_])by(?![A-Za-z0-9_])")


def _proof_statement_has_tactic_shape(statement: str) -> bool:
    return ":=" in statement or bool(_STANDALONE_BY_RE.search(statement))


class ParseError(Exception):
    """A whole-call parse/shape failure (contract §6 rows 1-2). `detail` is retry-prompt-ready
    feedback text; `reason_code` is set for shape violations (unset -- `None` -- for a bare
    JSON parse failure, since there is no fact/field to attribute a reason code to yet)."""

    def __init__(self, detail: str, reason_code: str | None = None):
        self.detail = detail
        self.reason_code = reason_code
        super().__init__(detail)


def _parse_json_object(text: str) -> dict:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ParseError(f"response was not valid JSON: {e}") from e
    if not isinstance(data, dict):
        raise ParseError(
            f"response must be a JSON object at the top level, got {type(data).__name__}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )
    return data


def _require_field(data: dict, key: str, context: str) -> object:
    if key not in data:
        raise ParseError(f"{context}: missing required field {key!r}", reason_code=ReasonCode.MALFORMED_MISSING_FIELD)
    return data[key]


def _require_str(data: dict, key: str, context: str) -> str:
    value = _require_field(data, key, context)
    if not isinstance(value, str) or value == "":
        raise ParseError(
            f"{context}: field {key!r} must be a non-empty string, got {value!r}",
            reason_code=ReasonCode.MALFORMED_MISSING_FIELD,
        )
    return value


# === Call 1 -- Regime classification (contract §2) ============================================


@dataclass(frozen=True)
class Classification:
    regimes: list[str]
    difficulty: int
    rationale: str
    expected_fact_mix: dict[str, int]


def parse_classification(text: str) -> Classification:
    data = _parse_json_object(text)
    context = "classification response"

    regimes = _require_field(data, "regimes", context)
    if not isinstance(regimes, list) or not regimes or not all(r in REGIMES for r in regimes):
        raise ParseError(
            f"{context}: 'regimes' must be a non-empty array drawn from {sorted(REGIMES)}, got {regimes!r}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )

    difficulty = _require_field(data, "difficulty", context)
    if not isinstance(difficulty, int) or isinstance(difficulty, bool) or not (1 <= difficulty <= 5):
        raise ParseError(
            f"{context}: 'difficulty' must be an integer 1-5, got {difficulty!r}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )

    rationale = _require_str(data, "rationale", context)

    mix = _require_field(data, "expected_fact_mix", context)
    if not isinstance(mix, dict) or set(mix) - {"casework", "membership", "global"}:
        raise ParseError(
            f"{context}: 'expected_fact_mix' must be an object with only "
            f"'casework'/'membership'/'global' keys, got {mix!r}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )
    for k, v in mix.items():
        if not isinstance(v, int) or isinstance(v, bool) or v < 0:
            raise ParseError(
                f"{context}.expected_fact_mix: {k!r} must be a non-negative integer, got {v!r}",
                reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
            )

    return Classification(regimes=list(regimes), difficulty=difficulty, rationale=rationale, expected_fact_mix=dict(mix))


# === Call 2 -- Dossier generation (contract §3) ================================================


@dataclass(frozen=True)
class DossierPayload:
    dossier_md: str
    domain: DomainSpec


def _parse_convention_entry(entry: object, index: int, context: str) -> ConventionPoint:
    if not isinstance(entry, dict):
        raise ParseError(
            f"{context}.conventions[{index}]: must be an object, got {entry!r}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )
    point = entry.get("point")
    statement = entry.get("statement")
    if point is not None and not isinstance(point, str):
        raise ParseError(
            f"{context}.conventions[{index}]: 'point' must be a string or null, got {point!r}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )
    if statement is not None and not isinstance(statement, str):
        raise ParseError(
            f"{context}.conventions[{index}]: 'statement' must be a string or null, got {statement!r}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )
    note = _require_str(entry, "note", f"{context}.conventions[{index}]")
    if point is None and statement is None and not note.startswith("NONE_DECLARED:"):
        raise ParseError(
            f"{context}.conventions[{index}]: a null point/statement sentinel requires a "
            f"'note' starting with 'NONE_DECLARED:', got {note!r}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )
    # `predicate` is authoring's own mechanically-checkable Lean predicate for a convention
    # point (authoring.facts.ConventionPoint's docstring) -- schema v1.1's conventions entry
    # shape is only {point, statement, note}, and the contract's Call 2 output field
    # (docs/design/llm_io_contract_v1.md §3) does not ask the model for one either. Every
    # parsed ConventionPoint therefore carries predicate=None; deriving one mechanically (or
    # asking a later call for it) is unspecified by the contract and out of scope here --
    # noted in the implementation report as a contract silence, not fixed by invention.
    return ConventionPoint(point=point, statement=statement, note=note, predicate=None)


def parse_dossier(text: str) -> DossierPayload:
    data = _parse_json_object(text)
    context = "dossier response"

    dossier_md = _require_str(data, "dossier_md", context)

    domain_data = _require_field(data, "domain", context)
    if not isinstance(domain_data, dict):
        raise ParseError(f"{context}.domain: must be an object, got {domain_data!r}", reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE)

    constraint = _require_str(domain_data, "constraint", f"{context}.domain")

    variables = _require_field(domain_data, "variables", f"{context}.domain")
    if not isinstance(variables, list) or not all(isinstance(v, str) and v for v in variables):
        raise ParseError(
            f"{context}.domain: 'variables' must be an array of non-empty strings, got {variables!r}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )

    conventions_data = _require_field(domain_data, "conventions", f"{context}.domain")
    if not isinstance(conventions_data, list) or not conventions_data:
        raise ParseError(
            f"{context}.domain: 'conventions' must be a non-empty array (use the "
            f"NONE_DECLARED sentinel if there is genuinely nothing to declare), got {conventions_data!r}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )
    conventions = [
        _parse_convention_entry(entry, i, f"{context}.domain") for i, entry in enumerate(conventions_data)
    ]

    domain = DomainSpec(constraint=constraint, conventions=conventions, variables=list(variables))
    return DossierPayload(dossier_md=dossier_md, domain=domain)


# === Call 3 -- Fact proposal (contract §4) =====================================================


@dataclass(frozen=True)
class FactParseRejection:
    """A per-fact statement-format pre-check failure (contract §4.1/§6 row 3) -- does not
    abort the whole call; `authoring.orchestrate` retries just these, once, then drops
    whatever is still bad."""

    index: int
    fragment: dict
    reason_code: str
    detail: str


def _leaks_forbidden_name(forbidden_name: str, *parts: str | None) -> bool:
    return any(part is not None and forbidden_name in part for part in parts)


def _parse_fact_entry(
    entry: object, index: int, *, task_symbol: str | None = None, forbidden_name: str | None = None
) -> ProposedFact | FactParseRejection:
    context = f"facts[{index}]"
    if not isinstance(entry, dict):
        raise ParseError(f"{context}: must be an object, got {entry!r}", reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE)

    fact_id = _require_str(entry, "id", context)
    fact_type = _require_str(entry, "type", context)
    if fact_type not in FACT_TYPES:
        raise ParseError(
            f"{context}: 'type' must be one of {sorted(FACT_TYPES)}, got {fact_type!r}",
            reason_code=ReasonCode.MALFORMED_UNKNOWN_TYPE,
        )
    mechanism = _require_str(entry, "mechanism", context)
    if mechanism not in MECHANISMS:
        raise ParseError(
            f"{context}: 'mechanism' must be one of {sorted(MECHANISMS)}, got {mechanism!r}",
            reason_code=ReasonCode.MALFORMED_BAD_MECHANISM,
        )
    if fact_type == "casework" and mechanism != "decide":
        raise ParseError(
            f"{context}: type 'casework' requires mechanism 'decide', got {mechanism!r}",
            reason_code=ReasonCode.MALFORMED_BAD_MECHANISM,
        )
    if fact_type == "global" and mechanism != "proof":
        raise ParseError(
            f"{context}: type 'global' requires mechanism 'proof', got {mechanism!r}",
            reason_code=ReasonCode.MALFORMED_BAD_MECHANISM,
        )

    statement = _require_str(entry, "statement", context)

    domain_inputs = entry.get("domain_inputs", {})
    if not isinstance(domain_inputs, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in domain_inputs.items()
    ):
        raise ParseError(
            f"{context}: 'domain_inputs', if present, must be an object of string -> string, got {domain_inputs!r}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )

    anchors = entry.get("anchors", [])
    if not isinstance(anchors, list) or not all(isinstance(a, str) and a for a in anchors):
        raise ParseError(
            f"{context}: 'anchors', if present, must be an array of non-empty strings, got {anchors!r}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )

    instance = entry.get("instance")
    polarity = entry.get("polarity")
    violated_property = entry.get("violated_property")
    expected_type = entry.get("expected_type")
    if fact_type == "membership":
        instance = _require_str(entry, "instance", context)
        polarity = _require_str(entry, "polarity", context)
        if polarity not in POLARITIES:
            raise ParseError(
                f"{context}: 'polarity' must be one of {sorted(POLARITIES)}, got {polarity!r}",
                reason_code=ReasonCode.MALFORMED_BAD_POLARITY,
            )
        if polarity == "reject" and not violated_property:
            raise ParseError(
                f"{context}: polarity 'reject' requires non-empty 'violated_property'",
                reason_code=ReasonCode.MALFORMED_MISSING_VIOLATED_PROPERTY,
            )
        expected_type = _require_str(entry, "expected_type", context)

    self_restatement = entry.get("self_restatement", False)
    if not isinstance(self_restatement, bool):
        raise ParseError(
            f"{context}: 'self_restatement', if present, must be a boolean, got {self_restatement!r}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )

    fact = ProposedFact(
        id=fact_id,
        type=fact_type,
        mechanism=mechanism,
        statement=statement,
        instance=instance,
        polarity=polarity,
        violated_property=violated_property,
        domain_inputs=dict(domain_inputs),
        anchors=list(anchors),
        expected_type=expected_type,
        self_restatement=self_restatement,
    )

    # Task-symbol pre-check (contract §4.4): the model must write every statement against the
    # task symbol, never the real Mathlib name it may have seen in `definition_source`/
    # docstring/mention-sidecar context. `anchors` is deliberately EXCLUDED -- anchors name
    # real Mathlib theorems on purpose (contract's own "anchors still name real Mathlib
    # theorems" scoping) and routinely contain the forbidden name as a substring of their own
    # qualified name (e.g. `Nat.clog_pow` contains `Nat.clog`).
    if forbidden_name is not None and _leaks_forbidden_name(forbidden_name, statement, instance, expected_type):
        return FactParseRejection(
            index=index,
            fragment=entry,
            reason_code=ReasonCode.MALFORMED_RAW_NAME_IN_STATEMENT,
            detail=(
                f"{context}: statement/instance/expected_type must reference the task symbol "
                f"{task_symbol!r}, not the real Mathlib name {forbidden_name!r}"
            ),
        )

    # Parser-layer statement-shape pre-check (contract §4.1), deliberately AFTER every
    # whole-call schema-shape check above so a format violation on an otherwise well-formed
    # fact is reported as the narrower, more specific per-fact rejection rather than folded
    # into a generic shape error.
    if mechanism == "proof" and _proof_statement_has_tactic_shape(statement):
        return FactParseRejection(
            index=index,
            fragment=entry,
            reason_code=ReasonCode.MALFORMED_STATEMENT_FORMAT,
            detail=(
                f"{context}: mechanism 'proof' statement must be a bare Prop (no ':=' or "
                f"'by' tactic block), got {statement!r}"
            ),
        )
    if mechanism == "decide" and not _looks_like_decide_command(statement):
        return FactParseRejection(
            index=index,
            fragment=entry,
            reason_code=ReasonCode.MALFORMED_STATEMENT_FORMAT,
            detail=(
                f"{context}: mechanism 'decide' statement must be a full runnable command "
                f"('#...' or '... := by decide'), got {statement!r}"
            ),
        )
    return fact


def parse_facts(
    text: str, *, task_symbol: str | None = None, forbidden_name: str | None = None
) -> tuple[list[ProposedFact], list[FactParseRejection]]:
    """Parse Call 3's output array. Raises `ParseError` (whole-call, contract §6 rows 1-2) for
    malformed JSON or a schema-shape violation (missing/wrong-typed field, bad enum value,
    type/mechanism mismatch). Returns `(facts, rejections)` for the narrower per-fact
    statement-format pre-check (§4.1/§6 row 3) instead of raising, so one badly-shaped
    statement doesn't discard an otherwise-good batch.

    `forbidden_name` (contract §4.4), when supplied, rejects (per-fact, not whole-call) any
    fact whose `statement`/`instance`/`expected_type` contains it -- the mechanical check that
    the model wrote against `task_symbol`, not the real Mathlib name. Both default to `None`
    (no check), backward compatible with callers that have no task-symbol context (or none
    that's meaningful, e.g. a `provenance.source: "fresh"` task with no real name to forbid)."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ParseError(f"response was not valid JSON: {e}") from e
    if not isinstance(data, list):
        raise ParseError(
            f"facts response must be a JSON array at the top level, got {type(data).__name__}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )

    facts: list[ProposedFact] = []
    rejections: list[FactParseRejection] = []
    seen_ids: set[str] = set()
    for i, entry in enumerate(data):
        parsed = _parse_fact_entry(entry, i, task_symbol=task_symbol, forbidden_name=forbidden_name)
        if isinstance(parsed, FactParseRejection):
            rejections.append(parsed)
            continue
        if parsed.id in seen_ids:
            raise ParseError(
                f"facts[{i}]: duplicate fact id {parsed.id!r} within one response",
                reason_code=ReasonCode.MALFORMED_MISSING_FIELD,
            )
        seen_ids.add(parsed.id)
        facts.append(parsed)
    return facts, rejections
