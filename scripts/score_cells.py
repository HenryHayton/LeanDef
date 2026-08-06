"""Admissibility + mechanism readout for a tree of prompt/decode cells.

Promoted from the ad-hoc pass that produced `scoring_output/pretuning_funnel.json`, because the
battery needs the same readout eight more times and a scratchpad script run eight times is eight
chances to run a slightly different one.

    uv run python scripts/score_cells.py --root prelim_testing/output/decode_exemplar \
        --out scoring_output/battery_funnel.json

**No facts.** The questions here are "did it produce a real definition" and, conditional on not
punting, "is the attempt any good" -- both answered by the admissibility gate alone. Fidelity is
saturated among admissible candidates (96.8-98.9% across three models) and would add hours for a
column that does not discriminate.

**Equivalence is run only on admissible candidates.** It is what separates a definition the kernel
proves equal to the real Mathlib object from one that merely type-checks, and the T battery is
judged partly on non-verbatim admissible for exactly that reason -- an intervention that raises
admissibility by producing more memorised recitations has not improved anything. An inadmissible
candidate cannot be verbatim, so the expensive probe is skipped for ~80% of the corpus.

**Dedup is per (task, normalised body).** Ten samples of the same task frequently produce the same
declaration; scoring it once and weighting by multiplicity is what makes a full cell affordable.
Every reported count is sample-weighted, so the dedup is invisible in the numbers.
"""

import argparse
import collections
import json
import re
import statistics
import sys
from pathlib import Path

from prelim.extract import Extraction, extract_definition
from pretuning import buckets as B
from pretuning.prompts import load_exemplars
from scoring.candidate import score_candidate_body
from scoring.runner import ServerHandle
from scoring.samples import load_task

MODEL_SLUG = "goedel-formalizer-v2-8b"   # extraction is model-independent; this names the caller


def norm(s: str | None) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def pct(num: int, den: int) -> float:
    return 100.0 * num / den if den else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="samples tree: <root>/<cell>/<task>/sample_NN.json")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cells", nargs="*", default=None)
    ap.add_argument("--no-equivalence", action="store_true",
                    help="skip the verbatim probe (faster; drops the non-verbatim column)")
    args = ap.parse_args()

    root = Path(args.root)
    exemplars = load_exemplars()
    exemplar_symbols = frozenset(e["task_symbol"] for e in exemplars)
    exemplar_bodies = {e["task_symbol"]: norm(e["definition"]) for e in exemplars}

    cell_names = args.cells or sorted(p.name for p in root.iterdir() if p.is_dir())
    handle = ServerHandle()
    out: dict[str, dict] = {}

    try:
        for cell in cell_names:
            per_task: dict[str, dict[str, tuple]] = collections.defaultdict(dict)
            weight: collections.Counter = collections.Counter()
            bucket_w: collections.Counter = collections.Counter()
            bucket_adm: collections.Counter = collections.Counter()
            n = unext = leaks = think = prefilled = 0
            subst_identical = subst_rederived = 0
            comp_tokens: list[int] = []

            for path in sorted((root / cell).rglob("sample_*.json")):
                d = json.loads(path.read_text(encoding="utf-8"))
                n += 1
                task = d["task_name"]
                completion = d.get("completion") or ""
                extra = d.get("extra") or {}
                expected = "VTask." + task.rsplit(".", 1)[-1]
                if d.get("completion_tokens") is not None:
                    comp_tokens.append(int(d["completion_tokens"]))
                if "<think>" in completion:
                    think += 1
                if extra.get("prefill_applied"):
                    prefilled += 1
                if extra.get("ban_applied") and B.contains_banned_token(completion):
                    leaks += 1

                r = extract_definition(MODEL_SLUG, completion, finish_reason=d.get("finish_reason"))
                got = isinstance(r, Extraction)
                bucket = B.classify(
                    extracted=got,
                    declaration=r.code if got else None,
                    declared_name=r.declared_name if got else None,
                    expected_name=expected,
                    exemplar_symbols=exemplar_symbols,
                    finish_reason=d.get("finish_reason"),
                )
                bucket_w[bucket] += 1

                if not got:
                    unext += 1
                    continue

                h = norm(r.code)
                if bucket == B.EXEMPLAR_SUBSTITUTION:
                    # Byte-identical vs re-derived is the diagnostic split: a re-derived variant
                    # means the model reconstructed the exemplar's object from scratch, i.e. it
                    # had taken the exemplar to BE the question, not merely copied a nearby string.
                    if h == exemplar_bodies.get(r.declared_name):
                        subst_identical += 1
                    else:
                        subst_rederived += 1

                body = B.body_of(r.code)
                is_sorry = norm(body) in ("sorry", "by sorry", "admit", "by admit")
                per_task[task][h] = (r.code, is_sorry, bucket == B.EXEMPLAR_SUBSTITUTION, bucket)
                weight[(task, h)] += 1

            res: collections.Counter = collections.Counter()
            res_ns: collections.Counter = collections.Counter()
            tasks_ok: set[str] = set()
            adm_verbatim = adm_nonverbatim = 0

            for task, bodies in per_task.items():
                t = load_task(task)
                for h, (code, is_sorry, is_copy, bucket) in bodies.items():
                    w = weight[(task, h)]
                    if is_sorry:
                        res["sorry"] += w
                        bucket_adm[(bucket, "sorry")] += w
                        continue
                    if is_copy:
                        # An exemplar answer is never an answer to THIS task, whatever the kernel
                        # would say about it in its own right. Splicing it under this task's
                        # pinned signature would just measure a type mismatch.
                        res["exemplar_copy"] += w
                        res_ns["exemplar_copy"] += w
                        bucket_adm[(bucket, "exemplar_copy")] += w
                        continue
                    server, env = handle.get()
                    rec = score_candidate_body(server, env, t["signature"], code, [],
                                               try_equivalence=False)
                    kind = "admitted" if rec["admissible"] else (rec["admissibility_failure"] or "other")
                    res[kind] += w
                    res_ns[kind] += w
                    bucket_adm[(bucket, kind)] += w
                    if not rec["admissible"]:
                        continue
                    tasks_ok.add(task)
                    if args.no_equivalence or not t.get("truth_real_name"):
                        continue
                    server, env = handle.get()
                    eq = score_candidate_body(server, env, t["signature"], code, [],
                                              truth_real_name=t["truth_real_name"],
                                              try_equivalence=True)
                    if eq.get("equivalence_certified"):
                        adm_verbatim += w
                    else:
                        adm_nonverbatim += w

            adm = res.get("admitted", 0)
            ns = sum(res_ns.values())
            out[cell] = {
                "n": n,
                "unextractable": unext,
                "funnel": dict(res),
                "nonsorry_funnel": dict(res_ns),
                "tasks_with_admissible": sorted(tasks_ok),
                "buckets": dict(bucket_w),
                "bucket_by_outcome": {f"{b}|{k}": v for (b, k), v in bucket_adm.items()},
                "substitution": {"identical": subst_identical, "rederived": subst_rederived,
                                 "total": subst_identical + subst_rederived},
                "banned_token_leaks": leaks,
                "think_block_present": think,
                "prefilled_samples": prefilled,
                "completion_tokens": {
                    "n": len(comp_tokens),
                    "median": statistics.median(comp_tokens) if comp_tokens else None,
                    "p10": (statistics.quantiles(comp_tokens, n=10)[0] if len(comp_tokens) > 10 else None),
                    "p90": (statistics.quantiles(comp_tokens, n=10)[8] if len(comp_tokens) > 10 else None),
                },
                "adm_per_100": round(pct(adm, n), 1),
                "adm_given_nonsorry": round(pct(adm, ns), 1),
                "adm_verbatim": adm_verbatim,
                "adm_nonverbatim": adm_nonverbatim,
            }
            print(f"{cell:<6} adm/100={out[cell]['adm_per_100']:>5.1f}  "
                  f"adm|nonsorry={out[cell]['adm_given_nonsorry']:>5.1f}%  "
                  f"nonverbatim={adm_nonverbatim:>4}  subst={out[cell]['substitution']['total']:>4}  "
                  f"leaks={leaks:>3}  tasks={len(tasks_ok):>2}", flush=True)
    finally:
        handle.close()

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nwrote {args.out}  (recycles={handle.recycles}, env_probe_fires={handle.env_probe_fires})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
