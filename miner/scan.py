"""Textual pre-filter over the Mathlib source tree.

Finds `def` declarations by scanning source text line by line -- no Lean, no REPL, no
compilation. Deliberately approximate: this is a *pre-filter*, and its false positives are
expected to be caught later by `miner.verify` against the live environment, per the task that
introduced this module. Known limitations of the line-based approach are noted inline where
they bite.

Skips: `theorem`, `lemma`, `instance`, `abbrev`, `structure`, `class` (only `def` is of
interest at this stage); `private def`, `noncomputable def`, and anything with a
`@[deprecated ...]` attribute directly attached. `protected def` is kept (it only restricts
unqualified-name access, not computability or relevance).
"""

import re
from dataclasses import dataclass
from pathlib import Path

_NAMESPACE_RE = re.compile(r"^namespace\s+(\S+)\s*$")
_SECTION_RE = re.compile(r"^section(?:\s+(\S+))?\s*$")
_END_RE = re.compile(r"^end(?:\s+(\S+))?\s*$")

# Identifier character class, matching Lean 4's actual grammar (`isIdFirst`/`isIdRest` in
# Init/Meta/Defs.lean of the pinned toolchain: c.isAlpha/isAlphanum, `_`, `'`, `!`, `?`, plus
# `isLetterLike` -- Greek, Coptic, Latin-1 supplement, Latin Extended-A, the "letter-like"
# block (ℕ ℤ etc.) -- and `isSubScriptAlnum` -- U+2080-2089 numeric subscripts (₀-₉),
# U+2090-209C and U+1D62-1D6A subscript letters (ₐ ᵢ ⱼ ...), U+2C7C (ⱼ)).
#
# Previously this used a plain `[A-Za-z0-9_'!?.]` class, which silently truncated any name
# with a unicode subscript suffix -- `image₂` became `image`, colliding with the real
# `Finset.image`, and similarly for `Semiconj₂` and four `map₂...` variants. Confirmed
# empirically that Python's `\w` (Unicode word-character class) already covers Lean's
# `isAlpha`/`isAlphanum`, all the Greek/Latin-extended/letter-like-block ranges, AND both
# subscript ranges (they're Unicode categories Lm/No, which `\w` matches) -- so `\w` plus the
# punctuation Lean additionally allows (`'`, `!`, `?`) is a correct, cheap fix requiring no
# manual Unicode range listing. `.` is kept (not part of a single Lean identifier, but needed
# here to capture already-dotted names like `_root_.Foo.bar` as one token, same as before).
_ID_FIRST = r"[^\W\d]"  # a \w character that isn't a digit (Lean disallows a leading digit)
_ID_REST = r"[\w'!?.]"

_DEF_RE = re.compile(
    r"^(?P<prefix>(?:private\s+|protected\s+|noncomputable\s+)*)def\s+"
    rf"(?P<name>{_ID_FIRST}{_ID_REST}*)"
)

# Recognized starts of a new top-level command -- used to decide where a captured
# declaration's source text ends. Deliberately broad (includes modifier-prefixed variants);
# an unrecognized column-0 line is still treated conservatively as ending the declaration
# (see `_capture_def`), so this list only needs to catch the common cases correctly.
_TOP_LEVEL_STARTERS = re.compile(
    r"^(private\s+|protected\s+|noncomputable\s+)*"
    r"(def|theorem|lemma|instance|abbrev|structure|class|namespace|end|section|variable|"
    r"open|@\[|/--)"
)


@dataclass
class ScanHit:
    """One `def` declaration surviving the textual pre-filter."""

    name: str  # fully-qualified, e.g. "Nat.dist"
    module_path: str  # relative to the Mathlib root, e.g. "Data/Nat/Dist.lean"
    source_text: str  # the declaration itself; docstring/attributes captured separately
    docstring: str | None = None
    mention_count: int = 0  # filled in by compute_mention_counts, 0 until then


def _clean_docstring(raw: str) -> str:
    text = raw.strip()
    if text.startswith("/--"):
        text = text[3:]
    if text.endswith("-/"):
        text = text[:-2]
    return text.strip()


def _peek_preamble(lines: list[str], i: int, n: int) -> tuple[str | None, list[str], int]:
    """Consume an optional docstring followed by zero or more `@[...]` attribute lines,
    starting at line `i`. Returns (docstring_or_None, attribute_lines, first_line_after)."""
    docstring = None
    if i < n and lines[i].strip().startswith("/--"):
        doc_lines = [lines[i]]
        j = i
        if "-/" not in lines[i]:
            j += 1
            while j < n and "-/" not in lines[j]:
                doc_lines.append(lines[j])
                j += 1
            if j < n:
                doc_lines.append(lines[j])
        docstring = _clean_docstring("\n".join(doc_lines))
        i = j + 1

    attr_lines: list[str] = []
    while i < n and lines[i].strip().startswith("@["):
        attr_lines.append(lines[i].strip())
        i += 1

    return docstring, attr_lines, i


def _is_allowed(def_match: re.Match, attr_lines: list[str]) -> bool:
    prefix = def_match.group("prefix")
    if "private" in prefix or "noncomputable" in prefix:
        return False
    if any("deprecated" in a for a in attr_lines):
        return False
    return True


def _capture_indented_block(lines: list[str], start: int, n: int) -> tuple[list[str], int]:
    """Capture lines starting at `start`, continuing through blank and indented lines, and
    stopping at the next column-0 non-blank line -- whether or not it's a recognized
    top-level starter. This is the main approximation in this scanner: an
    indentation-sensitive heuristic, not a parser. It matches Mathlib's own style
    (declarations at column 0, bodies indented) closely enough for a pre-filter, and a
    wrongly-captured tail is harmless here since `miner.verify` re-checks everything against
    the real elaborator. Returns (captured_lines, index_of_first_line_after)."""
    body_lines = [lines[start]]
    j = start + 1
    while j < n:
        raw_line = lines[j]
        stripped = raw_line.strip()
        if not stripped:
            body_lines.append(raw_line)
            j += 1
            continue
        if raw_line[:1].isspace():
            body_lines.append(raw_line)
            j += 1
            continue
        break
    return body_lines, j


def _capture_def(
    lines: list[str],
    start: int,
    def_match: re.Match,
    namespace_stack: list[tuple[str, str | None]],
    docstring: str | None,
    module_path: str,
    n: int,
) -> tuple[ScanHit, int]:
    body_lines, j = _capture_indented_block(lines, start, n)

    while body_lines and not body_lines[-1].strip():
        body_lines.pop()

    source_text = "\n".join(body_lines)
    ns_parts = [name for kind, name in namespace_stack if kind == "namespace" and name]
    qualified = ".".join([*ns_parts, def_match.group("name")])
    hit = ScanHit(name=qualified, module_path=module_path, source_text=source_text, docstring=docstring)
    return hit, j


def scan_text(text: str, module_path: str) -> list[ScanHit]:
    """Scan already-read Lean source text for `def` declarations. Split out from
    `scan_module` so unit tests can exercise the parser on small synthetic inputs without
    touching the filesystem."""
    lines = text.split("\n")
    n = len(lines)
    namespace_stack: list[tuple[str, str | None]] = []
    hits: list[ScanHit] = []

    i = 0
    while i < n:
        stripped = lines[i].strip()

        if not stripped:
            i += 1
            continue

        ns_match = _NAMESPACE_RE.match(stripped)
        if ns_match:
            namespace_stack.append(("namespace", ns_match.group(1)))
            i += 1
            continue

        sec_match = _SECTION_RE.match(stripped)
        if sec_match:
            namespace_stack.append(("section", sec_match.group(1)))
            i += 1
            continue

        if _END_RE.match(stripped):
            if namespace_stack:
                namespace_stack.pop()
            i += 1
            continue

        if stripped.startswith("/--") or stripped.startswith("@["):
            docstring, attr_lines, def_line_idx = _peek_preamble(lines, i, n)
            if def_line_idx < n:
                def_match = _DEF_RE.match(lines[def_line_idx].strip())
                if def_match:
                    if _is_allowed(def_match, attr_lines):
                        hit, i = _capture_def(
                            lines, def_line_idx, def_match, namespace_stack, docstring, module_path, n
                        )
                        hits.append(hit)
                    else:
                        _, i = _capture_def(
                            lines, def_line_idx, def_match, namespace_stack, docstring, module_path, n
                        )
                    continue
            # Docstring/attributes belonged to something other than a `def` (a theorem,
            # instance, etc.) -- move past the preamble and let the main loop handle
            # whatever comes next.
            i = def_line_idx
            continue

        def_match = _DEF_RE.match(stripped)
        if def_match:
            if _is_allowed(def_match, []):
                hit, i = _capture_def(lines, i, def_match, namespace_stack, None, module_path, n)
                hits.append(hit)
            else:
                _, i = _capture_def(lines, i, def_match, namespace_stack, None, module_path, n)
            continue

        i += 1

    return hits


def scan_module(path: Path, mathlib_root: Path) -> list[ScanHit]:
    """Scan one `.lean` file. `mathlib_root` is used only to compute `module_path` relative
    to it."""
    text = path.read_text(encoding="utf-8")
    module_path = str(path.relative_to(mathlib_root))
    return scan_text(text, module_path)


def scan_all(target_dirs: list[Path], mathlib_root: Path) -> list[ScanHit]:
    """Scan every `.lean` file under each directory in `target_dirs` (recursively)."""
    hits: list[ScanHit] = []
    for target_dir in target_dirs:
        for path in sorted(target_dir.rglob("*.lean")):
            hits.extend(scan_module(path, mathlib_root))
    return hits


_THEOREM_RE = re.compile(r"^(?:private\s+|protected\s+)*(?:theorem|lemma)\s+[A-Za-z_][A-Za-z0-9_'!?.]*")


def scan_theorem_statements(text: str) -> list[str]:
    """Extract the STATEMENT text (everything up to the first top-level `:=`) of every
    `theorem`/`lemma` declaration in this source text. Used only to refine the global-fact
    supply proxy (`miner.proxies`) by checking which theorem *statements* (not proofs, not
    comments) mention a candidate name -- a sharper signal than a raw text mention count.
    Not a general theorem scanner: proof bodies are discarded, and this is not meant to feed
    anything beyond that one refinement.
    """
    lines = text.split("\n")
    n = len(lines)
    statements: list[str] = []
    i = 0
    while i < n:
        stripped = lines[i].strip()
        if _THEOREM_RE.match(stripped):
            body_lines, j = _capture_indented_block(lines, i, n)
            statement_text = "\n".join(body_lines)
            if ":=" in statement_text:
                statement_text = statement_text.split(":=", 1)[0]
            statements.append(statement_text)
            i = j
            continue
        i += 1
    return statements
