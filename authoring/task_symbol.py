"""The task-symbol convention (contract §4.4). Every task carries a task-local symbol,
`VTask.<base name>`, used everywhere an object identity would otherwise be needed: the pinned
signature, every fact statement, and every splice -- both the true definition's body (aliased
under the symbol to build the ground-truth environment) and any candidate body (round-trip or,
eventually, real candidate scoring).

Resolves the driver session's own reported finding: splicing a candidate under a name that
already exists in the base (Mathlib-imported) environment fails outright (confirmed against
real Mathlib: `` `Nat.clog` has already been declared ``). The task symbol is guaranteed fresh
(no real Mathlib declaration uses the `VTask.` namespace), so splicing under it -- whether the
true body aliased via `VTask.clog := Nat.clog`, or a candidate body -- never collides with the
real declaration. Truth-side validation and candidate scoring become the same operation:
splice something under the task symbol into the base environment, then run facts against
whatever that splice produced.
"""

import re

_BASE_NAME_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_']*$")


def task_symbol_for(mathlib_name: str) -> str:
    """`VTask.<base>`, where `<base>` is the last dotted component of `mathlib_name` (e.g.
    `Nat.clog` -> `VTask.clog`). Deterministic and mechanical -- not a per-task choice."""
    base = mathlib_name.rsplit(".", 1)[-1]
    if not _BASE_NAME_RE.fullmatch(base):
        raise ValueError(f"cannot derive a task symbol from {mathlib_name!r}: base component {base!r} is not a valid Lean identifier")
    return f"VTask.{base}"
