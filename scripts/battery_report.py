"""Render the battery readout: funnel, buckets, substitution, decode observations, winners.

    uv run python scripts/battery_report.py --funnel scoring_output/battery_funnel.json

Reads what `scripts/score_cells.py` wrote and prints the tables the run brief asks for. The
winner selection at the end applies the PRE-STATED rules from `docs/preregistration_battery.md`
mechanically rather than by eye:

  T battery -- admissible/100 and non-verbatim admissible, buckets as mechanism
  A battery -- substitution rate FIRST (a fix that does not kill contamination fails regardless),
               then adm/100, then reach

The T rule's "beats T0 by more than ~2-3 points on adm/100" threshold decides whether the winner
goes into the frozen protocol at all, which is a separate question from which T cell is best; both
are reported.
"""

import argparse
import json
import sys
from pathlib import Path

from pretuning import buckets as B

FUNNEL_KEYS = ["admitted", "sorry", "compile_error", "wrong_type", "exemplar_copy",
               "name_shadowed", "new_axiom", "other"]
T_CELLS = ["T0", "T1", "T2", "T3"]
A_CELLS = ["A1", "A2", "A3"]
FREEZE_THRESHOLD = 2.0   # pre-stated: "more than ~2-3 points on adm/100"


def pct(num, den):
    return 100.0 * num / den if den else 0.0


def rule(title):
    print(f"\n{'=' * 100}\n{title}\n{'=' * 100}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--funnel", default="scoring_output/battery_funnel.json")
    ap.add_argument("--baseline", default="scoring_output/pretuning_funnel.json",
                    help="the eight-cell run, for the SA_R0 cross-run comparison")
    args = ap.parse_args()

    d = json.loads(Path(args.funnel).read_text())
    cells = [c for c in T_CELLS + A_CELLS + ["C1"] if c in d]

    rule("FUNNEL (sample-weighted; every cell is 41 tasks x 10 samples)")
    print(f"{'cell':<6}{'n':>5}{'unext':>7}" + "".join(f"{k[:11]:>13}" for k in FUNNEL_KEYS))
    for c in cells:
        f = d[c]["funnel"]
        print(f"{c:<6}{d[c]['n']:>5}{d[c]['unextractable']:>7}"
              + "".join(f"{f.get(k, 0):>13}" for k in FUNNEL_KEYS))

    rule("HEADLINE METRICS")
    print(f"{'cell':<6}{'adm/100':>9}{'adm|nonsorry':>14}{'non-verbatim':>14}{'verbatim':>10}"
          f"{'tasks':>7}{'med tok':>9}{'think%':>8}")
    for c in cells:
        r = d[c]
        med = r["completion_tokens"]["median"]
        print(f"{c:<6}{r['adm_per_100']:>9.1f}{r['adm_given_nonsorry']:>14.1f}"
              f"{r['adm_nonverbatim']:>14}{r['adm_verbatim']:>10}"
              f"{len(r['tasks_with_admissible']):>7}{(med if med else 0):>9.0f}"
              f"{pct(r['think_block_present'], r['n']):>8.1f}")

    rule("ESCAPE-ROUTE BUCKETS (named in code before any T1/T3 sample existed)")
    print(f"{'cell':<6}" + "".join(f"{b[:15]:>17}" for b in B.BUCKETS))
    for c in cells:
        b = d[c]["buckets"]
        print(f"{c:<6}" + "".join(f"{b.get(k, 0):>17}" for k in B.BUCKETS))
    print(f"\n{'cell':<6}" + "".join(f"{b[:15]:>17}" for b in B.BUCKETS) + "   (as % of samples)")
    for c in cells:
        b, n = d[c]["buckets"], d[c]["n"]
        print(f"{c:<6}" + "".join(f"{pct(b.get(k, 0), n):>16.1f}%" for k in B.BUCKETS))

    rule("BUCKET x ADMISSIBILITY -- does an escape route ever produce a real answer?")
    for c in cells:
        by = d[c]["bucket_by_outcome"]
        rows = {}
        for key, v in by.items():
            bucket, outcome = key.rsplit("|", 1)
            rows.setdefault(bucket, {})[outcome] = v
        print(f"\n  {c}")
        for bucket in B.BUCKETS:
            r = rows.get(bucket)
            if not r:
                continue
            tot = sum(r.values())
            adm = r.get("admitted", 0)
            top = sorted(r.items(), key=lambda kv: -kv[1])[:3]
            print(f"    {bucket:<26}n={tot:<5} admitted={adm:<5}({pct(adm, tot):>5.1f}%)  "
                  + "  ".join(f"{k}={v}" for k, v in top))

    rule("EXEMPLAR SUBSTITUTION (the A battery's first-order metric)")
    print(f"{'cell':<6}{'exemplars':>11}{'total':>8}{'identical':>11}{'re-derived':>12}{'% of samples':>14}")
    for c in cells:
        s = d[c]["substitution"]
        n_ex = {"A1": 0, "A3": 1}.get(c, 3)
        print(f"{c:<6}{n_ex:>11}{s['total']:>8}{s['identical']:>11}{s['rederived']:>12}"
              f"{pct(s['total'], d[c]['n']):>13.1f}%")

    rule("DECODE OBSERVATIONS")
    print(f"{'cell':<6}{'prefilled':>11}{'think present':>15}{'ban leak (defn)':>17}"
          f"{'ban leak (prose)':>18}{'med tok':>9}")
    for c in cells:
        r = d[c]
        med = r["completion_tokens"]["median"]
        print(f"{c:<6}{r['prefilled_samples']:>11}{r['think_block_present']:>15}"
              f"{r.get('banned_in_definition', 0):>17}{r.get('banned_in_prose_only', 0):>18}"
              f"{(med if med else 0):>9.0f}")

    base = Path(args.baseline)
    if base.exists():
        b = json.loads(base.read_text()).get("SA_R0")
        if b and "T0" in d:
            rule("CROSS-RUN DRIFT CHECK (T0 vs the eight-cell run's SA_R0)")
            b_adm = pct(b["funnel"].get("admitted", 0), b["n"])
            print(f"  SA_R0 (last week) adm/100 = {b_adm:.1f}   tasks = {len(b['tasks_with_admissible'])}")
            print(f"  T0    (this run)  adm/100 = {d['T0']['adm_per_100']:.1f}   "
                  f"tasks = {len(d['T0']['tasks_with_admissible'])}")
            print(f"  drift = {d['T0']['adm_per_100'] - b_adm:+.1f} points")

    rule("WINNERS, by the pre-stated rules")
    ts = [c for c in T_CELLS if c in d]
    if ts:
        best_t = max(ts, key=lambda c: (d[c]["adm_per_100"], d[c]["adm_nonverbatim"]))
        margin = d[best_t]["adm_per_100"] - d["T0"]["adm_per_100"] if "T0" in d else float("nan")
        print(f"  T winner: {best_t}  adm/100={d[best_t]['adm_per_100']:.1f}  "
              f"non-verbatim={d[best_t]['adm_nonverbatim']}  margin over T0 = {margin:+.1f} pts")
        print(f"  -> {'clears' if margin > FREEZE_THRESHOLD else 'does NOT clear'} the pre-stated "
              f"~{FREEZE_THRESHOLD:.0f}-3 point bar for entering the frozen protocol")
    a_s = [c for c in A_CELLS if c in d]
    if a_s:
        # Substitution rate first, per the pre-stated rule; adm/100 only breaks ties.
        best_a = min(a_s, key=lambda c: (pct(d[c]["substitution"]["total"], d[c]["n"]),
                                         -d[c]["adm_per_100"]))
        print(f"  A winner: {best_a}  substitution="
              f"{pct(d[best_a]['substitution']['total'], d[best_a]['n']):.1f}%  "
              f"adm/100={d[best_a]['adm_per_100']:.1f}  "
              f"reach={len(d[best_a]['tasks_with_admissible'])}")
    if "C1" in d:
        rule("C1 COMPOSITION CHECK")
        print(f"  C1 adm/100={d['C1']['adm_per_100']:.1f}  "
              f"substitution={pct(d['C1']['substitution']['total'], d['C1']['n']):.1f}%  "
              f"non-verbatim={d['C1']['adm_nonverbatim']}  "
              f"reach={len(d['C1']['tasks_with_admissible'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
