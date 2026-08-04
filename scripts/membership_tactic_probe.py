"""Can a membership-shaped tactic extension recover the pilot's 5 non-discharges?

The pilot discharged 14/14 global facts and 1/6 membership facts. The global successes were
largely `exact?` finding the anchor theorem on Mathlib's shelf -- a LOOKUP, not a proof search.
Membership facts are bespoke concrete claims with no library twin, so lookup cannot help them;
they need the definition UNFOLDED and the resulting concrete goal discharged.

That is a different tactic shape, and the pilot's timings say the gap is not budget: three of the
five failed in under a second, i.e. the ladder exhausted rather than timed out.

**Task-symbol unfolding needs the symbol**, so the tactic set is built per fact rather than
pinned globally. Both names are unfolded: the splice is `@[reducible] def VTask.X := _root_.Real`,
so naming only `VTask.X` may resolve to the alias without reaching the real definition's body.

Run on the Mac; seconds of compute once Mathlib is warm.
"""

import json
import time
from pathlib import Path

from harness.repl import get_warm_environment
from harness.results import CheckStatus
from harness.scoring import splice_real_name
from ladder.budgets import DEFAULT_LADDER_BUDGETS, LadderBudgets, TacticBudget
from ladder.tier2 import adjudicate_tier2
from scoring.samples import load_task

PILOT = Path("scoring_output/pilot_result.json")
OUT = Path("scoring_output/membership_probe.json")


def membership_tactics(symbol: str, real: str) -> tuple[TacticBudget, ...]:
    """Membership-shaped extension, cheapest first. `symbol`/`real` are unfolded explicitly."""
    return (
        TacticBudget("decide", 10.0),
        TacticBudget("tauto", 10.0),
        TacticBudget(f"simp [{symbol}, {real}]", 15.0),
        TacticBudget(f"simp [{symbol}, {real}] <;> omega", 15.0),
        TacticBudget(f"simp [{symbol}, {real}] <;> decide", 15.0),
        TacticBudget(f"constructor <;> simp [{symbol}, {real}]", 15.0),
        TacticBudget(f"simp only [{symbol}, {real}] <;> aesop", 30.0, heavy=True),
        TacticBudget(f"unfold {symbol} <;> aesop", 30.0, heavy=True),
    )


def main() -> int:
    pilot = json.loads(PILOT.read_text(encoding="utf-8"))
    failed = [f for f in pilot["facts"] if f["status"] != "CERTIFIED"]
    print(f"re-running {len(failed)} non-discharged pilot facts with the membership extension\n")

    server, imported = get_warm_environment()
    assert imported.status is CheckStatus.PASSED, imported.detail
    base_env = imported.env

    rows = []
    for i, f in enumerate(failed, 1):
        task = load_task(f["task"])
        sig, real = task["signature"], task["truth_real_name"]
        splice = splice_real_name(server, base_env, sig, real)
        if splice.status is not CheckStatus.PASSED:
            rows.append({**f, "recovered": False, "why": "truth splice failed"})
            print(f"[{i}/{len(failed)}] {f['task']}: truth splice failed")
            continue

        budgets = LadderBudgets(
            tier2_tactics=membership_tactics(sig.name, real),
            per_fact_total_wall_clock_s=DEFAULT_LADDER_BUDGETS.per_fact_total_wall_clock_s,
        )
        t0 = time.perf_counter()
        res = adjudicate_tier2(server, splice.env, f["fact_id"], f["statement"], budgets)
        elapsed = time.perf_counter() - t0
        won = res.winning.tactic if res.winning else None
        rows.append({
            "task": f["task"], "fact_id": f["fact_id"], "recovered": won is not None,
            "winning_tactic": won, "elapsed_s": round(elapsed, 2),
            "attempts": [{"tactic": a.tactic, "status": a.status.value,
                          "elapsed_s": round(a.elapsed_s, 3)} for a in res.attempts],
        })
        print(f"[{i}/{len(failed)}] {f['task']}/{f['fact_id']}: "
              f"{'RECOVERED via ' + won if won else 'still unknown'} ({elapsed:.1f}s)")

    server.kill()
    n = sum(1 for r in rows if r["recovered"])
    summary = {"n_failed_in_pilot": len(failed), "n_recovered": n, "rows": rows}
    OUT.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'=' * 60}\nrecovered {n}/{len(failed)}")
    winners = [r["winning_tactic"] for r in rows if r["recovered"]]
    if winners:
        print(f"winning tactics: {winners}")
    print("ADOPT uniformly for Stage E" if n >= 3 else "do NOT adopt (<3/5 recovered)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
