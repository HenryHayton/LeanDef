"""Proof-script cache (reward doc §3.2): "Search happens once; every re-encounter is replay."

**Backend: JSONL, not sqlite** -- chosen because (a) every other manifest/log artifact in this
codebase is JSONL (`harvest_manifest.jsonl`, `discharge_manifest.jsonl`, `mention_names.jsonl`,
`bedrock`'s `call_log.jsonl`), and this keeps the cache consistent with that convention rather
than introducing a second persistence format for one new module; (b) the access pattern is
"look up by exact key, append on new certification" -- a linear index built once at load time
is fine at the scale this session operates at (hundreds to low thousands of facts, not
millions); sqlite's transactional guarantees aren't needed for a single-process, single-writer
Mac-side cache; (c) JSONL is trivially diffable/greppable for a human reviewing cache contents,
which a binary sqlite file is not -- matches CLAUDE.md's "prefer boring, standard choices"
constraint. Revisit if Session B's EC2 throughput makes JSONL's O(n) load cost or lack of
concurrent-writer safety an actual bottleneck, not a hypothetical one.

**Cache key**: (statement hash, toolchain pin), exactly as the reward doc specifies. The
statement hash is SHA-256 over the canonical statement (the bare-Prop form, §3.1). The
toolchain pin is COMPUTED, not hardcoded, from `lean/lean-toolchain` (the Lean version) and
`lean/lake-manifest.json`'s own Mathlib `rev` (exact commit) -- "a re-pin invalidates the cache
by construction" holds automatically since the pin string itself changes the moment either file
does, with no separate invalidation step to remember or forget.
"""

import hashlib
import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path

from lean_interact import AutoLeanServer, Command

from harness import config as cfg
from harness.repl import run_checked
from harness.results import CheckResult

DEFAULT_CACHE_PATH = Path(__file__).resolve().parent / "output" / "proof_script_cache.jsonl"


def statement_hash(canonical_statement: str) -> str:
    return hashlib.sha256(canonical_statement.strip().encode("utf-8")).hexdigest()


def toolchain_pin(repo_root: Path | None = None) -> str:
    """`"<lean-toolchain contents>@<mathlib rev>"`. See module docstring for why this makes a
    re-pin invalidate the cache automatically."""
    repo_root = repo_root if repo_root is not None else cfg.REPO_ROOT
    lean_version = (repo_root / "lean" / "lean-toolchain").read_text(encoding="utf-8").strip()
    manifest = json.loads((repo_root / "lean" / "lake-manifest.json").read_text(encoding="utf-8"))
    mathlib_rev = next(
        (pkg["rev"] for pkg in manifest.get("packages", []) if pkg.get("name") == "mathlib"),
        "unknown",
    )
    return f"{lean_version}@{mathlib_rev}"


@dataclass(frozen=True)
class CacheEntry:
    """Reward doc §3.2's record shape exactly: statement hash, toolchain pin, discharging
    tier, the reconstructed proof script, the proof's axiom closure (§3.3), wall-clock of the
    original search. `canonical_statement` is kept alongside for human debugging/greppability
    and because `replay` needs it to reconstruct the check -- not part of the lookup key
    itself. `flagged_for_research` is set by a failed replay (§3.2: "flags the cache entry for
    re-search")."""

    statement_hash: str
    toolchain_pin: str
    tier: int
    script: str
    axiom_closure: list[str]
    wall_clock_s: float
    canonical_statement: str
    flagged_for_research: bool = False


class ProofScriptCache:
    """An in-memory index over a JSONL file, loaded once, appended to on every new
    certification. Not safe for concurrent writers (see module docstring) -- fine for this
    session's single-process Mac-side use."""

    def __init__(self, path: Path | None = None):
        self.path = path if path is not None else DEFAULT_CACHE_PATH
        self._entries: dict[tuple[str, str], CacheEntry] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        with self.path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                entry = CacheEntry(**data)
                self._entries[(entry.statement_hash, entry.toolchain_pin)] = entry

    def get(self, canonical_statement: str, pin: str) -> CacheEntry | None:
        return self._entries.get((statement_hash(canonical_statement), pin))

    def put(self, entry: CacheEntry) -> None:
        self._entries[(entry.statement_hash, entry.toolchain_pin)] = entry
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")

    def flag_for_research(self, entry: CacheEntry) -> None:
        """Appends a NEW line for the same key with `flagged_for_research=True` -- JSONL is
        append-only, and `_load`'s dict-overwrite-by-key semantics mean the newest line for a
        key wins on the next load, so this is a correct (if not space-optimal) update. Within
        one session, `self._entries` is also updated immediately, so in-session behavior is
        consistent regardless of on-disk redundancy."""
        self.put(replace(entry, flagged_for_research=True))


def replay(entry: CacheEntry, server: AutoLeanServer, env: int, *, timeout: float | None = None) -> CheckResult:
    """Run `entry.script` as a plain kernel check -- no search, so replay "runs anywhere,
    including the development Mac" (reward doc §3.2). Reconstructs `example : <canonical
    statement> := <script>` against `env`; the caller (`ladder.adjudicate`, or a test) reads
    `.status` to decide replay success vs. failure."""
    timeout = timeout if timeout is not None else cfg.DECIDE_TIMEOUT
    cmd = f"example : {entry.canonical_statement} := {entry.script}"
    return run_checked(server, Command(cmd=cmd, env=env), timeout=timeout)
