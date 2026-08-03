"""Prompt assembly for prelim testing.

**The information contract, which is the whole point of this module.** Every model receives
exactly what the pipeline's own round-trip check gives its fresh context, no more and no less:

  INCLUDED: the task's `dossier.md`, the pinned signature, and the instruction to write the
            definition under that exact signature with Mathlib imported.
  EXCLUDED, always: mention excerpts, real Mathlib names, anchors, fact statements, and any
            few-shot example containing a real definition.

The exclusion is enforced structurally rather than by discipline: `build_task_block` reads only
`dossier.md` and the pinned signature from `task.json`, so there is no code path by which a
mention excerpt or a fact could reach a prompt. `tests/test_prelim_prompts.py` additionally runs
`authoring.namematch` over every one of the 41x6 assembled prompts and asserts the task's real
Mathlib name never appears -- a mechanical guard against a future regression in this file.

**Per-model variation is etiquette only.** The shared task block is built once and handed
unchanged to each model's wrapper (`prelim.models.ModelSpec`), which may only add a system
message and lead-in/tail lines in that model's own documented dialect. A wrapper cannot alter
task content because it never sees the pieces separately.

**Determinism.** Same task + same model => byte-identical prompt, every time. The store's
`prompt_sha256` is only a useful grouping key if that holds, so nothing here may depend on
dict ordering, wall-clock time, or filesystem iteration order.
"""

import json
import os
import re
from pathlib import Path

from prelim import config as cfg
from prelim.models import CHAT, COMPLETION, ModelSpec, get_model

# The marker comments `authoring.consistency.inject_pinned_signature` writes. They are internal
# plumbing -- a model should never see them, and only 28 of the 41 dossiers carry them (the other
# 13 shipped before that mechanism existed, with the signature written into the same section by
# hand). Stripping the markers while keeping the signature line makes all 41 read uniformly.
_SIG_MARKER_RE = re.compile(r"^[ \t]*<!--[ \t]*PINNED-SIGNATURE:(?:BEGIN|END)[ \t]*-->[ \t]*\n?", re.MULTILINE)

ENV_TASKS_DIR = "PRELIM_TASKS_DIR"


def tasks_dir() -> Path:
    """Root holding one directory per task (`<task>/dossier.md`, `<task>/task.json`).

    Overridable via `$PRELIM_TASKS_DIR` for tests and for pointing at a different corpus; the
    default is the repo's consolidated copy.
    """
    override = os.environ.get(ENV_TASKS_DIR, "").strip()
    return Path(override) if override else cfg.TASKS_DIR


def available_tasks(*, root: Path | None = None) -> list[str]:
    """Task names with both required files present, sorted -- sorted so a driver iterating tasks
    processes them in a stable order across machines and relaunches."""
    root = root if root is not None else tasks_dir()
    if not root.exists():
        return []
    return sorted(
        p.name for p in root.iterdir()
        if p.is_dir() and (p / "dossier.md").is_file() and (p / "task.json").is_file()
    )


def load_task(task_name: str, *, root: Path | None = None) -> tuple[str, str]:
    """`(normalized_dossier_md, pinned_signature)` for one task.

    The pinned signature is read from `task.json` (`task_symbol` + `signature.type`) rather than
    scraped out of the dossier: that is the authoritative, mechanically-generated form, identical
    in shape across all 41 tasks, whereas the dossier's rendering of it varies by pipeline
    vintage.
    """
    root = root if root is not None else tasks_dir()
    task_dir = Path(root) / task_name
    dossier_path, task_json_path = task_dir / "dossier.md", task_dir / "task.json"
    if not dossier_path.is_file() or not task_json_path.is_file():
        raise FileNotFoundError(f"task {task_name!r} incomplete under {root} (need dossier.md and task.json)")

    data = json.loads(task_json_path.read_text(encoding="utf-8"))
    pinned_signature = f"{data['task_symbol']} : {data['signature']['type']}"
    dossier = _SIG_MARKER_RE.sub("", dossier_path.read_text(encoding="utf-8")).strip()
    return dossier, pinned_signature


def build_task_block(dossier_md: str, pinned_signature: str) -> str:
    """The shared, model-independent body of every prompt. Built once per task and handed
    unchanged to every model's wrapper -- this string IS the information contract."""
    return (
        "# Dossier\n"
        "\n"
        "The following is a complete informal specification of a single mathematical object.\n"
        "\n"
        f"{dossier_md}\n"
        "\n"
        "# Your task\n"
        "\n"
        f"Write the complete Lean 4 definition of `{_symbol_of(pinned_signature)}` with exactly "
        "this signature:\n"
        "\n"
        "```lean\n"
        f"{pinned_signature}\n"
        "```\n"
        "\n"
        "Mathlib is already imported. Output the definition and nothing else."
    )


def _symbol_of(pinned_signature: str) -> str:
    """`VTask.clog` from `VTask.clog : (b n : ℕ) -> ℕ`. Split on the FIRST ' : ' only, since the
    type itself routinely contains further colons (binders like `(b n : ℕ)`)."""
    return pinned_signature.split(" : ", 1)[0].strip()


def _compose(spec: ModelSpec, task_block: str) -> str:
    """lead_in + task block + tail, blank-line separated, with empty parts omitted."""
    return "\n\n".join(p for p in (spec.lead_in.strip(), task_block, spec.tail.strip()) if p)


def assemble_prompt(
    model_slug: str, task_name: str, *, root: Path | None = None
) -> list[dict] | str:
    """The prompt for one (model, task) pair.

    Returns a messages list for `CHAT` models and a single prompt string for `COMPLETION` models
    -- matching what `prelim.client.generate` accepts for each endpoint style, so a driver can
    pass the result straight through without knowing which kind it holds.
    """
    dossier, pinned_signature = load_task(task_name, root=root)
    return assemble_prompt_from_parts(model_slug, dossier, pinned_signature)


def assemble_prompt_from_parts(
    model_slug: str, dossier_md: str, pinned_signature: str
) -> list[dict] | str:
    """`assemble_prompt` without the filesystem -- the seam tests use to drive fixtures."""
    spec = get_model(model_slug)
    body = _compose(spec, build_task_block(dossier_md, pinned_signature))

    if spec.endpoint_style == COMPLETION:
        # A completion-style model sees the system prompt (if any) as a plain leading paragraph;
        # there are no roles to carry it.
        return f"{spec.system_prompt}\n\n{body}" if spec.system_prompt else body

    if spec.endpoint_style != CHAT:  # pragma: no cover - guarded by the model table
        raise ValueError(f"unknown endpoint_style {spec.endpoint_style!r} for {model_slug!r}")

    messages: list[dict] = []
    if spec.system_prompt:
        messages.append({"role": "system", "content": spec.system_prompt})
    messages.append({"role": "user", "content": body})
    return messages


def prompt_text(prompt: list[dict] | str) -> str:
    """Flatten a prompt to searchable text -- used by the leak guard and by anything reporting
    prompts to a human. Never sent to a model."""
    if isinstance(prompt, str):
        return prompt
    return "\n".join(m.get("content", "") for m in prompt)
