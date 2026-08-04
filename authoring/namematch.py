"""The one matcher for "does this text name this Lean declaration" (2026-07-31).

Consolidates three private implementations that had independently drifted apart and, between
them, carried the SAME bug three times -- each found only after the previous one was fixed and
unblocked the next stage:

- `authoring.consistency._contains_real_name` (dossier leak, round-trip recalled-target)
- `authoring.parse._leaks_forbidden_name` (per-fact raw-name leak)
- `authoring.validate`'s bare `pinned_name not in fact.statement` (global-fact pinned-name check)

The shared bug: for an UNNAMESPACED real name, the task symbol CONTAINS it -- `VTask.Monotone`
contains `Monotone` -- so any naive match flags the very symbol the model is required to use.
Live cost: three names unshippable at the dossier gate, then 100% of their facts rejected at the
parser gate (12/12, 14/14, 15/15), all while the artifacts were correct.

**Why a new module rather than reusing `consistency.py`'s copy**: `authoring.validate` is one of
the callers, and `authoring.consistency` already imports `authoring.validate` (for `ReasonCode`).
Putting the helper in `consistency.py` would make that cycle. This module imports only `re` and
`authoring.task_symbol`, so every caller can reach it.

Two boundary modes, because the callers genuinely differ and that difference is now an explicit
parameter instead of three separate functions:

- `IDENTIFIER` (default): the name must not be glued to more identifier characters on either
  side. Lean identifiers may contain `'`, which Python's own `\\b`/`\\w` do NOT -- that gap is why
  `Equiv.ofLeftInverse` used to match inside the entirely distinct declaration
  `Equiv.ofLeftInverse'`, the same false-positive class the `Nat.clog`/`Nat.clog2` case already
  forbade (`2` being a `\\w` character was the only reason that one happened to be caught).
- `SUBSTRING`: bare containment, no boundaries -- deliberately stricter, preserved for the
  per-fact leak check whose established semantics (see `docs/deferred.md`, 2026-07-28 sweep) are
  intentionally more aggressive than the dossier-level check.
"""

import re

# `LEAN_IDENT_CHAR` is imported, not restated (2026-08-04): `harness.signature` needs the
# identical notion of "glued to more identifier characters" for root-qualification, and this
# module's own docstring is a record of what duplicated matchers cost last time. `authoring`
# already depends on `harness` (see `authoring.pipeline`), so this direction adds no cycle.
from authoring.task_symbol import TASK_SYMBOL_PREFIX
from harness.signature import LEAN_IDENT_CHAR as _LEAN_IDENT_CHAR

IDENTIFIER = "identifier"
SUBSTRING = "substring"



def name_occurs(
    text: object,
    name: str,
    *,
    boundary: str = IDENTIFIER,
    exclude_task_symbol: bool = True,
) -> bool:
    """True when `name` occurs in `text` as a genuine reference to that declaration.

    `exclude_task_symbol` (default True) drops occurrences immediately preceded by
    `TASK_SYMBOL_PREFIX`, i.e. the task's own symbol. Pass False when `name` IS the task symbol
    and its presence is what you are looking for (`authoring.validate`'s pinned-name check),
    rather than a real Mathlib name whose leak you are guarding against.

    Non-string `text` returns False rather than raising -- callers may pass a field that a
    malformed LLM response left as a dict/list/int, and `x in 5` would raise while
    `x in {...}`/`x in [...]` would silently check the wrong thing (keys/elements, not text).
    """
    if not isinstance(text, str) or not name:
        return False
    guard = rf"(?<!{re.escape(TASK_SYMBOL_PREFIX)})" if exclude_task_symbol else ""
    if boundary == IDENTIFIER:
        left, right = rf"(?<!{_LEAN_IDENT_CHAR})", rf"(?!{_LEAN_IDENT_CHAR})"
    elif boundary == SUBSTRING:
        left = right = ""
    else:
        raise ValueError(f"boundary must be {IDENTIFIER!r} or {SUBSTRING!r}, got {boundary!r}")
    return re.search(guard + left + re.escape(name) + right, text) is not None


def any_name_occurs(texts, name: str, **kwargs) -> bool:
    """`name_occurs` over several fields; True if ANY carries the name."""
    return any(name_occurs(t, name, **kwargs) for t in texts)
