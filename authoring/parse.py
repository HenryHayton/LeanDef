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

**Every parse entry point is hardened against malformed input of any shape** -- wrong types,
dicts where strings were expected, extra nesting -- never raising a raw `TypeError`/`KeyError`/
`AttributeError`. This is not theoretical: a real Bedrock response (2026-07-28) sent `regimes`
as a list of `{type, description, estimated_count}` objects instead of the expected flat
string array, and crashed `parse_classification` with `TypeError: unhashable type: 'dict'` --
`authoring.orchestrate._call_llm_json`'s retry wrapper (contract §6 rows 1-2) only catches
`ParseError`, so anything else escapes past the retry machinery and takes the whole task down.
Individual checks are ordered so a type check always precedes anything that would crash on the
wrong type (e.g. `isinstance(r, str)` before `r in REGIMES`, since checking set membership of
an unhashable value raises `TypeError`); `@_hardened` on top of that is a last-resort net on
each public entry point (`parse_classification`/`parse_dossier`/`parse_facts`), converting any
`TypeError`/`KeyError`/`AttributeError`/`IndexError` that slips past the targeted checks into a
`ParseError` too, so the property holds even for a shape nobody anticipated.
"""

import functools
import json
import re
from dataclasses import dataclass

from authoring.facts import ConventionPoint, DomainSpec, ProposedFact
from authoring.validate import ReasonCode

REGIMES = frozenset({"casework", "membership", "global"})
FACT_TYPES = frozenset({"casework", "membership", "global"})
MECHANISMS = frozenset({"decide", "proof"})
POLARITIES = frozenset({"accept", "reject"})

# Schema v1.1.3 cap safeguard -- mirrors harness.task_schema.MAX_DOMAIN_INPUT_VALUES exactly
# (kept as a separate constant rather than importing across the authoring/harness boundary,
# matching this module's existing precedent of mirroring rather than importing schema rules).
MAX_DOMAIN_INPUT_VALUES = 3

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
    # DELIBERATELY stricter than `harness.task_schema._validate_statement_format`, which only
    # checks `":=" not in statement` for mechanism 'proof' -- confirmed by the 2026-07-28
    # parser-vs-schema strictness sweep (the fix session that made `expected_type` optional and
    # converted the remaining whole-call membership/mechanism raises to per-fact rejections).
    # Swept and found to be the ONLY remaining stricter-than-schema case in this module; kept as
    # is (contract §4.1 explicitly calls out the proof side as deliberately stricter than the
    # decide side, unlike `_looks_like_decide_command` above, which is an exact schema mirror).
    return ":=" in statement or bool(_STANDALONE_BY_RE.search(statement))


class ParseError(Exception):
    """A whole-call parse/shape failure (contract §6 rows 1-2). `detail` is retry-prompt-ready
    feedback text; `reason_code` is set for shape violations (unset -- `None` -- for a bare
    JSON parse failure, since there is no fact/field to attribute a reason code to yet)."""

    def __init__(self, detail: str, reason_code: str | None = None):
        self.detail = detail
        self.reason_code = reason_code
        super().__init__(detail)


def _hardened(func):
    """Last-resort net for a `parse_*` public entry point: any `TypeError`/`KeyError`/
    `AttributeError`/`IndexError` that escapes the function's own targeted checks becomes a
    `ParseError` instead -- see this module's docstring for why (a real crash this exact
    pattern would have caught). `ParseError` itself passes through unchanged; anything else
    (a genuine bug unrelated to malformed input, e.g. in `ProposedFact`'s own constructor)
    still propagates, since blanket-catching `Exception` would mask those too."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ParseError:
            raise
        except (TypeError, KeyError, AttributeError, IndexError) as e:
            raise ParseError(
                f"response did not match the expected shape ({type(e).__name__}: {e})",
                reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
            ) from e

    return wrapper


def _parse_json_object(text: str) -> dict:
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError) as e:
        raise ParseError(f"response was not valid JSON: {e}") from e
    if not isinstance(data, dict):
        raise ParseError(
            f"response must be a JSON object at the top level, got {type(data).__name__}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )
    return data


def _require_field(data: dict, key: str, context: str) -> object:
    if not isinstance(data, dict):
        raise ParseError(f"{context}: expected an object, got {type(data).__name__}", reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE)
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


@_hardened
def parse_classification(text: str) -> Classification:
    data = _parse_json_object(text)
    context = "classification response"

    regimes = _require_field(data, "regimes", context)
    # `isinstance(r, str)` MUST be checked before `r in REGIMES` -- `REGIMES` is a `frozenset`,
    # and membership-testing an unhashable value (a dict, a list) against a set/frozenset
    # raises `TypeError`, not a clean "not found." Confirmed the hard way: a real Bedrock
    # response sent `regimes` as a list of `{type, description, estimated_count}` objects
    # instead of flat strings (2026-07-28) and crashed exactly here before this ordering fix.
    if (
        not isinstance(regimes, list)
        or not regimes
        or not all(isinstance(r, str) for r in regimes)
        or not all(r in REGIMES for r in regimes)
    ):
        raise ParseError(
            f"{context}: 'regimes' must be a non-empty flat array of strings drawn from "
            f"{sorted(REGIMES)} (not objects/descriptions), got {regimes!r}",
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


# `return_shape` vocabulary this mirrors -- deliberately not imported from `miner.shape` (the
# authoring package has no dependency on `miner`; the three-string vocabulary itself is the
# only thing shared, and is stable/closed, not worth a cross-package import for).
_PROP_SHAPE = "prop"


def validate_classification_against_shape(classification: Classification, return_shape: str) -> Classification:
    """Parse-time mechanization of contract §2's stated rule ("a Prop-valued definition must
    not receive 'casework' -- casework collapses into membership for Prop-valued objects,
    since there is nothing to compute, only membership to decide"), checked against
    `return_shape` (mechanical truth read off the pinned type, threaded in by
    `authoring.orchestrate.run_classification_call`) rather than left to the model's own
    inference from prose. Raises `ParseError` -- a contract §6 rows-1-2 shape (one retry, then
    terminal for the call), the same machinery a malformed-JSON response already goes through,
    since this is exactly that: a well-formed but contract-violating response, not a per-fact
    concern (2c4b9e5's family) or a per-task concern (round-trip's flag family)."""
    if return_shape == _PROP_SHAPE and "casework" in classification.regimes:
        raise ParseError(
            f"classification response: 'casework' is not valid for a Prop-valued definition "
            f"(return_shape={return_shape!r}) -- casework collapses into membership for "
            f"Prop-valued objects (contract §2); use 'membership' instead",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )
    return classification


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


@_hardened
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


def _leaks_forbidden_name(forbidden_name: str, *parts: str | None, task_symbol: str | None = None) -> bool:
    # `isinstance(part, str)` guards against a non-string, non-None `part` (a dict/list/int a
    # caller forgot to type-check first) -- `x in 5` raises `TypeError`, `x in {...}`/`x in
    # [...]` wouldn't crash but would check the wrong thing (dict keys / list elements, not
    # substring containment). Defense in depth: `_parse_fact_entry` also type-checks
    # `instance`/`expected_type` before this is ever called.
    #
    # `task_symbol` (2026-07-31): for an UNNAMESPACED real name the task symbol CONTAINS it --
    # `VTask.Monotone` contains `Monotone` -- so a plain substring test flags the very symbol
    # every statement is required to use, rejecting 100% of facts (confirmed live: 12/12, 14/14
    # and 15/15 for Monotone, DependsOn and memPartition, every one a correct `VTask.` usage).
    # Occurrences of the task symbol are removed BEFORE the substring test, which keeps this
    # matcher's deliberate strictness (no word boundaries -- see `docs/deferred.md` and
    # `authoring.consistency._contains_real_name`, the word-boundary family) for everything
    # else: a statement mixing both, e.g. `VTask.Monotone (Monotone f)`, still leaks.
    def _strip(part: str) -> str:
        return part.replace(task_symbol, "") if task_symbol else part

    return any(isinstance(part, str) and forbidden_name in _strip(part) for part in parts)


def _parse_fact_entry(
    entry: object, index: int, *,
    task_symbol: str | None = None, forbidden_name: str | None = None, domain_constraint: str | None = None,
    decidability: str | None = None, domain_variables: list[str] | None = None,
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
    # Type<->mechanism coupling (2026-07-28, second pass): per-fact, not whole-call -- one
    # fact's wrong mechanism for its own type must not discard the rest of an otherwise-good
    # batch, same principle as the membership required-field checks below.
    if fact_type == "casework" and mechanism != "decide":
        return FactParseRejection(
            index=index,
            fragment=entry,
            reason_code=ReasonCode.MALFORMED_BAD_MECHANISM,
            detail=f"{context}: casework fact {fact_id!r} requires mechanism 'decide', got {mechanism!r}",
        )
    if fact_type == "global" and mechanism != "proof":
        return FactParseRejection(
            index=index,
            fragment=entry,
            reason_code=ReasonCode.MALFORMED_BAD_MECHANISM,
            detail=f"{context}: global fact {fact_id!r} requires mechanism 'proof', got {mechanism!r}",
        )

    statement = _require_str(entry, "statement", context)

    domain_inputs_raw = entry.get("domain_inputs", {})
    if not isinstance(domain_inputs_raw, dict) or not all(isinstance(k, str) for k in domain_inputs_raw):
        raise ParseError(
            f"{context}: 'domain_inputs', if present, must be an object keyed by strings, got {domain_inputs_raw!r}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )
    # Canonical-form safeguard (schema v1.1.3): a scalar string the model emits is normalized
    # to a single-element list HERE, at parse time -- lists are the ONLY shape anything
    # downstream of this function ever sees (ProposedFact, Fact, check_domain_containment),
    # so no reader branches on shape. docs/design/task_schema_v1_1.md's v1.1.3 changelog entry
    # is the design-of-record for this; the schema itself (harness.task_schema) requires the
    # list shape outright and does not accept a bare scalar.
    domain_inputs: dict[str, list[str]] = {}
    for k, v in domain_inputs_raw.items():
        if isinstance(v, str):
            v = [v]
        if not isinstance(v, list) or not v or not all(isinstance(x, str) and x for x in v):
            raise ParseError(
                f"{context}: 'domain_inputs' value for {k!r} must be a non-empty string or a "
                f"non-empty array of non-empty strings, got {entry['domain_inputs'][k]!r}",
                reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
            )
        domain_inputs[k] = v

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
    # Type-checked here for EVERY fact type (not just membership below, which re-requires them
    # as non-empty strings) -- casework/global facts don't require `instance`/`expected_type`,
    # but if present they still must be string-or-null, since `_leaks_forbidden_name` below
    # (and the eventual `Fact` construction) both assume that.
    if instance is not None and not isinstance(instance, str):
        raise ParseError(
            f"{context}: 'instance', if present, must be a string or null, got {instance!r}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )
    if expected_type is not None and not isinstance(expected_type, str):
        raise ParseError(
            f"{context}: 'expected_type', if present, must be a string or null, got {expected_type!r}",
            reason_code=ReasonCode.MALFORMED_SCHEMA_SHAPE,
        )
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

    # Rule 5 (2026-07-30, parse-time mirror closing docs/deferred.md's entry of that name):
    # every domain_inputs key must be one of the task's declared domain.variables, mirroring
    # `harness.task_schema._validate_domain_inputs` exactly. Per-fact, not whole-call, same
    # principle as every other domain_inputs check in this function. The real trigger (batch-41
    # Gate 1, 2026-07-30 re-run): a monotonicity-probing fact needed TWO values of `n` and, with
    # no schema-sanctioned way to say so, the model invented keys `n1`/`n2` -- caught only at
    # `emit_task`, after the full task's spend was gone. The feedback below names the fix
    # (a list under the declared key), not just the violation.
    if domain_variables is not None:
        bad_keys = sorted(k for k in fact.domain_inputs if k not in domain_variables)
        if bad_keys:
            return FactParseRejection(
                index=index,
                fragment=entry,
                reason_code=ReasonCode.MALFORMED_UNKNOWN_DOMAIN_VARIABLE,
                detail=(
                    f"{context}: fact {fact_id!r} domain_inputs key(s) {bad_keys!r} are not "
                    f"among the task's declared domain.variables {list(domain_variables)!r} -- "
                    "to instantiate one variable at several points, use a list under its own "
                    'declared key (e.g. "n": ["8", "9"]), not a new key per point'
                ),
            )

    # Cap safeguard (schema v1.1.3): mirrors harness.task_schema.MAX_DOMAIN_INPUT_VALUES.
    too_many = {k: v for k, v in fact.domain_inputs.items() if len(v) > MAX_DOMAIN_INPUT_VALUES}
    if too_many:
        return FactParseRejection(
            index=index,
            fragment=entry,
            reason_code=ReasonCode.MALFORMED_TOO_MANY_DOMAIN_INPUT_VALUES,
            detail=(
                f"{context}: fact {fact_id!r} domain_inputs {sorted(too_many)} exceed the "
                f"{MAX_DOMAIN_INPUT_VALUES}-value cap per variable"
            ),
        )

    # Semantic-presence safeguard (schema v1.1.3): every listed value must literally occur in
    # the fact's own statement text -- a string-level check, sufficient per this rule's own
    # design (not a Lean-level check; catches a domain_inputs entry that doesn't correspond to
    # anything the statement actually probes).
    missing_in_statement = [
        f"{k}={x!r}" for k, values in fact.domain_inputs.items() for x in values if x not in statement
    ]
    if missing_in_statement:
        return FactParseRejection(
            index=index,
            fragment=entry,
            reason_code=ReasonCode.MALFORMED_DOMAIN_INPUT_NOT_IN_STATEMENT,
            detail=(
                f"{context}: fact {fact_id!r} domain_inputs value(s) {missing_in_statement} do "
                f"not literally occur in the fact's own statement {statement!r}"
            ),
        )

    # Type-conditional required-field pre-check, mirroring `harness.task_schema._validate_fact`
    # exactly (that module is the authoritative source of these rules -- see its own per-type
    # branches). Added 2026-07-28 after a real slice run: 15/15 casework facts in one task
    # reached `emit_task` with an empty `domain_inputs` (the fact-proposal prompt's per-type
    # rules never told the model casework needed it), surviving every check up to that point
    # because nothing before the final schema validator enforced non-emptiness. Per-fact, not
    # whole-call, exactly like the statement-format pre-check below -- one bad fact must not
    # discard an otherwise-good batch, and the batched row-3 retry (`_retry_rejected_facts`)
    # already exists to recover from exactly this shape of rejection.
    if fact_type == "casework" and not fact.domain_inputs:
        return FactParseRejection(
            index=index,
            fragment=entry,
            reason_code=ReasonCode.MALFORMED_MISSING_DOMAIN_INPUTS,
            detail=(
                f"{context}: casework fact {fact_id!r} is missing required non-empty "
                "domain_inputs mapping each domain variable to the concrete value the fact uses"
            ),
        )
    if (
        fact_type == "membership"
        and domain_constraint is not None
        and domain_constraint.strip() != "True"
        and not fact.domain_inputs
    ):
        return FactParseRejection(
            index=index,
            fragment=entry,
            reason_code=ReasonCode.MALFORMED_MISSING_DOMAIN_INPUTS,
            detail=(
                f"{context}: membership fact {fact_id!r} is missing required non-empty "
                "domain_inputs mapping each domain variable to the concrete value the fact uses "
                f"(required because the task's domain constraint {domain_constraint!r} is not "
                "the unrestricted 'True' sentinel)"
            ),
        )
    if fact_type == "global" and not fact.anchors:
        return FactParseRejection(
            index=index,
            fragment=entry,
            reason_code=ReasonCode.MALFORMED_MISSING_ANCHORS,
            detail=(
                f"{context}: global fact {fact_id!r} is missing required non-empty anchors -- "
                "cite at least one fully-qualified Mathlib theorem the fact derives from"
            ),
        )
    if fact_type != "global" and fact.anchors:
        return FactParseRejection(
            index=index,
            fragment=entry,
            reason_code=ReasonCode.MALFORMED_ANCHORS_NOT_ALLOWED,
            detail=(
                f"{context}: {fact_type} fact {fact_id!r} must not set anchors (anchors are "
                f"global-fact-only), got {fact.anchors!r}"
            ),
        )

    # Membership required-field checks (2026-07-28, second pass): moved from whole-call
    # `_require_str` raises to per-fact `FactParseRejection`s -- the real 2026-07-28 gate run
    # (Nat.clog) rotated at `fact_proposal` because ONE membership fact out of 27 proposed facts
    # was missing `expected_type` (which `_require_str` demanded), and the whole-call
    # `ParseError` this produced discarded all 27 -- including 12 clean casework and 8 clean
    # global facts -- for one bad field on one fact. `instance`/`polarity`/`violated_property`
    # (on reject-polarity) genuinely ARE schema-required for membership
    # (`harness.task_schema._validate_fact`'s membership block), so they still gate -- just
    # per-fact now, feeding the same batched row-3 retry as domain_inputs/anchors above.
    # `expected_type` is deliberately NOT checked here at all (see below) -- it was never a
    # schema requirement, only an authoring-layer one this session removed.
    if fact_type == "membership":
        if not fact.instance:
            return FactParseRejection(
                index=index,
                fragment=entry,
                reason_code=ReasonCode.MALFORMED_MISSING_FIELD,
                detail=f"{context}: membership fact {fact_id!r} is missing required non-empty 'instance'",
            )
        if not isinstance(fact.polarity, str) or fact.polarity not in POLARITIES:
            return FactParseRejection(
                index=index,
                fragment=entry,
                reason_code=ReasonCode.MALFORMED_BAD_POLARITY,
                detail=(
                    f"{context}: membership fact {fact_id!r} has 'polarity' {fact.polarity!r}, "
                    f"must be one of {sorted(POLARITIES)}"
                ),
            )
        if fact.polarity == "reject" and not fact.violated_property:
            return FactParseRejection(
                index=index,
                fragment=entry,
                reason_code=ReasonCode.MALFORMED_MISSING_VIOLATED_PROPERTY,
                detail=(
                    f"{context}: membership fact {fact_id!r} has polarity 'reject' but is "
                    "missing required non-empty 'violated_property'"
                ),
            )
        # Decidability gate (2026-07-30, docs/design/llm_io_contract_v1.md §4.1/§4.4): a
        # `mechanism: decide` membership fact needs a real `Decidable` instance to check against
        # -- `decidability` (authoring.preflight.probe_decidability's own vocabulary, threaded
        # in from DefinitionInput) is `None` for a non-Prop task (never gates: decide-mechanism
        # membership facts on a value-typed object check decidable equality on the OUTPUT type,
        # not this) or a live `"decidable"|"undecidable"|"indeterminate"` verdict for a
        # Prop-valued one. Only `"decidable"` clears this -- `"indeterminate"` gates too, since
        # a probe that couldn't determine decidability is not permission to guess it can.
        if (
            mechanism == "decide"
            and decidability is not None
            and decidability != "decidable"
        ):
            return FactParseRejection(
                index=index,
                fragment=entry,
                reason_code=ReasonCode.MALFORMED_DECIDE_ON_UNDECIDABLE_PROP,
                detail=(
                    f"{context}: membership fact {fact_id!r} uses mechanism 'decide' but this "
                    f"task's decidability probe reports {decidability!r}, not 'decidable' -- use "
                    "mechanism 'proof' instead"
                ),
            )

    # Task-symbol pre-check (contract §4.4): the model must write every statement against the
    # task symbol, never the real Mathlib name it may have seen in `definition_source`/
    # docstring/mention-sidecar context. `anchors` is deliberately EXCLUDED -- anchors name
    # real Mathlib theorems on purpose (contract's own "anchors still name real Mathlib
    # theorems" scoping) and routinely contain the forbidden name as a substring of their own
    # qualified name (e.g. `Nat.clog_pow` contains `Nat.clog`).
    if forbidden_name is not None and _leaks_forbidden_name(
        forbidden_name, statement, instance, expected_type, task_symbol=task_symbol
    ):
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


@_hardened
def parse_facts(
    text: str, *,
    task_symbol: str | None = None, forbidden_name: str | None = None, domain_constraint: str | None = None,
    decidability: str | None = None, domain_variables: list[str] | None = None,
) -> tuple[list[ProposedFact], list[FactParseRejection]]:
    """Parse Call 3's output array. Raises `ParseError` (whole-call, contract §6 rows 1-2) for
    malformed JSON or a schema-shape violation (missing/wrong-typed field, bad enum value,
    type/mechanism mismatch). Returns `(facts, rejections)` for the narrower per-fact
    pre-checks (§4.1/§6 row 3) instead of raising, so one badly-shaped fact doesn't discard an
    otherwise-good batch -- statement format, and (2026-07-28) every type-conditional required
    field `harness.task_schema._validate_fact` enforces (non-empty `domain_inputs` for
    casework/domain-constrained membership, non-empty `anchors` for global, empty `anchors`
    for non-global): mirrored here so a fact missing one of these is caught and fed back to the
    model at THIS cheap, batched-retry stage, not discovered at `emit_task` after every real
    LLM/REPL cost for the task has already been spent.

    `forbidden_name` (contract §4.4), when supplied, rejects (per-fact, not whole-call) any
    fact whose `statement`/`instance`/`expected_type` contains it -- the mechanical check that
    the model wrote against `task_symbol`, not the real Mathlib name. `domain_constraint` (the
    dossier's `domain.constraint`, already known by the time fact-proposal runs), when
    supplied, gates the membership `domain_inputs` check the same way
    `harness.task_schema._validate_fact` does. `decidability` (2026-07-30,
    `authoring.preflight.probe_decidability`'s vocabulary), when supplied, gates a
    `mechanism: decide` membership fact to only `"decidable"` Props. `domain_variables`
    (2026-07-30, schema v1.1.3, the dossier's `domain.variables`), when supplied, gates
    `domain_inputs` keys to the declared set -- rule 5's parse-time mirror, closing the
    `docs/deferred.md` entry of that name (see `_parse_fact_entry`'s own comment for the real
    incident that was its trigger). The cap (≤3 values per variable) and semantic-presence
    (each value must occur in the fact's own statement) safeguards run unconditionally whenever
    a fact has `domain_inputs` at all -- unlike rule 5, they need no external context to
    evaluate, so there is no reason to gate them on `domain_variables` being supplied. All five
    parameters default to `None` (no check for the ones that ARE gated), backward compatible
    with callers that have no such context yet."""
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError) as e:
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
        parsed = _parse_fact_entry(
            entry, i, task_symbol=task_symbol, forbidden_name=forbidden_name,
            domain_constraint=domain_constraint, decidability=decidability,
            domain_variables=domain_variables,
        )
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
