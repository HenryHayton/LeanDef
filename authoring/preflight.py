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

**Decidability probe (2026-07-30)**: for every PASSing name whose pinned type ends in a bare
`Prop`, `probe_decidability` additionally attempts to synthesize `Decidable` for a
representative fully-applied instance, against a fresh `@[reducible]` splice of the real
definition (`docs/design/llm_io_contract_v1.md` §4.4's reducibility fix -- this probe is one of
its two consumers, alongside the truth/candidate splice itself). Recorded as `decidability`
(`DECIDABLE`/`UNDECIDABLE`/`INDETERMINATE`) on `PreflightResult`; see `probe_decidability`'s own
docstring for exactly which shapes are mechanically resolvable vs. `INDETERMINATE` (not guessed
at). Feeds the classification and fact-proposal calls' decide-vs-proof guidance and the
parse-time rule restricting `mechanism: decide` to `DECIDABLE` Props.

**Full truth-splice (2026-07-31, the "Harness Fixes" session)**: the `:= sorry` check above
only validates the TYPE reparses -- it never once spliced the REAL body. That gap is exactly
what let `Monotone`/`DependsOn`/`Function.extend` through preflight clean and then rotate at
`truth_splice` in a real, live, paid batch run (`harness.signature.PinnedSignature
.splice_real_name`'s own docstring has the full root-cause story: a bare-unqualified-real-name
self-reference collision for `Monotone`/`DependsOn`, a genuine noncomputability for
`Function.extend`). Every PASSing name now also gets a real `splice_real_name` attempt (the
exact same call `authoring.pipeline`'s truth-splice stage makes); a failure here is
`FAIL_TRUTH_SPLICE`, at $0 (no Bedrock call was ever at risk), catching this whole failure
class at selection time instead of mid-batch.
"""

import re
from dataclasses import dataclass
from pathlib import Path

from lean_interact import AutoLeanServer, Command

from authoring.task_symbol import task_symbol_for
from harness.repl import run_checked
from harness.results import CheckStatus
from harness.signature import PinnedSignature
from harness.scoring import splice_real_name

FAIL_PP_ELISION = "pp_elision"
FAIL_STUCK_METAVARIABLE = "stuck_metavariable"
FAIL_TRUTH_SPLICE = "truth_splice"  # 2026-07-31: the FULL real-body splice, distinct from the
# type-only (":= sorry") check above -- see run_preflight's own note on why this exists.
FAIL_CRASH = "crash"
FAIL_INVALID_SYMBOL = "invalid_symbol"
FAIL_OTHER = "other"

DECIDABLE = "decidable"
UNDECIDABLE = "undecidable"
INDETERMINATE = "indeterminate"

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


# --- Decidability probe (2026-07-30) -----------------------------------------------------
#
# Mechanical sizing of which Prop-valued names support decide-mechanism facts and executable
# worked examples (only `decidable` ones can) vs. which are structural-only (`undecidable`,
# `indeterminate`) -- see `docs/design/llm_io_contract_v1.md` §4.1/§4.4 and the 41-name batch's
# Gate 2 (`Nat.ModEq`) report for why this matters. Deliberately minimal: only attempted for a
# return type that is exactly `Prop` with NO further curried tail (`Relation.Map`-shaped
# curried-Prop returns are conservatively treated as `indeterminate` here, not misclassified as
# non-Prop -- see this probe's own docstring) and only when every explicit binder's type has a
# known simple concrete value below; anything else is `indeterminate` rather than guessed at,
# per this task's own explicit instruction.
_SIMPLE_CONCRETE_VALUES: dict[str, str] = {
    "ℕ": "0",  # the only type any of the batch-41 Prop-valued names' explicit binders actually
    # use (confirmed by inspection, 2026-07-30) -- extend only when a real name needs another
    # type, not speculatively for types nothing here has been run against.
}


def _parse_binder_groups(pinned_type: str) -> list[tuple[str, list[str], str]]:
    """`(kind, names, type_text)` for each top-level bracketed binder group in a `pinned_type`
    string built by `check_output_to_pinned_type` (bracket kind preserved there: `(` explicit,
    `{` implicit, `[` instance). The trailing, unbracketed return-type fragment is not a binder
    group and is not returned here -- callers read the return type from `pinned_type`'s own
    tail (`pinned_type.split(" -> ")[-1]`) directly."""
    groups: list[tuple[str, list[str], str]] = []
    kind_by_char = {"(": "explicit", "{": "implicit", "[": "instance"}
    for part in pinned_type.split(" -> "):
        part = part.strip()
        if not part or part[0] not in kind_by_char:
            continue  # the trailing return-type fragment (never bracketed), or malformed input
        kind = kind_by_char[part[0]]
        inner = part[1:-1] if part and part[-1] in ")}]" else part[1:]
        name_part, sep, type_part = inner.partition(":")
        names = name_part.split() if sep else []
        groups.append((kind, names, type_part.strip() if sep else name_part.strip()))
    return groups


def probe_decidability(
    name: str, pinned_type: str, symbol: str, server: AutoLeanServer, env: int, *, timeout: float = 30.0
) -> tuple[str, str]:
    """Attempt to synthesize `Decidable` for a representative fully-applied instance of a
    Prop-valued name, against a fresh `@[reducible]` splice of the REAL definition
    (`harness.scoring.splice_real_name` -- root-qualified and noncomputable-retry-aware, the
    same call `run_preflight`'s own full truth-splice check and `authoring.pipeline`'s
    truth-splice stage make, so this probe can't hit the bare-unqualified-name self-reference
    bug `PinnedSignature.splice_real_name`'s docstring describes).

    Returns `(decidability, detail)`, `decidability` one of `DECIDABLE`/`UNDECIDABLE`/
    `INDETERMINATE`. `INDETERMINATE` covers every case this probe cannot mechanically resolve
    without guessing: a return type that isn't a bare `Prop` (including a further-curried
    `... -> Prop` tail, e.g. `Relation.Map` -- conservatively not attempted, not misjudged),
    any implicit/instance binder (no mechanically derivable concrete value), or an explicit
    binder whose type isn't in `_SIMPLE_CONCRETE_VALUES`. Never raises for a REPL-level failure
    (splice error, timeout) -- folded into `INDETERMINATE` with the detail preserved, since an
    infrastructure hiccup here must not be confused with a genuine `UNDECIDABLE` verdict."""
    tail = pinned_type.split(" -> ")[-1].strip()
    if tail != "Prop":
        return INDETERMINATE, (
            "return type is not a bare 'Prop' (either not Prop-valued, or a further-curried "
            f"tail this probe does not attempt): {tail!r}"
        )

    groups = _parse_binder_groups(pinned_type)
    if any(kind in ("implicit", "instance") for kind, _, _ in groups):
        return INDETERMINATE, "has implicit/instance binders -- no mechanically derivable concrete instantiation"

    values: list[str] = []
    for _, names, type_text in groups:
        if type_text not in _SIMPLE_CONCRETE_VALUES:
            return INDETERMINATE, f"explicit binder type {type_text!r} has no known simple concrete value"
        values.extend([_SIMPLE_CONCRETE_VALUES[type_text]] * len(names))

    sig = PinnedSignature(name=symbol, type_sig=pinned_type)
    splice_check = splice_real_name(server, env, sig, name, timeout=timeout)
    if splice_check.status is not CheckStatus.PASSED:
        return INDETERMINATE, f"reducible splice failed: {splice_check.detail}"

    args = " ".join(values)
    probe_cmd = f"#check (inferInstance : Decidable ({symbol} {args}))"
    probe_check = run_checked(server, Command(cmd=probe_cmd, env=splice_check.env), timeout=timeout)
    if probe_check.status is CheckStatus.PASSED:
        return DECIDABLE, f"synthesized Decidable ({symbol} {args})"
    if probe_check.status is CheckStatus.FAILED:
        return UNDECIDABLE, probe_check.detail or "Decidable instance synthesis failed"
    return INDETERMINATE, f"probe errored: {probe_check.detail}"


@dataclass(frozen=True)
class PreflightResult:
    name: str
    status: str  # "pass" | "fail"
    category: str | None = None  # one of the FAIL_* constants above, only when status == "fail"
    detail: str = ""
    pinned_type: str | None = None  # only when status == "pass"
    task_symbol: str | None = None  # only when status == "pass"
    decidability: str | None = None  # DECIDABLE|UNDECIDABLE|INDETERMINATE, only for a
    # Prop-valued name that passed; None for anything else (never attempted).
    decidability_detail: str = ""


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

        # Full truth-splice (2026-07-31): the type-only check above says nothing about whether
        # the REAL body splices under it -- exactly the gap that let Monotone/DependsOn/
        # Function.extend through preflight clean. Real REPL check, real splice_real_name
        # (root-qualified, noncomputable-retry-aware) -- the same call the pipeline itself
        # makes, so a name that passes THIS is confirmed at $0, not discovered mid-batch.
        sig = PinnedSignature(name=symbol, type_sig=pinned_type)
        tcheck = splice_real_name(server, env, sig, name, timeout=timeout)
        if tcheck.status is CheckStatus.ERRORED:
            results.append(PreflightResult(name, "fail", FAIL_CRASH, tcheck.detail, pinned_type, symbol))
            continue
        if tcheck.status is not CheckStatus.PASSED:
            results.append(PreflightResult(name, "fail", FAIL_TRUTH_SPLICE, tcheck.detail, pinned_type, symbol))
            continue

        decidability, decidability_detail = None, ""
        if pinned_type.split(" -> ")[-1].strip() == "Prop":
            decidability, decidability_detail = probe_decidability(name, pinned_type, symbol, server, env, timeout=timeout)

        results.append(PreflightResult(
            name, "pass", pinned_type=pinned_type, task_symbol=symbol,
            decidability=decidability, decidability_detail=decidability_detail,
        ))
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
