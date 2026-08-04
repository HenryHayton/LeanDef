"""Loading tasks and candidate samples, and re-deriving extraction on read.

**Extraction is recomputed, never read from disk.** Every prelim sample carries an
`extra.extraction_ok` flag frozen at generation time, and the extractor was fixed mid-run on
2026-08-03 (a fence pair-matching bug that skipped the block containing the real `def`). The
store's resume logic correctly never regenerates those samples, so the stored flag can disagree
with what the current extractor says. Extraction is a pure, millisecond-cheap function of the
stored `completion`, so the honest move is to recompute and record the disagreement.

`scripts/show_samples.py` does the same thing for humans and imports `reextract` from here, so
there is exactly one implementation of "what does this completion actually contain".
"""

import json
from pathlib import Path

from harness.facts import Fact
from harness.signature import PinnedSignature
from prelim.extract import Extraction, extract_definition
from scoring import config as cfg


def reextract(sample: dict) -> dict:
    """Return `sample` with extraction fields recomputed from `completion`.

    Adds `extracted_code` / `extraction_ok` at the TOP level (the stored copies live under
    `extra`) plus `extraction_disagreed`, which the verdict record persists so an analysis can
    ask how much the mid-run extractor fix moved.
    """
    result = extract_definition(
        sample.get("model_slug", ""), sample.get("completion") or "",
        finish_reason=sample.get("finish_reason"),
    )
    stored = (sample.get("extra") or {}).get("extraction_ok")
    ok = isinstance(result, Extraction)
    out = dict(sample)
    out["extraction_ok"] = ok
    out["extracted_code"] = result.code if ok else None
    out["extraction_reason"] = None if ok else result.reason
    out["declared_name"] = result.declared_name if ok else None
    out["renamed_symbol"] = result.renamed_symbol if ok else None
    out["extraction_disagreed"] = stored is not None and stored != ok
    return out


def load_task(task_name: str, *, tasks_root: Path | None = None) -> dict:
    """`{signature, facts, truth_real_name, ...}` for one task."""
    root = tasks_root if tasks_root is not None else cfg.tasks_dir()
    data = json.loads((Path(root) / task_name / "task.json").read_text(encoding="utf-8"))
    sig = data["signature"]
    return {
        "task_name": task_name,
        "signature": PinnedSignature(name=sig["name"], type_sig=sig["type"]),
        "imports": sig.get("imports") or ["Mathlib"],
        "facts": [Fact.from_dict(f) for f in data["facts"]],
        # The real Mathlib name, for the equivalence fast path's truth splice. It lives in
        # provenance because a dossier must never leak it to a model -- scoring is downstream of
        # generation, so using it here cannot contaminate anything.
        "truth_real_name": (data.get("provenance") or {}).get("mathlib_name"),
        "axiom_baseline": frozenset(data.get("axiom_baseline") or []),
    }


def load_samples(model_slug: str, task_name: str, *, samples_root: Path | None = None) -> list[dict]:
    """Every sample for one (model, task), sorted by index, with extraction recomputed."""
    root = samples_root if samples_root is not None else cfg.samples_dir()
    task_dir = Path(root) / model_slug / task_name
    if not task_dir.exists():
        return []
    samples = []
    for path in sorted(task_dir.glob("sample_*.json")):
        try:
            samples.append(reextract(json.loads(path.read_text(encoding="utf-8"))))
        except (OSError, json.JSONDecodeError):
            continue
    return sorted(samples, key=lambda s: s.get("sample_index", 0))


def available_models(*, samples_root: Path | None = None) -> list[str]:
    root = Path(samples_root if samples_root is not None else cfg.samples_dir())
    if not root.exists():
        return []
    return sorted(p.name for p in root.iterdir() if p.is_dir())


def available_tasks(model_slug: str, *, samples_root: Path | None = None) -> list[str]:
    root = Path(samples_root if samples_root is not None else cfg.samples_dir()) / model_slug
    if not root.exists():
        return []
    return sorted(p.name for p in root.iterdir() if p.is_dir())
