"""The runtime fact representation.

Matches `docs/design/task_schema_v1.md`'s `facts[]` entries. Replaces the bare `list[str]`
fact representation flagged in `docs/decidability_bias_survey.md` finding 3: `mechanism` is
now a declared field on every fact, not implicit in whatever the statement string happens to
end with.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Fact:
    """One entry from a task's `facts[]` array. `instance`, `polarity`, and
    `violated_property` are only meaningful for `type == "membership"` -- see
    `docs/design/task_schema_v1.md` "task.json fields"."""

    id: str
    type: str  # "casework" | "membership" | "global"
    mechanism: str  # "decide" | "proof"
    statement: str
    instance: object | None = None
    polarity: str | None = None  # "accept" | "reject"
    violated_property: str | None = None  # required when polarity == "reject"

    @classmethod
    def from_dict(cls, data: dict) -> "Fact":
        """Build a `Fact` from a task.json fact entry -- typically one already validated by
        `harness.task_schema.validate_task_data`, but this does not itself validate; it only
        reads the fields the schema defines."""
        return cls(
            id=data["id"],
            type=data["type"],
            mechanism=data["mechanism"],
            statement=data["statement"],
            instance=data.get("instance"),
            polarity=data.get("polarity"),
            violated_property=data.get("violated_property"),
        )
