"""Select the Stage C pilot's ~20 proof facts. A measurement sample, not a convenience sample.

Deterministic and reproducible: no randomness, no "first N". The strata are chosen so the
resulting discharge rate generalises rather than describing one corner of the corpus --
the number this produces is the C->C2 trigger, so a biased sample would misdirect the hammer
decision in either direction.

Strata, per the pilot spec:
  - spread across >= 10 distinct tasks (no task may dominate)
  - both proof types present: `global` (242 in corpus) and `membership` (33 -- deliberately
    over-sampled relative to its 12% share, because a stratum that never appears cannot be
    measured, and membership facts are the ones whose difficulty we know least about)
  - >= 2 facts from Prop-valued tasks (11 of 41 -- different elaboration shape)
  - >= 2 facts from the richest fact suites (a proxy for structurally rich definitions)
"""

import json
from pathlib import Path

TASKS = Path(__file__).resolve().parent.parent / "prelim_testing" / "tasks"
TARGET = 20


def load():
    out = {}
    for path in sorted(TASKS.glob("*/task.json")):
        d = json.loads(path.read_text(encoding="utf-8"))
        proof = [f for f in d["facts"] if f["mechanism"] == "proof"]
        if not proof:
            continue
        out[path.parent.name] = {
            "facts": proof,
            "n_facts": len(d["facts"]),
            "prop": d["signature"]["type"].rstrip().rstrip("()").strip().endswith("Prop"),
            "truth": (d.get("provenance") or {}).get("mathlib_name"),
            "signature": d["signature"],
        }
    return out


def select(tasks: dict) -> list[dict]:
    picked: list[dict] = []
    used_tasks: set[str] = set()

    def take(task_name, fact, why):
        picked.append({
            "task": task_name, "fact_id": fact["id"], "type": fact["type"],
            "statement": fact["statement"], "anchors": fact["anchors"],
            "prop_valued": tasks[task_name]["prop"], "n_facts_in_suite": tasks[task_name]["n_facts"],
            "truth": tasks[task_name]["truth"], "stratum": why,
        })
        used_tasks.add(task_name)

    # 1. membership facts first -- the scarce stratum. One per task, breadth over depth.
    for name in sorted(tasks):
        if len(picked) >= 6:
            break
        m = [f for f in tasks[name]["facts"] if f["type"] == "membership"]
        if m and name not in used_tasks:
            take(name, m[0], "membership")

    # 2. Prop-valued tasks -- a different elaboration shape.
    for name in sorted(n for n in tasks if tasks[n]["prop"]):
        if sum(1 for p in picked if p["prop_valued"]) >= 4:
            break
        if name not in used_tasks:
            take(name, tasks[name]["facts"][0], "prop_valued")

    # 3. richest suites -- structurally rich definitions.
    for name, _ in sorted(tasks.items(), key=lambda kv: -kv[1]["n_facts"])[:6]:
        if sum(1 for p in picked if p["stratum"] == "rich_suite") >= 4:
            break
        if name not in used_tasks:
            take(name, tasks[name]["facts"][0], "rich_suite")

    # 4. fill to TARGET with global facts from tasks not yet represented -- breadth.
    for name in sorted(tasks):
        if len(picked) >= TARGET:
            break
        if name in used_tasks:
            continue
        g = [f for f in tasks[name]["facts"] if f["type"] == "global"]
        if g:
            take(name, g[0], "global_breadth")
    return picked


def main():
    tasks = load()
    picked = select(tasks)
    out = Path(__file__).resolve().parent.parent / "scoring_output" / "pilot_selection.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(picked, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"selected {len(picked)} facts across {len({p['task'] for p in picked})} tasks -> {out}")
    for k in ("membership", "prop_valued", "rich_suite", "global_breadth"):
        print(f"  {k:16s} {sum(1 for p in picked if p['stratum'] == k)}")
    print(f"  prop-valued tasks represented: {sum(1 for p in picked if p['prop_valued'])}")
    print(f"  types: global={sum(1 for p in picked if p['type']=='global')} "
          f"membership={sum(1 for p in picked if p['type']=='membership')}")


if __name__ == "__main__":
    main()
