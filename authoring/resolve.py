"""Assemble a `DefinitionInput` for a real mined definition -- the corpus-facing half the
pipeline deliberately left to callers.

`authoring.pipeline.DefinitionInput`'s docstring says assembling this from a real corpus "is out
of scope for this driver -- callers (the end-to-end test, a future batch script) supply it". The
29 July batch-50 run supplied it from a scratchpad script that was never promoted, so every later
batch would otherwise re-derive it. This is that script, promoted, reading only committed
artifacts:

    harvest manifest      name, module_path, docstring, source_text, return_shape
    mention sidecar       the mentioning theorems (global-fact anchor feedstock)
    preflight json        pinned type (printed and REPARSED, so it is known to round-trip)
                          and decidability

The pinned TYPE comes from preflight rather than from the manifest deliberately: preflight's
value is the print-then-reparse survivor, which is the only form guaranteed to elaborate when
spliced. A type read straight from the manifest can carry namespace-relative names that do not
resolve at the root namespace -- the failure mode preflight exists to catch.
"""

import json
from pathlib import Path

from authoring.pipeline import DefinitionInput
from miner.harvest import MentionRecord

DEFAULT_MANIFEST = Path("miner/output/harvest_manifest_batch4.jsonl")
DEFAULT_MENTIONS = Path("miner/output/mention_names_batch4.jsonl")


class DefinitionNotFound(KeyError):
    pass


def _index(path: Path, key: str) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            out[r[key]] = r
    return out


def make_resolver(
    preflight_path: Path,
    manifest_path: Path = DEFAULT_MANIFEST,
    mentions_path: Path = DEFAULT_MENTIONS,
    *,
    mention_cap: int | None = None,
):
    """`name -> DefinitionInput`, reading the three committed artifacts once."""
    manifest = _index(manifest_path, "name")
    mentions = _index(mentions_path, "name")
    preflight = json.loads(preflight_path.read_text(encoding="utf-8"))

    def resolve(name: str) -> DefinitionInput:
        rec = manifest.get(name)
        if rec is None:
            raise DefinitionNotFound(f"{name} is not in {manifest_path}")
        pf = preflight.get(name)
        if pf is None or pf.get("status") != "pass":
            raise DefinitionNotFound(f"{name} has no passing preflight entry in {preflight_path}")

        verified = rec.get("verified") or {}
        records = [MentionRecord(**m) for m in (mentions.get(name, {}).get("mentions") or [])]
        if mention_cap is not None:
            records = records[:mention_cap]

        return DefinitionInput(
            name=name,
            # 'name' here is informational -- the driver always splices under the task symbol it
            # computes itself (see DefinitionInput's own docstring).
            signature_dict={"name": name, "type": pf["pinned_type"], "imports": ["Mathlib"]},
            definition_source=verified.get("source_text") or rec.get("source_text") or "",
            docstring=verified.get("docstring") or rec.get("docstring") or "",
            return_shape=rec.get("return_shape") or verified.get("return_shape") or "value",
            decidability=pf.get("decidability"),
            mention_records=records,
        )

    return resolve
