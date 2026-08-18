"""Emit the mid-size training manifest: every task with a kernel-proven vacuity detector.

    uv run python scripts/build_midsize_training.py

The selection bar ("T3") is the one that decides whether a task can do its job at all. Below
it, a task cannot demonstrably refute a vacuous `def VTask.X _ := True` candidate: the reject
fact either does not exist or was never kernel-certified, so it returns UNKNOWN and drops out
of fidelity's denominator. A task clears T3 when ALL of:

  * `task.json` validates against the current schema
  * >= 3 facts
  * >= 1 accept-side fact      (it can confirm, not only refute -- two-sided)
  * >= 1 CERTIFIED reject fact (the detector is kernel-proven, not merely present)

Reject-shaped is `polarity == "reject"` or a negation token in the statement, matching the
counting used throughout the batch reports.

**No held-out split is carved out of this corpus, by design.** Held-out data for this run is
authored FRESH during training instead: a task authored after the model was trained cannot have
leaked into it, which a frozen carve-out of an existing corpus cannot promise.

Consequently `pilot_corpus_v1`'s former held-out members are INCLUDED here like any other task.
Nothing was ever evaluated against them as held-out (checked: `pilot_result.json` is an
unrelated early-August tier-2 discharge measurement, and the scoring runs that mention some of
them are the general batch-200 sweeps), so holding them back would forfeit 7 qualifying tasks
to protect a split that is no longer in use. Every entry keeps its `pilot_role` tag.

Each entry is pinned by a SHA-256 prefix of its `task.json`, so later authoring or re-discharge
work that mutates a task is detectable at harvest time rather than silently changing the corpus.
"""

import hashlib
import json
import sys
from pathlib import Path

CORPORA = [("july_2026-07-29", "prelim_testing/tasks"),
           ("batch200_2026-08-11", "prelim_testing/tasks_batch200"),
           ("batch2500_2026-08-16", "prelim_testing/tasks_batch2500")]
PILOT = Path("training/config/pilot_corpus_v1.json")
OUT = Path("training/config/midsize_training_v1.json")


def is_reject(f: dict) -> bool:
    return f.get("polarity") == "reject" or any(
        t in (f.get("statement") or "") for t in ("¬", "∉", "≠"))


def main() -> int:
    from harness.task_schema import validate_task_data

    pilot_role = {}
    if PILOT.exists():
        p = json.loads(PILOT.read_text(encoding="utf-8"))
        for group in ("training", "heldout", "annex"):
            for t in p.get(group, []):
                pilot_role[t["name"]] = group

    entries, skipped = [], 0
    for corpus, d in CORPORA:
        for task_dir in sorted(Path(d).iterdir()):
            tj = task_dir / "task.json"
            if not tj.exists():
                continue
            raw = tj.read_bytes()
            data = json.loads(raw.decode("utf-8"))
            facts = data["facts"]
            reject = [f for f in facts if is_reject(f)]
            accept = [f for f in facts if not is_reject(f)]
            cert_reject = [f for f in reject if f.get("validation_status") == "CERTIFIED"]
            try:
                validate_task_data(data)
            except Exception:  # noqa: BLE001 -- schema-invalid tasks simply do not qualify
                skipped += 1
                continue
            if not (len(facts) >= 3 and accept and cert_reject):
                skipped += 1
                continue
            entries.append({
                "name": task_dir.name,
                "corpus": corpus,
                "task_dir": str(task_dir),
                "task_json": str(tj),
                "task_hash_sha256_16": hashlib.sha256(raw).hexdigest()[:16],
                "pilot_role": pilot_role.get(task_dir.name),
                "n_facts": len(facts),
                "n_accept": len(accept),
                "n_reject": len(reject),
                "n_certified_reject": len(cert_reject),
                "n_certified": sum(1 for f in facts
                                   if f.get("validation_status") == "CERTIFIED"),
                "n_decide": sum(1 for f in facts if f.get("mechanism") == "decide"),
                "mathlib_name": (data.get("provenance") or {}).get("mathlib_name"),
                "signature_name": (data.get("signature") or {}).get("name"),
            })

    entries.sort(key=lambda e: (-e["n_certified_reject"], -e["n_facts"], e["name"]))
    by_corpus = {c: sum(1 for e in entries if e["corpus"] == c) for c, _ in CORPORA}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "corpus_id": "midsize_training_v1",
        "created": "2026-08-18",
        "n_tasks": len(entries),
        "selection_bar": {
            "id": "T3",
            "summary": "kernel-proven vacuity detector, two-sided",
            "requires": ["task.json validates against the current schema",
                         "at least 3 facts",
                         "at least 1 accept-side fact",
                         "at least 1 reject fact with validation_status == CERTIFIED"],
            "reject_shaped_rule": "polarity == 'reject' OR statement contains one of ¬ ∉ ≠",
            "why": ("Below this bar a task cannot demonstrably refute a vacuous "
                    "`def VTask.X _ := True` candidate: its reject fact returns UNKNOWN and "
                    "drops out of fidelity's denominator."),
        },
        "drawn_from": {c: d for c, d in CORPORA},
        "by_corpus": by_corpus,
        "tasks_considered": len(entries) + skipped,
        "tasks_excluded": skipped,
        "heldout_policy": {
            "split_in_this_file": None,
            "plan": ("Held-out data is authored FRESH during the training run rather than "
                     "carved out of this corpus. Tasks authored after training cannot have "
                     "leaked into it, which a frozen carve-out cannot promise."),
            "former_pilot_heldout_included": sorted(
                e["name"] for e in entries if e["pilot_role"] == "heldout"),
            "former_pilot_heldout_note": (
                "pilot_corpus_v1 froze these as held-out. That split is retired, nothing was "
                "ever evaluated against them as held-out, so they are trained on like any "
                "other task."),
        },
        "warnings": [
            ("Every task in `tasks` is trainable -- there is no held-out subset to filter "
             "out. See `heldout_policy`."),
            ("task_hash_sha256_16 pins each task.json. Authoring and re-discharge work is "
             "ongoing on batch2500, so verify hashes at harvest time; a mismatch means the "
             "task changed after this manifest was written."),
            ("Fidelity is a near-vacuous metric on this corpus (FAIL is nearly unreachable "
             "on forward facts). Separation against mutant suites is the signal that "
             "survived scrutiny. See docs/batch_reports/vacuity_specimen_2026-08-11.md."),
        ],
        "tasks": entries,
    }, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"{len(entries)} tasks -> {OUT}")
    print(f"  by corpus: {by_corpus}")
    print(f"  excluded (failed the bar or schema): {skipped}")
    print(f"  pilot roles: " + str({r: sum(1 for e in entries if e['pilot_role'] == r)
                                    for r in ('training', 'heldout', 'annex')}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
