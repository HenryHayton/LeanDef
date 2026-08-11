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

    # --- schema v1.2 (11 Aug 2026): fields that must survive to scoring time -----------------
    #
    # `self_restatement` closes a standing debt. The fact-proposal prompt has always asked the
    # model to declare when a fact merely restates its anchor theorem or the definition's own
    # unfolding, and `authoring.facts.ProposedFact` has always collected it -- but it was
    # documented as "authoring-time-only: never reaches a shipped task.json fact entry", so no
    # scorer could ever act on it. Measured consequence: 13.1% of proof-mechanism facts in the
    # authored corpus are `rfl`-provable restatements of the definition (a FLOOR -- an earlier
    # n=5 study using "exact? cites its own anchor" found 100%), and they resolve at 87.7%
    # against 58.0% for real facts, inflating every fidelity figure derived from them.
    self_restatement: bool = False
    # "boundary" | "interior" on decide-mechanism facts. An interior arithmetic spot-check
    # (`choose 10 3 = 120`) survives every plausible misreading -- boundary and side-condition
    # errors compute the interior correctly -- so it discriminates almost nothing.
    boundary_vs_interior: str | None = None
    # For a near-miss reject fact: the ONE defining clause this witness violates, satisfying all
    # others. `None` on a generic non-example, which is still shippable but weaker.
    near_miss_clause: str | None = None
    # The anchor as actually RESOLVED in the pinned environment (a theorem's full name). An
    # anchor that resolves to a definition rather than a theorem is a restatement by
    # construction and is rejected at validation.
    anchors_resolved: list[str] = field(default_factory=list)
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
            # schema v1.2 -- absent on every pre-v1.2 task.json, hence the defaults.
            self_restatement=bool(data.get("self_restatement", False)),
            boundary_vs_interior=data.get("boundary_vs_interior"),
            near_miss_clause=data.get("near_miss_clause"),
            anchors_resolved=data.get("anchors_resolved", []),
        )
