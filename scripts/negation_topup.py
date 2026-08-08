"""Refutation pass: try to PROVE THE NEGATION of every fact the ladder left UNKNOWN.

    # on the box (queue behind the tier-3 top-up; same env):
    export PATH="$HOME/.elan/bin:$PATH"
    VERIFIER_LEAN_PROJECT_DIR=$HOME/verifier-lean \
    LEAN_INTERACT_LOAD_DYNLIB=$HOME/verifier-lean/.lake/packages/cvc5/.lake/build/lib/libcvc5_cvc5.so \
    SCORING_EXTRA_IMPORTS=Hammer \
    SCORING_SCORES_DIR=scoring_output/smoke32b_scores \
    .venv/bin/python scripts/negation_topup.py

**What this adds to the verdict vocabulary, and why it is principled.** Proof facts have never
been able to return FAIL: a tactic failing to prove is not evidence against the candidate, and
that invariant stands. This pass reaches FAIL by the only other road with the same epistemic
standing as a PASS -- the KERNEL certifying `¬ (fact)` against the candidate's spliced
environment. An UNKNOWN today conflates "automation too weak" with "false of this candidate";
a landed refutation splits them, and enters fidelity's denominator where it belongs. This is the
candidate-side half of the reward doc's "two-sided" suite, manufactured from the facts we
already have rather than waiting on authored mutants.

The asymmetry is preserved deliberately: failing to refute proves nothing and the verdict stays
UNKNOWN. Most attempts are EXPECTED to lose -- most facts are true of most admissible
candidates -- which is why the negation tier-3 budget is 20s rather than the forward 60s.

`push_neg` leads every tactic: `¬ ∀ x, P x` becomes `∃ x, ¬ P x`, and witness search is the
shape automation is genuinely good at when the fact really is false. The task symbol is unfolded
(`simp only [VTask.X]`) in the deeper variants, since a refutation usually has to see through
the candidate's own definition.

Every FAIL carries the refutation script AND an axiom audit of the refuting theorem -- a
refutation smuggled through a nonstandard axiom must not stand. A refutation that fails its
audit is recorded as UNKNOWN with the incident in `detail`, not as a FAIL.

A fact refuted against EVERY admissible candidate -- including near-verbatim ones -- indicts the
fact, not the candidates. The per-fact refutation tally printed at the end feeds exactly the
existing suspect-fact reading; eyeball it before believing any individual FAIL.
"""

import argparse
import collections
import dataclasses
import json
import sys
import time
from pathlib import Path

from harness.admissibility import STANDARD_MATHLIB_AXIOMS
from harness.results import CheckStatus
from harness.scoring import splice_candidate_declaration
from ladder.axiom_audit import audit_proof_axioms
from ladder.budgets import DEFAULT_LADDER_BUDGETS, TacticBudget
from ladder.tier2 import adjudicate_tier2
from ladder.tier3 import adjudicate_tier3_hammer
from scoring import config as cfg
from scoring import store
from scoring.samples import load_task
from scoring.verdicts import Verdict, fidelity, resolution_rate

# The forward 60s hammer budget is for goals we hope are provable. Negations of TRUE facts are
# unprovable by construction, and most facts are true of most admissible candidates, so most of
# this pass's hammer calls are destined to fail -- they get 20s, not 60.
NEGATION_TIER3_WALL_CLOCK_S = 20.0


def negation_goal(statement: str) -> str:
    """`¬ (statement)`, parenthesised so binders in the statement cannot capture the negation.

    Statements are full Props (usually `∀`-led); `¬ (∀ x, P x)` is well-formed and `push_neg`
    rewrites it to the witness form. Inner newlines are preserved -- Lean is whitespace-tolerant
    inside parentheses.
    """
    return f"¬ ({statement.strip()})"


def negation_budgets(task_symbol: str):
    tactics = (
        TacticBudget("push_neg <;> simp_all", 15.0),
        TacticBudget("push_neg <;> omega", 10.0),
        TacticBudget("decide", 10.0),
        TacticBudget("push_neg <;> aesop", 30.0, heavy=True),
        TacticBudget(f"simp only [{task_symbol}] <;> push_neg <;> aesop", 30.0, heavy=True),
    )
    return dataclasses.replace(
        DEFAULT_LADDER_BUDGETS,
        tier2_tactics=tactics,
        tier3_wall_clock_s=NEGATION_TIER3_WALL_CLOCK_S,
    )


def refute_one(server, env, fact_id, statement, task_symbol, imports, *, hammer: bool):
    """`(refuted, tier, script, detail)` for one fact. UNKNOWN on anything short of a clean,
    audited kernel certification of the negation."""
    goal = negation_goal(statement)
    budgets = negation_budgets(task_symbol)

    t2 = adjudicate_tier2(server, env, f"neg_{fact_id}", goal, budgets, imports=imports)
    winning, name, script, tier, out_env = t2.winning, t2.winning_theorem_name, t2.winning_script, 2, t2.env
    if winning is None and hammer and budgets.tier3_enabled:
        t3 = adjudicate_tier3_hammer(server, out_env, f"neg_{fact_id}", goal, [], budgets, imports=imports)
        winning, name, script, tier, out_env = t3.winning, t3.winning_theorem_name, t3.winning_script, 3, t3.env
    if winning is None:
        return False, None, None, "", out_env

    audit = audit_proof_axioms(server, out_env, name, permitted=STANDARD_MATHLIB_AXIOMS)
    if not audit.passed:
        return (False, None, None,
                f"negation proved but FAILED the axiom audit ({audit.detail[:160]}) -- not a FAIL",
                out_env)
    return True, tier, script, f"refuted: negation proved at tier {tier}", out_env


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--no-hammer", action="store_true")
    args = ap.parse_args()
    scores_dir = cfg.scores_dir()

    todo = []
    for record in store.iter_verdicts(scores_dir=scores_dir):
        if not record.get("admissible") or not record.get("extracted_code"):
            continue
        if record.get("negation_topup"):
            continue
        unresolved = [fv["fact_id"] for fv in (record.get("fact_verdicts") or [])
                      if fv.get("verdict") == Verdict.UNKNOWN.value]
        if unresolved:
            todo.append((record, unresolved))
    if args.limit:
        todo = todo[: args.limit]

    n_facts = sum(len(u) for _, u in todo)
    print(f"{len(todo)} candidates, {n_facts} unknown facts to attempt refuting  "
          f"{dict(collections.Counter(r['model_slug'] for r, _ in todo))}", flush=True)

    from scoring.runner import ServerHandle
    handle = ServerHandle()
    refuted_by_fact = collections.Counter()
    done = refuted = audited_out = 0
    t0 = time.perf_counter()
    try:
        for record, unresolved in todo:
            model, task, idx = record["model_slug"], record["task_name"], record["sample_index"]
            t = load_task(task)
            statements = {f.id: f.statement for f in t["facts"] if f.id in set(unresolved)}
            server, env = handle.get()
            outcome = splice_candidate_declaration(server, env, t["signature"], record["extracted_code"])
            if outcome.result.status is not CheckStatus.PASSED:
                continue
            cand_env = outcome.result.env
            imports = cfg.imports_for(t.get("imports"))
            by_id = {fv["fact_id"]: fv for fv in record["fact_verdicts"]}
            changed = False
            for fid, stmt in statements.items():
                ok, tier, script, detail, cand_env = refute_one(
                    server, cand_env, fid, stmt, t["signature"].name, imports,
                    hammer=not args.no_hammer)
                if "axiom audit" in detail:
                    audited_out += 1
                    by_id[fid]["detail"] = detail
                    changed = True
                if not ok:
                    stages = by_id[fid].setdefault("unknown_after", [])
                    if "neg_tier3" not in stages:
                        stages.append("neg_tier3")
                    changed = True
                if ok:
                    refuted += 1
                    refuted_by_fact[f"{task}/{fid}"] += 1
                    by_id[fid].update(verdict=Verdict.FAIL.value, tier=tier, script=script,
                                      detail=detail, certified_via="negation")
                    changed = True
            record["negation_topup"] = True
            if changed:
                verdicts = [Verdict(fv["verdict"]) for fv in record["fact_verdicts"]]
                record["fidelity"] = fidelity(verdicts)
                record["resolution_rate"] = resolution_rate(verdicts)
            store.write_verdict(record, scores_dir=scores_dir)
            done += 1
            if done % 10 == 0:
                rate = done / max(time.perf_counter() - t0, 1e-6)
                print(f"{done}/{len(todo)}  refuted={refuted}/{n_facts}  "
                      f"eta {((len(todo)-done)/rate)/60:.0f} min", flush=True)
    finally:
        handle.close()

    print(f"\nDONE {done} candidates: {refuted}/{n_facts} facts REFUTED "
          f"(kernel-certified false of their candidate), {audited_out} refutations rejected by "
          f"the axiom audit, {(time.perf_counter()-t0)/60:.1f} min")
    if refuted_by_fact:
        print("\nrefutations by fact (a fact refuted against MANY candidates indicts the fact):")
        for k, v in refuted_by_fact.most_common(15):
            print(f"  {v:>3}x  {k}")
    Path("scoring_output/negation_topup_summary.json").write_text(json.dumps({
        "candidates": done, "facts_attempted": n_facts, "facts_refuted": refuted,
        "audit_rejected": audited_out, "refuted_by_fact": dict(refuted_by_fact),
    }, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
