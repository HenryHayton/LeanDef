"""Task Schema v1 validator.

Enforces `docs/design/task_schema_v1.md` exactly -- that document is the frozen spec; this
module is its mechanical check. Errors are specific and reference the offending field by
path, since this validator is the miner's debugging interface (no miner exists yet).

This module is structural only; see the schema doc's "v1 clarifications" section
("status of structural vs. semantic validation") for what that does and does not cover.
"""

import json
from dataclasses import dataclass
from pathlib import Path

SCHEMA_VERSION = "1"
FACT_TYPES = frozenset({"casework", "membership", "global"})
MECHANISMS = frozenset({"decide", "proof"})
POLARITIES = frozenset({"accept", "reject"})
PROVENANCE_SOURCES = frozenset({"mathlib", "fresh"})
REVIEW_STATUSES = frozenset({"unreviewed", "agent_reviewed", "human_reviewed"})


class TaskSchemaError(ValueError):
    """A task.json (or task directory) violates docs/design/task_schema_v1.md. The message
    names the offending field path and what was expected."""


@dataclass(frozen=True)
class ValidatedTask:
    """A task.json payload that has passed every structural check in this module."""

    task_dir: Path
    data: dict


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise TaskSchemaError(message)


def _require_field(obj: dict, field: str, context: str) -> object:
    _require(field in obj, f"{context}: missing required field '{field}'")
    return obj[field]


def _require_str(obj: dict, field: str, context: str) -> str:
    value = _require_field(obj, field, context)
    _require(
        isinstance(value, str) and value != "",
        f"{context}: field '{field}' must be a non-empty string, got {value!r}",
    )
    return value


def _validate_conventions(conventions: object, context: str) -> None:
    _require(isinstance(conventions, list), f"{context}: 'conventions' must be an array")
    _require(
        len(conventions) > 0,
        f"{context}: 'conventions' must not be empty -- use the NONE_DECLARED sentinel "
        "entry if this object truly has no meaningful conventions",
    )

    def is_sentinel(entry: object) -> bool:
        return isinstance(entry, dict) and entry.get("point") is None and entry.get("statement") is None

    sentinels = [e for e in conventions if is_sentinel(e)]
    if sentinels:
        _require(
            len(conventions) == 1,
            f"{context}: a NONE_DECLARED sentinel entry (point and statement both null) "
            "must be the only entry in 'conventions', found other entries alongside it",
        )
        note = sentinels[0].get("note")
        _require(
            isinstance(note, str) and note.startswith("NONE_DECLARED:"),
            f"{context}: sentinel entry's 'note' must start with 'NONE_DECLARED:', got {note!r}",
        )
        return

    for i, entry in enumerate(conventions):
        entry_ctx = f"{context}.conventions[{i}]"
        _require(isinstance(entry, dict), f"{entry_ctx}: must be an object")
        _require_str(entry, "point", entry_ctx)
        _require_str(entry, "statement", entry_ctx)
        _require_str(entry, "note", entry_ctx)


def _validate_domain(domain: object, context: str) -> None:
    _require(isinstance(domain, dict), f"{context}: 'domain' must be an object")
    _require_str(domain, "constraint", f"{context}.domain")
    conventions = _require_field(domain, "conventions", f"{context}.domain")
    _validate_conventions(conventions, f"{context}.domain")


def _validate_signature(signature: object, context: str) -> None:
    _require(isinstance(signature, dict), f"{context}: 'signature' must be an object")
    _require_str(signature, "name", f"{context}.signature")
    _require_str(signature, "type", f"{context}.signature")
    imports = _require_field(signature, "imports", f"{context}.signature")
    _require(
        isinstance(imports, list) and all(isinstance(i, str) for i in imports),
        f"{context}.signature: 'imports' must be an array of strings, got {imports!r}",
    )


def _validate_admissibility_contract(contract: object, context: str) -> None:
    _require(isinstance(contract, dict), f"{context}: 'admissibility_contract' must be an object")
    single = contract.get("single_declaration")
    _require(
        single is True,
        f"{context}.admissibility_contract: 'single_declaration' must be true, got {single!r}",
    )


def _validate_fact_provenance(provenance: object, context: str) -> None:
    _require(isinstance(provenance, dict), f"{context}: 'provenance' must be an object")
    _require_str(provenance, "validation_run_id", f"{context}.provenance")
    _require_str(provenance, "note", f"{context}.provenance")


def _validate_fact(fact: object, index: int) -> str:
    context = f"facts[{index}]"
    _require(isinstance(fact, dict), f"{context}: must be an object")
    fact_id = _require_str(fact, "id", context)

    fact_type = _require_str(fact, "type", context)
    _require(
        fact_type in FACT_TYPES,
        f"{context}: 'type' must be one of {sorted(FACT_TYPES)}, got {fact_type!r}",
    )

    mechanism = _require_str(fact, "mechanism", context)
    _require(
        mechanism in MECHANISMS,
        f"{context}: 'mechanism' must be one of {sorted(MECHANISMS)}, got {mechanism!r}",
    )

    if fact_type == "global":
        _require(
            mechanism == "proof",
            f"{context}: type 'global' requires mechanism 'proof' (reward doc §2.3 -- "
            f"global facts are always proof-based), got mechanism {mechanism!r}",
        )
    elif fact_type == "casework":
        _require(
            mechanism == "decide",
            f"{context}: type 'casework' requires mechanism 'decide' (reward doc §2.1), "
            f"got mechanism {mechanism!r}",
        )
    # type == "membership": either mechanism is allowed (reward doc §2.2).

    _require_str(fact, "statement", context)

    if fact_type == "membership":
        _require_str(fact, "instance", context)
        polarity = _require_str(fact, "polarity", context)
        _require(
            polarity in POLARITIES,
            f"{context}: 'polarity' must be one of {sorted(POLARITIES)}, got {polarity!r}",
        )
        if polarity == "reject":
            _require_str(fact, "violated_property", context)

    _validate_fact_provenance(_require_field(fact, "provenance", context), context)

    return fact_id


def _validate_task_provenance(provenance: object, context: str) -> None:
    _require(isinstance(provenance, dict), f"{context}: 'provenance' must be an object")
    source = _require_str(provenance, "source", f"{context}.provenance")
    _require(
        source in PROVENANCE_SOURCES,
        f"{context}.provenance: 'source' must be one of {sorted(PROVENANCE_SOURCES)}, got {source!r}",
    )
    _require_str(provenance, "dossier_generator", f"{context}.provenance")
    _require_str(provenance, "validation_run_id", f"{context}.provenance")
    review_status = _require_str(provenance, "review_status", f"{context}.provenance")
    _require(
        review_status in REVIEW_STATUSES,
        f"{context}.provenance: 'review_status' must be one of {sorted(REVIEW_STATUSES)}, "
        f"got {review_status!r}",
    )
    if "mathlib_name" in provenance and provenance["mathlib_name"] is not None:
        _require(
            isinstance(provenance["mathlib_name"], str),
            f"{context}.provenance: 'mathlib_name', if present, must be a string",
        )


def validate_task_data(data: dict) -> None:
    """Validate an already-parsed task.json payload against every rule in
    `docs/design/task_schema_v1.md`. Raises `TaskSchemaError` with a specific message on the
    first violation found. See the module docstring for what is deliberately NOT checked."""
    _require(isinstance(data, dict), "task.json: top level must be an object")

    _require_str(data, "task_id", "task.json")
    schema_version = _require_str(data, "schema_version", "task.json")
    _require(
        schema_version == SCHEMA_VERSION,
        f"task.json: 'schema_version' must be {SCHEMA_VERSION!r}, got {schema_version!r}",
    )

    _validate_signature(_require_field(data, "signature", "task.json"), "task.json")
    _validate_domain(_require_field(data, "domain", "task.json"), "task.json")

    axiom_baseline = _require_field(data, "axiom_baseline", "task.json")
    _require(
        isinstance(axiom_baseline, list) and all(isinstance(a, str) for a in axiom_baseline),
        f"task.json: 'axiom_baseline' must be an array of strings, got {axiom_baseline!r}",
    )

    _validate_admissibility_contract(
        _require_field(data, "admissibility_contract", "task.json"), "task.json"
    )

    facts = _require_field(data, "facts", "task.json")
    _require(isinstance(facts, list), "task.json: 'facts' must be an array")
    seen_ids: set[str] = set()
    for i, fact in enumerate(facts):
        fact_id = _validate_fact(fact, i)
        _require(
            fact_id not in seen_ids,
            f"facts[{i}]: duplicate fact id {fact_id!r} -- fact ids must be unique within a task",
        )
        seen_ids.add(fact_id)

    heldout = _require_field(data, "heldout", "task.json")
    _require(isinstance(heldout, bool), f"task.json: 'heldout' must be a boolean, got {heldout!r}")

    mutants = _require_field(data, "mutants", "task.json")
    _require(
        mutants == [],
        f"task.json: 'mutants' is RESERVED and must be [] in schema v1, got {mutants!r}",
    )

    prover_budget = _require_field(data, "prover_budget", "task.json")
    _require(
        prover_budget is None,
        f"task.json: 'prover_budget' is RESERVED and must be null in schema v1, got {prover_budget!r}",
    )

    _validate_task_provenance(_require_field(data, "provenance", "task.json"), "task.json")


def validate_task_dir(task_dir: Path) -> ValidatedTask:
    """Load and validate a task directory per the schema's "Artifact shape": task.json must
    parse as JSON and pass `validate_task_data`; a sibling dossier.md must exist.

    `axiom_baseline` is normalized (sorted, deduplicated) on the returned `ValidatedTask.data`
    -- order and duplicates in the source file don't affect gate behaviour (subset-of-baseline
    checks don't care about either), so this canonicalizes rather than rejects them.
    """
    task_dir = Path(task_dir)
    task_json_path = task_dir / "task.json"
    dossier_path = task_dir / "dossier.md"

    _require(task_json_path.is_file(), f"{task_dir}: missing task.json")
    _require(dossier_path.is_file(), f"{task_dir}: missing dossier.md")

    try:
        data = json.loads(task_json_path.read_text())
    except json.JSONDecodeError as e:
        raise TaskSchemaError(f"{task_json_path}: invalid JSON: {e}") from e

    validate_task_data(data)
    data["axiom_baseline"] = sorted(set(data["axiom_baseline"]))
    return ValidatedTask(task_dir=task_dir, data=data)
