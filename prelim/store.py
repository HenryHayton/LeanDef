"""The on-disk sample store for prelim testing.

Layout: `prelim_testing/output/samples/<model_slug>/<task_name>/sample_<nn>.json`.

**Every sample file is self-describing.** It carries the model, task, sample index, sampling
params, the EXACT messages sent, the completion, and the timing/token/provenance fields -- so a
single file can be read and understood without the driver, the config, or any sibling file. That
matters because these files are the raw material for scoring (a separate build) and for any
later re-analysis; a store whose meaning depends on external context ages badly.

**Atomic writes.** Write to a temp file in the same directory, then `os.replace` onto the final
name. `os.replace` is atomic within a filesystem, so a crash (or a killed pod) can leave the temp
file behind but can never leave a half-written `sample_07.json`. This is load-bearing for resume:
`is_complete` treats file existence as meaningful, so a truncated file that merely *looks*
present would cause the driver to skip work that never actually finished.

**The resume contract**, which is the reason this module exists rather than a dict of paths:
`is_complete(model_slug, task, idx)` is true iff the file exists AND parses as JSON AND has a
non-null `completion` field. Anything else is NOT complete -- and a file that exists but fails
those checks is renamed aside to `.corrupt` rather than silently overwritten, so the evidence
survives for inspection. Stage 3's driver calls this on relaunch to skip finished work.
"""

import json
import logging
import os
import re
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path

from prelim import config as cfg

log = logging.getLogger(__name__)

# Schema version for the sample file. Bumped if the shape changes incompatibly, so a later
# reader can tell what it is looking at rather than guessing from which keys happen to exist.
SAMPLE_SCHEMA_VERSION = 1

_SLUG_STRIP_RE = re.compile(r"[^a-z0-9]+")


def model_slug(model_name: str) -> str:
    """Filesystem-safe directory name for a Hugging Face model id.

    `Goedel-LM/Goedel-Prover-V2-8B` -> `goedel-prover-v2-8b`. The org prefix is dropped: these
    slugs are directory names read by humans scanning a progress display, the model set is small
    and hand-picked, and the full name is recorded inside every sample file anyway. Lowercased,
    every run of non-alphanumerics collapsed to a single hyphen, ends trimmed.
    """
    if not model_name or not model_name.strip():
        raise ValueError("model_name must be a non-empty string")
    base = model_name.strip().rsplit("/", 1)[-1]
    slug = _SLUG_STRIP_RE.sub("-", base.lower()).strip("-")
    if not slug:
        raise ValueError(f"model_name {model_name!r} has no slug-able characters")
    return slug


def prompt_sha256(prompt_messages: list[dict]) -> str:
    """Stable hash of the exact messages sent, for cheap grouping later ("which samples came
    from the same prompt?") without re-reading and re-comparing full prompt bodies.

    `sort_keys=True` so a dict-ordering difference between runs never changes the hash;
    `ensure_ascii=False` so the hash is over the real characters (these prompts contain Lean's
    unicode heavily) rather than an escaping artifact.
    """
    payload = json.dumps(prompt_messages, sort_keys=True, ensure_ascii=False)
    return sha256(payload.encode("utf-8")).hexdigest()


@dataclass
class Sample:
    """One generation, as stored. Field order here is the field order on disk."""

    schema_version: int
    model_name: str
    model_slug: str
    task_name: str
    sample_index: int
    temperature: float
    max_tokens: int
    prompt_messages: list[dict]
    prompt_sha256: str
    completion: str | None
    finish_reason: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    wall_time_s: float | None
    attempts: int
    endpoint_url: str | None
    timestamp: str
    extra: dict = field(default_factory=dict)


def sample_path(model_slug_: str, task_name: str, sample_index: int, *, samples_dir: Path | None = None) -> Path:
    """`<samples_dir>/<model_slug>/<task_name>/sample_<nn>.json`, zero-padded to 2 digits (wider
    if a run ever exceeds 99 samples, which sorts correctly either way at these magnitudes)."""
    root = samples_dir if samples_dir is not None else cfg.SAMPLES_DIR
    return Path(root) / model_slug_ / task_name / f"sample_{sample_index:02d}.json"


def build_sample(
    *,
    model_name: str,
    task_name: str,
    sample_index: int,
    temperature: float,
    max_tokens: int,
    prompt_messages: list[dict],
    completion: str | None,
    finish_reason: str | None = None,
    prompt_tokens: int | None = None,
    completion_tokens: int | None = None,
    wall_time_s: float | None = None,
    attempts: int = 1,
    endpoint_url: str | None = None,
    extra: dict | None = None,
) -> Sample:
    """Assemble a `Sample` with the derived fields (slug, prompt hash, timestamp) filled in."""
    return Sample(
        schema_version=SAMPLE_SCHEMA_VERSION,
        model_name=model_name,
        model_slug=model_slug(model_name),
        task_name=task_name,
        sample_index=sample_index,
        temperature=temperature,
        max_tokens=max_tokens,
        prompt_messages=prompt_messages,
        prompt_sha256=prompt_sha256(prompt_messages),
        completion=completion,
        finish_reason=finish_reason,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        wall_time_s=wall_time_s,
        attempts=attempts,
        endpoint_url=endpoint_url,
        timestamp=datetime.now(UTC).isoformat(),
        extra=extra or {},
    )


def write_sample(sample: Sample, *, samples_dir: Path | None = None) -> Path:
    """Write atomically (temp file in the same directory, then `os.replace`). Returns the path.

    The temp file is created in the DESTINATION directory, not `/tmp`: `os.replace` is only
    atomic within a single filesystem, and a cross-device rename would silently degrade to a
    copy, reintroducing exactly the partial-file window this exists to close.
    """
    path = sample_path(sample.model_slug, sample.task_name, sample.sample_index, samples_dir=samples_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(asdict(sample), ensure_ascii=False, indent=2)

    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=f".{path.stem}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())  # durable before the rename, so a power loss can't leave an empty file
        os.replace(tmp_name, path)
    except Exception:
        Path(tmp_name).unlink(missing_ok=True)
        raise
    return path


def read_sample(path: Path) -> dict | None:
    """Parsed sample dict, or None if the file is missing or unparseable."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def is_complete(
    model_slug_: str, task_name: str, sample_index: int, *, samples_dir: Path | None = None
) -> bool:
    """THE RESUME CONTRACT. True iff the sample file exists, parses as JSON, and has a non-null
    `completion`. A file that exists but fails either check is renamed aside to `<name>.corrupt`
    (logged, never silently overwritten) and reported NOT complete, so the driver regenerates it
    and the damaged evidence is still there to look at.

    A null `completion` counts as incomplete deliberately: `prelim.client` never returns empty
    text for a failure, so a stored null can only mean a partial write or a caller that recorded
    a failure placeholder -- in both cases the work genuinely is not done.
    """
    path = sample_path(model_slug_, task_name, sample_index, samples_dir=samples_dir)
    if not path.exists():
        return False
    data = read_sample(path)
    if data is None:
        _quarantine(path, "unparseable JSON")
        return False
    if data.get("completion") is None:
        _quarantine(path, "completion field is null/absent")
        return False
    return True


def _quarantine(path: Path, reason: str) -> None:
    """Rename a bad sample file aside. Never raises: quarantine failing must not take down an
    overnight run, and the caller's answer (NOT complete) is correct either way."""
    target = path.with_suffix(path.suffix + ".corrupt")
    try:
        os.replace(path, target)
        log.warning("quarantined %s (%s) -> %s", path, reason, target.name)
    except OSError as e:  # pragma: no cover - defensive
        log.warning("could not quarantine %s (%s): %s", path, reason, e)


def summarize(*, samples_dir: Path | None = None) -> dict[str, dict[str, int]]:
    """`{model_slug: {task_name: complete_sample_count}}` for the driver's progress display and
    end-of-run sanity check. Counts only files that satisfy the same completeness rule
    `is_complete` uses, so the summary can never claim work the resume logic would redo.

    Reads the tree directly rather than any index: the filesystem IS the state (no separate
    manifest to drift), which is what makes a killed-and-relaunched run safe.
    """
    root = Path(samples_dir if samples_dir is not None else cfg.SAMPLES_DIR)
    out: dict[str, dict[str, int]] = {}
    if not root.exists():
        return out
    for model_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        per_task: dict[str, int] = {}
        for task_dir in sorted(p for p in model_dir.iterdir() if p.is_dir()):
            count = 0
            for f in task_dir.glob("sample_*.json"):
                data = read_sample(f)
                if data is not None and data.get("completion") is not None:
                    count += 1
            per_task[task_dir.name] = count
        out[model_dir.name] = per_task
    return out


def summarize_totals(*, samples_dir: Path | None = None) -> dict[str, int]:
    """`{model_slug: total_complete_samples}` -- the one-line form ("goedel: 410/410")."""
    return {model: sum(tasks.values()) for model, tasks in summarize(samples_dir=samples_dir).items()}
