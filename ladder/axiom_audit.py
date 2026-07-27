"""The fact-proof axiom rule (reward doc §3.3) -- "Not yet implemented in this codebase
(confirmed by the read-only repo audit)" per that doc's own text; this module is the first.

Every proof any tier produces -- tier-2 tactics through tier-5 LLM proofs -- passes a
no-`sorry` + axiom-closure check before its fact is marked CERTIFIED. The permitted set is the
standard Mathlib triple, matching `harness.admissibility.STANDARD_MATHLIB_AXIOMS` in VALUE but
INTENTIONALLY NOT IMPORTED from there: the reward doc is explicit that this is "distinct from
the candidate's own admissibility baseline (§1), which continues to govern the candidate
declaration alone." A fact-proof audit and a candidate-declaration audit happening to permit
the same three axioms today is a coincidence of Mathlib's own dependency structure, not a
shared concept -- importing one constant from the other would wire two independently-evolvable
rules together by accident. The `#print axioms` regex parser IS duplicated (not imported) from
`harness.admissibility`, for the same reason `miner.discharge`'s own module docstring already
gives for duplicating `_looks_like_env_death`: a small private detector, copied rather than
reached-for across a module boundary.
"""

import re
from dataclasses import dataclass

from lean_interact import AutoLeanServer, Command

from harness import config as cfg
from harness.repl import run_checked
from harness.results import CheckStatus

PERMITTED_FACT_PROOF_AXIOMS: frozenset[str] = frozenset({"propext", "Classical.choice", "Quot.sound"})

_AXIOM_LIST_RE = re.compile(r"depends on axioms:\s*\[(.*?)\]")
_NO_AXIOMS_RE = re.compile(r"does not depend on any axioms")

# Lean 4 reports a proof containing `sorry` as depending on the axiom `sorryAx` -- confirmed
# empirically against the real REPL before relying on it (see this session's test suite, which
# plants a genuine `sorry` and asserts this fires), not assumed from documentation alone.
_SORRY_AXIOM = "sorryAx"


def _parse_axioms(message_data: str) -> frozenset[str] | None:
    """Parse one `#print axioms` info message. Returns `None` if it matches neither known
    shape -- the caller treats that as a failed audit rather than guessing."""
    if _NO_AXIOMS_RE.search(message_data):
        return frozenset()
    m = _AXIOM_LIST_RE.search(message_data)
    if m is None:
        return None
    return frozenset(n.strip() for n in m.group(1).split(",") if n.strip())


@dataclass(frozen=True)
class AxiomAuditResult:
    passed: bool
    axioms: frozenset[str]
    excess_axioms: frozenset[str]
    has_sorry: bool
    detail: str = ""


def audit_proof_axioms(
    server: AutoLeanServer,
    env: int,
    theorem_name: str,
    *,
    permitted: frozenset[str] | None = None,
    timeout: float | None = None,
) -> AxiomAuditResult:
    """`theorem_name` must already be a declared theorem in `env` -- `#print axioms` inspects a
    real declaration, not a bare command text, so the caller (`ladder.tier2`/`ladder.adjudicate`)
    declares the discharging script under a name before calling this, rather than this function
    re-running the proof itself (search happens once, per §3.2 -- an audit is not a second
    search)."""
    permitted = permitted if permitted is not None else PERMITTED_FACT_PROOF_AXIOMS
    timeout = timeout if timeout is not None else cfg.DECIDE_TIMEOUT

    check = run_checked(server, Command(cmd=f"#print axioms {theorem_name}", env=env), timeout=timeout)
    if check.status is not CheckStatus.PASSED:
        return AxiomAuditResult(
            passed=False, axioms=frozenset(), excess_axioms=frozenset(), has_sorry=False,
            detail=f"could not check axioms: {check.detail}",
        )

    raw = check.raw_response
    info_messages = [m.data for m in raw.messages if m.severity == "info"] if raw is not None else []
    axioms: frozenset[str] | None = None
    for data in info_messages:
        parsed = _parse_axioms(data)
        if parsed is not None:
            axioms = parsed
            break

    if axioms is None:
        return AxiomAuditResult(
            passed=False, axioms=frozenset(), excess_axioms=frozenset(), has_sorry=False,
            detail=f"could not parse `#print axioms` output: {info_messages!r}",
        )

    has_sorry = _SORRY_AXIOM in axioms
    excess = axioms - permitted
    passed = not has_sorry and not excess
    detail_parts = []
    if has_sorry:
        detail_parts.append("proof contains `sorry`")
    if excess:
        detail_parts.append(f"excess axioms beyond the permitted set: {sorted(excess)}")
    return AxiomAuditResult(
        passed=passed, axioms=axioms, excess_axioms=excess, has_sorry=has_sorry,
        detail="; ".join(detail_parts),
    )
