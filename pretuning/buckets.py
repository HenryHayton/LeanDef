"""Escape-route buckets for the token-ban cells, named BEFORE the run.

Banning `sorry` cannot make a model able to write a definition it could not write. It can only
make it stop saying `sorry`. So the sorry rate in T1/T3 is guaranteed to fall, and reporting that
fall as a result would be measuring the intervention against itself. What is actually in question
is where the punt GOES: whether the ban converts a punt into a construction attempt (the outcome
that would matter) or merely into a differently-spelled punt.

These six buckets are committed here, in code, before any T1/T3 sample exists, so the reading
cannot be fitted to the data afterwards. They are deliberately mechanical -- no judgement call
survives contact with 3,000 samples -- and they are an axis SEPARATE from the funnel, not a
refinement of it. A `tactic_junk_body` can be admissible (`def f : ℕ := by exact 3` type-checks
and is complete); an `exemplar_substitution` never answers the task but is perfectly well-formed
Lean. The cross-tab of bucket against admissibility is the readable object, not either alone.

Precedence is fixed and total, so every sample lands in exactly one bucket:

    truncation_at_cap > exemplar_substitution > degenerate_body > tactic_junk_body
                      > real_construction_attempt > other
"""

import re

TRUNCATION_AT_CAP = "truncation_at_cap"
EXEMPLAR_SUBSTITUTION = "exemplar_substitution"
DEGENERATE_BODY = "degenerate_body"
TACTIC_JUNK_BODY = "tactic_junk_body"
REAL_CONSTRUCTION_ATTEMPT = "real_construction_attempt"
OTHER = "other"

BUCKETS: tuple[str, ...] = (
    REAL_CONSTRUCTION_ATTEMPT, TACTIC_JUNK_BODY, DEGENERATE_BODY,
    EXEMPLAR_SUBSTITUTION, TRUNCATION_AT_CAP, OTHER,
)

# Bodies that are placeholders however they are spelled. `?_` and `_` are Lean's own holes;
# `sorry`/`admit` are what the ban exists to remove and are listed so that a LEAK -- a banned
# token reaching the output anyway -- is classified honestly rather than counted as construction.
_PLACEHOLDER_BODIES = frozenset({
    "", "_", "?_", "sorry", "by sorry", "admit", "by admit", "sorryAx", "by exact sorry",
    "by trivial", "trivial",
})

# A body that is nothing but a tactic invocation: the model has handed the definition itself to
# proof automation. `exact?`/`apply?` are search tactics that do not even claim to know the
# answer; `aesop`/`simp`/`decide`/`omega` are the automation a punting formalizer reaches for.
_TACTIC_ONLY_RE = re.compile(
    r"^by\s+(exact\?|apply\?|aesop|simp\b.*|decide|omega|tauto|norm_num\b.*|trivial|"
    r"first\b.*|repeat\b.*|assumption)\s*$",
    re.DOTALL,
)

_UNFINISHED_TAIL_RE = re.compile(r"(?::=|[+\-*/,∧∨→←↔=<>]|\bthen\b|\belse\b|\bwith\b|=>)$")


def body_of(declaration: str) -> str:
    """Everything after the first top-level `:=`. Empty string when there is no body at all.

    Splitting on the first `:=` is right for the shapes this classifier sees: a declaration whose
    binders contain `:=` (an optional-argument default) would split early, but that shape does not
    occur in this corpus's pinned signatures and a mis-split shows up as a degenerate body rather
    than as a silently wrong verdict.
    """
    return declaration.split(":=", 1)[1].strip() if ":=" in declaration else ""


def classify(
    *,
    extracted: bool,
    declaration: str | None,
    declared_name: str | None,
    expected_name: str,
    exemplar_symbols: frozenset[str] | set[str],
    finish_reason: str | None,
) -> str:
    """The one bucket this sample belongs to. See the module docstring for precedence."""
    if finish_reason == "length":
        # Checked first and unconditionally: a generation cut off at the cap tells us nothing
        # about what the model would have written, so reading its partial body as a construction
        # attempt (or as a punt) would be inventing evidence either way.
        return TRUNCATION_AT_CAP

    if not extracted or not declaration:
        return OTHER

    if declared_name and declared_name in exemplar_symbols and declared_name != expected_name:
        return EXEMPLAR_SUBSTITUTION

    body = body_of(declaration)
    normalised = " ".join(body.split())
    if normalised in _PLACEHOLDER_BODIES or _UNFINISHED_TAIL_RE.search(body.rstrip()):
        return DEGENERATE_BODY

    if _TACTIC_ONLY_RE.match(normalised):
        return TACTIC_JUNK_BODY

    return REAL_CONSTRUCTION_ATTEMPT


def contains_banned_token(text: str) -> bool:
    """Did a banned word reach the output despite the ban? Reported separately from the buckets.

    A leak is not a bucket: it is a statement about whether the intervention was actually applied,
    and it needs to be visible even when the sample it appears in is otherwise a fine construction
    attempt (a stray `sorry` in a think-block, say).
    """
    return re.search(r"\b(sorry|sorryAx|admit)\b", text or "") is not None
