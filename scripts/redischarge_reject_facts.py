"""Re-discharge uncertified proof-mechanism REJECT facts with the negation tactic set.

    uv run python scripts/redischarge_reject_facts.py [--dry-run] [--limit N]

Part 2 of the pre-pilot fixes. `authoring.fact_validation.discharge_budgets_for` now puts
`NEGATION_TACTICS` in front of the pinned forward set for reject-shaped facts; this re-runs
validation for exactly the facts that were affected, and nothing else.

**Scope is enumerated from the shipped files, not from the handoff's counts** -- and the counts
differ: 116 facts across 68 tasks, against the handoff's "75 across 38". The handoff counted only
facts in tasks where NO reject fact was certified; tasks that already have a working detector but
carry additional uncertified reject facts were missed, and those facts are equally affected.

**Certified facts are never touched.** Only facts that are (a) reject-shaped, (b) proof-mechanism,
(c) not already CERTIFIED are re-run. Everything else is copied through byte-for-byte.

**No box needed.** Discharge calls `adjudicate_tier2` only -- tier 3 (hammer, Linux-only) is never
invoked on this path -- so a local warm Mathlib is equivalent to the box and avoids the EC2 cost
and credential churn. Verified by reading `validate_fact`, not assumed.

Writes are atomic (tmp + replace) and the pre/post `task.json` SHA-256 of every touched file is
recorded, so the training session can re-pin its corpus from the delta report.
"""

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

TASKS = Path("prelim_testing/tasks_batch200")
OUT = Path("scoring_output/redischarge_report.json")


def is_reject(f: dict) -> bool:
    return f.get("polarity") == "reject" or any(t in f["statement"] for t in ("¬", "∉", "≠"))


def targets_of(facts: list) -> list:
    return [f["id"] for f in facts
            if is_reject(f) and f["mechanism"] == "proof"
            and f.get("validation_status") != "CERTIFIED"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    from authoring.fact_validation import CERTIFIED, validate_fact
    from harness.facts import Fact
    from harness.repl import get_warm_environment
    from harness.results import CheckStatus
    from harness.scoring import splice_real_name
    from harness.signature import PinnedSignature
    from scoring.candidate import truth_signature_for

    todo = []
    for d in sorted(TASKS.iterdir()):
        tj = d / "task.json"
        if not tj.exists():
            continue
        data = json.loads(tj.read_text(encoding="utf-8"))
        ids = targets_of(data["facts"])
        if ids:
            todo.append((d.name, tj, ids))
    if args.limit:
        todo = todo[: args.limit]
    n_facts = sum(len(i) for _, _, i in todo)
    print(f"{len(todo)} tasks, {n_facts} uncertified proof-mechanism reject facts", flush=True)
    if args.dry_run:
        return 0

    server, base = get_warm_environment()
    if base.status is not CheckStatus.PASSED:
        raise RuntimeError(base.detail)

    report = {"tasks": {}, "converted": 0, "attempted": 0, "unchanged": 0, "other": 0}
    t0 = time.perf_counter()
    for i, (name, tj, ids) in enumerate(todo, 1):
        raw = tj.read_bytes()
        data = json.loads(raw.decode("utf-8"))
        sig = PinnedSignature(name=data["signature"]["name"],
                              type_sig=data["signature"]["type"])
        real = (data.get("provenance") or {}).get("mathlib_name")
        imports = data["signature"].get("imports")
        splice = splice_real_name(server, base.env, truth_signature_for(sig), real)
        if splice.status is not CheckStatus.PASSED:
            report["tasks"][name] = {"error": f"truth splice failed: {(splice.detail or '')[:120]}"}
            continue
        truth_env = splice.env

        changes = []
        by_id = {f["id"]: f for f in data["facts"]}
        for fid in ids:
            fd = by_id[fid]
            fact = Fact.from_dict(fd)
            before = fd.get("validation_status")
            v = validate_fact(server, truth_env, fact, sig.name, real, imports=imports)
            report["attempted"] += 1
            if v.status == CERTIFIED:
                fd["validation_status"] = CERTIFIED
                fd["cached_script"] = v.winning_script
                fd["axiom_closure"] = v.axiom_closure
                fd["discharge"] = {"tier": v.tier, "wall_clock_s": v.wall_clock_s,
                                   "at": "authoring", "script": v.winning_script,
                                   "self_cited": bool(fd.get("self_restatement"))}
                report["converted"] += 1
                changes.append({"fact_id": fid, "before": before, "after": CERTIFIED,
                                "winning_tactic": v.winning_script})
            elif v.status in ("REJECTED_RESTATEMENT", "REJECTED_ANCHOR",
                              "QUARANTINED_FALSE_OF_TRUTH"):
                # A re-run exercises the whole ladder, so a fact can turn out defective now.
                # Recorded, NOT silently dropped -- the fact keeps its shipped status and the
                # finding surfaces in the report for a human call.
                report["other"] += 1
                changes.append({"fact_id": fid, "before": before, "after": f"FLAGGED:{v.status}",
                                "detail": v.detail[:160], "applied": False})
            else:
                report["unchanged"] += 1

        if any(c.get("after") == CERTIFIED for c in changes):
            new = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            tmp = tj.with_suffix(".json.tmp")
            tmp.write_bytes(new)
            os.replace(tmp, tj)
            report["tasks"][name] = {
                "hash_before": hashlib.sha256(raw).hexdigest(),
                "hash_after": hashlib.sha256(new).hexdigest(),
                "changes": changes,
            }
        elif changes:
            report["tasks"][name] = {"hash_before": hashlib.sha256(raw).hexdigest(),
                                     "hash_after": hashlib.sha256(raw).hexdigest(),
                                     "changes": changes}
        if i % 10 == 0:
            rate = i / max(time.perf_counter() - t0, 1e-6)
            print(f"  {i}/{len(todo)} tasks  converted={report['converted']}/{report['attempted']}"
                  f"  eta {(len(todo)-i)/rate/60:.0f} min", flush=True)
    server.kill()

    report["wall_clock_min"] = round((time.perf_counter() - t0) / 60, 1)
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\nCONVERTED {report['converted']}/{report['attempted']} "
          f"(unchanged {report['unchanged']}, flagged {report['other']}) "
          f"in {report['wall_clock_min']} min -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
