"""Selection-time preflight: does a candidate name's pinned signature survive print-then-
reparse? Promoted from the batch-50 scratchpad session's `gather_and_validate_50.py`
(2026-07-28/29), generalized to run against any name list rather than one hardcoded batch.

**Mechanism**: `#check <name>` against the warm base environment gives the real, fully-
elaborated type Lean's pretty-printer produces; `check_output_to_pinned_type` converts that
printed text into a standalone pi-type expression (stripping the leading `Name.{universes}`,
joining each binder group with `->`); the result is spliced as `def <task_symbol> : <type> :=
sorry` and must elaborate cleanly. A name whose printed type can't be reparsed this way cannot
be pinned as a task signature at all -- this is a hard, mechanical precondition for authoring,
independent of the curation questions below.

**Does NOT change pp options.** The 2026-07-29 recursor-class pseudo-gate decision
(`miner/output/excluded_recursor_class.json`) stands on its own terms: default printing (no
`pp.proofs true` or similar) is the current policy, and a `pp_elision` failure here remains a
mechanical exclusion category, not itself evidence a definition is a bad task target -- that
determination, for the 6 names it was made for, was recorded separately in curation as a
deliberate, provisional, human decision. See that JSON file's own docstring-equivalent
`summary`/`provisional_note` fields for the full reasoning; this module does not re-decide it,
and a future caller finding a NEW `pp_elision` name here should not assume the same curation
verdict applies without that same deliberation.
"""

import re
from dataclasses import dataclass
from pathlib import Path

from lean_interact import AutoLeanServer, Command

from authoring.task_symbol import task_symbol_for
from harness.repl import run_checked
from harness.results import CheckStatus

FAIL_PP_ELISION = "pp_elision"
FAIL_STUCK_METAVARIABLE = "stuck_metavariable"
FAIL_CRASH = "crash"
FAIL_INVALID_SYMBOL = "invalid_symbol"
FAIL_OTHER = "other"

_UNIV_RE = re.compile(r"^\.\{[^}]*\}")


def _split_top_level_groups(text: str) -> list[str]:
    """Split '{a} [b] (c) : Result' into ['{a}', '[b]', '(c)', ': Result'], respecting
    bracket nesting (e.g. a binder type containing its own parens)."""
    groups = []
    depth = 0
    start = 0
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c in "({[":
            depth += 1
        elif c in ")}]":
            depth -= 1
            if depth == 0:
                groups.append(text[start:i + 1].strip())
                start = i + 1
        elif c == ":" and depth == 0:
            tail = text[i:].strip()
            if tail:
                groups.append(tail)
            start = n
            break
        i += 1
    remainder = text[start:].strip()
    if remainder and remainder not in groups:
        if remainder.startswith(":"):
            groups.append(remainder)
    return [g for g in groups if g]


def check_output_to_pinned_type(check_text: str, real_name: str) -> str:
    """Convert '#check <name>' output (e.g. 'Monotone.{u, v} {a} [b] (c) : Prop') into a
    standalone pi-type expression usable as 'def X : <this> := body' -- each binder group
    chained with the Lean4 Pi-arrow ' -> ' (bare ASCII arrow, always accepted)."""
    text = check_text.strip()
    if not text.startswith(real_name):
        raise ValueError(f"unexpected #check output shape (doesn't start with {real_name!r}): {text!r}")
    rest = text[len(real_name):]
    m = _UNIV_RE.match(rest)
    if m:
        rest = rest[m.end():]
    rest = rest.strip()
    groups = _split_top_level_groups(rest)
    parts = []
    for g in groups:
        if g.startswith(":"):
            parts.append(g[1:].strip())
        else:
            parts.append(g)
    return " -> ".join(parts)


@dataclass(frozen=True)
class PreflightResult:
    name: str
    status: str  # "pass" | "fail"
    category: str | None = None  # one of the FAIL_* constants above, only when status == "fail"
    detail: str = ""
    pinned_type: str | None = None  # only when status == "pass"
    task_symbol: str | None = None  # only when status == "pass"


def _categorize(detail: str) -> str:
    lowered = detail.lower()
    if "synthesize placeholder" in lowered:
        return FAIL_PP_ELISION
    if "stuck" in lowered and "typeclass" in lowered:
        return FAIL_STUCK_METAVARIABLE
    return FAIL_OTHER


def run_preflight(names: list[str], server: AutoLeanServer, env: int, *, timeout: float = 30.0) -> list[PreflightResult]:
    """Run the print-then-reparse check for every name in `names` against the given warm
    environment. Never raises for an individual name's failure -- every failure mode becomes a
    `PreflightResult(status="fail", ...)` instead, since one bad name must not stop the rest of
    a batch's preflight from running."""
    results = []
    for name in names:
        try:
            symbol = task_symbol_for(name)
        except ValueError as e:
            results.append(PreflightResult(name, "fail", FAIL_INVALID_SYMBOL, str(e)))
            continue

        check = run_checked(server, Command(cmd=f"#check {name}", env=env), timeout=timeout)
        if check.status is CheckStatus.ERRORED:
            results.append(PreflightResult(name, "fail", FAIL_CRASH, check.detail))
            continue
        if check.status is not CheckStatus.PASSED or check.raw_response is None:
            results.append(PreflightResult(name, "fail", FAIL_OTHER, check.detail or "no #check output"))
            continue
        infos = [m.data for m in check.raw_response.messages]
        if not infos:
            results.append(PreflightResult(name, "fail", FAIL_OTHER, "no #check output"))
            continue
        raw = infos[0]

        try:
            pinned_type = check_output_to_pinned_type(raw, name)
        except Exception as e:  # noqa: BLE001 -- a malformed #check shape must not crash the batch
            results.append(PreflightResult(name, "fail", FAIL_OTHER, f"conversion failed: {e}"))
            continue

        validate_cmd = f"def {symbol} : {pinned_type} := sorry"
        vcheck = run_checked(server, Command(cmd=validate_cmd, env=env), timeout=timeout)
        if vcheck.status is CheckStatus.ERRORED:
            results.append(PreflightResult(name, "fail", FAIL_CRASH, vcheck.detail, pinned_type, symbol))
            continue
        if vcheck.status is not CheckStatus.PASSED:
            results.append(PreflightResult(name, "fail", _categorize(vcheck.detail or ""), vcheck.detail, pinned_type, symbol))
            continue

        results.append(PreflightResult(name, "pass", pinned_type=pinned_type, task_symbol=symbol))
    return results


def write_preflight_json(results: list[PreflightResult], output_path: Path) -> None:
    import json
    from dataclasses import asdict

    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {r.name: {k: v for k, v in asdict(r).items() if k != "name"} for r in results}
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def load_preflight_json(path: Path) -> dict[str, PreflightResult]:
    import json

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {name: PreflightResult(name=name, **fields) for name, fields in data.items()}
