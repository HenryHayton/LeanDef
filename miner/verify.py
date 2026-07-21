"""Environment verification of pre-filter survivors.

Uses `harness.repl`'s hardened REPL plumbing (warm server, per-call timeouts, ERRORED
handling) -- nothing here reimplements that machinery, only builds new Lean commands on top
of it, per the task that introduced this module.

Every survivor is recorded, whether verification succeeds or not: a definition failing any
check stays in the output marked `included=False` with `exclusion_reason` set, so the
pipeline's behaviour is auditable rather than silently dropping things.

Known limitation, flagged rather than papered over (see the task that introduced this
module): true dependency-closure size is not computed. `lean_interact`'s `declarations` field
(which would give a clean constant list) only populates for declarations newly introduced in
a command -- `#print <existing name>` doesn't declare anything, so it stays empty even with
`declarations=True` (confirmed empirically before writing this). Re-submitting the printed
body as a throwaway declaration to get a real `.value.constants` list was considered and
rejected as too fragile for this stage (parsing pretty-printed output back into valid input,
multi-line bodies, re-elaboration edge cases). What's implemented instead is
`referenced_constants`: a best-effort text scan of `#print`'s pretty-printed body for
identifier-shaped tokens, minus bound variables and Lean keywords -- an immediate-reference
proxy, not a transitive closure, and not even a rigorous immediate-dependency list (notation
and operators aren't resolved to the constants they desugar to).
"""

import re
from dataclasses import dataclass, field

from lean_interact import AutoLeanServer, Command

from harness import config as cfg
from harness.repl import run_checked, warm_import
from harness.results import CheckStatus
from miner.scan import ScanHit

# Canonical trivial inputs, one per recognized argument type. Anything not listed here is
# "unsupported" -- the executability check is skipped and flagged, not guessed.
CANONICAL_INPUTS: dict[str, str] = {
    "ℕ": "0",
    "Nat": "0",
    "ℤ": "0",
    "Int": "0",
    "Bool": "true",
    "List ℕ": "[]",
    "List Nat": "[]",
    "List Bool": "[]",
    "Finset ℕ": "(∅ : Finset ℕ)",
}

_BRACKET_OPEN = "({[⦃"
_BRACKET_CLOSE = ")}]⦄"
_BRACKET_KIND = {"(": "explicit", "{": "implicit", "[": "instance", "⦃": "strict_implicit"}

_LEAN_KEYWORDS = frozenset(
    {
        "fun",
        "let",
        "in",
        "if",
        "then",
        "else",
        "match",
        "with",
        "do",
        "by",
        "from",
        "have",
        "show",
        "suffices",
        "this",
        "true",
        "false",
        "sorry",
    }
)

_IDENTIFIER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_'.]*")
_AXIOM_LIST_RE = re.compile(r"depends on axioms:\s*\[(.*?)\]")
_NO_AXIOMS_RE = re.compile(r"does not depend on any axioms")


@dataclass(frozen=True)
class BinderGroup:
    kind: str  # "explicit" | "implicit" | "instance" | "strict_implicit"
    names: list[str]
    type_text: str


@dataclass
class VerifiedDef:
    """The verification outcome for one pre-filter survivor."""

    name: str
    module_path: str
    source_text: str
    docstring: str | None
    mention_count: int

    included: bool
    exclusion_reason: str = ""

    elaborates: bool = False
    binder_groups: list[BinderGroup] = field(default_factory=list)
    explicit_arg_types: list[str] = field(default_factory=list)
    return_type: str = ""
    executable: bool | None = None  # None = not attempted (unsupported input type)
    executability_detail: str = ""
    exec_mechanism: str = "none"  # "eval" | "decide" | "none" -- see verify_definition
    output_decidable_eq: bool | None = None  # None when return_type == "Prop" (not meaningful there)
    referenced_constants: list[str] = field(default_factory=list)  # best-effort; see module docstring
    axioms: list[str] = field(default_factory=list)


def _strip_universe_annotation(rest: str) -> str:
    """Skip a leading universe-parameter annotation -- '.{u_1}' or '.{u₁, u₂}' -- that Lean's
    `#check` output attaches directly to a polymorphic declaration's name, before any binder
    groups or the return-type colon (e.g. `Pairwise.{u_1} {α : Type u_1} (r : ...) : Prop`).
    Without this, arity parsing silently found zero binder groups for *any* universe-
    polymorphic definition -- i.e. most of Mathlib -- because `_parse_binder_groups` bailed
    out on the unexpected leading '.'; this was the real cause of the 0-explicit-argument
    cases found reviewing harvest batch 1 (`Pairwise`, `Function.Bijective`, ...), not a
    section-variable-specific quirk as first guessed there."""
    if not rest.startswith(".{"):
        return rest
    depth = 0
    for idx, ch in enumerate(rest):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return rest[idx + 1 :]
    return rest  # unbalanced braces -- give up, let the caller's parse fail visibly


def _split_check_output(message: str, name: str) -> tuple[str, str] | None:
    """Split '#check' output '<name> <binder groups...> : <returnType>' into
    (binders_text, return_type), tracking bracket depth so a colon inside a binder group's
    type doesn't get mistaken for the top-level separator."""
    if not message.startswith(name):
        return None
    rest = _strip_universe_annotation(message[len(name) :])
    depth = 0
    for idx, ch in enumerate(rest):
        if ch in _BRACKET_OPEN:
            depth += 1
        elif ch in _BRACKET_CLOSE:
            depth -= 1
        elif ch == ":" and depth == 0:
            return rest[:idx].strip(), rest[idx + 1 :].strip()
    return None


def _split_top_level_arrows(type_text: str) -> list[str]:
    """Split a Lean type on top-level `→` arrows -- not ones nested inside brackets, e.g.
    `Set (Nat → Nat)` stays whole, but `List α → List α` splits into two. Used to recover
    trailing *anonymous* explicit arguments that `#check` shows as a bare arrow chain rather
    than a named `(x : T)` group -- typically arguments injected via an enclosing `variable`
    declaration rather than written in the `def`'s own header (see
    `docs/harvest_review_batch1.md`'s `List.orderedInsert`/`List.kerase` examples: their true
    arity, per `#check`, is higher than their source header alone shows)."""
    parts: list[str] = []
    depth = 0
    current: list[str] = []
    for ch in type_text:
        if ch in _BRACKET_OPEN:
            depth += 1
            current.append(ch)
        elif ch in _BRACKET_CLOSE:
            depth -= 1
            current.append(ch)
        elif ch == "→" and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    parts.append("".join(current).strip())
    return parts


def _parse_binder_groups(binders_text: str) -> list[BinderGroup]:
    groups: list[BinderGroup] = []
    i = 0
    n = len(binders_text)
    close_of = {"(": ")", "{": "}", "[": "]", "⦃": "⦄"}
    while i < n:
        ch = binders_text[i]
        if ch.isspace():
            i += 1
            continue
        if ch not in _BRACKET_OPEN:
            break  # unexpected content between groups -- stop rather than guess
        open_ch = ch
        close_ch = close_of[open_ch]
        depth = 1
        j = i + 1
        while j < n and depth > 0:
            if binders_text[j] == open_ch:
                depth += 1
            elif binders_text[j] == close_ch:
                depth -= 1
            j += 1
        inner = binders_text[i + 1 : j - 1]
        if ":" in inner:
            names_part, type_part = inner.split(":", 1)
            names = names_part.split()
            type_text = type_part.strip()
        else:
            names = []
            type_text = inner.strip()
        groups.append(BinderGroup(kind=_BRACKET_KIND[open_ch], names=names, type_text=type_text))
        i = j
    return groups


def _explicit_arg_types(groups: list[BinderGroup]) -> list[str]:
    types: list[str] = []
    for g in groups:
        if g.kind != "explicit":
            continue
        types.extend([g.type_text] * max(len(g.names), 1))
    return types


def _all_binder_names(groups: list[BinderGroup]) -> set[str]:
    names: set[str] = set()
    for g in groups:
        names.update(g.names)
    return names


def _extract_referenced_identifiers(printed_body: str, bound_names: set[str]) -> list[str]:
    body = printed_body.rsplit(":=", 1)[1] if ":=" in printed_body else printed_body
    seen: list[str] = []
    seen_set: set[str] = set()
    for tok in _IDENTIFIER_RE.findall(body):
        if tok in bound_names or tok in _LEAN_KEYWORDS or tok in seen_set:
            continue
        seen_set.add(tok)
        seen.append(tok)
    return seen


def _parse_axiom_message(data: str) -> frozenset[str] | None:
    """Mirrors `harness.admissibility`'s private axiom-message parser (duplicated rather
    than imported -- that parser is a private implementation detail of the admissibility
    gate; unifying them would be a reasonable follow-up, not done here)."""
    if _NO_AXIOMS_RE.search(data):
        return frozenset()
    m = _AXIOM_LIST_RE.search(data)
    if m is None:
        return None
    return frozenset(n.strip() for n in m.group(1).split(",") if n.strip())


def verify_definition(
    server: AutoLeanServer,
    base_env: int,
    hit: ScanHit,
    *,
    timeout: float | None = None,
) -> VerifiedDef:
    """Interrogate the live environment about one pre-filter survivor. Always returns a
    `VerifiedDef`; `included=False` with `exclusion_reason` set means it failed some check,
    not that anything raised."""
    timeout = timeout if timeout is not None else cfg.DECIDE_TIMEOUT
    result = VerifiedDef(
        name=hit.name,
        module_path=hit.module_path,
        source_text=hit.source_text,
        docstring=hit.docstring,
        mention_count=hit.mention_count,
        included=False,
    )

    check = run_checked(server, Command(cmd=f"#check {hit.name}", env=base_env), timeout=timeout)
    if check.status is not CheckStatus.PASSED or check.raw_response is None:
        result.exclusion_reason = f"does not elaborate: {check.detail or check.status.name}"
        return result
    result.elaborates = True

    info_messages = [m.data for m in check.raw_response.messages if m.severity == "info"]
    split = None
    for msg in info_messages:
        split = _split_check_output(msg, hit.name)
        if split is not None:
            break
    if split is None:
        result.exclusion_reason = f"could not parse '#check' output: {info_messages!r}"
        return result

    binders_text, raw_return_type = split
    result.binder_groups = _parse_binder_groups(binders_text)

    # The text after the last named binder group may itself be a bare arrow chain (trailing
    # *anonymous* explicit arguments -- see `_split_top_level_arrows`'s docstring). All but
    # the last segment are additional explicit argument types; the last segment is the true
    # return type.
    arrow_segments = _split_top_level_arrows(raw_return_type)
    trailing_arg_types, result.return_type = arrow_segments[:-1], arrow_segments[-1]
    result.explicit_arg_types = _explicit_arg_types(result.binder_groups) + trailing_arg_types

    unknown_types = [t for t in result.explicit_arg_types if t not in CANONICAL_INPUTS]
    if unknown_types:
        result.executable = None
        result.executability_detail = f"unsupported input type(s), not attempted: {unknown_types}"
    else:
        args = " ".join(f"({CANONICAL_INPUTS[t]})" for t in result.explicit_arg_types)
        eval_cmd = f"#eval {hit.name}" + (f" {args}" if args else "")
        eval_result = run_checked(server, Command(cmd=eval_cmd, env=base_env), timeout=timeout)
        result.executable = eval_result.status is CheckStatus.PASSED
        result.executability_detail = "" if result.executable else eval_result.detail

    is_prop = result.return_type.strip() == "Prop"
    if is_prop:
        result.exec_mechanism = "decide" if result.executable is True else "none"
        # DecidableEq(Prop) is not a real Mathlib instance, so this check is meaningless for
        # every Prop-valued definition regardless of whether the *specific proposition* it
        # produces is individually decidable -- see docs/harvest_review_batch1.md's
        # Nat.Prime example and miner/proxies.py's module docstring. Skipped entirely rather
        # than run-and-ignore, to save the (always-failing) REPL round-trip.
        result.output_decidable_eq = None
    else:
        result.exec_mechanism = "eval" if result.executable is True else "none"
        decidable_cmd = f"example : DecidableEq ({result.return_type}) := inferInstance"
        decidable_result = run_checked(server, Command(cmd=decidable_cmd, env=base_env), timeout=timeout)
        result.output_decidable_eq = decidable_result.status is CheckStatus.PASSED

    print_result = run_checked(server, Command(cmd=f"#print {hit.name}", env=base_env), timeout=timeout)
    if print_result.status is CheckStatus.PASSED and print_result.raw_response is not None:
        print_messages = [m.data for m in print_result.raw_response.messages if m.severity == "info"]
        if print_messages:
            result.referenced_constants = _extract_referenced_identifiers(
                print_messages[0], bound_names=_all_binder_names(result.binder_groups)
            )

    axiom_result = run_checked(server, Command(cmd=f"#print axioms {hit.name}", env=base_env), timeout=timeout)
    if axiom_result.status is CheckStatus.PASSED and axiom_result.raw_response is not None:
        for msg in axiom_result.raw_response.messages:
            if msg.severity != "info":
                continue
            axioms = _parse_axiom_message(msg.data)
            if axioms is not None:
                result.axioms = sorted(axioms)
                break

    result.included = True
    return result


def verify_all(
    server: AutoLeanServer,
    base_env: int,
    hits: list[ScanHit],
    *,
    timeout: float | None = None,
) -> list[VerifiedDef]:
    """Verify every hit against the SAME `base_env`, with no recovery if that environment
    dies partway through (see `verify_all_with_recovery` for that). Kept simple and
    predictable for tests and small batches; `harness.harvest` uses the recovering version
    for real runs, since a real corpus is exactly where this bites (see that function's
    docstring)."""
    return [verify_definition(server, base_env, hit, timeout=timeout) for hit in hits]


_ENV_DEATH_MARKERS = ("Unknown environment", "unknown environment")


def _looks_like_env_death(exclusion_reason: str) -> bool:
    return any(marker in exclusion_reason for marker in _ENV_DEATH_MARKERS)


def verify_all_with_recovery(
    server: AutoLeanServer,
    initial_base_env: int,
    hits: list[ScanHit],
    *,
    timeout: float | None = None,
    imports: list[str] | None = None,
    warmup_timeout: float | None = None,
) -> list[VerifiedDef]:
    """Like `verify_all`, but detects when the shared base environment has died mid-batch
    and re-establishes a fresh one instead of letting every remaining candidate cascade-fail.

    This is a real failure mode, not a hypothetical one: `harness.repl.run_checked` already
    documents that a server restart invalidates every environment id from before it, and this
    stage's own first full-corpus run hit it -- a single slow check (past whatever timeout
    that run used) killed and restarted the server, and every subsequent candidate then
    failed with a REPL-level "Unknown environment" error, misleadingly recorded as "does not
    elaborate." This function catches that specific signature and recovers by re-importing
    and continuing with the new environment, rather than losing the rest of the batch to one
    slow definition.
    """
    base_env = initial_base_env
    results: list[VerifiedDef] = []
    for hit in hits:
        result = verify_definition(server, base_env, hit, timeout=timeout)
        if not result.included and _looks_like_env_death(result.exclusion_reason):
            reimport = warm_import(server, imports=imports, timeout=warmup_timeout)
            if reimport.status is CheckStatus.PASSED:
                base_env = reimport.env
                result = verify_definition(server, base_env, hit, timeout=timeout)
        results.append(result)
    return results
