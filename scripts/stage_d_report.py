"""First-look analysis of the Stage D tree. DECIDE-COMPONENT ONLY, PROVISIONAL.

Every view here is one of the pre-registration's committed views, computed as specified:
per-fact verified fraction macro-averaged over tasks (mean of per-task fractions) with the
pooled micro-average alongside, denominators excluding UNKNOWN/ERROR/NOT_ATTEMPTED, coverage
reported next to every fraction.

This reads the tree and computes; it never rescores. That is the whole point of persisting
per-fact verdicts rather than aggregates -- a view nobody thought of yet costs a pandas pass,
not a box session.
"""

import collections
import json
from pathlib import Path

from scoring import store

RECALLED_TARGET = {  # 31 Jul closing report, first-pass names only (repaired flags unrecoverable)
    "Nat.clog", "Nat.choose", "Nat.divisors", "Int.greatestOfBdd",
    "Finset.strongDownwardInduction", "Nat.log",
}


def load():
    rows = []
    for r in store.iter_verdicts():
        decide = [f for f in r["fact_verdicts"] if f["mechanism"] == "decide"]
        counts = collections.Counter(f["verdict"] for f in decide)
        resolved = counts["pass"] + counts["fail"]
        rows.append({
            "model": r["model_slug"], "task": r["task_name"], "sample": r["sample_index"],
            "admissible": r["admissible"], "failure": r["admissibility_failure"],
            "equiv": r.get("equivalence_certified", False),
            "noncomputable": r.get("noncomputable", False),
            "scored_as": r.get("scored_as"), "hash": r.get("candidate_hash"),
            "n_decide": len(decide), "n_pass": counts["pass"], "n_fail": counts["fail"],
            "n_unknown": counts["unknown"], "n_error": counts["error"],
            "resolved": resolved,
            "frac": (counts["pass"] / resolved) if resolved else None,
            "verdicts": {f["fact_id"]: f["verdict"] for f in decide},
        })
    return rows


def main() -> int:
    rows = load()
    models = sorted({r["model"] for r in rows})
    print(f"records: {len(rows)}   models: {len(models)}   tasks: {len({r['task'] for r in rows})}")
    print("\n*** DECIDE-COMPONENT ONLY — PROVISIONAL — NOT THE COMMITTED SELECTION ***\n")

    # (1) primary metric -----------------------------------------------------------------------
    print("=" * 100)
    print("MODEL x VERIFIED-RATE (decide component)")
    print(f"{'model':<28} {'macro':>8} {'micro':>8} {'cand':>6} {'adm':>6} {'adm%':>6} "
          f"{'scored facts':>13} {'coverage':>9} {'nc%':>6} {'equiv':>6}")
    table = {}
    for m in models:
        mr = [r for r in rows if r["model"] == m]
        adm = [r for r in mr if r["admissible"]]
        per_task = collections.defaultdict(lambda: [0, 0])
        tot_pass = tot_res = tot_facts = 0
        for r in adm:
            t = per_task[r["task"]]
            t[0] += r["n_pass"]
            t[1] += r["resolved"]
            tot_pass += r["n_pass"]
            tot_res += r["resolved"]
            tot_facts += r["n_decide"]
        task_fracs = [p / n for p, n in per_task.values() if n]
        macro = sum(task_fracs) / len(task_fracs) if task_fracs else None
        micro = tot_pass / tot_res if tot_res else None
        cov = tot_res / tot_facts if tot_facts else None
        nc = sum(1 for r in mr if r["noncomputable"]) / len(mr) if mr else 0
        eq = sum(1 for r in mr if r["equiv"])
        table[m] = {"macro": macro, "micro": micro, "n": len(mr), "adm": len(adm),
                    "coverage": cov, "nc_rate": nc, "equiv": eq, "resolved": tot_res}
        f = lambda x: f"{x:.1%}" if x is not None else "   n/a"  # noqa: E731
        print(f"{m:<28} {f(macro):>8} {f(micro):>8} {len(mr):>6} {len(adm):>6} "
              f"{f(len(adm)/len(mr)):>6} {tot_res:>6}/{tot_facts:<6} {f(cov):>9} {f(nc):>6} {eq:>6}")

    # (2) funnel -------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("FUNNEL (candidate counts; every candidate appears exactly once)")
    kinds = ["compile_error", "wrong_type", "sorry", "name_shadowed", "new_axiom", "errored"]
    print(f"{'model':<28} {'total':>6} " + " ".join(f"{k:>14}" for k in kinds) + f" {'admitted':>9}")
    for m in models:
        mr = [r for r in rows if r["model"] == m]
        c = collections.Counter(r["failure"] for r in mr if not r["admissible"])
        print(f"{m:<28} {len(mr):>6} " + " ".join(f"{c.get(k,0):>14}" for k in kinds)
              + f" {sum(1 for r in mr if r['admissible']):>9}")

    # (3) per-candidate histogram --------------------------------------------------------------
    print("\n" + "=" * 100)
    print("PER-CANDIDATE decide-fact pass fraction (admissible only)")
    bins = [(0, .001, "0%"), (.001, .25, "0-25%"), (.25, .5, "25-50%"),
            (.5, .75, "50-75%"), (.75, .999, "75-100%"), (.999, 1.01, "100%")]
    print(f"{'model':<28} " + " ".join(f"{lbl:>9}" for _, _, lbl in bins) + f" {'unscored':>9}")
    for m in models:
        adm = [r for r in rows if r["model"] == m and r["admissible"]]
        h = [sum(1 for r in adm if r["frac"] is not None and lo <= r["frac"] < hi) for lo, hi, _ in bins]
        print(f"{m:<28} " + " ".join(f"{x:>9}" for x in h)
              + f" {sum(1 for r in adm if r['frac'] is None):>9}")

    # (4) coverage per task --------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("LOWEST-COVERAGE TASKS (resolved / attempted decide facts, admissible candidates, all models)")
    cov = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        if r["admissible"]:
            c = cov[r["task"]]
            c[0] += r["resolved"]
            c[1] += r["n_decide"]
    ranked = sorted(((res / att if att else 0), t, res, att) for t, (res, att) in cov.items() if att)
    for c, t, res, att in ranked[:8]:
        print(f"  {c:6.1%}  {t:<40} {res}/{att}")
    zero = [t for c, t, _, _ in ranked if c == 0]
    print(f"  tasks with ZERO decide coverage: {len(zero)}")

    # (5) suspect facts ------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("SUSPECT FACTS (FAILED by every admissible candidate of every model)")
    fact_v = collections.defaultdict(collections.Counter)
    for r in rows:
        if r["admissible"]:
            for fid, v in r["verdicts"].items():
                fact_v[(r["task"], fid)][v] += 1
    suspects = [(t, f, c) for (t, f), c in fact_v.items() if c["fail"] > 0 and c["pass"] == 0]
    for t, f, c in sorted(suspects)[:12]:
        print(f"  {t:<38} {f:<34} fail={c['fail']}")
    print(f"  total suspect facts: {len(suspects)}  (excluded from denominators per pre-registration)")

    # (6) RECALLED_TARGET ----------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("RECALLED_TARGET slice (first-pass names only; 'harder' flags unrecoverable for repaired)")
    for m in models:
        mr = [r for r in rows if r["model"] == m and r["admissible"]]
        rt = [r for r in mr if r["task"] in RECALLED_TARGET]
        other = [r for r in mr if r["task"] not in RECALLED_TARGET]
        def agg(g):
            p = sum(x["n_pass"] for x in g)
            n = sum(x["resolved"] for x in g)
            return f"{p/n:.1%} ({n} facts)" if n else "n/a"
        print(f"  {m:<28} recalled={agg(rt):<22} other={agg(other)}")

    # (7) band-rule preview --------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("BAND-RULE PREVIEW (15-55%, midpoint 35%) — DECIDE-ONLY, NOT THE COMMITTED SELECTION")
    for m in models:
        v = table[m]["macro"]
        if v is None:
            print(f"  {m:<28} n/a")
            continue
        where = "IN BAND" if 0.15 <= v <= 0.55 else ("ABOVE (skyline)" if v > 0.55 else "BELOW")
        print(f"  {m:<28} macro={v:.1%}  |35% - v|={abs(v-0.35):.3f}  {where}")

    Path("scoring_output/stage_d_report.json").write_text(
        json.dumps({"table": table, "n_records": len(rows), "n_suspect": len(suspects)}, indent=2),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
