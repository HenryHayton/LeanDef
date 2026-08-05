"""The evidence pack — the artefact base selection is made from.

Complete-data versions of every committed report view, computed per the pre-registration
(denominators exclude UNKNOWN/ERROR/NOT_ATTEMPTED; dedup provenance preserved; slices as
specified). Deliberately NOT a single ranking: the 2026-08-07 amendment removed the sole primary
metric precisely because Stage D showed different metrics disagreeing about direction.

The verbatim proxy is `equivalence_certified` — a candidate the kernel proved definitionally
equal to the truth. That is a stronger and cheaper signal than any textual heuristic, and it is
what makes the UNKNOWN-by-phrasing question answerable: if proof-fact UNKNOWNs concentrate on
non-verbatim candidates, the ladder is measuring phrasing rather than correctness.
"""

import collections
import json
from pathlib import Path

from scoring import store

RECALLED_TARGET = {
    "Nat.clog", "Nat.choose", "Nat.divisors", "Int.greatestOfBdd",
    "Finset.strongDownwardInduction", "Nat.log",
}
TRAINABILITY = {
    "goedel-prover-v2-8b": "Qwen2.5-7B family · 8B · 4k-32k ctx · MIT-style · LoRA-standard",
    "goedel-formalizer-v2-8b": "Qwen2.5-7B family · 8B · 4k-32k ctx · MIT-style · LoRA-standard",
    "qwen2-5-coder-7b-instruct": "Qwen2.5 native · 7B · 32k ctx · Apache-2.0 · LoRA-standard",
}


def rows():
    out = []
    for r in store.iter_verdicts():
        fv = r["fact_verdicts"]
        dec = [f for f in fv if f["mechanism"] == "decide"]
        prf = [f for f in fv if f["mechanism"] == "proof"]
        cd = collections.Counter(f["verdict"] for f in dec)
        cp = collections.Counter(f["verdict"] for f in prf)
        res_d = cd["pass"] + cd["fail"]
        res_p = cp["pass"] + cp["fail"]
        tiers = collections.Counter()
        for f in fv:
            if f["verdict"] == "pass":
                tiers[f.get("certified_via") if f.get("certified_via") == "equivalence" else f"tier{f.get('tier')}"] += 1
        out.append({
            "model": r["model_slug"], "task": r["task_name"], "sample": r["sample_index"],
            "admissible": r["admissible"], "failure": r["admissibility_failure"],
            "equiv": r.get("equivalence_certified", False), "noncomputable": r.get("noncomputable", False),
            "hash": r.get("candidate_hash"), "scored_as": r.get("scored_as"),
            "code": r.get("extracted_code"), "detail": r.get("admissibility_detail", ""),
            "d_pass": cd["pass"], "d_fail": cd["fail"], "d_unknown": cd["unknown"], "d_res": res_d,
            "p_pass": cp["pass"], "p_unknown": cp["unknown"], "p_error": cp["error"],
            "p_attempted": cp["pass"] + cp["unknown"] + cp["error"], "p_res": res_p,
            "n_facts": len(fv), "n_pass": cd["pass"] + cp["pass"],
            "all_pass": r["admissible"] and (cd["fail"] == 0) and (cd["pass"] + cp["pass"] > 0)
                        and cp["unknown"] == 0 and cd["unknown"] == 0,
            "tiers": tiers,
        })
    return out


def pct(x):
    return f"{x:.1%}" if x is not None else "n/a"


def main() -> int:
    R = rows()
    models = sorted({r["model"] for r in R})
    print(f"# Evidence pack — {len(R)} candidate records, {len(models)} models, "
          f"{len({r['task'] for r in R})} tasks\n")

    print("=" * 104)
    print("SURVIVOR RATE + COMPONENTS (survivor = admissible, no FAIL, at least one PASS, nothing unresolved)")
    hdr = (f"{'model':<27}{'survivors':>11}{'admis':>8}{'decide fid':>12}{'proof fid':>11}"
           f"{'proof cov':>11}{'nc%':>7}{'equiv':>7}")
    print(hdr)
    summary = {}
    for m in models:
        mr = [r for r in R if r["model"] == m]
        adm = [r for r in mr if r["admissible"]]
        dp = sum(r["d_pass"] for r in adm)
        dr = sum(r["d_res"] for r in adm)
        pp = sum(r["p_pass"] for r in adm)
        pr_ = sum(r["p_res"] for r in adm)
        patt = sum(r["p_attempted"] for r in adm)
        surv = sum(1 for r in mr if r["all_pass"])
        summary[m] = {
            "candidates": len(mr), "admissible": len(adm), "survivors": surv,
            "survivor_rate": surv / len(mr) if mr else None,
            "admissibility": len(adm) / len(mr) if mr else None,
            "decide_fidelity": dp / dr if dr else None,
            "proof_fidelity": pp / pr_ if pr_ else None,
            "proof_coverage": pr_ / patt if patt else None,
            "noncomputable_rate": sum(1 for r in mr if r["noncomputable"]) / len(mr) if mr else None,
            "equivalence": sum(1 for r in mr if r["equiv"]),
        }
        s = summary[m]
        print(f"{m:<27}{surv:>5}/{len(mr):<5}{pct(s['admissibility']):>8}{pct(s['decide_fidelity']):>12}"
              f"{pct(s['proof_fidelity']):>11}{pct(s['proof_coverage']):>11}"
              f"{pct(s['noncomputable_rate']):>7}{s['equivalence']:>7}")

    print("\n" + "=" * 104)
    print("PER-TIER DISCHARGE CASCADE (which tier certified each passing fact) — the 23 Jul measurement")
    print(f"{'model':<27}{'tier1':>9}{'tier2':>9}{'tier3':>9}{'tier4':>9}{'equivalence':>13}{'total':>9}")
    for m in models:
        agg = collections.Counter()
        for r in R:
            if r["model"] == m:
                agg.update(r["tiers"])
        tot = sum(agg.values())
        print(f"{m:<27}{agg.get('tier1',0):>9}{agg.get('tier2',0):>9}{agg.get('tier3',0):>9}"
              f"{agg.get('tier4',0):>9}{agg.get('equivalence',0):>13}{tot:>9}")
        summary[m]["cascade"] = dict(agg)

    print("\n" + "=" * 104)
    print("UNKNOWN SPLIT: verbatim (kernel-proved equal to truth) vs non-verbatim")
    print("  If UNKNOWNs concentrate on non-verbatim candidates, the ladder measures PHRASING, not correctness.")
    print(f"{'model':<27}{'verbatim UNK':>16}{'non-verbatim UNK':>20}")
    for m in models:
        adm = [r for r in R if r["model"] == m and r["admissible"]]
        vb = [r for r in adm if r["equiv"]]
        nv = [r for r in adm if not r["equiv"]]
        def unk(g):
            u = sum(r["p_unknown"] for r in g)
            a = sum(r["p_attempted"] for r in g)
            return f"{u}/{a} = {u/a:.1%}" if a else "n/a"
        print(f"{m:<27}{unk(vb):>16}{unk(nv):>20}")
        summary[m]["unknown_verbatim"] = unk(vb)
        summary[m]["unknown_nonverbatim"] = unk(nv)

    print("\n" + "=" * 104)
    print("FUNNEL")
    kinds = ["compile_error", "wrong_type", "sorry", "name_shadowed", "new_axiom", "errored"]
    print(f"{'model':<27}{'total':>7}" + "".join(f"{k:>15}" for k in kinds) + f"{'admitted':>10}{'survivors':>11}")
    for m in models:
        mr = [r for r in R if r["model"] == m]
        c = collections.Counter(r["failure"] for r in mr if not r["admissible"])
        print(f"{m:<27}{len(mr):>7}" + "".join(f"{c.get(k,0):>15}" for k in kinds)
              + f"{sum(1 for r in mr if r['admissible']):>10}{sum(1 for r in mr if r['all_pass']):>11}")

    print("\n" + "=" * 104)
    print("MODEL x TASK: best-of-10, all-fail and sometimes-succeeds counts")
    print(f"{'model':<27}{'tasks w/ >=1 survivor':>24}{'tasks all-fail':>17}{'distinct answers/task':>23}")
    for m in models:
        mr = [r for r in R if r["model"] == m]
        by_task = collections.defaultdict(list)
        for r in mr:
            by_task[r["task"]].append(r)
        any_ok = sum(1 for g in by_task.values() if any(x["all_pass"] for x in g))
        allfail = sum(1 for g in by_task.values() if not any(x["all_pass"] for x in g))
        distinct = sum(len({x["hash"] for x in g}) for g in by_task.values()) / max(len(by_task), 1)
        print(f"{m:<27}{any_ok:>16}/{len(by_task):<7}{allfail:>17}{distinct:>23.1f}")
        summary[m]["tasks_with_survivor"] = any_ok
        summary[m]["tasks_all_fail"] = allfail

    print("\n" + "=" * 104)
    print("RECALLED_TARGET slice ('harder' inferred for the repaired population — 31 Jul report)")
    for m in models:
        mr = [r for r in R if r["model"] == m]
        rt = [r for r in mr if r["task"] in RECALLED_TARGET]
        ot = [r for r in mr if r["task"] not in RECALLED_TARGET]
        def sv(g):
            return f"{sum(1 for x in g if x['all_pass'])}/{len(g)}" if g else "n/a"
        print(f"  {m:<27} recalled survivors {sv(rt):<12} other {sv(ot)}")

    print("\n" + "=" * 104)
    print("SUSPECT FACTS (FAILED by every admissible candidate of every model)")
    suspects = []
    facts = collections.defaultdict(collections.Counter)
    for rec in store.iter_verdicts():
        if not rec["admissible"]:
            continue
        for f in rec["fact_verdicts"]:
            facts[(rec["task_name"], f["fact_id"])][f["verdict"]] += 1
    for (t, fid), c in facts.items():
        if c["fail"] > 0 and c["pass"] == 0:
            suspects.append((t, fid, c["fail"]))
    for t, fid, n in sorted(suspects)[:15]:
        print(f"  {t:<38}{fid:<36}fail={n}")
    print(f"  total: {len(suspects)}")

    print("\n" + "=" * 104)
    print("TRAINABILITY")
    for m in models:
        print(f"  {m:<27} {TRAINABILITY.get(m, 'unknown')}")

    Path("scoring_output/evidence_pack.json").write_text(
        json.dumps({"summary": summary, "suspects": suspects, "n_records": len(R)},
                   indent=2, default=str), encoding="utf-8")
    print("\nwrote scoring_output/evidence_pack.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
