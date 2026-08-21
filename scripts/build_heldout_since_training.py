"""Emit the held-out evaluation set: T3 tasks authored AFTER the training snapshot.

    uv run python scripts/build_heldout_since_training.py [--snapshot d81ba57]

The mid-size training run used the 177-task snapshot of
`training/config/midsize_training_v1.json` (git commit d81ba57, 18 Aug). Authoring continued
after that, so every task added since is held-out **by construction**: it did not exist when the
model was trained and therefore cannot have leaked into it. That is a stronger guarantee than a
carve-out of an existing corpus, which can only promise that a task was withheld, not that it
was unknown.

Membership is computed by diffing the CURRENT manifest against the exact snapshot recovered from
git, so the split is reproducible and auditable rather than asserted.

**FROZEN ONCE WRITTEN.** This set is derived -- it recomputes "everything authored since the
snapshot" -- so it grows on every authoring run. An evaluation set that moves underneath you
makes two scoring runs incomparable, so the script REFUSES to overwrite an existing file.
Use `--version N` to cut a new numbered set, or `--force` to deliberately rewrite one.

Facts are inlined -- id, statement, mechanism, polarity, validation_status, and the discharge
tier where one exists -- so the evaluation harness can score against this file without walking
the task directories. `task_json` still points at each task on disk for anything more.

**Only CERTIFIED facts are scoring-safe.** A PROVISIONALLY_VALIDATED fact was never kernel-
confirmed against ground truth, so a candidate disagreeing with it is not necessarily wrong.
Counts for both are given per task; `n_certified` is the honest denominator.
"""

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

MANIFEST = Path("training/config/midsize_training_v1.json")
OUT_TEMPLATE = "training/config/heldout_since_training_v{n}.json"


def snapshot_names(commit: str) -> set:
    raw = subprocess.run(["git", "show", f"{commit}:{MANIFEST}"],
                         capture_output=True, text=True, check=True).stdout
    return {e["name"] for e in json.loads(raw)["tasks"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", default="d81ba57",
                    help="git commit of the manifest that training consumed")
    ap.add_argument("--version", type=int, default=1,
                    help="which numbered held-out set to write")
    ap.add_argument("--force", action="store_true",
                    help="overwrite a frozen set (you almost never want this)")
    args = ap.parse_args()

    out = Path(OUT_TEMPLATE.format(n=args.version))
    if out.exists() and not args.force:
        existing = json.loads(out.read_text(encoding="utf-8"))
        print(f"REFUSING to overwrite {out} -- it is frozen at "
              f"{existing['n_heldout_tasks']} tasks / {existing['n_facts']} facts.\n"
              f"An evaluation set that grows underneath you makes scoring runs "
              f"incomparable.\n"
              f"  to cut a NEW set:      --version {args.version + 1}\n"
              f"  to rewrite this one:   --force")
        return 1

    trained_on = snapshot_names(args.snapshot)
    current = json.loads(MANIFEST.read_text(encoding="utf-8"))
    fresh = [e for e in current["tasks"] if e["name"] not in trained_on]

    entries = []
    for e in fresh:
        data = json.loads(Path(e["task_json"]).read_text(encoding="utf-8"))
        facts = []
        for f in data["facts"]:
            facts.append({
                "id": f.get("id"),
                "statement": f.get("statement"),
                "mechanism": f.get("mechanism"),
                "polarity": f.get("polarity"),
                "validation_status": f.get("validation_status"),
                "discharge_tier": (f.get("discharge") or {}).get("tier"),
                "scoring_safe": f.get("validation_status") == "CERTIFIED",
            })
        entries.append({
            "name": e["name"],
            "corpus": e["corpus"],
            "task_dir": e["task_dir"],
            "task_json": e["task_json"],
            "task_hash_sha256_16": e["task_hash_sha256_16"],
            "mathlib_name": e["mathlib_name"],
            "signature_name": e["signature_name"],
            "signature_type": (data.get("signature") or {}).get("type"),
            "n_facts": len(facts),
            "n_certified": sum(1 for f in facts if f["scoring_safe"]),
            "n_reject": e["n_reject"],
            "n_certified_reject": e["n_certified_reject"],
            "facts": facts,
        })

    entries.sort(key=lambda x: (-x["n_certified_reject"], -x["n_facts"], x["name"]))
    n_facts = sum(x["n_facts"] for x in entries)
    n_cert = sum(x["n_certified"] for x in entries)
    by_corpus = {}
    for x in entries:
        by_corpus[x["corpus"]] = by_corpus.get(x["corpus"], 0) + 1

    out.write_text(json.dumps({
        "set_id": f"heldout_since_training_v{args.version}",
        "frozen": ("This set is frozen. The generator refuses to overwrite it, because it is "
                   "derived from 'everything authored since the snapshot' and would otherwise "
                   "grow on every authoring run, making scoring runs incomparable."),
        "created": "2026-08-20",
        "purpose": ("Held-out evaluation set for the mid-size training run. Every task here was "
                    "authored AFTER the model was trained, so it cannot have leaked into "
                    "training -- a guarantee a corpus carve-out cannot make."),
        "trained_on_snapshot": {
            "manifest": str(MANIFEST),
            "git_commit": args.snapshot,
            "n_tasks": len(trained_on),
        },
        "n_heldout_tasks": len(entries),
        "n_facts": n_facts,
        "n_certified_facts": n_cert,
        "by_corpus": by_corpus,
        "selection_bar": current["selection_bar"],
        "disjointness": ("Computed by diffing the current manifest against the training snapshot "
                         "recovered from git, not asserted. Verified zero overlap by name."),
        "scoring_notes": [
            ("Score only facts with scoring_safe == true (validation_status CERTIFIED). A "
             f"PROVISIONALLY_VALIDATED fact was never kernel-confirmed against ground truth; "
             f"{n_facts - n_cert} of {n_facts} facts here fall in that category."),
            ("Fidelity is near-vacuous on this corpus: FAIL is nearly unreachable on forward "
             "facts and UNKNOWN leaves the denominator, so a `:= True` candidate scores ~1.000. "
             "Separation against mutant suites is the signal that survived scrutiny."),
            ("n_certified_reject > 0 on every task by construction (the T3 bar), so every task "
             "here can demonstrably refute a vacuous candidate."),
        ],
        "tasks": entries,
    }, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"trained-on snapshot {args.snapshot}: {len(trained_on)} tasks")
    print(f"current manifest:                  {current['n_tasks']} tasks")
    print(f"HELD-OUT (authored since):         {len(entries)} tasks, {n_facts} facts "
          f"({n_cert} certified)")
    print(f"  by corpus: {by_corpus}")
    print(f"  overlap with trained set: {len({e['name'] for e in entries} & trained_on)}")
    print(f"-> {out}  (frozen; re-running will refuse to overwrite)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
