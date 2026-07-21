"""Best-effort name -> defining-module index over the full Mathlib source tree.

Used by `miner.gates`' dependency-vocabulary-tier gate to resolve a `VerifiedDef`'s
`referenced_constants` (themselves a best-effort extraction -- see `miner.verify`'s module
docstring) to the module each name is declared in, so the gate can check whether that module
falls inside the common-vocabulary list. A textual heuristic, not an elaborator-backed lookup
-- consistent with `miner.scan`'s own pre-filter, and for the same reason: this only decides
which candidates are worth a live-REPL round-trip in `miner.verify`, so an occasional wrong
answer here costs at most a mis-gated candidate, not a wrong fact anywhere downstream.

Known limitations: only scans `def | theorem | lemma | instance | abbrev | structure | class |
inductive` declaration lines, tracking `namespace`/`section` nesting the same (simplified) way
`miner.scan` does -- `open` declarations and section `variable`-injected context are not
resolved, and a name declared under multiple namespaces sharing a bare identifier resolves to
whichever file this scan reaches first (sorted path order), not necessarily the one a given
reference actually means. Good enough for a gate whose failure mode is a re-tunable threshold
miss, not a correctness bug elsewhere.
"""

import re
from pathlib import Path

_NAMESPACE_RE = re.compile(r"^namespace\s+(\S+)\s*$")
_SECTION_RE = re.compile(r"^section(?:\s+(\S+))?\s*$")
_END_RE = re.compile(r"^end(?:\s+(\S+))?\s*$")

_ID_FIRST = r"[^\W\d]"
_ID_REST = r"[\w'!?.]"

_DECL_RE = re.compile(
    r"^(?:private\s+|protected\s+|noncomputable\s+|@\[.*?\]\s*)*"
    r"(?:def|theorem|lemma|instance|abbrev|structure|class|inductive)\s+"
    rf"(?P<name>{_ID_FIRST}{_ID_REST}*)"
)


def _index_text(text: str, module_path: str, index: dict[str, str]) -> None:
    namespace_stack: list[str] = []
    for raw_line in text.split("\n"):
        stripped = raw_line.strip()
        if not stripped:
            continue
        ns_match = _NAMESPACE_RE.match(stripped)
        if ns_match:
            namespace_stack.append(ns_match.group(1))
            continue
        sec_match = _SECTION_RE.match(stripped)
        if sec_match:
            if sec_match.group(1):
                namespace_stack.append(sec_match.group(1))
            continue
        if _END_RE.match(stripped):
            if namespace_stack:
                namespace_stack.pop()
            continue
        m = _DECL_RE.match(stripped)
        if m:
            bare = m.group("name")
            qualified = ".".join([*namespace_stack, bare])
            index.setdefault(qualified, module_path)
            index.setdefault(bare, module_path)


def build_declaration_index(mathlib_root: Path) -> dict[str, str]:
    """Scan every `.lean` file under `mathlib_root` and record the first module path that
    introduces each name, both bare and fully namespace-qualified. Pure text/regex, no REPL --
    this is a preprocessing pass, not a verification step, and stays cheap (a few seconds over
    ~8800 files) regardless of how wide `TARGET_MODULES` gets."""
    index: dict[str, str] = {}
    for path in sorted(mathlib_root.rglob("*.lean")):
        text = path.read_text(encoding="utf-8")
        module_path = str(path.relative_to(mathlib_root))
        _index_text(text, module_path, index)
    return index
