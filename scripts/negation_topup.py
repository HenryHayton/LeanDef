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
from harness.signature import root_qualify
from ladder.axiom_audit import audit_proof_axioms
from ladder.budgets import DEFAULT_LADDER_BUDGETS, TacticBudget
from ladder.tier2 import adjudicate_tier2
from ladder.tier3 import adjudicate_tier3_hammer
from scoring import config as cfg
from scoring import store
from scoring.samples import load_task
from scoring.verdicts import Verdict, fidelity, resolution_rate

# The forward 60s hammer budget is for goals we hope are provable. This pass's goals are harder to
# call: it runs on facts the forward ladder left UNKNOWN, so each negation is either true (the
# candidate is wrong) or unprovable (the fact is true but hard), and there is no way to tell which
# without spending the budget. They get 20s, not 60.
NEGATION_TIER3_WALL_CLOCK_S = 20.0

# --- staged tactic sets ---------------------------------------------------------------------------
#
# The stages are DISJOINT, and run in separate passes at different points in the ladder, because
# their costs differ by an order of magnitude and the population shrinks between them.
#
#   cheap   decide + simp_all + omega.  35s/fact worst case, and typically far less: these fail
#           fast or not at all. Runs immediately after the forward tiers 1-4 pass, over everything
#           still unknown.
#   search  the two aesop searches.  60s/fact, genuine proof search. DEFERRED until after tier-5
#           forward has resolved what it can, so it runs over a much smaller population that is
#           enriched for facts which are actually false.
#   hammer  tier-3.  Runs with `search`.
#
# Splitting them this way is what makes the ordering work: 1663 facts x 60s of aesop is ~28 hours,
# the same 60s over whatever survives tier-5 forward is affordable. Running the cheap set first
# costs almost nothing and can only shrink what the expensive sets have to look at.
STAGE_CHEAP = "cheap"
STAGE_SEARCH = "search"
STAGES = (STAGE_CHEAP, STAGE_SEARCH)


def negation_tactics(task_symbol: str, stage: str) -> tuple:
    """The tactic set for one stage. Disjoint across stages -- `search` does NOT re-run `cheap`."""
    if stage == STAGE_CHEAP:
        return (
            TacticBudget("push_neg <;> simp_all", 15.0),
            TacticBudget("push_neg <;> omega", 10.0),
            TacticBudget("decide", 10.0),
        )
    return (
        TacticBudget("push_neg <;> aesop", 30.0, heavy=True),
        TacticBudget(f"simp only [{task_symbol}] <;> push_neg <;> aesop", 30.0, heavy=True),
    )


def stages_done(record: dict) -> set:
    """Which negation stages have already run against this candidate.

    `negation_topup: True` is the LEGACY marker, written before the pass was split into stages by
    a run that used the full tactic set plus hammer. Those candidates have had strictly more work
    done than either stage would do, so they count as done for both -- otherwise the 12 candidates
    from that run would be needlessly re-searched.
    """
    done = set(record.get("negation_stages") or [])
    if record.get("negation_topup"):
        done |= set(STAGES)
    return done


def negation_goal(statement: str) -> str:
    """`¬ (statement)`, parenthesised so binders in the statement cannot capture the negation.

    Statements are full Props (usually `∀`-led); `¬ (∀ x, P x)` is well-formed and `push_neg`
    rewrites it to the witness form. Inner newlines are preserved -- Lean is whitespace-tolerant
    inside parentheses.
    """
    return f"¬ ({statement.strip()})"


def negation_budgets(task_symbol: str, stage: str = STAGE_SEARCH):
    return dataclasses.replace(
        DEFAULT_LADDER_BUDGETS,
        tier2_tactics=negation_tactics(task_symbol, stage),
        tier3_wall_clock_s=NEGATION_TIER3_WALL_CLOCK_S,
    )


def refute_one(server, env, fact_id, statement, task_symbol, imports, *, hammer: bool,
               stage: str = STAGE_SEARCH):
    """`(refuted, tier, script, detail)` for one fact. UNKNOWN on anything short of a clean,
    audited kernel certification of the negation."""
    goal = negation_goal(statement)
    budgets = negation_budgets(task_symbol, stage)

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


def refutes_truth_too(server, base_env, statement, real_name, task_symbol, imports,
                      *, stage: str = STAGE_SEARCH) -> bool:
    """Does the same negation prove against the TRUTH? Then the FACT is defective, not the
    candidate. Found live on the pass's first-ever refutation (Nat.log/log_lt_of_lt_pow,
    2026-08-09): the mined fact lacked Mathlib's n ≠ 0 hypothesis, was false of Nat.log itself,
    and the sole 'candidate FAIL' was really a truth-side defect. A refutation only counts
    against a candidate if the truth SURVIVES the same attack."""
    truth_stmt = statement.replace(task_symbol, root_qualify(real_name))
    goal = negation_goal(truth_stmt)
    # The SAME attack that beat the candidate, not a stronger or weaker one: the question is
    # whether this particular refutation also kills the truth, so the tactic set has to match.
    budgets = negation_budgets(root_qualify(real_name), stage)
    t2 = adjudicate_tier2(server, base_env, "neg_truth_probe", goal, budgets, imports=imports)
    return t2.winning is not None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--no-hammer", action="store_true")
    ap.add_argument("--stage", choices=STAGES, default=STAGE_SEARCH,
                    help="which tactic set to run; stages are disjoint and tracked separately, so "
                         "`cheap` now and `search` later does not redo work")
    args = ap.parse_args()
    scores_dir = cfg.scores_dir()

    todo = []
    for record in store.iter_verdicts(scores_dir=scores_dir):
        if not record.get("admissible") or not record.get("extracted_code"):
            continue
        if args.stage in stages_done(record):
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
    suspect_facts = collections.Counter()
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
                    hammer=not args.no_hammer, stage=args.stage)
                if "axiom audit" in detail:
                    audited_out += 1
                    by_id[fid]["detail"] = detail
                    changed = True
                if not ok:
                    # Record WHICH negation stage failed, not a single flat marker: "unknown after
                    # decide/simp_all/omega" and "unknown after aesop search" are different claims,
                    # and a later stage must be able to tell them apart.
                    marker = f"neg_{args.stage}" + ("" if args.no_hammer else "_hammer")
                    stages = by_id[fid].setdefault("unknown_after", [])
                    if marker not in stages:
                        stages.append(marker)
                    changed = True
                if ok and t.get("truth_real_name") and refutes_truth_too(
                        server, env, stmt, t["truth_real_name"], t["signature"].name, imports,
                        stage=args.stage):
                    by_id[fid]["detail"] = ("refutation also proves against the truth -- "
                                            "suspect FACT, not a candidate FAIL")
                    by_id[fid].setdefault("unknown_after", []).append("neg_suspect_fact")
                    suspect_facts[f"{task}/{fid}"] += 1
                    changed = True
                    ok = False
                if ok:
                    refuted += 1
                    refuted_by_fact[f"{task}/{fid}"] += 1
                    by_id[fid].update(verdict=Verdict.FAIL.value, tier=tier, script=script,
                                      detail=detail, certified_via="negation")
                    changed = True
            record["negation_stages"] = sorted(stages_done(record) | {args.stage})
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
        "suspect_facts": dict(suspect_facts),
    }, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
