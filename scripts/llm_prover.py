"""Tier 5 -- the capped LLM prover, in both directions. Two phases, two machines.

    # Phase 1, LAPTOP (needs Bedrock credentials, not Lean):
    uv run python scripts/llm_prover.py generate --direction forward
    uv run python scripts/llm_prover.py generate --direction negation

    # Phase 2, BOX (needs Lean+Hammer env, not Bedrock):
    SCORING_SCORES_DIR=scoring_output/smoke32b_scores \
    .venv/bin/python scripts/llm_prover.py check --direction forward

This is the ladder tier the design of record specified and left as a stub ("capped LLM prover"),
extended with the operator's negation cascade (2026-08-07): forward proof attempt first; a fact
still unknown then gets its NEGATION attempted; UNKNOWN is only FINAL once every stage has run.
Each stage a fact survives is appended to its verdict's `unknown_after` list, so a provisional
UNKNOWN and an exhausted one are distinguishable at a glance.

**The soundness rule.** The LLM never decides anything. It proposes a tactic script; the script
is kernel-checked in the candidate's spliced environment and axiom-audited exactly like a tier-2
or tier-3 win. `sorry` inside a generated proof surfaces as `sorryAx` in the axiom closure and is
rejected. PASS and FAIL only ever come from the kernel; Sonnet is a search heuristic on a token
budget.

**Why two phases.** Generation is network-bound (Bedrock, thinking on, ~1-5 min/call) and
parallelises to whatever the quota allows; checking is Lean-bound and lives where the Hammer
project lives. Neither machine has the other's credentials, and the JSONL between them is
resumable -- the run that hits the daily token wall (as the dossier probe did) checkpoints and
continues after the reset instead of losing its spend.
"""

import argparse
import collections
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from scoring import config as cfg
from scoring import store
from scoring.verdicts import Verdict, fidelity, resolution_rate

STAGE = {"forward": "llm_forward", "negation": "llm_negation"}
STAMP = {"forward": "llm_forward_topup", "negation": "llm_negation_topup"}

SYSTEM = (
    "You are an expert Lean 4 / Mathlib 4 prover. You produce a single tactic proof for the "
    "goal you are given, in the environment described. Reply with ONLY a fenced ```lean block "
    "containing a tactic script beginning with `by`. No prose. Never use `sorry` or `admit`."
)


def negation_goal(statement: str) -> str:
    return f"¬ ({statement.strip()})"


def build_prompt(record: dict, statement: str, direction: str) -> str:
    goal = statement if direction == "forward" else negation_goal(statement)
    intro = ("Prove the following fact about the definition below."
             if direction == "forward" else
             "The fact below may be FALSE of this particular definition. Prove its NEGATION -- "
             "typically: `push_neg`, then exhibit a concrete counterexample witness.")
    return (
        f"{intro}\n\n"
        f"The definition (already elaborated in the environment, with Mathlib imported):\n\n"
        f"```lean\n{record['extracted_code']}\n```\n\n"
        f"The goal to prove:\n\n```lean\n{goal}\n```\n\n"
        f"Reply with only the tactic proof for this exact goal, as a fenced lean block "
        f"starting with `by`."
    )


def extract_script(text: str) -> str | None:
    """The tactic script from the reply: last fenced block, must start with `by`."""
    blocks = re.findall(r"```(?:lean4?|)\s*\n(.*?)```", text or "", re.DOTALL | re.IGNORECASE)
    for block in reversed(blocks or [text or ""]):
        script = block.strip()
        if script.startswith("by"):
            return script
    return None


def unresolved_facts(scores_dir):
    """(record, [fact_id...]) for admissible records with UNKNOWN facts."""
    for record in store.iter_verdicts(scores_dir=scores_dir):
        if not record.get("admissible") or not record.get("extracted_code"):
            continue
        unknown = [fv["fact_id"] for fv in (record.get("fact_verdicts") or [])
                   if fv.get("verdict") == Verdict.UNKNOWN.value]
        if unknown:
            yield record, unknown


def key_of(record, fact_id, direction):
    return f"{record['model_slug']}|{record['task_name']}|{record['sample_index']}|{fact_id}|{direction}"


def cmd_generate(args) -> int:
    from bedrock import config as bcfg
    from bedrock.client import BedrockClient

    scores_dir = cfg.scores_dir()
    out_path = Path(args.scripts)
    done_keys = set()
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            try:
                done_keys.add(json.loads(line)["key"])
            except (json.JSONDecodeError, KeyError):
                continue

    units = []
    for record, unknown in unresolved_facts(scores_dir):
        from scoring.samples import load_task
        t = load_task(record["task_name"])
        statements = {f.id: f.statement for f in t["facts"]}
        for fid in unknown:
            key = key_of(record, fid, args.direction)
            if key in done_keys or fid not in statements:
                continue
            units.append((key, record, fid, statements[fid]))
    if args.limit:
        units = units[: args.limit]
    print(f"{len(units)} scripts to generate ({len(done_keys)} already on disk)", flush=True)

    client = BedrockClient(read_timeout_s=900.0)
    thinking = None if args.no_thinking else {"type": "adaptive"}
    lock_path = out_path.with_suffix(".lock")  # single-writer append; no concurrent generators
    assert not lock_path.exists(), f"another generator appears active ({lock_path})"
    lock_path.write_text(str(time.time()))
    done = errors = 0
    t0 = time.perf_counter()

    def one(unit):
        key, record, fid, stmt = unit
        prompt = build_prompt(record, stmt, args.direction)
        res = client.send(SYSTEM, prompt, model_id=bcfg.AUTHORING_MODEL_ID,
                          max_tokens=args.max_tokens, thinking=thinking)
        return key, res.text, (res.usage or {})

    try:
        with ThreadPoolExecutor(max_workers=args.concurrency) as pool, \
                out_path.open("a", encoding="utf-8") as fh:
            futures = {pool.submit(one, u): u for u in units}
            for fut in as_completed(futures):
                key = futures[fut][0]
                try:
                    key, text, usage = fut.result()
                    script = extract_script(text)
                    fh.write(json.dumps({"key": key, "script": script,
                                         "output_tokens": usage.get("output_tokens")}) + "\n")
                    fh.flush()
                    done += 1
                except Exception as e:  # noqa: BLE001 -- quota walls must checkpoint, not crash
                    errors += 1
                    print(f"ERROR {key}: {type(e).__name__}: {str(e)[:120]}", flush=True)
                if (done + errors) % 20 == 0:
                    rate = (done + errors) / max(time.perf_counter() - t0, 1e-6)
                    print(f"{done+errors}/{len(units)} (err={errors}) "
                          f"eta {(len(units)-done-errors)/rate/60:.0f} min", flush=True)
    finally:
        lock_path.unlink(missing_ok=True)
    print(f"\nGENERATED {done}, errors {errors} (errors resume on re-run; quota walls land here)")
    return 0 if errors == 0 else 1


def cmd_check(args) -> int:
    from harness.admissibility import STANDARD_MATHLIB_AXIOMS
    from harness.repl import run_checked
    from harness.results import CheckStatus
    from harness.scoring import splice_candidate_declaration
    from ladder.axiom_audit import audit_proof_axioms
    from lean_interact import Command
    from scoring.runner import ServerHandle
    from scoring.samples import load_task

    scores_dir = cfg.scores_dir()
    scripts = {}
    for line in Path(args.scripts).read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
            if row.get("script"):
                scripts[row["key"]] = row["script"]
        except json.JSONDecodeError:
            continue
    print(f"{len(scripts)} generated scripts loaded", flush=True)

    stage, stamp = STAGE[args.direction], STAMP[args.direction]
    handle = ServerHandle()
    checked = certified = audit_rejected = 0
    by_fact = collections.Counter()
    t0 = time.perf_counter()
    try:
        todo = [(r, u) for r, u in unresolved_facts(scores_dir) if not r.get(stamp)]
        for record, unknown in todo:
            t = load_task(record["task_name"])
            statements = {f.id: f.statement for f in t["facts"]}
            relevant = [(fid, scripts.get(key_of(record, fid, args.direction)))
                        for fid in unknown]
            server, env = handle.get()
            outcome = splice_candidate_declaration(server, env, t["signature"],
                                                   record["extracted_code"])
            if outcome.result.status is not CheckStatus.PASSED:
                continue
            cand_env = outcome.result.env
            by_id = {fv["fact_id"]: fv for fv in record["fact_verdicts"]}
            for i, (fid, script) in enumerate(relevant):
                stages = by_id[fid].setdefault("unknown_after", [])
                if script is None:
                    if stage not in stages:
                        stages.append(stage)
                    continue
                goal = statements[fid] if args.direction == "forward" else negation_goal(statements[fid])
                name = f"llm_{args.direction}_{i}"
                decl = f"theorem {name} : {goal} := {script}"
                checked += 1
                result = run_checked(server, Command(cmd=decl, env=cand_env), timeout=120.0)
                ok = result.status is CheckStatus.PASSED
                if ok:
                    cand_env = result.env
                    audit = audit_proof_axioms(server, cand_env, name,
                                               permitted=STANDARD_MATHLIB_AXIOMS)
                    if not audit.passed:
                        audit_rejected += 1
                        ok = False
                        by_id[fid]["detail"] = f"LLM proof rejected by axiom audit: {audit.detail[:160]}"
                if ok:
                    certified += 1
                    by_fact[f"{record['task_name']}/{fid}"] += 1
                    verdict = Verdict.PASS if args.direction == "forward" else Verdict.FAIL
                    by_id[fid].update(
                        verdict=verdict.value, tier=5, script=script,
                        certified_via=stage,
                        detail=("proved by capped LLM prover, kernel-checked"
                                if args.direction == "forward"
                                else "refuted: negation proved by capped LLM prover, kernel-checked"),
                    )
                elif stage not in stages:
                    stages.append(stage)
            record[stamp] = True
            verdicts = [Verdict(fv["verdict"]) for fv in record["fact_verdicts"]]
            record["fidelity"] = fidelity(verdicts)
            record["resolution_rate"] = resolution_rate(verdicts)
            store.write_verdict(record, scores_dir=scores_dir)
    finally:
        handle.close()

    print(f"\nCHECKED {checked} scripts: {certified} kernel-certified, "
          f"{audit_rejected} rejected by axiom audit, {(time.perf_counter()-t0)/60:.1f} min")
    for k, v in by_fact.most_common(15):
        print(f"  {v:>3}x  {k}")
    Path(f"scoring_output/llm_{args.direction}_summary.json").write_text(json.dumps({
        "checked": checked, "certified": certified, "audit_rejected": audit_rejected,
        "by_fact": dict(by_fact)}, indent=1), encoding="utf-8")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate")
    g.add_argument("--direction", choices=("forward", "negation"), required=True)
    g.add_argument("--scripts", default=None)
    g.add_argument("--concurrency", type=int, default=12)
    g.add_argument("--max-tokens", type=int, default=4096)
    g.add_argument("--limit", type=int, default=None)
    g.add_argument("--no-thinking", action="store_true")
    c = sub.add_parser("check")
    c.add_argument("--direction", choices=("forward", "negation"), required=True)
    c.add_argument("--scripts", default=None)
    args = ap.parse_args()
    if args.scripts is None:
        args.scripts = f"scoring_output/llm_scripts_{args.direction}.jsonl"
    return cmd_generate(args) if args.cmd == "generate" else cmd_check(args)


if __name__ == "__main__":
    sys.exit(main())
