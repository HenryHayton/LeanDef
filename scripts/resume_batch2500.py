"""Resume the batch-2500 authoring run without re-paying for known-bad names.

    uv run python scripts/resume_batch2500.py --limit 400

`run_batch200.py`'s resume skips names that already have a `task.json`. Rotated names leave no
`task.json`, so every resume re-attempts them and pays again -- and a name that rotated at
`dossier`/`classification`/`mechanical_validation` failed on the definition's own content and
will rotate again. Over a run this size, resumed many times as credentials expire, that is the
same handful of names bought over and over.

**Only content-stage rotations are ledgered.** A rotation at `credentials`/`repl`/`truth_splice`
is environmental -- expired token, dead REPL -- and those names go back in the queue, because
the next attempt has a real chance. The stage is read from the batch review markdown, which
records `rotated at \\`<stage>\\`` per task, rather than being guessed at.

The ledger is rebuilt from the review files every run, so deleting it loses nothing.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

OUT_DIR = Path("prelim_testing/tasks_batch2500")
PASSING = Path("authoring/batches/batch2500_passing.txt")
LEDGER = Path("authoring/batches/batch2500_rotated.txt")
# Definitions reserved as held-out evaluation data. They are authored FRESH at training time,
# from this same pool -- so if authoring is allowed to consume them now, there is nothing
# uncontaminated left to author later. See training/config/heldout_slate_v1.json.
HELDOUT = Path("training/config/heldout_slate_v1_names.txt")
WORKING = Path("authoring/batches/_batch2500_working.txt")

# Stages where the definition's own content is what failed. Anything else is environmental.
# Keyed on the FAILURE, not the stage. Keying on the stage was wrong: `classification` is
# simply where the first Bedrock call happens, so an expired token rotates every remaining task
# there. Treating that stage as content-fatal permanently dropped 18 names that had only met a
# dead credential -- 19 of the first 30 rotations were environmental, not content.
# Matched against the rotation body. Anything NOT matched here is treated as the definition's
# own fault and permanently excluded, so this list failing open is expensive: an AccessDenied
# outage ledgered 264 healthy names in one run before "AccessDenied"/"403" were added. When in
# doubt about a new failure string, add it -- a name wrongly retried costs one task's spend, a
# name wrongly ledgered is lost from the corpus silently.
ENVIRONMENTAL = ("BedrockRetriesExhausted", "redential", "transport error", "ReadTimeout",
                 "Unknown environment", "Connection", "Throttl",
                 "AccessDenied", "not authorized", "403", "ExpiredToken",
                 "ServiceUnavailable", "InternalServerException", "ModelNotReady",
                 "500", "502", "503", "504")

ROTATION = re.compile(r"^### (\S+) -- ROTATED \(rotated at `([a-z_]+)`\)(.*?)(?=^### |\Z)",
                      re.M | re.S)


def build_ledger() -> dict:
    """name -> stage, for rotations that were the DEFINITION's fault and will recur."""
    rotated = {}
    for review in sorted(OUT_DIR.glob("batch_review_*.md")):
        for name, stage, body in ROTATION.findall(review.read_text(encoding="utf-8")):
            if any(k in body for k in ENVIRONMENTAL):
                rotated.pop(name, None)  # dead token / dead REPL: back in the queue
            else:
                rotated[name] = stage
    return rotated


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=400)
    ap.add_argument("--chunk-size", type=int, default=20,
                    help="tasks per REPL lifetime; each chunk boundary costs a cold Mathlib "
                         "import, so bigger is faster but holds the REPL longer")
    args = ap.parse_args()

    names = [n.strip() for n in PASSING.read_text(encoding="utf-8").splitlines() if n.strip()]
    done = {p.name for p in OUT_DIR.iterdir() if (p / "task.json").exists()} if OUT_DIR.exists() else set()
    rotated = build_ledger()
    LEDGER.write_text("".join(f"{n}\t{s}\n" for n, s in sorted(rotated.items())), encoding="utf-8")

    heldout = set()
    if HELDOUT.exists():
        heldout = {n.strip() for n in HELDOUT.read_text(encoding="utf-8").splitlines() if n.strip()}

    todo = [n for n in names if n not in done and n not in rotated and n not in heldout]
    print(f"passing {len(names)} | shipped {len(done)} | content-rotated {len(rotated)} "
          f"| heldout-reserved {len(heldout)} | remaining {len(todo)}", flush=True)
    if not todo:
        print("nothing left in the passing list -- preflight more names")
        return 0

    WORKING.write_text("\n".join(todo) + "\n", encoding="utf-8")
    return subprocess.call([
        "uv", "run", "python", "scripts/run_batch200.py",
        "--limit", str(args.limit),
        "--names", str(WORKING),
        "--preflight", "authoring/batches/batch2500_preflight.json",
        "--manifest", "miner/output/harvest_manifest_batch5.jsonl",
        "--mentions", "miner/output/mention_names_batch5.jsonl",
        "--out", str(OUT_DIR),
        "--chunk-size", str(args.chunk_size),
    ])


if __name__ == "__main__":
    sys.exit(main())
