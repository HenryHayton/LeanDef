"""The runtime fact representation.

Matches `docs/design/task_schema_v1_1.md`'s `facts[]` entries. Replaces the bare `list[str]`
fact representation flagged in `docs/decidability_bias_survey.md` finding 3: `mechanism` is
now a declared field on every fact, not implicit in whatever the statement string happens to
end with.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FactProvenance:
    """Mirrors a fact's `provenance` object: `{ validation_run_id, note }`. The structural
    validator (`harness.task_schema`) has required this shape on every fact since schema v1;
    this dataclass is what makes it a real, carried runtime value instead of a validated-then-
    discarded JSON key (schema v1.1, see its Changelog)."""

    validation_run_id: str
    note: str

    @classmethod
    def from_dict(cls, data: dict) -> "FactProvenance":
        return cls(validation_run_id=data["validation_run_id"], note=data["note"])


@dataclass(frozen=True)
class Fact:
    """One entry from a task's `facts[]` array. `instance`, `polarity`, and
    `violated_property` are only meaningful for `type == "membership"` -- see
    `docs/design/task_schema_v1_1.md` "task.json fields"."""

    id: str
    type: str  # "casework" | "membership" | "global"
    mechanism: str  # "decide" | "proof"
    statement: str
    instance: str | None = None  # always a Lean term string -- see task_schema_v1_1.md "Clarifications"
    polarity: str | None = None  # "accept" | "reject"
    violated_property: str | None = None  # required when polarity == "reject"

    # Ladder-era fields (schema v1.1) -- see docs/design/task_schema_v1_1.md's Changelog.
    domain_inputs: dict[str, list[str]] = field(default_factory=dict)  # named domain variable
    # -> non-empty list of concrete Lean terms (schema v1.1.3, was str -> str in v1.1), e.g.
    # {"b": ["2"], "n": ["8", "9"]} -- a multi-element list means this one fact instantiates
    # that variable at several points, never several implicit facts.
    anchors: list[str] = field(default_factory=list)  # global facts only: named Mathlib
    # theorem(s) this fact cites, resolved in the pinned environment; [] for non-global facts.
    validation_status: str | None = None  # "CERTIFIED" | "PROVISIONALLY_VALIDATED"
    discharge: dict | None = None  # {"tier": 1-5, "wall_clock_s": float, "at": "authoring"|"reward"}
    cached_script: str | None = None  # the reconstructed proof script; null until a tier 2-5 proof exists
    axiom_closure: list[str] | None = None  # required non-null whenever cached_script is non-null
    provenance: FactProvenance | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "Fact":
        """Build a `Fact` from a task.json fact entry -- typically one already validated by
        `harness.task_schema.validate_task_data`, but this does not itself validate; it only
        reads the fields the schema defines."""
        provenance_data = data.get("provenance")
        return cls(
            id=data["id"],
            type=data["type"],
            mechanism=data["mechanism"],
            statement=data["statement"],
            instance=data.get("instance"),
            polarity=data.get("polarity"),
            violated_property=data.get("violated_property"),
            domain_inputs=data.get("domain_inputs", {}),
            anchors=data.get("anchors", []),
            validation_status=data.get("validation_status"),
            discharge=data.get("discharge"),
            cached_script=data.get("cached_script"),
            axiom_closure=data.get("axiom_closure"),
            provenance=FactProvenance.from_dict(provenance_data) if provenance_data else None,
        )
