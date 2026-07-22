"""The authoring-time fact representation: what an LLM (or, in this task, a hand-written
fixture) proposes before mechanical validation, per `docs/design/reward_structure_2026-07-21.md`
§3.4 ("Propose, never certify") and `docs/design/verifier_architecture_2026-07-20.md` §5.

`ProposedFact` is deliberately built as a superset of `harness.facts.Fact` (the frozen,
schema-aligned runtime shape) rather than a parallel format -- every field `Fact` has, this
has too, with the same names and meaning. `to_fact()` projects onto exactly that shape once a
fact is validated. The extra fields below (`domain_inputs`, `anchors`, `expected_type`) are
authoring-time-only: they exist to drive `authoring.validate`'s checks and are never part of a
shipped `task.json` fact entry, because `docs/design/task_schema_v1.md` has no field for any
of them. That is a real gap in the frozen schema, not an oversight here -- see this package's
own problems list (reported alongside the task that introduced it) for why each is needed:

- `domain_inputs`: the schema's `domain.constraint` is described as "a Lean-parsable predicate
  over the input variable(s)" but nothing in `task.json` declares what those variables are
  named, how many there are, or how a specific fact's concrete inputs bind to them. Mechanical
  domain-containment checking needs exactly that binding, so it lives here instead.
- `anchors`: global facts cite "named anchor theorem(s) in Mathlib" per the task that
  introduced this validator, but `task.json`'s `facts[]` entry has no field to hold them --
  only `provenance` (a free-form string), which is the wrong place for something that gets
  individually resolved and checked in the pinned environment.
- `expected_type`: the type a membership fact's `instance` term must elaborate at. Not the
  same as `signature.type` (the pinned *definition's* type) -- for a fact about a concrete
  candidate object, it's the type of that object itself (e.g. `Fin 3 → Fin 3` for one
  `Monotone` instance), which the schema does not capture anywhere either.
"""

from dataclasses import dataclass, field

from harness.facts import Fact


@dataclass(frozen=True)
class ConventionPoint:
    """Mirrors one entry of `task.json`'s `domain.conventions` array (schema: `point`,
    `statement`, `note`), plus one authoring-time-only addition: `predicate`.

    The schema's `point` is free-form prose (e.g. `"0"`, or, for a multi-argument signature,
    whatever string the authoring LLM wrote) with no declared format -- there is no way to
    mechanically test whether a fact's concrete inputs "match" a convention point from `point`
    alone without re-parsing an arbitrary string, which is exactly the fragility this project
    avoids elsewhere (see `miner.verify`'s module docstring on why a similar re-parsing idea
    was rejected there). `predicate` sidesteps that: an explicit, decidable Lean predicate
    over the same input-variable names as the domain constraint, checked the same way (see
    `authoring.validate.check_domain_containment`). `None` when a convention point has no
    mechanically-checkable form (e.g. the `NONE_DECLARED` sentinel) -- such points are simply
    never matched by the containment checker, which is correct: there's nothing to match.
    """

    point: str
    statement: str
    note: str
    predicate: str | None = None


@dataclass(frozen=True)
class DomainSpec:
    """Mirrors `task.json`'s `domain` field, restricted to what the containment checker
    needs: `constraint` and `conventions`. Deliberately does not carry the dossier-facing
    prose consistency-check fields -- out of scope for this validator (see the task's stop
    points: this task does not touch the structural validator or the schema itself)."""

    constraint: str
    conventions: list[ConventionPoint] = field(default_factory=list)


@dataclass(frozen=True)
class ProposedFact:
    """One authoring-time fact proposal, covering all three `docs/design/reward_structure_2026-07-21.md`
    §2 types. Every field `harness.facts.Fact` has is here under the same name; `to_fact()`
    drops the authoring-time-only extras once validation is done with them.

    `mechanism` is always declared explicitly on every fact, never inferred -- per the task
    that introduced this module and per `harness.facts.Fact`'s own docstring, which fixed the
    same rule for the runtime shape this type feeds into.
    """

    id: str
    type: str  # "casework" | "membership" | "global"
    mechanism: str  # "decide" | "proof"
    statement: str
    instance: str | None = None
    polarity: str | None = None  # "accept" | "reject" -- membership only
    violated_property: str | None = None  # required when polarity == "reject"

    # Authoring-time-only fields -- see this module's docstring for why each exists and why
    # the frozen schema doesn't already have a place for it.
    domain_inputs: dict[str, str] = field(default_factory=dict)  # named input var -> concrete
    # Lean term, e.g. {"b": "2", "n": "37"}. Required (non-empty) for casework facts and for
    # membership facts whose domain constraint isn't the unrestricted "True" sentinel.
    anchors: list[str] = field(default_factory=list)  # global facts only: named Mathlib
    # theorem(s) this fact cites; each is resolved in the pinned environment.
    expected_type: str | None = None  # membership facts only: the type `instance` must
    # elaborate at.

    def to_fact(self) -> Fact:
        """Project onto `harness.facts.Fact`, the frozen runtime/schema-aligned shape --
        drops `domain_inputs`, `anchors`, `expected_type`. Callers should only do this once a
        fact has been ACCEPTED (or PROVISIONALLY_VALIDATED); this method itself performs no
        validation, it only reshapes already-validated data."""
        return Fact(
            id=self.id,
            type=self.type,
            mechanism=self.mechanism,
            statement=self.statement,
            instance=self.instance,
            polarity=self.polarity,
            violated_property=self.violated_property,
        )
