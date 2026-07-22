"""Mechanical validation of proposed facts against the true (ground-truth) Mathlib definition,
per the task that introduced this module: "propose, never certify -- every proposed fact is
validated mechanically against the ground truth before it can exist in a task."

Nothing here scores a *candidate*: unlike `harness.scoring` (which splices a candidate body
under the pinned signature and runs facts against it), this module runs facts against the
*true* definition already present in Mathlib under its real name -- no splicing, no candidate,
no admissibility gate. It reuses `harness.repl`'s hardened REPL plumbing (warm environment,
per-call timeouts, ERRORED handling) exactly as `miner.verify` does, building new Lean
commands on top of it rather than reimplementing any of it.

Three type-specific validators (`validate_casework_fact`, `validate_membership_fact`,
`validate_global_fact`) plus one cross-cutting check used by the first two
(`check_domain_containment`, the new capability this task adds) are dispatched by
`validate_fact`; `validate_facts` runs a whole proposed suite and returns a `ValidationRun`
with the counts/rejection listing this task calls for.

Global facts are never certified here -- no prover exists yet (see
`docs/design/verifier_architecture_2026-07-20.md` §5) -- so the best this module can do is
verify everything mechanically checkable short of the proof itself: the statement elaborates
as a `Prop`, it mentions the pinned name, and every named anchor theorem actually resolves in
the pinned environment. Proof-mechanism membership facts get the same "structural only, no
prover" treatment, per the reward-structure doc's own note that proof-requiring membership
facts still need the real prover eventually -- both come back `PROVISIONALLY_VALIDATED`, never
`ACCEPTED`, so nothing downstream mistakes "well-formed" for "certified."
"""

from collections import Counter
from dataclasses import dataclass, field
from enum import Enum

from lean_interact import AutoLeanServer, Command

from authoring.facts import DomainSpec, ProposedFact
from harness import config as cfg
from harness.repl import run_checked
from harness.results import CheckStatus


class Verdict(Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PROVISIONALLY_VALIDATED = "provisionally_validated"
    FLAGGED = "flagged"


class ReasonCode:
    """Machine-readable reason codes attached to every `ValidationOutcome`. A plain string
    namespace, not an `Enum`: reason codes are freely reused as plain strings in the
    JSON-shaped `evidence`/manifest output, and nothing here needs `Enum`'s closed-vocabulary
    guarantees the way `Verdict` (or `harness.results.CheckStatus`) does."""

    CERTIFIED_TRUE_OF_GROUND_TRUTH = "CERTIFIED_TRUE_OF_GROUND_TRUTH"
    FALSE_OF_GROUND_TRUTH = "FALSE_OF_GROUND_TRUTH"
    ERRORED = "ERRORED"
    OUT_OF_DOMAIN = "OUT_OF_DOMAIN"
    DOMAIN_UNDECIDED = "DOMAIN_UNDECIDED"
    INSTANCE_DOES_NOT_ELABORATE = "INSTANCE_DOES_NOT_ELABORATE"
    MALFORMED_MISSING_VIOLATED_PROPERTY = "MALFORMED_MISSING_VIOLATED_PROPERTY"
    MALFORMED_MISSING_ANCHORS = "MALFORMED_MISSING_ANCHORS"
    MALFORMED_BAD_MECHANISM = "MALFORMED_BAD_MECHANISM"
    MALFORMED_BAD_POLARITY = "MALFORMED_BAD_POLARITY"
    MALFORMED_MISSING_FIELD = "MALFORMED_MISSING_FIELD"
    MALFORMED_UNKNOWN_TYPE = "MALFORMED_UNKNOWN_TYPE"
    ANCHOR_NOT_FOUND = "ANCHOR_NOT_FOUND"
    PROPOSITION_DOES_NOT_ELABORATE = "PROPOSITION_DOES_NOT_ELABORATE"
    DOES_NOT_MENTION_PINNED_NAME = "DOES_NOT_MENTION_PINNED_NAME"
    STRUCTURAL_ONLY_NO_PROVER = "STRUCTURAL_ONLY_NO_PROVER"
    GLOBAL_DOMAIN_UNCHECKED = "GLOBAL_DOMAIN_UNCHECKED"


@dataclass(frozen=True)
class ValidationOutcome:
    """The verdict for one proposed fact. `evidence` is a JSON-shaped dict carrying whatever
    execution evidence backs the verdict -- commands run, their status, elapsed time, any
    domain-containment sub-check -- which is exactly the material
    `docs/design/task_schema_v1.md`'s validation manifest requires be recorded alongside a
    validated fact."""

    fact_id: str
    verdict: Verdict
    reason_code: str
    detail: str = ""
    evidence: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ValidationRun:
    """The outcome of validating a whole proposed fact suite -- the "per run" half of this
    module's output contract (the "per fact" half is `ValidationOutcome`)."""

    outcomes: list[ValidationOutcome]

    def counts_by_verdict(self) -> dict[str, int]:
        return dict(Counter(o.verdict.value for o in self.outcomes))

    def counts_by_reason(self) -> dict[str, int]:
        return dict(Counter(o.reason_code for o in self.outcomes))

    def rejections(self) -> list[ValidationOutcome]:
        return [o for o in self.outcomes if o.verdict is Verdict.REJECTED]

    def flagged(self) -> list[ValidationOutcome]:
        return [o for o in self.outcomes if o.verdict is Verdict.FLAGGED]

    def render_summary(self) -> str:
        """The standing human-readable review: counts by verdict and reason, every rejection
        listed with its reason -- per the task that introduced this module."""
        lines = [f"Validation run: {len(self.outcomes)} fact(s)", ""]
        lines.append("By verdict:")
        for verdict, count in sorted(self.counts_by_verdict().items()):
            lines.append(f"  {verdict}: {count}")
        lines.append("")
        lines.append("By reason code:")
        for reason, count in sorted(self.counts_by_reason().items()):
            lines.append(f"  {reason}: {count}")
        rejections = self.rejections()
        if rejections:
            lines.append("")
            lines.append("Rejections:")
            for o in rejections:
                lines.append(f"  {o.fact_id}: {o.reason_code} -- {o.detail}")
        flagged = self.flagged()
        if flagged:
            lines.append("")
            lines.append("Flagged for human review:")
            for o in flagged:
                lines.append(f"  {o.fact_id}: {o.reason_code} -- {o.detail}")
        return "\n".join(lines)


def _apply_predicate(predicate: str, names: list[str], values: list[str]) -> str:
    """Render `predicate` (a Lean expression over the free variables named in `names`) applied
    to concrete `values`, via lambda application -- e.g. `predicate="n ≥ 1"`,
    `names=["n"]`, `values=["6"]"` renders `(fun n => (n ≥ 1)) (6)`. Beta-reducing via lambda
    application, rather than textually substituting `values` for `names` inside `predicate`,
    sidesteps every string-substitution hazard (a variable name that's also a substring of a
    longer identifier, shadowing, precedence) -- the same reasoning `miner.verify` gives for
    preferring structured REPL round-trips over re-parsing pretty-printed text."""
    lambda_expr = f"(fun {' '.join(names)} => ({predicate}))"
    args = " ".join(f"({v})" for v in values)
    return f"{lambda_expr} {args}"


def _decide_bool(server: AutoLeanServer, env: int, expr: str, *, timeout: float) -> tuple[bool | None, dict]:
    """Evaluate `decide (expr)`, returning `(True/False, evidence)` if `expr` is decidable in
    the pinned environment, or `(None, evidence)` if it errors (most commonly: no `Decidable`
    instance -- an undecidable predicate at these inputs). Term-mode `#eval decide (...)`
    rather than tactic-mode `example : expr := by decide` deliberately: the tactic *fails*
    (with an error) both when `expr` is undecidable AND when it's decidably false (`decide`
    only succeeds when it can produce a proof, i.e. when `expr` is true) -- confirmed
    empirically before writing this -- so a bare pass/fail read of tactic-mode `decide` cannot
    tell "false" apart from "undecidable" without parsing error-message text. `#eval decide`
    instead always succeeds when a `Decidable` instance exists, printing `true`/`false` as
    data, and only the genuinely-undecidable case produces a REPL error -- so `PASSED` and the
    literal printed text is a clean three-way read."""
    cmd = f"#eval decide ({expr})"
    result = run_checked(server, Command(cmd=cmd, env=env), timeout=timeout)
    evidence = {"command": cmd, "status": result.status.name, "elapsed_s": result.elapsed_s, "detail": result.detail}
    if result.status is CheckStatus.PASSED and result.raw_response is not None:
        infos = [m.data.strip() for m in result.raw_response.messages if m.severity == "info"]
        if infos == ["true"]:
            return True, evidence
        if infos == ["false"]:
            return False, evidence
    return None, evidence


def check_domain_containment(
    server: AutoLeanServer,
    env: int,
    domain: DomainSpec,
    inputs: dict[str, str],
    *,
    timeout: float | None = None,
) -> tuple[str, dict]:
    """The domain-containment checker: does `inputs` (a binding of the domain constraint's
    named variables to concrete Lean terms) satisfy `domain.constraint`? Returns one of
    `"IN_DOMAIN"`, `"IN_DOMAIN_VIA_CONVENTION"`, `"OUT_OF_DOMAIN"`, `"DOMAIN_UNDECIDED"`, plus
    an evidence dict.

    The schema's own validation rule (`task_schema_v1.md` "Validation rule") is "every fact
    ... must lie inside `constraint` OR be a stated convention point" -- not the constraint
    alone. This checker honors both halves: a fact whose inputs fail the raw constraint is
    still in-domain if they match a convention point's own (authoring-time-only) `predicate`
    (see `authoring.facts.ConventionPoint`). Skipping the convention half would misclassify
    every legitimate junk-value fact (e.g. the schema's own `n = 0` example) as OUT_OF_DOMAIN --
    flagged in this module's problems list as an interpretation call, since the task's own
    description of this checker only mentions the constraint predicate.
    """
    timeout = timeout if timeout is not None else cfg.DECIDE_TIMEOUT
    if domain.constraint.strip() == "True":
        return "IN_DOMAIN", {"note": "domain constraint is the unrestricted 'True' sentinel"}
    if not inputs:
        return "DOMAIN_UNDECIDED", {"note": "no domain_inputs supplied for a non-trivial domain constraint"}

    names = list(inputs.keys())
    values = list(inputs.values())
    decided, evidence = _decide_bool(server, env, _apply_predicate(domain.constraint, names, values), timeout=timeout)
    if decided is True:
        return "IN_DOMAIN", evidence
    if decided is False:
        for cp in domain.conventions:
            if cp.predicate is None:
                continue
            cp_decided, cp_evidence = _decide_bool(
                server, env, _apply_predicate(cp.predicate, names, values), timeout=timeout
            )
            if cp_decided is True:
                return "IN_DOMAIN_VIA_CONVENTION", {**evidence, "matched_convention_point": cp.point, **cp_evidence}
        return "OUT_OF_DOMAIN", evidence
    return "DOMAIN_UNDECIDED", evidence


def _run_statement(server: AutoLeanServer, env: int, fact: ProposedFact, *, timeout: float) -> ValidationOutcome:
    """Shared tail for casework and decidable-membership facts, once domain/elaboration
    checks are clear: execute `fact.statement` against the true definition and classify."""
    check = run_checked(server, Command(cmd=fact.statement, env=env), timeout=timeout)
    evidence = {
        "command": fact.statement,
        "status": check.status.name,
        "elapsed_s": check.elapsed_s,
        "detail": check.detail,
    }
    if check.status is CheckStatus.PASSED:
        return ValidationOutcome(fact.id, Verdict.ACCEPTED, ReasonCode.CERTIFIED_TRUE_OF_GROUND_TRUTH, evidence=evidence)
    if check.status is CheckStatus.FAILED:
        return ValidationOutcome(
            fact.id, Verdict.REJECTED, ReasonCode.FALSE_OF_GROUND_TRUTH, detail=check.detail, evidence=evidence
        )
    return ValidationOutcome(fact.id, Verdict.REJECTED, ReasonCode.ERRORED, detail=check.detail, evidence=evidence)


def validate_casework_fact(
    server: AutoLeanServer,
    env: int,
    fact: ProposedFact,
    domain: DomainSpec,
    *,
    timeout: float | None = None,
) -> ValidationOutcome:
    """Validate a decidable-casework fact: domain containment, then execution against the
    true definition. A fact false of the ground truth, erroring, or timing out (folded into
    `ERRORED` by `harness.repl.run_checked`) is rejected with a recorded reason; a passing
    fact's execution evidence is recorded for the validation manifest."""
    timeout = timeout if timeout is not None else cfg.DECIDE_TIMEOUT
    if fact.mechanism != "decide":
        return ValidationOutcome(
            fact.id,
            Verdict.REJECTED,
            ReasonCode.MALFORMED_BAD_MECHANISM,
            detail=f"casework facts must have mechanism 'decide' (schema rule); got {fact.mechanism!r}",
        )

    domain_verdict, domain_evidence = check_domain_containment(server, env, domain, fact.domain_inputs, timeout=timeout)
    if domain_verdict == "OUT_OF_DOMAIN":
        return ValidationOutcome(
            fact.id,
            Verdict.REJECTED,
            ReasonCode.OUT_OF_DOMAIN,
            detail="fact's concrete input(s) fail the task's domain constraint",
            evidence={"domain_check": domain_evidence},
        )
    if domain_verdict == "DOMAIN_UNDECIDED":
        return ValidationOutcome(
            fact.id,
            Verdict.FLAGGED,
            ReasonCode.DOMAIN_UNDECIDED,
            detail="domain containment could not be mechanically decided for these inputs",
            evidence={"domain_check": domain_evidence},
        )

    outcome = _run_statement(server, env, fact, timeout=timeout)
    return ValidationOutcome(
        outcome.fact_id,
        outcome.verdict,
        outcome.reason_code,
        detail=outcome.detail,
        evidence={"domain_check": domain_evidence, "execution": outcome.evidence},
    )


def validate_membership_fact(
    server: AutoLeanServer,
    env: int,
    fact: ProposedFact,
    domain: DomainSpec,
    *,
    timeout: float | None = None,
) -> ValidationOutcome:
    """Validate a membership fact: malformed-tag checks, domain containment, instance
    elaboration, then (mechanism `decide`) execution against the true definition or
    (mechanism `proof`) structural-only sign-off as `PROVISIONALLY_VALIDATED` -- no prover
    exists yet to do more."""
    timeout = timeout if timeout is not None else cfg.DECIDE_TIMEOUT

    if fact.polarity not in ("accept", "reject"):
        return ValidationOutcome(
            fact.id,
            Verdict.REJECTED,
            ReasonCode.MALFORMED_BAD_POLARITY,
            detail=f"membership facts require polarity 'accept' or 'reject'; got {fact.polarity!r}",
        )
    if fact.polarity == "reject" and not fact.violated_property:
        return ValidationOutcome(
            fact.id,
            Verdict.REJECTED,
            ReasonCode.MALFORMED_MISSING_VIOLATED_PROPERTY,
            detail="reject-polarity membership facts require violated_property (schema §2.2 diagnostic tag)",
        )
    if fact.instance is None or fact.expected_type is None:
        return ValidationOutcome(
            fact.id,
            Verdict.REJECTED,
            ReasonCode.MALFORMED_MISSING_FIELD,
            detail="membership facts require both instance and expected_type",
        )

    domain_verdict, domain_evidence = check_domain_containment(server, env, domain, fact.domain_inputs, timeout=timeout)
    if domain_verdict == "OUT_OF_DOMAIN":
        return ValidationOutcome(
            fact.id,
            Verdict.REJECTED,
            ReasonCode.OUT_OF_DOMAIN,
            detail="fact's concrete input(s) fail the task's domain constraint",
            evidence={"domain_check": domain_evidence},
        )
    if domain_verdict == "DOMAIN_UNDECIDED":
        return ValidationOutcome(
            fact.id,
            Verdict.FLAGGED,
            ReasonCode.DOMAIN_UNDECIDED,
            detail="domain containment could not be mechanically decided for these inputs",
            evidence={"domain_check": domain_evidence},
        )

    elaborate_cmd = f"#check (({fact.instance}) : ({fact.expected_type}))"
    elaborate_check = run_checked(server, Command(cmd=elaborate_cmd, env=env), timeout=timeout)
    elaborate_evidence = {
        "command": elaborate_cmd,
        "status": elaborate_check.status.name,
        "elapsed_s": elaborate_check.elapsed_s,
        "detail": elaborate_check.detail,
    }
    if elaborate_check.status is not CheckStatus.PASSED:
        return ValidationOutcome(
            fact.id,
            Verdict.REJECTED,
            ReasonCode.INSTANCE_DOES_NOT_ELABORATE,
            detail=elaborate_check.detail or "instance term did not elaborate at its expected type",
            evidence={"domain_check": domain_evidence, "elaboration": elaborate_evidence},
        )

    if fact.mechanism == "decide":
        outcome = _run_statement(server, env, fact, timeout=timeout)
        return ValidationOutcome(
            outcome.fact_id,
            outcome.verdict,
            outcome.reason_code,
            detail=outcome.detail,
            evidence={
                "domain_check": domain_evidence,
                "elaboration": elaborate_evidence,
                "execution": outcome.evidence,
            },
        )
    if fact.mechanism == "proof":
        return ValidationOutcome(
            fact.id,
            Verdict.PROVISIONALLY_VALIDATED,
            ReasonCode.STRUCTURAL_ONLY_NO_PROVER,
            detail="instance elaborates and is well-formed; no prover exists yet to certify the proposition itself",
            evidence={"domain_check": domain_evidence, "elaboration": elaborate_evidence},
        )
    return ValidationOutcome(
        fact.id,
        Verdict.REJECTED,
        ReasonCode.MALFORMED_BAD_MECHANISM,
        detail=f"membership facts require mechanism 'decide' or 'proof'; got {fact.mechanism!r}",
    )


def validate_global_fact(
    server: AutoLeanServer,
    env: int,
    fact: ProposedFact,
    domain: DomainSpec,
    pinned_name: str,
    *,
    timeout: float | None = None,
) -> ValidationOutcome:
    """Validate a global fact, structurally only -- no prover exists yet
    (`docs/design/verifier_architecture_2026-07-20.md` §5), so the result is always
    `PROVISIONALLY_VALIDATED` at best, never `ACCEPTED`. Checks, in order: mechanism is
    `proof` (schema rule); at least one anchor is declared; the statement mentions the pinned
    name; the statement elaborates as a `Prop`; every named anchor theorem resolves in the
    pinned environment. Domain containment is structural-only (see
    `_global_domain_looks_unchecked`'s docstring) -- flagged for review, never rejected."""
    timeout = timeout if timeout is not None else cfg.DECIDE_TIMEOUT

    if fact.mechanism != "proof":
        return ValidationOutcome(
            fact.id,
            Verdict.REJECTED,
            ReasonCode.MALFORMED_BAD_MECHANISM,
            detail=f"global facts must have mechanism 'proof' (schema rule); got {fact.mechanism!r}",
        )
    if not fact.anchors:
        return ValidationOutcome(
            fact.id,
            Verdict.REJECTED,
            ReasonCode.MALFORMED_MISSING_ANCHORS,
            detail="global facts require at least one named Mathlib anchor theorem",
        )
    if pinned_name not in fact.statement:
        return ValidationOutcome(
            fact.id,
            Verdict.REJECTED,
            ReasonCode.DOES_NOT_MENTION_PINNED_NAME,
            detail=f"statement does not mention pinned name {pinned_name!r}",
        )

    prop_cmd = f"#check ({fact.statement} : Prop)"
    prop_check = run_checked(server, Command(cmd=prop_cmd, env=env), timeout=timeout)
    prop_evidence = {
        "command": prop_cmd,
        "status": prop_check.status.name,
        "elapsed_s": prop_check.elapsed_s,
        "detail": prop_check.detail,
    }
    if prop_check.status is not CheckStatus.PASSED:
        return ValidationOutcome(
            fact.id,
            Verdict.REJECTED,
            ReasonCode.PROPOSITION_DOES_NOT_ELABORATE,
            detail=prop_check.detail or "statement did not elaborate as a Prop",
            evidence={"proposition_check": prop_evidence},
        )

    anchor_evidence = {}
    missing_anchors = []
    for anchor in fact.anchors:
        anchor_cmd = f"#check {anchor}"
        anchor_check = run_checked(server, Command(cmd=anchor_cmd, env=env), timeout=timeout)
        anchor_evidence[anchor] = {
            "command": anchor_cmd,
            "status": anchor_check.status.name,
            "detail": anchor_check.detail,
        }
        if anchor_check.status is not CheckStatus.PASSED:
            missing_anchors.append(anchor)
    if missing_anchors:
        return ValidationOutcome(
            fact.id,
            Verdict.REJECTED,
            ReasonCode.ANCHOR_NOT_FOUND,
            detail=f"anchor theorem(s) not found in the pinned environment: {missing_anchors}",
            evidence={"proposition_check": prop_evidence, "anchor_checks": anchor_evidence},
        )

    if _global_domain_looks_unchecked(fact, domain):
        return ValidationOutcome(
            fact.id,
            Verdict.FLAGGED,
            ReasonCode.GLOBAL_DOMAIN_UNCHECKED,
            detail=(
                "domain constraint is non-trivial and does not appear (verbatim) in the statement -- "
                "structural heuristic only, not a real containment check; flagged for human review"
            ),
            evidence={"proposition_check": prop_evidence, "anchor_checks": anchor_evidence},
        )

    return ValidationOutcome(
        fact.id,
        Verdict.PROVISIONALLY_VALIDATED,
        ReasonCode.STRUCTURAL_ONLY_NO_PROVER,
        detail="proposition elaborates, mentions the pinned name, and every anchor resolves; no prover exists yet",
        evidence={"proposition_check": prop_evidence, "anchor_checks": anchor_evidence},
    )


def _global_domain_looks_unchecked(fact: ProposedFact, domain: DomainSpec) -> bool:
    """Structural-only domain check for global facts, per the task that introduced this
    module: "flag for review if the proposition visibly quantifies outside the domain; do not
    over-engineer this." What this actually does: if the domain constraint is the unrestricted
    `True` sentinel, or the statement contains no `∀` at all (nothing is being universally
    quantified, so there's nothing to visibly quantify outside the domain -- e.g. a fact about
    one concrete, already-fixed instance), there's nothing to flag. Otherwise, treat the
    constraint's text as present-or-absent verbatim inside the statement as a crude proxy for
    "this statement visibly carries the same restriction" -- e.g. a statement whose hypotheses
    literally contain `1 < b ∧ 1 < n` reads as guarded; one that doesn't gets flagged for a
    human to look at, not rejected outright (this checker cannot tell a genuinely-restricted-
    but-differently-phrased hypothesis from an actual out-of-domain universal, and doesn't try
    to)."""
    constraint = domain.constraint.strip()
    if constraint == "True":
        return False
    if "∀" not in fact.statement:
        return False
    return constraint not in fact.statement


def validate_fact(
    server: AutoLeanServer,
    env: int,
    fact: ProposedFact,
    domain: DomainSpec,
    pinned_name: str,
    *,
    timeout: float | None = None,
) -> ValidationOutcome:
    """Dispatch on `fact.type` to the matching validator."""
    if fact.type == "casework":
        return validate_casework_fact(server, env, fact, domain, timeout=timeout)
    if fact.type == "membership":
        return validate_membership_fact(server, env, fact, domain, timeout=timeout)
    if fact.type == "global":
        return validate_global_fact(server, env, fact, domain, pinned_name, timeout=timeout)
    return ValidationOutcome(
        fact.id,
        Verdict.REJECTED,
        ReasonCode.MALFORMED_UNKNOWN_TYPE,
        detail=f"unknown fact type {fact.type!r}; expected 'casework', 'membership', or 'global'",
    )


def validate_facts(
    server: AutoLeanServer,
    env: int,
    facts: list[ProposedFact],
    domain: DomainSpec,
    pinned_name: str,
    *,
    timeout: float | None = None,
) -> ValidationRun:
    """Validate a whole proposed fact suite against the true definition, in order."""
    return ValidationRun(
        outcomes=[validate_fact(server, env, fact, domain, pinned_name, timeout=timeout) for fact in facts]
    )
