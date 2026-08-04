"""Stage C pilot: ~20 authored proof facts against the TRUTH splice, tiers 1-2 only.

Produces the C->C2 trigger number: **of the facts that elaborate, what fraction does tier 2
discharge?** Everything else here exists to make that number interpretable rather than a bare
percentage.

**Tiers 1-2 only, enforced structurally.** `ladder.adjudicate.adjudicate_fact` calls tier 3
unconditionally, and Hammer IS installed on the box, so routing through it would silently run
the hammer this session is explicitly not authorised to run. This driver therefore calls the
elaboration probe and `adjudicate_tier2` directly -- the tier-3 code is never reached, rather
than being reached and asked nicely to stop.

**Against the truth splice, not a candidate.** These facts were authored to be true of the real
definition, so a failure to discharge is a statement about the LADDER (or about the fact), not
about any model. That is what makes this a calibration rather than a score. A fact that fails
even to elaborate is a corpus finding and is reported separately: on authored facts it should be
near zero, unlike the 55/60 seen on context-stripped mined statements.

Every tier-2 success is written to a side ledger (fact id -> script), the first real payment on
the truth-side debt: all 275 proof facts in the corpus are `PROVISIONALLY_VALIDATED` with
`cached_script: null`. `task.json` is NOT mutated mid-prelim.
"""

import argparse
import collections
import json
import time
from pathlib import Path

from ladder.adjudicate import _probe_elaboration
from ladder.budgets import DEFAULT_LADDER_BUDGETS
from ladder.cache import CacheEntry, ProofScriptCache, statement_hash, toolchain_pin
from ladder.statuses import AdjudicationStatus, ElaborationStatus
from ladder.tier2 import adjudicate_tier2
from scoring.samples import load_task
from scoring.runner import ServerHandle
from harness.scoring import splice_real_name
from harness.results import CheckStatus


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selection", default="scoring_output/pilot_selection.json")
    ap.add_argument("--out", default="scoring_output/pilot_result.json")
    ap.add_argument("--ledger", default="scoring_output/pilot_script_ledger.jsonl")
    ap.add_argument("--cache", default="ladder/output/proof_script_cache.jsonl")
    args = ap.parse_args()

    selection = json.loads(Path(args.selection).read_text(encoding="utf-8"))
    cache = ProofScriptCache(Path(args.cache))
    pin = toolchain_pin()
    budgets = DEFAULT_LADDER_BUDGETS

    handle = ServerHandle()
    server, base_env = handle.get()

    results, ledger = [], []
    truth_envs: dict[str, int] = {}
    t_start = time.perf_counter()

    for i, item in enumerate(selection, 1):
        task_name, fact_id = item["task"], item["fact_id"]
        row = {**item, "elaborates": None, "status": None, "tier": None,
               "winning_tactic": None, "wall_s": 0.0, "attempts": []}
        started = time.perf_counter()

        # Truth splice, once per task: the fact must be checked against the REAL definition.
        if task_name not in truth_envs:
            task = load_task(task_name)
            sig, real = task["signature"], task["truth_real_name"]
            splice = splice_real_name(server, base_env, sig, real)
            if splice.status is not CheckStatus.PASSED or splice.env is None:
                row.update(status="TRUTH_SPLICE_FAILED", detail=(splice.detail or "")[:400])
                row["wall_s"] = time.perf_counter() - started
                results.append(row)
                print(f"[{i:2d}/{len(selection)}] {task_name}/{fact_id}: TRUTH SPLICE FAILED", flush=True)
                continue
            truth_envs[task_name] = splice.env
        env = truth_envs[task_name]

        elaboration = _probe_elaboration(server, env, item["statement"], budgets)
        row["elaborates"] = elaboration.value
        if elaboration is not ElaborationStatus.ELABORATES:
            row["status"] = "DID_NOT_ELABORATE"
            row["wall_s"] = time.perf_counter() - started
            results.append(row)
            print(f"[{i:2d}/{len(selection)}] {task_name}/{fact_id}: did not elaborate", flush=True)
            continue

        t2 = adjudicate_tier2(server, env, fact_id, item["statement"], budgets)
        truth_envs[task_name] = t2.env  # tier 2's recovery loop may have replaced it
        row["attempts"] = [
            {"tactic": a.tactic, "status": a.status.value, "elapsed_s": round(a.elapsed_s, 4)}
            for a in t2.attempts
        ]
        if t2.winning is not None:
            row.update(status="CERTIFIED", tier=2, winning_tactic=t2.winning.tactic)
            if t2.winning_script:
                entry = CacheEntry(
                    statement_hash=statement_hash(item["statement"]), toolchain_pin=pin,
                    tier=2, script=t2.winning_script, axiom_closure=[],
                    wall_clock_s=round(time.perf_counter() - started, 3),
                    canonical_statement=item["statement"],
                )
                try:
                    cache.put(entry)
                except Exception as e:  # noqa: BLE001
                    row["cache_write_error"] = str(e)
                ledger.append({"task": task_name, "fact_id": fact_id,
                               "tactic": t2.winning.tactic, "script": t2.winning_script})
        else:
            died = any(a.status is AdjudicationStatus.ENV_DEATH for a in t2.attempts)
            row["status"] = "ENV_DEATH" if died else "UNKNOWN"

        row["wall_s"] = time.perf_counter() - started
        results.append(row)
        print(f"[{i:2d}/{len(selection)}] {task_name}/{fact_id}: {row['status']}"
              f"{' via ' + row['winning_tactic'] if row['winning_tactic'] else ''}"
              f" ({row['wall_s']:.1f}s)", flush=True)

    handle.close()

    elaborated = [r for r in results if r["elaborates"] == "elaborates"]
    certified = [r for r in elaborated if r["status"] == "CERTIFIED"]
    per_tactic = collections.defaultdict(list)
    winners = collections.Counter()
    for r in results:
        for a in r["attempts"]:
            per_tactic[a["tactic"]].append(a["elapsed_s"])
        if r["winning_tactic"]:
            winners[r["winning_tactic"]] += 1

    summary = {
        "generated_at_unix": int(time.time()),
        "n_selected": len(selection),
        "n_elaborated": len(elaborated),
        "n_did_not_elaborate": sum(1 for r in results if r["status"] == "DID_NOT_ELABORATE"),
        "n_truth_splice_failed": sum(1 for r in results if r["status"] == "TRUTH_SPLICE_FAILED"),
        "n_certified_tier2": len(certified),
        "tier2_discharge_rate_of_elaborated": (len(certified) / len(elaborated)) if elaborated else None,
        "tier2_discharge_rate_of_selected": len(certified) / len(selection) if selection else None,
        "winning_tactics": dict(winners),
        "per_tactic_timing": {
            t: {"n": len(v), "total_s": round(sum(v), 2), "mean_s": round(sum(v) / len(v), 3),
                "max_s": round(max(v), 2)}
            for t, v in sorted(per_tactic.items())
        },
        "cache_entries_written": len(ledger),
        "server_recycles": handle.recycles,
        "env_probe_fires": handle.env_probe_fires,
        "total_wall_s": round(time.perf_counter() - t_start, 1),
        "facts": results,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    with Path(args.ledger).open("a", encoding="utf-8") as f:
        for e in ledger:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    rate = summary["tier2_discharge_rate_of_elaborated"]
    print("\n" + "=" * 70)
    print(f"elaborated:        {len(elaborated)}/{len(selection)}")
    print(f"tier-2 certified:  {len(certified)}/{len(elaborated)}"
          f"  -> discharge rate {rate:.1%}" if rate is not None else "  -> n/a")
    print(f"winning tactics:   {dict(winners)}")
    print(f"cache entries:     {len(ledger)}")
    print(f"total wall:        {summary['total_wall_s']}s")
    if rate is not None:
        trigger = ("no hammer for prelim" if rate >= 0.60
                   else "C2 FIRES (wake tier 3)" if rate < 0.30 else "JUDGMENT (between 30% and 60%)")
        print(f"C->C2 trigger read: {trigger}  [reported, not acted on]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
