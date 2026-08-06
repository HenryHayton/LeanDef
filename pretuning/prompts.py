"""Assembling a pre-tuning prompt: common base + cell-specific factors.

Structure, identical in every cell except where the two factors vary:

  1. three worked exemplars   (dossier -> pinned signature -> [prose ->] definition)
  2. signature-conformance instruction   (identical in all eight cells)
  3. the task's dossier
  4. the task's pinned signature
  5. the task's notation glossary   (mechanical, meaning-level -- `pretuning.glossary`)
  6. anti-sorry text   (factor 1; empty in S0)
  7. scaffold text   (factor 2; empty in R0)

**The leak guard runs over the FULLY ASSEMBLED prompt, exemplar text included.** The exemplars
are real Mathlib definitions, so they carry real Mathlib names by construction -- which is fine
for the exemplar's own object but must never coincide with the task's target. Checking only the
task block, as the prelim did, would miss exactly that: an exemplar naming `Nat.log` in a prompt
whose task is `Nat.clog` would hand over a near-answer. The three chosen exemplars are burned
from task selection so this cannot arise for them, but the guard is mechanical rather than
trusting that.
"""

import json
from pathlib import Path

from authoring.namematch import IDENTIFIER, name_occurs
from pretuning.cells import Cell
from pretuning.glossary import render_glossary

EXEMPLARS_PATH = Path(__file__).resolve().parent / "exemplars.json"

CONFORMANCE = (
    "The definition must have exactly the pinned signature above. Do not change binder style or "
    "explicitness, do not bundle or unbundle arguments, and do not add or drop typeclass "
    "assumptions."
)

_SIG_MARKER = "<!-- PINNED-SIGNATURE:"


def load_exemplars() -> list[dict]:
    ex = json.loads(EXEMPLARS_PATH.read_text(encoding="utf-8"))
    missing = [e["task_symbol"] for e in ex
               if not (e.get("verified_compiles") and e.get("verified_admissible")
                       and e.get("verified_type_matches"))]
    if missing:
        raise RuntimeError(
            f"unverified exemplars would be shipped into every prompt: {missing}. "
            "Run scripts/build_exemplars.py and fix before assembling."
        )
    return sorted(ex, key=lambda e: e["slot"])


def _strip_markers(dossier_md: str) -> str:
    return "\n".join(ln for ln in dossier_md.splitlines() if _SIG_MARKER not in ln)


def render_exemplar(ex: dict, *, with_prose: bool) -> str:
    parts = [
        "## Example",
        "",
        "### Dossier",
        "",
        _strip_markers(ex["dossier_md"]).strip(),
        "",
        "### Pinned signature",
        "",
        "```lean",
        ex["pinned_signature"],
        "```",
        "",
    ]
    if with_prose:
        parts += ["### Characterization", "", ex["r1_prose"].strip(), ""]
    parts += ["### Definition", "", "```lean", ex["definition"].strip(), "```", ""]
    return "\n".join(parts)


def build_prompt(cell: Cell, dossier_md: str, pinned_signature: str) -> str:
    """The complete user-message text for one (cell, task)."""
    pinned_type = pinned_signature.split(" : ", 1)[1] if " : " in pinned_signature else pinned_signature
    symbol = pinned_signature.split(" : ", 1)[0]

    blocks = [
        "# Worked examples",
        "",
        "Each example shows a dossier, the signature pinned for it, and the complete definition "
        "that answers it." + (" A brief characterization is written before each definition."
                              if cell.uses_prose_exemplars else ""),
        "",
    ]
    blocks += [render_exemplar(e, with_prose=cell.uses_prose_exemplars) for e in load_exemplars()]
    blocks += [
        "# Your task",
        "",
        "The following is a complete informal specification of a single mathematical object.",
        "",
        _strip_markers(dossier_md).strip(),
        "",
        f"Write the complete Lean 4 definition of `{symbol}`. It must have exactly this type:",
        "",
        "```lean",
        pinned_signature,
        "```",
        "",
        CONFORMANCE,
        "",
    ]
    glossary = render_glossary(pinned_type)
    if glossary:
        blocks += [glossary, ""]
    if cell.anti_sorry_text:
        blocks += [cell.anti_sorry_text, ""]
    if cell.scaffold_text:
        blocks += [cell.scaffold_text, ""]
    blocks += ["Mathlib is already imported."]
    return "\n".join(blocks).strip() + "\n"


def check_prompt_leak(prompt: str, forbidden_real_name: str) -> tuple[bool, str]:
    """`(ok, detail)` -- the task's real Mathlib name must not appear anywhere in the assembled
    prompt, exemplars included. Identifier-boundary matching, the same matcher the dossier gate
    and the prelim leak test use."""
    if name_occurs(prompt, forbidden_real_name, boundary=IDENTIFIER):
        return False, f"real name {forbidden_real_name!r} appears in the assembled prompt"
    return True, ""
