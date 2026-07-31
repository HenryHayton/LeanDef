"""Dossier/domain consistency checker (contract §3.4, §8 item 8 -- added retroactively to the
contract's own inventory after the prior implementation session found it missing).

Implements the three sub-checks exactly as specified:

- (a) **Conventions↔prose matching**: every `domain.conventions` entry must have a matching
  prose sentence in the dossier's Conventions section. Matcher: `entry.statement` as a
  substring of that section, OR a keyword from `entry.note` appearing in it -- deliberately
  crude, matching this codebase's established precedent for "mechanical where possible, not
  over-engineered" text heuristics (`authoring.validate._global_domain_looks_unchecked`'s own
  "crude proxy" is the model for this one). Failures FLAG, never reject (contract's own rule).
- (b) **Executable worked examples**: the dossier's Worked Examples section is parsed for
  `Claim: ...` bullets, each optionally followed by a fenced ` ```lean ` command block. A
  bullet with a command executes that command against the TRUE definition (via
  `harness.repl.run_checked`, the same plumbing `authoring.validate` uses); a bullet with no
  command instead attempts the weaker check -- does the claim elaborate as a `Prop`? -- and
  falls back to `UNCHECKED_PROSE_EXAMPLE` (not a rejection) if it doesn't, since elaboration
  failure is ambiguous between "this actually was prose" and "malformed Lean," and the
  contract's own instruction is to not reject on that ambiguity. A genuine `FAILED` execution
  (not `ERRORED` -- infrastructure failure is never charged against the dossier) rejects.
- (c) **Signature injection integrity** (RETIRED signature-substring check, contract §3.4(c),
  2026-07-31 -- see the changelog note in docs/design/llm_io_contract_v1.md): the model is no
  longer asked to transcribe the pinned signature into the dossier's Signature section at all
  -- 8 identical transcription failures across two live sessions (mostly on implicit-binder-
  heavy signatures: Nat.binaryRec, Equiv.subtypePreimage, SimpleGraph.replaceVertex,
  Function.Embedding.setValue) proved this was asking the wrong worker to do a machine's job.
  `inject_pinned_signature` mechanically inserts the exact signature string into the dossier's
  Signature section, immediately after generation, at the ONE choke point both
  `authoring.pipeline` and `authoring.cleanup` call through; `check_signature_injection` is a
  trivial integrity assertion (is the injected block still there, byte-exact?) rather than a
  real check of model output -- the guarantee the old check existed to provide (round-trip
  sees the exact signature) is now delivered by construction. Failure (which should only ever
  mean a bug in the injection call site, never a model mistake) still rejects.

**Section-parsing convention, not itself part of the contract**: `extract_sections` splits
`dossier_md` on markdown ATX headers (`#`.."######"), matching against the six section names
contract §3.1 names (tolerant of leading numbering, e.g. "## 3. Conventions" or "## Conventions"
both resolve to `"conventions"`). The `Claim: ...` bullet + fenced-command convention for
worked examples is likewise not contract-specified; `authoring/prompts/dossier.txt` was updated
in the same pass to actually ask for it (see that file's own note on why) -- without a fixed
convention, (b) has nothing reliable to parse.
"""

import re
from dataclasses import dataclass, field

from lean_interact import Command

from authoring.facts import DomainSpec
from authoring.validate import ReasonCode
from harness import config as cfg
from harness.repl import run_checked
from harness.results import CheckStatus

# --- Section extraction (pure text, no REPL) --------------------------------------------------

_HEADER_LINE_RE = re.compile(r"^#{1,6}\s+(.*)$", re.MULTILINE)

_SECTION_KEYS = {
    "object": "object",
    "signature": "signature",
    "conventions": "conventions",
    "worked examples": "worked_examples",
    "boundaries": "boundaries",
    "not to be confused with": "not_to_be_confused_with",
}


def _normalize_header(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"^\d+[.)]\s*", "", text)  # strip leading "1. " / "1) " numbering
    return text.strip()


def extract_sections(dossier_md: str) -> dict[str, str]:
    """Split `dossier_md` into `{section_key: body_text}` by markdown ATX headers, keyed by
    the six names contract §3.1 fixes. Headers that don't match one of those six (or content
    before the first recognized header) are ignored -- this is a best-effort reader of an
    LLM-produced document, not a strict format validator."""
    matches = list(_HEADER_LINE_RE.finditer(dossier_md))
    sections: dict[str, str] = {}
    for i, m in enumerate(matches):
        key = _SECTION_KEYS.get(_normalize_header(m.group(1)))
        if key is None:
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(dossier_md)
        sections[key] = dossier_md[start:end].strip()
    return sections


# === (a) Conventions <-> prose matching =========================================================

_STOPWORDS = frozenset(
    {"the", "a", "an", "is", "are", "for", "of", "to", "and", "or", "by", "in", "on", "at",
     "this", "that", "with", "as", "its", "not", "has", "have", "was", "were", "over"}
)


def _note_keywords(note: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z']+", note.lower())
    return [w for w in words if len(w) >= 4 and w not in _STOPWORDS]


@dataclass(frozen=True)
class ConventionMatchResult:
    point: str | None
    matched: bool
    matcher: str  # "sentinel_skip" | "statement_substring" | "note_keyword" | "no_match"
    detail: str = ""


def check_conventions_prose_match(domain: DomainSpec, dossier_md: str) -> list[ConventionMatchResult]:
    conventions_text = extract_sections(dossier_md).get("conventions", "").lower()
    results = []
    for cp in domain.conventions:
        if cp.point is None and cp.statement is None:
            # NONE_DECLARED sentinel -- nothing concrete to match, same philosophy
            # authoring.facts.ConventionPoint's own docstring states for this case.
            results.append(ConventionMatchResult(point=None, matched=True, matcher="sentinel_skip"))
            continue
        if cp.statement and cp.statement.lower() in conventions_text:
            results.append(ConventionMatchResult(point=cp.point, matched=True, matcher="statement_substring"))
            continue
        keywords = _note_keywords(cp.note)
        hit = next((k for k in keywords if k in conventions_text), None)
        if hit is not None:
            results.append(
                ConventionMatchResult(point=cp.point, matched=True, matcher="note_keyword", detail=f"matched keyword {hit!r}")
            )
        else:
            results.append(
                ConventionMatchResult(
                    point=cp.point, matched=False, matcher="no_match",
                    detail=f"no statement substring or note keyword for point {cp.point!r} found in the dossier's Conventions section",
                )
            )
    return results


# === (b) Executable worked examples ============================================================

_CLAIM_BULLET_RE = re.compile(r"^\s*(?:[-*]|\d+[.)])\s*Claim:\s*(.+)\s*$", re.IGNORECASE | re.MULTILINE)
# Both fence delimiters may be indented (a fenced block nested under a list bullet, as the
# dossier prompt's own example shows) -- `[ \t]*` tolerates that on both the opening line
# (after the language tag) and the closing line (before the backticks).
_FENCE_RE = re.compile(r"```(?:lean4?)?[ \t]*\n(.*?)\n[ \t]*```", re.DOTALL)

EXECUTED = "EXECUTED"
ELABORATED = "ELABORATED"
UNCHECKED_PROSE_EXAMPLE = "UNCHECKED_PROSE_EXAMPLE"
EXECUTION_FAILED = "EXECUTION_FAILED"
ERRORED = "ERRORED"
MALFORMED_NO_WORKED_EXAMPLES = "MALFORMED_NO_WORKED_EXAMPLES"


@dataclass(frozen=True)
class WorkedExampleItem:
    claim: str
    command: str | None


def parse_worked_examples(dossier_md: str) -> list[WorkedExampleItem]:
    """`Claim: <text>` bullets in the Worked Examples section; a bullet immediately followed
    (before the next bullet) by a fenced ` ```lean ` block carries that block as its runnable
    command."""
    text = extract_sections(dossier_md).get("worked_examples", "")
    bullets = list(_CLAIM_BULLET_RE.finditer(text))
    items = []
    for i, m in enumerate(bullets):
        claim = m.group(1).strip()
        start = m.end()
        end = bullets[i + 1].start() if i + 1 < len(bullets) else len(text)
        chunk = text[start:end]
        fence_m = _FENCE_RE.search(chunk)
        items.append(WorkedExampleItem(claim=claim, command=fence_m.group(1).strip() if fence_m else None))
    return items


@dataclass(frozen=True)
class WorkedExampleCheck:
    claim: str
    kind: str
    detail: str = ""


def check_worked_examples(server, env: int, dossier_md: str, *, timeout: float | None = None) -> list[WorkedExampleCheck]:
    timeout = timeout if timeout is not None else cfg.DECIDE_TIMEOUT
    items = parse_worked_examples(dossier_md)
    if not items:
        return [
            WorkedExampleCheck(
                claim="", kind=MALFORMED_NO_WORKED_EXAMPLES,
                detail="no 'Claim: ...' bullets found in the dossier's Worked Examples section",
            )
        ]
    checks: list[WorkedExampleCheck] = []
    for item in items:
        if item.command:
            check = run_checked(server, Command(cmd=item.command, env=env), timeout=timeout)
            if check.status is CheckStatus.PASSED:
                checks.append(WorkedExampleCheck(item.claim, EXECUTED, detail=item.command))
            elif check.status is CheckStatus.FAILED:
                checks.append(WorkedExampleCheck(item.claim, EXECUTION_FAILED, detail=check.detail))
            else:
                checks.append(WorkedExampleCheck(item.claim, ERRORED, detail=check.detail))
        else:
            prop_cmd = f"#check ({item.claim} : Prop)"
            check = run_checked(server, Command(cmd=prop_cmd, env=env), timeout=timeout)
            if check.status is CheckStatus.PASSED:
                checks.append(WorkedExampleCheck(item.claim, ELABORATED))
            else:
                checks.append(
                    WorkedExampleCheck(
                        item.claim, UNCHECKED_PROSE_EXAMPLE,
                        detail="claim did not elaborate as a bare Prop; treated as prose, not rejected",
                    )
                )
    return checks


# === (c) Signature injection (mechanical, 2026-07-31) ==========================================

SIGNATURE_INJECTION_START = "<!-- PINNED-SIGNATURE:BEGIN -->"
SIGNATURE_INJECTION_END = "<!-- PINNED-SIGNATURE:END -->"


def _injected_signature_block(pinned_signature: str) -> str:
    return f"{SIGNATURE_INJECTION_START}\n{pinned_signature.strip()}\n{SIGNATURE_INJECTION_END}"


def inject_pinned_signature(dossier_md: str, pinned_signature: str) -> str:
    """Mechanically inserts the exact pinned signature into `dossier_md`'s Signature section,
    immediately after that section's header and before any model-authored prose -- the single
    choke point `authoring.pipeline._author_task_inner` and `authoring.cleanup.repair_one` both
    call right after `run_dossier_call` returns, before the dossier is used for anything else
    (consistency check, round trip, fact proposal). `dossier.txt`'s own prompt tells the model
    not to restate the signature itself, so this is the only place it ever enters the dossier.

    Raises `ValueError` if `dossier_md` has no recognizable Signature header (`extract_sections`'
    own header-matching, reused here rather than re-implemented) or already contains an injected
    block (this must run exactly once, on fresh model output -- a second call on already-
    injected text is a caller bug, not something to silently tolerate)."""
    if SIGNATURE_INJECTION_START in dossier_md:
        raise ValueError("dossier_md already contains an injected signature block -- inject_pinned_signature must run exactly once, on raw model output")
    for m in _HEADER_LINE_RE.finditer(dossier_md):
        if _SECTION_KEYS.get(_normalize_header(m.group(1))) == "signature":
            insertion_point = m.end()
            block = f"\n\n{_injected_signature_block(pinned_signature)}\n"
            return dossier_md[:insertion_point] + block + dossier_md[insertion_point:]
    raise ValueError("no 'Signature' section header found in dossier_md -- cannot inject pinned signature")


def check_signature_injection(pinned_signature: str, dossier_md: str) -> tuple[bool, str]:
    """Trivial integrity assertion, NOT a check of model output: is the exact, marker-delimited
    block `inject_pinned_signature` writes still present, byte-exact, in `dossier_md`? Matches
    on the marker-wrapped block specifically (not a bare substring search over the whole
    document), so a dossier whose model-authored prose happens to ALSO mention the pinned-
    signature text elsewhere is never confused with an intact injection."""
    ok = _injected_signature_block(pinned_signature) in dossier_md
    detail = "" if ok else f"injected signature block for {pinned_signature!r} missing or modified in dossier_md"
    return ok, detail


# === (d) Real-name leak (round-trip information barrier) =======================================


def _contains_real_name(text: str, forbidden_name: str) -> bool:
    """Word-boundary match of `forbidden_name` anywhere in `text`. The one shared matcher for
    every "does this text contain the real Mathlib name" check in this codebase's authoring
    layer -- `check_no_real_name_leak` (dossier body) and `check_round_trip_recalls_target`
    (round-trip candidate body) both call this rather than each rolling their own regex.
    Deliberately distinct from `authoring.parse._leaks_forbidden_name`'s plain substring match
    (no word-boundary) -- that one is a per-fact statement/instance/expected_type check with its
    own established semantics (2026-07-28 sweep confirmed it, see docs/deferred.md); this module
    is the word-boundary family. Two matchers, not three -- nothing here adds a third variant."""
    pattern = re.compile(r"\b" + re.escape(forbidden_name) + r"\b")
    return pattern.search(text) is not None


def check_no_real_name_leak(dossier_md: str, forbidden_name: str) -> tuple[bool, str]:
    """The dossier must never contain the real Mathlib name, word-boundary matched, ANYWHERE
    -- not just the Signature section `authoring.parse.parse_facts`'s own leak check covers for
    fact statements. `check_worked_examples` (b) above cannot substitute for this: a worked-
    example code block that (illegitimately) cites the real name instead of the task symbol
    still EXECUTES successfully against the true definition -- the real name genuinely is valid
    and true there -- so it registers as a clean `EXECUTED` pass either way. Confirmed
    empirically, not hypothetically: the 2026-07-28 slice run's dossier attempt 3 leaked
    `Nat.clog` into a worked-example command (`example : Nat.clog 2 8 = 3 := by decide`, next
    to a `Claim:` line correctly using `VTask.clog`) and would have sailed through (b) as
    EXECUTED had the response not separately been truncated by the max_tokens bug. This is the
    contract's round-trip information barrier (§5, §4): the dossier is the ONLY thing the blind
    round-trip call and the fact-proposal call ever see, so a leaked real name defeats the
    whole point of testing whether the dossier ALONE determines the object."""
    if not _contains_real_name(dossier_md, forbidden_name):
        return True, ""
    return False, (
        f"{ReasonCode.DOSSIER_LEAKS_REAL_NAME}: dossier contains the real Mathlib name "
        f"{forbidden_name!r} -- must use the task symbol exclusively, everywhere in the dossier"
    )


def check_round_trip_recalls_target(candidate_body: str, forbidden_name: str) -> bool:
    """Word-boundary match of the real Mathlib name against a round-trip candidate BODY
    (distinct from (d) above, which checks the dossier). Decided 2026-07-29, after a real
    round-trip attempt against `Nat.clog` returned the literal text `Nat.clog b n` -- the model
    recalling the true target's name from pretraining rather than deriving it from the dossier.
    Unlike the dossier check, this is NOT a rejection -- see `authoring.pipeline`'s
    `ROUND_TRIP_FLAG_RECALLED_TARGET`: detection ships the task, flagged, never retried, never
    rotated, since a clean round-trip pass on a recalled body is not evidence the dossier alone
    determines the object (the check abstains where it cannot measure). Full qualified name,
    word-boundary, string-level only -- deliberately NOT resolving whether a bare base-name
    reference (e.g. `clog` without the `Nat.` prefix) is a genuine reference to the real
    declaration in the candidate's elaborated body; see the report this decision was recorded
    in for why that's left unimplemented rather than guessed at."""
    return _contains_real_name(candidate_body, forbidden_name)


# === Top-level ===================================================================================


@dataclass(frozen=True)
class ConsistencyCheckResult:
    convention_matches: list[ConventionMatchResult] = field(default_factory=list)
    worked_example_checks: list[WorkedExampleCheck] = field(default_factory=list)
    signature_injection_ok: bool = False
    signature_detail: str = ""
    real_name_leak_ok: bool = True
    real_name_leak_detail: str = ""

    @property
    def passed(self) -> bool:
        """(b), (c), and (d) reject; (a) only flags -- contract §3.4's own split, (d) added
        this session as an equally-rejecting check (an information-barrier violation, not a
        soft prose-match miss)."""
        example_failure = any(
            c.kind in (EXECUTION_FAILED, MALFORMED_NO_WORKED_EXAMPLES) for c in self.worked_example_checks
        )
        return self.signature_injection_ok and not example_failure and self.real_name_leak_ok

    @property
    def flags(self) -> list[ConventionMatchResult]:
        return [m for m in self.convention_matches if not m.matched]


def check_dossier_consistency(
    server,
    env: int,
    pinned_signature: str,
    dossier_md: str,
    domain: DomainSpec,
    *,
    timeout: float | None = None,
    forbidden_name: str | None = None,
) -> ConsistencyCheckResult:
    """`forbidden_name` (the real Mathlib name, e.g. `"Nat.clog"`), when supplied, runs check
    (d) above. Defaults to `None` (no check) -- backward compatible with callers that have no
    real name to forbid (matching `authoring.parse.parse_facts`'s own `forbidden_name` default
    convention)."""
    convention_matches = check_conventions_prose_match(domain, dossier_md)
    worked_example_checks = check_worked_examples(server, env, dossier_md, timeout=timeout)
    signature_ok, signature_detail = check_signature_injection(pinned_signature, dossier_md)
    if forbidden_name is not None:
        real_name_leak_ok, real_name_leak_detail = check_no_real_name_leak(dossier_md, forbidden_name)
    else:
        real_name_leak_ok, real_name_leak_detail = True, ""
    return ConsistencyCheckResult(
        convention_matches=convention_matches,
        worked_example_checks=worked_example_checks,
        signature_injection_ok=signature_ok,
        signature_detail=signature_detail,
        real_name_leak_ok=real_name_leak_ok,
        real_name_leak_detail=real_name_leak_detail,
    )
