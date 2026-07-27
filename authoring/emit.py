"""Task emitter (contract §8 item 2): validated artifacts -> `task.json` + `dossier.md` on
disk, per `docs/design/task_schema_v1_1.md`'s "Artifact shape". A validator
(`harness.task_schema.validate_task_dir`) has existed since schema v1.1 landed; nothing wrote
the files it validates until this module.

Self-check, in the emitter itself: `emit_task` writes both files, then immediately calls
`validate_task_dir` on what it just wrote and returns that result. A write that produces an
invalid task.json is a bug in the emitter (or in whatever upstream data it was handed) and
must be caught here, not downstream at consumption time. On self-check failure this function
lets `harness.task_schema.TaskSchemaError` propagate -- deliberately not cleaning up the
written files first: a human debugging why the emitter produced something invalid needs to see
exactly what was written, not have it erased out from under them.

Field-shape responsibility split, matching this codebase's existing structural/semantic split
(`docs/design/task_schema_v1_1.md` "Clarifications", 2026-07-21): this module's job is
projecting already-validated runtime objects (`harness.facts.Fact`, `authoring.facts.DomainSpec`)
into the exact JSON shape the schema wants -- it performs no mechanical/semantic validation of
its own (that already happened in `authoring.validate` before a `Fact` ever reaches here).
"""

import json
from dataclasses import dataclass
from pathlib import Path

from authoring.facts import DomainSpec
from harness.facts import Fact
from harness.task_schema import ValidatedTask, validate_task_dir


def _convention_to_dict(cp) -> dict:
    return {"point": cp.point, "statement": cp.statement, "note": cp.note}


def _domain_to_dict(domain: DomainSpec) -> dict:
    """Schema shape is `{constraint, variables, conventions}`; drops `ConventionPoint.predicate`
    -- authoring-only (never part of the schema's conventions entry shape), per that
    dataclass's own docstring."""
    return {
        "constraint": domain.constraint,
        "variables": list(domain.variables),
        "conventions": [_convention_to_dict(cp) for cp in domain.conventions],
    }


def _fact_to_dict(fact: Fact) -> dict:
    """The exact reverse of `harness.facts.Fact.from_dict` -- one field, one schema key,
    nothing invented or dropped."""
    data = {
        "id": fact.id,
        "type": fact.type,
        "mechanism": fact.mechanism,
        "statement": fact.statement,
        "domain_inputs": dict(fact.domain_inputs),
        "anchors": list(fact.anchors),
        "validation_status": fact.validation_status,
        "discharge": fact.discharge,
        "cached_script": fact.cached_script,
        "axiom_closure": fact.axiom_closure,
        "provenance": (
            {"validation_run_id": fact.provenance.validation_run_id, "note": fact.provenance.note}
            if fact.provenance is not None
            else None
        ),
    }
    if fact.type == "membership":
        data["instance"] = fact.instance
        data["polarity"] = fact.polarity
        if fact.polarity == "reject":
            data["violated_property"] = fact.violated_property
    return data


@dataclass(frozen=True)
class EmittedTask:
    task_dir: Path
    validated: ValidatedTask


def emit_task(
    task_dir: Path,
    *,
    task_id: str,
    task_symbol: str,
    signature: dict,
    domain: DomainSpec,
    axiom_baseline: list[str],
    facts: list[Fact],
    dossier_md: str,
    heldout: bool,
    provenance: dict,
    admissibility_contract: dict | None = None,
    ladder_budget_override: dict | None = None,
) -> EmittedTask:
    """Write `task_dir/task.json` and `task_dir/dossier.md`, then re-validate what was written
    via `harness.task_schema.validate_task_dir` as a self-check. Raises `TaskSchemaError`
    (propagated from that self-check) if the written task.json is not schema-valid; the files
    are left in place either way.

    `signature` and `provenance` are taken as plain dicts matching the schema's own shape
    (`{name, type, imports}` and the task-level provenance object respectively) rather than a
    dedicated dataclass -- `harness.signature.PinnedSignature` has no `imports` field (it is
    scoring-side, not schema-side), and inventing a parallel dataclass just to hold three/five
    already-named keys would duplicate the schema doc's own field list for no mechanical
    benefit. `mutants` is not a parameter: schema v1.1 fixes it at `[]` (RESERVED), so this
    function writes that literal rather than accepting a value nothing may legally set yet.

    `task_symbol` (schema v1.1.2, contract §4.4) is REQUIRED and this function is the single
    place that enforces the schema's coherence rule (`signature.name == task_symbol`): whatever
    `name` key the caller's `signature` dict carries is overwritten with `task_symbol` before
    writing, on a copy (the caller's dict is never mutated) -- since this emitter is the only
    producer of task.json, this guarantees the rule holds for everything shipped through it,
    rather than relying on every caller to keep two fields in sync by hand.
    """
    task_dir = Path(task_dir)
    task_dir.mkdir(parents=True, exist_ok=True)
    signature = {**signature, "name": task_symbol}

    task_data = {
        "task_id": task_id,
        "schema_version": "1.1",
        "task_symbol": task_symbol,
        "signature": signature,
        "domain": _domain_to_dict(domain),
        "axiom_baseline": list(axiom_baseline),
        "admissibility_contract": admissibility_contract or {"single_declaration": True},
        "ladder_budget_override": ladder_budget_override,
        "facts": [_fact_to_dict(f) for f in facts],
        "heldout": heldout,
        "mutants": [],
        "provenance": provenance,
    }

    (task_dir / "task.json").write_text(json.dumps(task_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (task_dir / "dossier.md").write_text(dossier_md, encoding="utf-8")

    validated = validate_task_dir(task_dir)
    return EmittedTask(task_dir=task_dir, validated=validated)
