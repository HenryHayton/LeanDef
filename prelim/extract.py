"""Pulling a single clean Lean definition out of whatever a model actually said.

**Extraction failure is DATA, not an error.** A model that cannot produce an extractable
definition is telling us its score, and that is exactly the measurement prelim testing exists to
make. So nothing here raises: `extract_definition` returns either an `Extraction` (with the code
and some flags describing what had to be done to get it) or an `ExtractionFailure` (with a
machine-readable reason). Both are recorded; neither halts a run.

What real prover/formalizer output looks like, and therefore what this must survive:

- fenced blocks, tagged ```lean, ```lean4, or bare ```
- long chain-of-thought prose before the code (Goedel and DeepSeek are explicitly prompted to
  plan first; Kimina is reasoning-heavy by design)
- prose AFTER the code -- "This definition works because..." -- which must not be captured
- several fenced blocks, only one of which is the answer (a plan sketch, then the real thing)
- no fence at all: a bare `def` sitting in prose
- `noncomputable def`, `@[simp] def`, `private def`, and other modifier/attribute prefixes
- the declaration truncated mid-body because the token budget ran out

Symbol policy: we prefer the block declaring `VTask.` (that is the name we asked for). If no
candidate declares a `VTask.` symbol but exactly one declaration exists, we take it and set
`renamed_symbol=True` -- scoring splices under our own name anyway, so a model that called it
`clog` instead of `VTask.clog` has still answered the question; the flag records that it did not
follow the naming instruction, which is itself worth measuring.
"""

import re
from dataclasses import dataclass, field

# Reasons, as stable strings (the driver and scoring group on these).
NO_DEF_FOUND = "no_def_found"
TRUNCATED_MID_DEF = "truncated_mid_def"
MULTIPLE_AMBIGUOUS = "multiple_ambiguous"

# A fenced block: ```lean / ```lean4 / ```. Non-greedy body, tolerant of a missing closing fence
# (a truncated response often has none) -- the `(?:```|\Z)` alternative catches end-of-string.
_FENCE_RE = re.compile(r"```(?:lean4?|)[ \t]*\r?\n(.*?)(?:```|\Z)", re.DOTALL | re.IGNORECASE)

# The start of a Lean declaration, at line start, allowing attributes and modifiers before it.
# `abbrev`/`instance` are included because a model may legitimately reach for them; `theorem`
# and `lemma` are NOT -- we asked for a definition, and a returned theorem is a wrong answer we
# want to see as such rather than silently accept.
_DECL_START_RE = re.compile(
    r"^(?:@\[[^\]]*\][ \t]*)*"          # zero or more attribute groups, e.g. @[simp]
    r"(?:private[ \t]+|protected[ \t]+|noncomputable[ \t]+|partial[ \t]+|unsafe[ \t]+)*"
    r"(?:def|abbrev|instance)[ \t]+"
    r"([A-Za-z_][A-Za-z0-9_.'!?]*)",     # the declared name
    re.MULTILINE,
)

# Lines that end a declaration when they appear at column 0 after it has started: another
# top-level declaration, a command, or a prose paragraph. Indented lines are part of the body.
_NEXT_TOPLEVEL_RE = re.compile(
    r"^(?:@\[|def[ \t]|abbrev[ \t]|instance[ \t]|theorem[ \t]|lemma[ \t]|example[ \t]|"
    r"structure[ \t]|inductive[ \t]|class[ \t]|namespace[ \t]|end[ \t]|open[ \t]|"
    r"import[ \t]|#|--\s*[A-Z]|private[ \t]|protected[ \t]|noncomputable[ \t])",
)


@dataclass(frozen=True)
class Extraction:
    """A successfully extracted definition."""

    code: str
    declared_name: str
    renamed_symbol: bool = False      # declared something other than a VTask.* symbol
    from_fence: bool = False          # found inside a fenced block rather than bare prose
    truncated_trailing: bool = False  # trailing prose/declarations were cut off the end
    n_candidates: int = 1             # how many declaration candidates were seen in total


@dataclass(frozen=True)
class ExtractionFailure:
    """No usable definition. `reason` is one of the module-level constants."""

    reason: str
    detail: str = ""
    n_candidates: int = 0
    partial: str | None = None  # best-effort fragment, for eyeballing what went wrong
    extra: dict = field(default_factory=dict)


def _candidate_regions(text: str) -> list[tuple[str, bool]]:
    """`(region_text, from_fence)` regions that might hold a declaration.

    Fenced blocks first (in order), then -- only if no fence yielded a declaration -- the whole
    text as one bare region. Fences are strongly preferred: when a model both plans in prose and
    emits a fenced answer, the fence is the answer.
    """
    regions = [(m.group(1), True) for m in _FENCE_RE.finditer(text)]
    return regions or [(text, False)]


def _slice_declaration(region: str, start: int) -> tuple[str, bool]:
    """From `start` (a declaration's first character) to the end of that declaration.

    Ends at the first column-0 line that begins a new top-level declaration/command, or at a
    blank line followed by column-0 prose. Indented continuation lines always belong to the body,
    which is what makes `where`-clauses and multi-line bodies survive intact.
    """
    lines = region[start:].splitlines(keepends=True)
    kept: list[str] = []
    truncated = False
    for i, line in enumerate(lines):
        if i == 0:
            kept.append(line)
            continue
        stripped = line.strip()
        if not stripped:
            kept.append(line)
            continue
        indented = line[0] in " \t"
        if not indented:
            if _NEXT_TOPLEVEL_RE.match(line):
                truncated = True
                break
            # Column-0 non-Lean-looking text after a blank line reads as prose commentary.
            if kept and not kept[-1].strip():
                truncated = True
                break
        kept.append(line)
    return "".join(kept).rstrip(), truncated


def _looks_truncated(code: str) -> bool:
    """Heuristic: does this declaration look cut off mid-body?

    Deliberately narrow -- only signals that are unambiguous without parsing Lean: a body that
    ends right after `:=`, or with an obviously dangling operator/opening bracket. Anything
    subtler is left to the Lean kernel at scoring time, which is the real judge.
    """
    tail = code.rstrip()
    if not tail:
        return True
    if tail.endswith(":="):
        return True
    if re.search(r"(?:[+\-*/,∧∨→←↔=<>]|\bthen\b|\belse\b|\bwith\b|\bfun\b|=>)$", tail):
        return True
    opens = sum(tail.count(c) for c in "([{")
    closes = sum(tail.count(c) for c in ")]}")
    return opens > closes


def extract_definition(
    model_slug: str, completion_text: str, *, finish_reason: str | None = None
) -> Extraction | ExtractionFailure:
    """Extract one Lean definition from `completion_text`.

    `model_slug` is accepted for signature stability and per-model tuning later; extraction is
    currently model-independent by design -- the output shapes overlap far more than they differ,
    and one code path means one set of bugs. `finish_reason` (`"length"` from the endpoint) is
    used to distinguish a genuinely truncated generation from a merely unparseable one.
    """
    text = completion_text or ""
    if not text.strip():
        return ExtractionFailure(NO_DEF_FOUND, "completion was empty", n_candidates=0)

    # Reasoning-model output puts deliberation in `<think>...</think>`, and models that quote
    # candidate fragments while reasoning ("the body would be ```lean fun x => ...```") leave
    # several fenced blocks in there that are NOT the answer. Counting them produced
    # MULTIPLE_AMBIGUOUS on StepFun-Formalizer-32B for output whose real answer sat, complete,
    # immediately after the closing tag. Only text after the LAST `</think>` is the answer.
    #
    # An UNTERMINATED `<think>` is left alone: that is a truncated generation, and discarding
    # everything would turn a truncation into a spurious `no_def_found`.
    if "</think>" in text:
        after = text.rsplit("</think>", 1)[1]
        if after.strip():
            text = after

    regions = _candidate_regions(text)
    candidates: list[Extraction] = []
    for region, from_fence in regions:
        for m in _DECL_START_RE.finditer(region):
            code, truncated_trailing = _slice_declaration(region, m.start())
            if not code.strip():
                continue
            candidates.append(
                Extraction(
                    code=code,
                    declared_name=m.group(1),
                    renamed_symbol=not m.group(1).startswith("VTask."),
                    from_fence=from_fence,
                    truncated_trailing=truncated_trailing,
                )
            )

    if not candidates and any(from_fence for _, from_fence in regions):
        # Fences existed but none contained a declaration -- rescan the WHOLE text.
        #
        # Live regression (2026-08-03): a reasoning-heavy model emitted EIGHT fenced blocks (its
        # <think> section quotes several snippets before the answer). With an odd/interleaved
        # number of fence delimiters the pair-matching drifts, so the block holding the real
        # `def` lands BETWEEN two matched regions and was never scanned -- the model was scored
        # `no_def_found` for output that plainly contained a definition. Falling back to the
        # unfenced whole text costs nothing when fences worked (this branch is unreachable then)
        # and rescues exactly this case. Fence-derived regions are still preferred first, so a
        # model that fences correctly is unaffected.
        for m in _DECL_START_RE.finditer(text):
            code, truncated_trailing = _slice_declaration(text, m.start())
            if code.strip():
                candidates.append(
                    Extraction(
                        code=code, declared_name=m.group(1),
                        renamed_symbol=not m.group(1).startswith("VTask."),
                        from_fence=False, truncated_trailing=truncated_trailing,
                    )
                )

    if not candidates:
        # A `length` finish with no parseable declaration is a truncation, not a refusal --
        # a distinction that matters when reading a model's score.
        if finish_reason == "length":
            return ExtractionFailure(
                TRUNCATED_MID_DEF,
                "generation hit the token limit before a complete declaration appeared",
                n_candidates=0,
                partial=text[-500:],
            )
        return ExtractionFailure(
            NO_DEF_FOUND, "no def/abbrev/instance declaration found", n_candidates=0,
            partial=text[:500],
        )

    n = len(candidates)
    vtask = [c for c in candidates if not c.renamed_symbol]

    if vtask:
        chosen = vtask[-1]  # the last VTask declaration: a model that revises emits the fix last
    elif n == 1:
        chosen = candidates[0]
    else:
        # Several declarations, none using the name we asked for: genuinely ambiguous. Guessing
        # would silently score the wrong body, which is worse than recording the ambiguity.
        return ExtractionFailure(
            MULTIPLE_AMBIGUOUS,
            f"{n} declarations found, none declaring a VTask.* symbol: "
            f"{[c.declared_name for c in candidates]}",
            n_candidates=n,
            partial=candidates[0].code[:500],
        )

    if finish_reason == "length" and _looks_truncated(chosen.code):
        return ExtractionFailure(
            TRUNCATED_MID_DEF,
            "generation hit the token limit mid-declaration",
            n_candidates=n,
            partial=chosen.code[-500:],
        )

    return Extraction(
        code=chosen.code,
        declared_name=chosen.declared_name,
        renamed_symbol=chosen.renamed_symbol,
        from_fence=chosen.from_fence,
        truncated_trailing=chosen.truncated_trailing,
        n_candidates=n,
    )
