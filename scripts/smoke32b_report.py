"""The 32B base-model smoke readout: funnel, reach, character, decision inputs.

    uv run python scripts/smoke32b_report.py

Reads the fact-pass verdict tree plus the raw samples. Every fidelity figure is printed with its
RESOLUTION RATE beside it -- 1.0 from 9 of 29 facts and 1.0 from 29 of 29 print identically
otherwise, and with tier 3 disabled on this machine the resolved set is thinner than it would be
on the box, so the pairing is not optional here.
"""

import collections
import json
import statistics
import sys
from pathlib import Path

from prelim.extract import Extraction, extract_definition
from pretuning import buckets as B
from scoring.verdicts import Verdict, fidelity, resolution_rate

SAMPLES = Path("prelim_testing/output/smoke32b")
SCORES = Path("scoring_output/smoke32b_scores")

# The 26 tasks no 8B model ever solved, and the 15 the 8B union did reach. From the prelim
# evidence pack -- reach into the FIRST set is what the decision rule keys on.
NEVER_SOLVED_BY_8B = {
    "Equiv.ofLeftInverse", "Equiv.piCongrRight", "Equiv.piEquivPiSubtypeProd",
    "Equiv.subtypePreimage", "Finset.strongDownwardInduction", "Finset.strongInduction",
    "Finset.sumLexLift", "Function.Bijective", "Function.extend", "Int.leastOfBdd",
    "Int.greatestOfBdd", "List.prev", "Matroid.map", "Filter.comk", "memPartition",
    "Graph.banana", "Pi.Lex", "Multiset.Pi.cons", "SimpleGraph.replaceVertex",
    "Function.Embedding.setValue", "OrderHom.prevFixed", "Nat.binaryRec", "Nat.bitCasesOn",
    "Nat.evenOddRec", "Multiset.noncommFoldr", "Filter.Germ.IsConstant",
}

FUNNEL_KEYS = ["admitted", "compile_error", "sorry", "wrong_type", "name_shadowed",
               "self_delegation", "new_axiom", "errored", "other"]


def pct(a, b):
    return 100.0 * a / b if b else 0.0


def main() -> int:
    models = sorted(p.name for p in SCORES.iterdir() if p.is_dir())
    rows = {}

    for m in models:
        funnel = collections.Counter()
        buckets = collections.Counter()
        tasks_ok, noncomp, verbatim, nonverbatim = set(), 0, 0, 0
        fid_vals, res_vals = [], []
        n_scored = 0

        for path in (SCORES / m).rglob("sample_*.json"):
            rec = json.loads(path.read_text(encoding="utf-8"))
            n_scored += 1
            kind = "admitted" if rec.get("admissible") else (rec.get("admissibility_failure") or "other")
            funnel[kind] += 1
            if rec.get("noncomputable"):
                noncomp += 1
            if rec.get("admissible"):
                tasks_ok.add(rec["task_name"])
                if rec.get("equivalence_certified"):
                    verbatim += 1
                else:
                    nonverbatim += 1
                verdicts = [Verdict(v["verdict"]) for v in (rec.get("fact_verdicts") or [])
                            if v.get("verdict")]
                if verdicts:
                    f = fidelity(verdicts)
                    if f is not None:
                        fid_vals.append(f)
                    res_vals.append(resolution_rate(verdicts) or 0.0)

        n_samples = capped = 0
        toks = []
        for path in (SAMPLES / m).rglob("sample_*.json"):
            d = json.loads(path.read_text(encoding="utf-8"))
            n_samples += 1
            comp = d.get("completion") or ""
            if d.get("finish_reason") == "length":
                capped += 1
            if d.get("completion_tokens") is not None:
                toks.append(d["completion_tokens"])
            r = extract_definition(m, comp, finish_reason=d.get("finish_reason"))
            ok = isinstance(r, Extraction)
            buckets[B.classify(
                extracted=ok, declaration=r.code if ok else None,
                declared_name=r.declared_name if ok else None,
                expected_name="VTask." + d["task_name"].rsplit(".", 1)[-1],
                exemplar_symbols=frozenset(), finish_reason=d.get("finish_reason"),
                completion=comp)] += 1

        rows[m] = dict(
            n_samples=n_samples, n_scored=n_scored, funnel=funnel, buckets=buckets,
            tasks_ok=tasks_ok, noncomp=noncomp, verbatim=verbatim, nonverbatim=nonverbatim,
            capped=capped, med_tok=statistics.median(toks) if toks else 0,
            fid=statistics.mean(fid_vals) if fid_vals else None,
            res=statistics.mean(res_vals) if res_vals else None,
            n_with_facts=len(res_vals),
        )

    print("=" * 104)
    print("FUNNEL (per scored candidate; SELF_DELEGATION is new this run)")
    print("=" * 104)
    print(f"{'model':<26}{'scored':>8}" + "".join(f"{k[:13]:>15}" for k in FUNNEL_KEYS))
    for m, r in rows.items():
        print(f"{m:<26}{r['n_scored']:>8}" + "".join(f"{r['funnel'].get(k,0):>15}" for k in FUNNEL_KEYS))

    print("\n" + "=" * 104)
    print("HEADLINE (adm/100 over ALL samples, not just scored ones)")
    print("=" * 104)
    print(f"{'model':<26}{'samples':>9}{'adm/100':>9}{'non-verb':>10}{'verbatim':>10}"
          f"{'reach':>8}{'capped%':>9}{'noncomp':>9}{'med tok':>9}")
    for m, r in rows.items():
        print(f"{m:<26}{r['n_samples']:>9}{pct(r['funnel'].get('admitted',0), r['n_samples']):>9.1f}"
              f"{r['nonverbatim']:>10}{r['verbatim']:>10}{len(r['tasks_ok']):>7}/41"
              f"{pct(r['capped'], r['n_samples']):>8.1f}%{r['noncomp']:>9}{r['med_tok']:>9.0f}")

    print("\n" + "=" * 104)
    print("REACH: previously-solved vs NEWLY CRACKED from the 26 no 8B ever solved")
    print("=" * 104)
    for m, r in rows.items():
        new = sorted(r["tasks_ok"] & NEVER_SOLVED_BY_8B)
        old = sorted(r["tasks_ok"] - NEVER_SOLVED_BY_8B)
        print(f"\n{m}:  {len(r['tasks_ok'])}/41 total = {len(old)} previously-solved "
              f"+ {len(new)} NEWLY CRACKED")
        print(f"   newly cracked: {new}")

    print("\n" + "=" * 104)
    print("BUCKETS (pre-registered; statement_shape was pre-registered for StepFun)")
    print("=" * 104)
    print(f"{'model':<26}" + "".join(f"{b[:15]:>17}" for b in B.BUCKETS))
    for m, r in rows.items():
        print(f"{m:<26}" + "".join(f"{r['buckets'].get(b,0):>17}" for b in B.BUCKETS))

    print("\n" + "=" * 104)
    print("FIDELITY -- INDICATIVE ONLY, tier 3 disabled (no Hammer on this machine, needs Linux)")
    print("=" * 104)
    print(f"{'model':<26}{'candidates w/ facts':>21}{'mean fidelity':>15}{'mean RESOLUTION':>18}")
    for m, r in rows.items():
        f = f"{r['fid']:.3f}" if r["fid"] is not None else "n/a"
        s = f"{r['res']:.3f}" if r["res"] is not None else "n/a"
        print(f"{m:<26}{r['n_with_facts']:>21}{f:>15}{s:>18}")
    print("\n  Resolution is the share of facts that returned PASS or FAIL. Fidelity divides by")
    print("  that set, so a high fidelity over a low resolution is a thin result, not a strong one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
