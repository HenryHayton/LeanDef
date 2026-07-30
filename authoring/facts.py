"""The authoring-time fact representation: what an LLM (or, in this task, a hand-written
fixture) proposes before mechanical validation, per `docs/design/reward_structure_2026-07-21.md`
§5 ("Propose, never certify") and `docs/design/verifier_architecture_2026-07-20.md` §5.

`ProposedFact` is deliberately built as a superset of `harness.facts.Fact` (the frozen,
schema-aligned runtime shape) rather than a parallel format -- every field `Fact` has, this
has too, with the same names and meaning. `to_fact()` projects onto exactly that shape once a
fact has a verdict, filling in the schema-required `validation_status` (and, when a proof has
been discharged, `discharge`/`cached_script`/`axiom_closure`/`provenance`) from the caller.

As of schema v1.1, `domain_inputs` and `anchors` are no longer authoring-time-only: they ship
in `task.json` (see `docs/design/task_schema_v1_1.md`'s Changelog) and `to_fact()` carries them
through unchanged. `expected_type` remains the one field below that never reaches a shipped
task.json fact entry -- see that document's "Open points" for why it stays authoring-only:

- `domain_inputs`: the schema's `domain.constraint` is a Lean-parsable predicate over named
  domain variables (`domain.variables`, schema v1.1); a fact's own `domain_inputs` binds its
  concrete inputs to those names. Mechanical domain-containment checking needs exactly that
  binding, and reward-time re-checks and human/agent review of a shipped task now read it too.
- `anchors`: global facts cite named anchor theorem(s) in Mathlib, individually resolved and
  checked in the pinned environment (`authoring.validate.validate_global_fact`) and consumed
  again downstream as the tier-3 explicit premises (reward doc §3, tier 3).
- `expected_type`: the type a membership fact's `instance` term must elaborate at. Not the
  same as `signature.type` (the pinned *definition's* type) -- for a fact about a concrete
  candidate object, it's the type of that object itself (e.g. `Fin 3 → Fin 3` for one
  `Monotone` instance). Authoring-only: it drives the one-time
  `#check ((instance) : (expected_type))` elaboration probe and nothing downstream reads it
  again -- a `decide`-mechanism fact's `statement` already bakes the check in full, and a
  `proof`-mechanism fact's bare-Prop `statement` already carries the instance's type via the
  term itself. OPTIONAL as of 2026-07-28 (not a `harness.task_schema` requirement, confirmed by
  that session's parser-vs-schema sweep) -- when absent, `authoring.validate
  .validate_membership_fact` falls back to a plain `#check (instance)` elaboration probe rather
  than rejecting the fact; sharper when present, never load-bearing when it isn't.
"""

from dataclasses import dataclass, field

from harness.facts import Fact, FactProvenance


@dataclass(frozen=True)
class ConventionPoint:
    """Mirrors one entry of `task.json`'s `domain.conventions` array (schema: `point`,
    `statement`, `note`), plus one authoring-time-only addition: `predicate`.

    `point`/`statement` are `str | None` so the schema's own `NONE_DECLARED` sentinel entry
    (both null) is representable here, not just in raw JSON (schema v1.1 fixed a latent gap:
    the schema has allowed the sentinel since v1, but this dataclass could not hold it until
    now).

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

    point: str | None
    statement: str | None
    note: str
    predicate: str | None = None


@dataclass(frozen=True)
class DomainSpec:
    """Mirrors `task.json`'s `domain` field, restricted to what the containment checker
    needs: `constraint`, `variables`, and `conventions`. Deliberately does not carry the
    dossier-facing prose consistency-check fields -- out of scope for this validator (see the
    task that introduced it: this module does not touch the structural validator or the schema
    itself).

    `conventions` has no default (schema v1.1): the schema has required this field to be
    non-empty (using the `NONE_DECLARED` sentinel where there is genuinely nothing to declare)
    since v1, so a `DomainSpec` silently defaulting to `[]` -- a shape the schema has never
    accepted -- was a latent mismatch between this dataclass and the spec it mirrors.
    """

    constraint: str
    conventions: list[ConventionPoint]
    variables: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ProposedFact:
    """One authoring-time fact proposal, covering all three `docs/design/reward_structure_2026-07-21.md`
    §2 types. Every field `harness.facts.Fact` has is here under the same name; `to_fact()`
    drops only the authoring-time-only extra (`expected_type`) once validation is done with it.

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

    domain_inputs: dict[str, list[str]] = field(default_factory=dict)  # named domain variable
    # -> non-empty list of concrete Lean terms (schema v1.1.3), e.g. {"b": ["2"], "n": ["37"]}.
    # Required (non-empty) for casework facts and for membership facts whose domain constraint
    # isn't the unrestricted "True" sentinel. A multi-element list instantiates that variable
    # at several points within this one fact -- see authoring.parse's canonicalization.
    anchors: list[str] = field(default_factory=list)  # global facts only: named Mathlib
    # theorem(s) this fact cites; each is resolved in the pinned environment.

    # Authoring-time-only: never reaches a shipped task.json fact entry -- see this module's
    # docstring for why.
    expected_type: str | None = None  # membership facts only: the type `instance` must
    # elaborate at.

    # Contract §4.2 (self-citation rule): the model's own declaration that a global fact
    # restates its anchor theorem near-verbatim. Authoring-time-only for now, like
    # `expected_type` above but for a different reason: the schema home for a self-citation
    # signal is `discharge.self_cited` (schema v1.1.1), and `discharge` stays `null` for every
    # fact this pipeline ships (no ladder exists yet to produce a real discharge record) -- so
    # there is currently nowhere downstream for this declaration to land. Collected and carried
    # through the batch review (contract §7's "self-citation rates") so it isn't silently
    # dropped; projecting it into a real `discharge.self_cited` is future work once discharge
    # records exist.
    self_restatement: bool = False

    def to_fact(
        self,
        *,
        validation_status: str,
        provenance: FactProvenance | None = None,
        discharge: dict | None = None,
        cached_script: str | None = None,
        axiom_closure: list[str] | None = None,
    ) -> Fact:
        """Project onto `harness.facts.Fact`, the frozen runtime/schema-aligned shape -- drops
        only `expected_type`. Callers should only do this once a fact has a verdict (`ACCEPTED`
        / `CERTIFIED`, or `PROVISIONALLY_VALIDATED`); this method itself performs no
        validation, it only reshapes already-validated data plus whatever ladder-discharge
        evidence the caller has for it. `validation_status` is required (not defaulted) so a
        caller can never ship a fact without deciding which schema v1.1 status it earned."""
        return Fact(
            id=self.id,
            type=self.type,
            mechanism=self.mechanism,
            statement=self.statement,
            instance=self.instance,
            polarity=self.polarity,
            violated_property=self.violated_property,
            domain_inputs=dict(self.domain_inputs),
            anchors=list(self.anchors),
            validation_status=validation_status,
            discharge=discharge,
            cached_script=cached_script,
            axiom_closure=axiom_closure,
            provenance=provenance,
        )
