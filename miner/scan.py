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

# `section` may carry a modifier (`noncomputable section` -- affects computability of every
# `def` inside; `public section` -- Lean's module-visibility marker, ubiquitous: 2,703 of the
# corpus's ~8,600 files open one) and/or a leading `@[...]` attribute (`@[expose] public
# section`), same as a `def`/`theorem`. Both were previously unrecognized -- a bare `section`
# regex requiring the line to start with the literal word "section" -- so the stack never
# pushed for these, and whatever `end`/`end <name>` later closes them instead pops one level
# too many off the REAL namespace/section stack, corrupting every declaration's qualified name
# from that point in the file onward. Confirmed as a live bug (not hypothetical) by scanning
# every file `TARGET_MODULES` covers for a stack-underflow signal: 18 files show one, and in
# every single case the unrecognized opener immediately before it is `public section` or
# `noncomputable section` (optionally `@[expose]`-prefixed, optionally named, e.g.
# `noncomputable section Extend`) -- e.g. `Logic/Function/Basic.lean`'s `noncomputable section
# Extend` / `end Extend` pair, which wrongly popped `namespace Function` and corrupted
# `Involutive`/`Injective2`'s qualified names (see the batch-4 miner-repairs follow-up task).
# `private section`/`protected section`/`scoped section` were checked and confirmed to never
# occur anywhere in the corpus (0 matches) -- not real Lean syntax, not fixed since there is
# nothing to fix. `meta section` (48 occurrences corpus-wide) is real Lean syntax with the same
# theoretical risk, but does not occur anywhere within `TARGET_MODULES` -- no live example in
# scope, so left unrecognized per this fix's own "only what has a live example" rule; flagged
# for whoever next widens `TARGET_MODULES` into a corner that uses it.
_SECTION_RE = re.compile(r"^(?:@\[[^\]]*\]\s+)?(?:public\s+|noncomputable\s+)*section(?:\s+(\S+))?\s*$")
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

_ROOT_ESCAPE = "_root_."


def _qualify_name(raw_name: str, ns_parts: list[str]) -> str:
    """Build a declaration's fully-qualified name from its captured (possibly dotted) name and
    the enclosing `namespace` stack -- honoring Lean's `_root_.` escape (batch-4 review §7(a)):
    a name written `_root_.Foo.bar` resolves from the global root, ignoring every enclosing
    namespace, and must NOT have the namespace stack prepended onto it. Before this fix, `def
    _root_.Foo.bar` inside `namespace Baz` was qualified as `Baz._root_.Foo.bar` (wrong,
    doubly-qualified, and fails `#check` outright) instead of `Foo.bar` -- and even with an
    empty namespace stack, the literal `_root_.` marker itself was never stripped. Shared by
    `def`-name qualification (`_capture_def`) and mentioning-theorem-name qualification
    (`_scan_theorem_statements_impl`, for `miner.harvest`'s mention-persistence) so both apply
    the rule identically.

    Also strips a spurious trailing `.` (batch-4 miner-repairs follow-up task, universe-
    annotation bug): `_ID_REST` includes `.` (needed to capture already-dotted names like
    `_root_.Foo.bar` as one token), so a `def`/`theorem` immediately followed by an explicit
    universe annotation -- `def bitCasesOn.{u} ...`, `def optionEquivSumPUnit.{v, w} ...` --
    has its name-capture stop exactly at that `.`, one character short of where the real name
    ends, since `{` (unlike every real identifier continuation) isn't in `_ID_REST`. A trailing
    `.` can never be part of a genuinely complete Lean identifier -- a dotted name's last
    segment is never empty -- so stripping it is unconditionally safe, not merely a heuristic
    for this one shape. Confirmed against all four live corpus cases (`Int.bitCasesOn.`,
    `Equiv.optionEquivSumPUnit.`, `Multiset.`, `Option.traverse.`, each previously ending the
    non-elaborating population's `Invalid field notation` error) plus a fifth: `_THEOREM_RE`
    shares this same `_ID_REST`-based capture and was confirmed to carry the identical defect
    for a universe-annotated `theorem`/`lemma`, exercised by its own acceptance test."""
    raw_name = raw_name.rstrip(".")
    if raw_name.startswith(_ROOT_ESCAPE):
        return raw_name[len(_ROOT_ESCAPE) :]
    return ".".join([*ns_parts, raw_name])


def _find_module_doc_skip_lines(lines: list[str]) -> set[int]:
    """Line indices that fall inside a `/-! ... -/` module-doc block (batch-4 review §7(b)):
    unlike `/--` (a declaration docstring, handled separately by `_peek_preamble`), `/-!` marks
    module/section-level prose that can contain illustrative, non-real `def`/`theorem` examples
    (confirmed: `Data/Nat/Log.lean`'s `logTR`, `Data/Int/Log.lean`'s `digits`,
    `Data/Multiset/Sym.lean`'s `sym` inside a ```lean code fence, and two duplicate-named
    phantoms in `Logic/Equiv/Functor.lean`) -- scanned as if they were live top-level code
    before this fix. Lean block comments nest, so this tracks `/-`/`-/` depth (starting at the
    `/-!` itself, which opens with a plain `/-`) rather than looking for the first `-/`, which
    would stop at a NESTED block's close instead of the outer one's. Returns the full set of
    line indices from the opening `/-!` line through the line containing the matching close, so
    the main scan loop can skip them wholesale -- including any namespace/section/end/def-
    looking text inside, none of which is real code."""
    skip: set[int] = set()
    i = 0
    n = len(lines)
    while i < n:
        if lines[i].strip().startswith("/-!"):
            depth = 0
            j = i
            pos = 0
            closed = False
            while j < n:
                text = lines[j]
                while pos < len(text):
                    if text[pos : pos + 2] == "/-":
                        depth += 1
                        pos += 2
                    elif text[pos : pos + 2] == "-/":
                        depth -= 1
                        pos += 2
                        if depth == 0:
                            closed = True
                            break
                    else:
                        pos += 1
                skip.add(j)
                if closed:
                    break
                j += 1
                pos = 0
            i = j + 1
        else:
            i += 1
    return skip


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
    qualified = _qualify_name(def_match.group("name"), ns_parts)
    hit = ScanHit(name=qualified, module_path=module_path, source_text=source_text, docstring=docstring)
    return hit, j


def scan_text(text: str, module_path: str) -> list[ScanHit]:
    """Scan already-read Lean source text for `def` declarations. Split out from
    `scan_module` so unit tests can exercise the parser on small synthetic inputs without
    touching the filesystem."""
    lines = text.split("\n")
    n = len(lines)
    skip_lines = _find_module_doc_skip_lines(lines)
    namespace_stack: list[tuple[str, str | None]] = []
    hits: list[ScanHit] = []

    i = 0
    while i < n:
        if i in skip_lines:
            i += 1
            continue

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
    """Scan every `.lean` file under each entry in `target_dirs`. An entry may be a directory
    (scanned recursively) or a single `.lean` file (scanned directly) -- batch 2's widened
    `TARGET_MODULES` (docs/design/definition_selection_2026-07-21.md §6) deliberately mixes
    both, since several "basics" selections are individual files (e.g. `Algebra/Group/Defs.lean`)
    rather than whole subtrees."""
    hits: list[ScanHit] = []
    for target in target_dirs:
        if target.is_file():
            hits.extend(scan_module(target, mathlib_root))
            continue
        for path in sorted(target.rglob("*.lean")):
            hits.extend(scan_module(path, mathlib_root))
    return hits


# The name-capture group's FIRST-character class is deliberately kept identical to the
# original (ASCII-only `[A-Za-z_]`), not widened to `_ID_FIRST`: widening it could recognize
# additional lines as theorem/lemma declarations (any whose name starts with a non-ASCII
# letter), changing which statements feed `theorem_mention_count` -- a gate input
# (`miner.gates.theorem_mention_floor_gate`) -- in a way unrelated to bugs A/B and outside this
# fix's invariant (batch-4 manifest's 727 eligible definitions must see zero gate-outcome
# regressions). The REST portion uses `_ID_REST` (same correct, unicode-aware class `_DEF_RE`
# already uses) purely for capturing the name once a match has already started -- `*` is
# zero-or-more, so widening it cannot change WHETHER a line matches, only how much of an
# already-matched name is captured, avoiding a same-shape truncation bug on a subscripted
# theorem name (see `_ID_REST`'s own comment) in the new name capture piece 1 adds.
_THEOREM_RE = re.compile(rf"^(?:private\s+|protected\s+)*(?:theorem|lemma)\s+(?P<name>[A-Za-z_]{_ID_REST}*)")

# Bracket-aware statement/proof split (docs/theorem_mention_audit.md H2): the naive
# `text.split(":=", 1)[0]` cuts at the FIRST ":=" anywhere, but Lean 4's named-argument
# application syntax -- `f (arg := value)` -- routinely appears *inside a theorem's own stated
# type* (not just its proof), e.g. `lemma foo : Injective (bar (a := a)) := by ...`. The `:=`
# inside `(a := a)` isn't the real statement/proof separator, so splitting there silently
# discards everything after, including any candidate mention appearing later in the actual
# statement. Confirmed to affect 1.82% of all Mathlib theorem/lemma statements (3212/176167)
# in the audit. Fixed the same way `miner.verify._split_check_output` already splits `#check`
# output on a bracket-depth-0 colon: only a `:=` at bracket depth 0 is the real separator.
_BRACKET_OPEN = "({[⦃"
_BRACKET_CLOSE = ")}]⦄"


def _split_statement_at_top_level_assign(text: str) -> str:
    """Return everything before the first `:=` at bracket depth 0. If no such `:=` exists
    (bracket-unbalanced or genuinely absent), returns `text` unchanged -- same fallback
    behavior as the old naive split had when `":=" not in text`."""
    depth = 0
    n = len(text)
    i = 0
    while i < n - 1:
        ch = text[i]
        if ch in _BRACKET_OPEN:
            depth += 1
        elif ch in _BRACKET_CLOSE:
            depth -= 1
        elif ch == ":" and text[i + 1] == "=" and depth == 0:
            return text[:i]
        i += 1
    return text


def _scan_theorem_statements_impl(text: str) -> list[tuple[str, str, str]]:
    """Shared implementation: extracts (qualified_name, statement_text, namespace_prefix) for
    every `theorem`/`lemma` declaration. `namespace_prefix` is the dot-joined stack of enclosing
    `namespace` blocks active at that exact statement's point of declaration (empty string at
    top level) -- mirrors `scan_text`'s own qualification convention exactly: `section`s still
    push/pop the stack (to keep depth balanced against `end`) but only `namespace` entries
    contribute to the prefix, matching how Lean itself only qualifies declarations by
    enclosing `namespace`s, never by `section`s. `qualified_name` uses the same `_qualify_name`
    (and therefore the same `_root_.` handling) as `_capture_def`'s `def`-name qualification.

    Also skips `/-! ... -/` module-doc spans (`_find_module_doc_skip_lines`), same as
    `scan_text` -- a doc-comment illustrating a `theorem`-shaped example must not be scanned as
    a real one.
    """
    lines = text.split("\n")
    n = len(lines)
    skip_lines = _find_module_doc_skip_lines(lines)
    namespace_stack: list[tuple[str, str | None]] = []
    results: list[tuple[str, str, str]] = []
    i = 0
    while i < n:
        if i in skip_lines:
            i += 1
            continue
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
        theorem_match = _THEOREM_RE.match(stripped)
        if theorem_match:
            body_lines, j = _capture_indented_block(lines, i, n)
            statement_text = _split_statement_at_top_level_assign("\n".join(body_lines))
            ns_parts = [name for kind, name in namespace_stack if kind == "namespace" and name]
            qualified = _qualify_name(theorem_match.group("name"), ns_parts)
            results.append((qualified, statement_text, ".".join(ns_parts)))
            i = j
            continue
        i += 1
    return results


def scan_theorem_statements(text: str) -> list[str]:
    """Extract the STATEMENT text (everything up to the first top-level `:=`) of every
    `theorem`/`lemma` declaration in this source text. Used to refine the global-fact
    supply proxy (`miner.proxies`) by checking which theorem *statements* (not proofs, not
    comments) mention a candidate name -- a sharper signal than a raw text mention count.
    Not a general theorem scanner: proof bodies are discarded, and this is not meant to feed
    anything beyond that one refinement. See `scan_theorem_statements_with_namespace` for the
    namespace-aware variant `miner.harvest.compute_theorem_mention_counts` actually uses.
    """
    return [statement for _, statement, _ in _scan_theorem_statements_impl(text)]


def scan_theorem_statements_with_namespace(text: str) -> list[tuple[str, str]]:
    """Like `scan_theorem_statements`, but also returns the namespace prefix active at each
    statement's point of declaration (docs/theorem_mention_audit.md H1): a theorem stated
    inside `namespace Finset ... end Finset` mentions `Finset.pi` as bare `pi`, per ordinary
    Lean namespace resolution, and the audit found this is the dominant reason
    `theorem_mention_count` undercounts -- the qualified-name-only match used before this fix
    missed the majority of real mentions. Used by
    `miner.harvest.compute_theorem_mention_counts` to count a mention when a statement
    contains either the candidate's fully-qualified name (anywhere) or its bare name from
    within a matching namespace -- deliberately NOT an unscoped bare-name match, which the
    audit quantified at up to 98% collision noise on short names (`pi`, `empty`, `fix`, ...).
    """
    return [(statement, ns) for _, statement, ns in _scan_theorem_statements_impl(text)]


def scan_theorem_declarations_with_namespace(text: str) -> list[tuple[str, str, str]]:
    """Like `scan_theorem_statements_with_namespace`, but also returns each theorem/lemma's own
    fully-qualified name (`_root_.`-aware, see `_qualify_name`) as `(qualified_name,
    statement_text, namespace_prefix)`. Added for `miner.harvest`'s mention-name persistence
    (bundled miner repairs task, piece 1): naming the mentioning theorem, not just matching
    against its statement text, which is all `scan_theorem_statements_with_namespace`'s
    existing callers (`miner.harvest.compute_theorem_mention_counts`,
    `miner.discharge.find_mentioning_statements`) ever needed."""
    return _scan_theorem_statements_impl(text)
