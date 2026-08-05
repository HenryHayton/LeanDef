"""Tier-3 (LeanHammer) shakedown. The hammer has never run on real corpus data.

Three targets, in order, each answering a different question:

(a) **The pilot residue** -- `¬ VTask.Fibration ...`, the one fact tier 2 could not discharge even
    with the membership extension. It is true by construction (authored against the real
    definition), so it is a fair "can the hammer do what the cheap tiers cannot" test.
(b) **Reproving tier-2 successes, cache DISABLED.** If the hammer cannot independently reprove
    goals a cheap tactic already got, it is not working -- and a cache hit would hide that.
(c) **A deliberately FALSE statement.** The hammer must NOT prove it. This is the one that
    matters most: a tier that returns CERTIFIED on a false goal is worse than no tier at all,
    because everything downstream trusts CERTIFIED absolutely.

Tier 3 is invoked DIRECTLY rather than through `adjudicate_fact`, so what is measured is the
hammer and not tier 2 winning first.

Also measures **hammer with vs without explicit anchor premises** (the `anchors` field), the
comparison the 23 July design asked for -- cheap here because it is the same call twice.
"""

import argparse
import json
import os
import time
from pathlib import Path

from harness.repl import get_warm_environment
from harness.results import CheckStatus
from harness.scoring import splice_real_name
from ladder.budgets import DEFAULT_LADDER_BUDGETS
from ladder.tier3 import adjudicate_tier3_hammer
from scoring.samples import load_task

RESIDUE_TASK = "Relation.Fibration"
FALSE_STATEMENT = "∀ n : ℕ, n + 1 = n"  # unprovable; the hammer must not claim otherwise


def run_one(server, env, label, fact_id, statement, anchors, budgets):
    t0 = time.perf_counter()
    res = adjudicate_tier3_hammer(server, env, fact_id, statement, anchors, budgets)
    elapsed = time.perf_counter() - t0
    won = res.winning is not None
    status = res.winning.status.value if res.winning else (
        res.attempts[-1].status.value if res.attempts else "no_attempt")
    print(f"  {label:<34} {'CERTIFIED' if won else status.upper():<12} {elapsed:6.1f}s "
          f"premises={len(anchors)}", flush=True)
    if won and res.winning_script:
        print(f"      script: {res.winning_script[:110]}")
    detail = (res.attempts[-1].detail if res.attempts else "") or ""
    if not won and detail:
        print(f"      detail: {detail[:150]}")
    return {"label": label, "fact_id": fact_id, "certified": won, "status": status,
            "elapsed_s": round(elapsed, 2), "n_premises": len(anchors),
            "script": res.winning_script, "env": res.env, "detail": detail[:600]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", default="scoring_output/pilot_result.json")
    ap.add_argument("--out", default="scoring_output/hammer_shakedown.json")
    ap.add_argument("--n-reprove", type=int, default=4)
    args = ap.parse_args()

    print(f"LEAN_INTERACT_LOAD_DYNLIB={os.environ.get('LEAN_INTERACT_LOAD_DYNLIB', '(unset)')}")
    print(f"VERIFIER_REPL_PATH={os.environ.get('VERIFIER_REPL_PATH', '(unset)')}\n")

    pilot = json.loads(Path(args.pilot).read_text(encoding="utf-8"))
    residue = [f for f in pilot["facts"] if f["status"] != "CERTIFIED" and f["task"] == RESIDUE_TASK]
    reprove = [f for f in pilot["facts"] if f["status"] == "CERTIFIED"][: args.n_reprove]

    from scoring import config as scfg
    imports = scfg.imports_for(['Mathlib'])
    print(f'warming with imports={imports}')
    server, imported = get_warm_environment(imports=imports)
    assert imported.status is CheckStatus.PASSED, imported.detail
    base_env = imported.env
    budgets = DEFAULT_LADDER_BUDGETS
    rows = []
    truth_envs: dict[str, int] = {}

    def env_for(task_name):
        if task_name not in truth_envs:
            task = load_task(task_name)
            sp = splice_real_name(server, base_env, task["signature"], task["truth_real_name"])
            assert sp.status is CheckStatus.PASSED, sp.detail
            truth_envs[task_name] = sp.env
        return truth_envs[task_name]

    print("(a) PILOT RESIDUE -- tier 2 could not discharge these")
    for f in residue:
        env = env_for(f["task"])
        rows.append(run_one(server, env, f"{f['task']}/with-anchors", f["fact_id"],
                            f["statement"], f["anchors"], budgets))
        rows.append(run_one(server, env, f"{f['task']}/no-anchors", f["fact_id"] + "_bare",
                            f["statement"], [], budgets))

    print("\n(b) REPROVE tier-2 successes, cache disabled -- hammer must get them independently")
    for f in reprove:
        env = env_for(f["task"])
        rows.append(run_one(server, env, f"{f['task']}/reprove", f["fact_id"] + "_h",
                            f["statement"], f["anchors"], budgets))

    print("\n(c) SOUNDNESS -- a FALSE statement; CERTIFIED here would invalidate the tier")
    rows.append(run_one(server, base_env, "FALSE_STATEMENT", "shakedown_false",
                        FALSE_STATEMENT, [], budgets))

    server.kill()

    false_row = rows[-1]
    reproved = [r for r in rows if r["label"].endswith("/reprove")]
    residue_rows = [r for r in rows if "Fibration" in r["label"]]
    summary = {
        "soundness_ok": not false_row["certified"],
        "residue_certified": any(r["certified"] for r in residue_rows),
        "reproved": sum(1 for r in reproved if r["certified"]),
        "reprove_attempted": len(reproved),
        "anchors_helped": None,
        "rows": rows,
    }
    with_a = next((r for r in residue_rows if r["label"].endswith("with-anchors")), None)
    without_a = next((r for r in residue_rows if r["label"].endswith("no-anchors")), None)
    if with_a and without_a:
        summary["anchors_helped"] = bool(with_a["certified"]) and not without_a["certified"]

    Path(args.out).write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n" + "=" * 72)
    print(f"soundness (false stmt NOT proved): {'PASS' if summary['soundness_ok'] else '*** FAIL ***'}")
    print(f"pilot residue discharged:          {summary['residue_certified']}")
    print(f"reproved tier-2 successes:         {summary['reproved']}/{summary['reprove_attempted']}")
    print(f"anchors made the difference:       {summary['anchors_helped']}")
    ok = summary["soundness_ok"] and summary["reproved"] > 0
    print(f"\nSHAKEDOWN: {'PASS -- proceed to Stage E' if ok else 'FAIL -- stop and report'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
