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
WORKING = Path("authoring/batches/_batch2500_working.txt")

# Stages where the definition's own content is what failed. Anything else is environmental.
# `round_trip_generation` is deliberately NOT here: it is a model call that can fail
# transiently, so those names stay in the queue.
CONTENT_STAGES = {"dossier", "dossier_consistency", "classification", "mechanical_validation",
                  "fact_proposal", "composition", "emit"}

ROTATION = re.compile(r"^### (\S+) -- ROTATED \(rotated at `([a-z_]+)`\)", re.M)


def build_ledger() -> dict:
    """name -> stage, for every content-stage rotation across all review files."""
    rotated = {}
    for review in sorted(OUT_DIR.glob("batch_review_*.md")):
        for name, stage in ROTATION.findall(review.read_text(encoding="utf-8")):
            if stage in CONTENT_STAGES:
                rotated[name] = stage
            else:
                rotated.pop(name, None)  # environmental: put it back in the queue
    return rotated


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=400)
    args = ap.parse_args()

    names = [n.strip() for n in PASSING.read_text(encoding="utf-8").splitlines() if n.strip()]
    done = {p.name for p in OUT_DIR.iterdir() if (p / "task.json").exists()} if OUT_DIR.exists() else set()
    rotated = build_ledger()
    LEDGER.write_text("".join(f"{n}\t{s}\n" for n, s in sorted(rotated.items())), encoding="utf-8")

    todo = [n for n in names if n not in done and n not in rotated]
    print(f"passing {len(names)} | shipped {len(done)} | content-rotated {len(rotated)} "
          f"| remaining {len(todo)}", flush=True)
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
    ])


if __name__ == "__main__":
    sys.exit(main())
