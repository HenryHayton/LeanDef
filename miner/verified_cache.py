"""Verification cache: reuse already-verified records, and survive a crash mid-harvest.

Two problems, one mechanism (batch 5, 10 Aug 2026).

**Reuse.** `harvest()` verifies every scan hit on every run. That was affordable while the corpus
was 3,185 candidates (batch 4: 2.6h at ~3.23s/candidate); at batch-5 scope it is 15,387 hits, and
12,242 of them are genuinely new -- re-verifying the 3,145 already-verified ones is ~2.8 hours of
REPL time spent re-deriving records we already hold. The brief's rule is explicit: verify only new
candidates, reuse existing verified records untouched.

**Resume.** The same batch-4 review that recorded the 3.23s/candidate rate also recorded
environment deaths as the dominant cost risk of a long run (~107s to re-import Mathlib each). A
batch-5-scale run is ~11 hours; without an on-disk checkpoint, a death in hour 9 that the recovery
path cannot absorb costs the entire run. `miner.verify.verify_all_with_recovery` already handles a
death *within* a run; this handles losing the *process*.

**The cache key includes the SOURCE TEXT hash, not just the name.** A definition whose body
changed is a different definition even under the same name, and reusing a stale record for it
would silently gate the wrong text. Since the Mathlib pin is fixed this cannot fire in a normal
run -- which is exactly why it is cheap insurance against an abnormal one (a re-pin, a partially
synced tree, a hand-edited file), the failure mode being invisible rather than loud.

Records are appended as they are produced, so a kill -9 loses at most the current chunk.
"""

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from miner.verify import BinderGroup, VerifiedDef

DEFAULT_CACHE_PATH = Path(__file__).resolve().parent / "output" / "verified_cache.jsonl"


def cache_key(name: str, module_path: str, source_text: str) -> str:
    digest = hashlib.sha1(source_text.encode("utf-8")).hexdigest()[:16]
    return f"{name}|{module_path}|{digest}"


def _to_verified(payload: dict) -> VerifiedDef:
    """Rebuild a `VerifiedDef`, restoring `BinderGroup`s from their dict form.

    `asdict` flattens nested dataclasses, so binder groups come back as plain dicts and must be
    reconstructed -- `_count_hypothesis_binders` and the arity work both access `.kind`/`.type_text`
    as attributes, and a dict would fail there rather than here, far from the cause.
    """
    data = dict(payload)
    data.pop("_key", None)
    data["binder_groups"] = [BinderGroup(**g) for g in (data.get("binder_groups") or [])]
    return VerifiedDef(**data)


def load_cache(path: Path | None = None) -> dict[str, VerifiedDef]:
    path = path if path is not None else DEFAULT_CACHE_PATH
    if not path.exists():
        return {}
    out: dict[str, VerifiedDef] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
            out[payload["_key"]] = _to_verified(payload)
        except (json.JSONDecodeError, KeyError, TypeError):
            # A torn final line (kill mid-write) or a record from an older schema is skipped, not
            # fatal: the candidate simply gets re-verified, which is correct-but-slower rather
            # than wrong. Never let a damaged cache abort a run that can rebuild it.
            continue
    return out


def append_records(records: list[VerifiedDef], path: Path | None = None) -> None:
    path = path if path is not None else DEFAULT_CACHE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for r in records:
            payload = asdict(r)
            payload["_key"] = cache_key(r.name, r.module_path, r.source_text)
            fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
