"""Zero-cost, read-only static sweep over the Mathlib source tree for name-keyed
`Decidable`-family instances (2026-07-30) -- an INVENTORY, not a gate (see the 41-name batch's
Gate 2 report, §9.1, and `docs/design/llm_io_contract_v1.md` §4.4's reducibility fix). Sizes how
many mined candidates are exposed to that fix's own motivating bug: a `Decidable`/`DecidableEq`/
`DecidablePred`/`DecidableRel` instance keyed to a definition's own head symbol is invisible to
Lean's typeclass search through a plain-`def` task-symbol splice (or a candidate's own
re-declaration of the same body under a fresh name) -- `@[reducible]` fixes the splice side;
this module answers "how many names would have needed it."

**Mechanism**: one pass over every Mathlib `.lean` file (`build_instance_index`) finds every
`instance ...`-declaration line and, within a small trailing window (tolerating a wrapped
signature), every `Decidable`/`DecidableEq`/`DecidablePred`/`DecidableRel` mention immediately
followed by an identifier -- that identifier is the instance's "target head symbol." A regex
heuristic over source TEXT, not a Lean elaboration. `find_name_keyed_instances` then looks a
candidate name up two ways: its full qualified name, matched repo-wide (unambiguous); its bare
base name (last dotted component), matched ONLY within the candidate's own declaring file
(`module_path`, from the harvest manifest) -- a bare-base-name instance outside that file risks
being a same-named-but-unrelated identifier, so it is not counted.

**Known limitations, stated plainly rather than silently accepted**: (a) misses an instance
declaration whose class application spans more than the trailing window; (b) cannot resolve an
`open Namespace`-qualified reference that is neither the bare base name nor the full qualified
name; (c) a same-file base-name match could still, rarely, be an unrelated instance that
happens to share the base name (e.g. two different `Foo.decEq`-shaped names in one file) --
this module reports MATCHES for human review, it does not claim certainty. Precise enough for
an inventory; not proposed as a preflight gate."""

import re
from dataclasses import dataclass
from pathlib import Path

from miner.config import MATHLIB_ROOT

_INSTANCE_LINE_RE = re.compile(r"^\s*instance\b")
_DECIDABLE_TARGET_RE = re.compile(r"\b(Decidable(?:Eq|Pred|Rel)?)\b\s*\(?\s*([A-Za-z_][A-Za-z0-9_.']*)")
_WINDOW_LINES = 3  # tolerates a signature wrapped across a couple of lines; see module docstring


@dataclass(frozen=True)
class InstanceHit:
    class_name: str  # "Decidable" | "DecidableEq" | "DecidablePred" | "DecidableRel"
    target_head: str  # the identifier immediately following the class name in the source
    module_path: str  # repo-relative path under Mathlib/, e.g. "Data/Nat/ModEq.lean"
    line_no: int  # 1-based, where the `instance` line itself starts
    line_text: str  # the matched `instance` line, stripped, for human review


def _scan_file(path: Path, mathlib_root: Path) -> list[InstanceHit]:
    module_path = str(path.relative_to(mathlib_root))
    hits: list[InstanceHit] = []
    lines = path.read_text(encoding="utf-8", errors="replace").split("\n")
    for i, line in enumerate(lines):
        if not _INSTANCE_LINE_RE.match(line):
            continue
        window = "\n".join(lines[i:i + _WINDOW_LINES])
        for class_name, target in _DECIDABLE_TARGET_RE.findall(window):
            hits.append(InstanceHit(class_name, target, module_path, i + 1, line.strip()))
    return hits


def build_instance_index(mathlib_root: Path | None = None) -> list[InstanceHit]:
    """One pass over every Mathlib `.lean` file -- a few seconds, no REPL (same cost class as
    `miner.depindex.build_declaration_index`, which this mirrors)."""
    mathlib_root = mathlib_root if mathlib_root is not None else MATHLIB_ROOT
    hits: list[InstanceHit] = []
    for path in sorted(mathlib_root.rglob("*.lean")):
        hits.extend(_scan_file(path, mathlib_root))
    return hits


def find_name_keyed_instances(name: str, module_path: str, index: list[InstanceHit]) -> list[InstanceHit]:
    """`name`: full qualified real Mathlib name (e.g. `"Nat.ModEq"`); `module_path`: its own
    declaring file's repo-relative path under `Mathlib/` (e.g. `"Data/Nat/ModEq.lean"`), from
    the harvest manifest -- see module docstring for why base-name matches are file-scoped."""
    base = name.rsplit(".", 1)[-1]
    return [
        hit for hit in index
        if hit.target_head == name or (hit.target_head == base and hit.module_path == module_path)
    ]


def run_exposure_sweep(names_and_module_paths: dict[str, str], index: list[InstanceHit] | None = None) -> dict[str, list[dict]]:
    """`names_and_module_paths`: `{full_name: module_path}`. Returns `{full_name: [hit_dict,
    ...]}`, JSON-serializable directly. `index` may be pre-built (`build_instance_index`) and
    reused across many names -- building it once and querying it 721 times is the entire point
    of the two-phase design (see module docstring)."""
    index = index if index is not None else build_instance_index()
    result: dict[str, list[dict]] = {}
    for name, module_path in names_and_module_paths.items():
        hits = find_name_keyed_instances(name, module_path, index)
        result[name] = [
            {"class_name": h.class_name, "module_path": h.module_path, "line_no": h.line_no, "line_text": h.line_text}
            for h in hits
        ]
    return result
