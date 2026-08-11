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
    """The tactic script from the reply.

    Two shapes: a bare `by ...` block (what the Sonnet prompt asks for), or a full
    `theorem ... := by ...` (what prover-trained models emit natively -- their training task is
    completing whole proof files, and asking them for anything else fights the training). For
    the second shape the script is everything from the LAST top-level `:= by` onward.
    """
    blocks = re.findall(r"```(?:lean4?|)\s*\n(.*?)```", text or "", re.DOTALL | re.IGNORECASE)
    for block in reversed(blocks or [text or ""]):
        script = block.strip()
        if script.startswith("by"):
            return script
        m = None
        for m in re.finditer(r":=\s*(by\b)", script):
            pass
        if m:
            return script[m.start(1):].strip()
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


def arm_of(record, fact_id) -> str:
    """Deterministic assignment of a GOAL to a backend arm.

    Hashed, not positional: generation walks goals in alphabetical task order, so "first half /
    second half" would hand the arms systematically different tasks and confound the comparison.
    sha1 rather than hash() -- Python salts hash() per process, and the assignment must be
    reproducible across machines and runs. The DIRECTION is deliberately excluded: a goal's
    forward and negation attempts belong to the same arm, so each arm owns its half end-to-end.

    Two-stage split. Stage 1 (2026-08-09, operator design): 50/50 goedel-8b vs "the rest",
    unchanged since -- the goedel-8b bucket is bit-for-bit stable across every later change here,
    so its in-flight/completed attempts are never invalidated by a later split.

    Stage 2 (2026-08-10, operator design: "split sonnet's current workload in half, attack the
    second half with goedel-32b on another pod"): the REST bucket (previously "sonnet" outright)
    sub-splits 50/50 into "sonnet" / "goedel32b" via an independently salted hash. Safe to
    introduce after generation had already started, because at the moment this was added the
    live sonnet backlog (399 unresolved fact-pairs) had zero overlap with either script file on
    disk -- confirmed by direct check -- so no in-flight sonnet attempt gets relabeled out from
    under itself.
    """
    import hashlib
    base = f"{record['model_slug']}|{record['task_name']}|{record['sample_index']}|{fact_id}"
    if hashlib.sha1(base.encode()).digest()[0] % 2:
        return "goedel"
    sub = hashlib.sha1((base + "|32b-split").encode()).digest()[0] % 2
    return "goedel32b" if sub else "sonnet"


def _refutes_truth_too(server, base_env, statement: str, real_name: str, task_symbol: str,
                       imports, script: str | None = None) -> bool:
    """Does the refuting argument also refute the TRUTH? Then the FACT is defective.

    **The model's own script is tried FIRST, with the task symbol rewritten to the real name.**
    A refutation is a WITNESS -- `refine ⟨0, 1, ?_⟩` -- and a generic tactic ladder cannot
    rediscover which witness. Measured on the case that motivated this: for
    `Nat.divisors/divisors_mem_iff` the ladder below returns False (it never guesses n=0, d=1),
    while the model's four-line script proves the truth's negation instantly. Relying on the
    ladder alone therefore certified a FAIL against a fact already known to be defective --
    twice, on two different runs, before this was traced.

    The generic ladder is kept as a fallback for the case where the script is unusable against
    the truth (it may `unfold` the candidate's own symbol, which has no counterpart there).
    """
    import dataclasses

    from harness.repl import run_checked
    from harness.results import CheckStatus
    from harness.signature import root_qualify
    from ladder.budgets import DEFAULT_LADDER_BUDGETS, TacticBudget
    from ladder.tier2 import adjudicate_tier2
    from lean_interact import Command

    if script:
        truth_goal = negation_goal(statement.replace(task_symbol, root_qualify(real_name)))
        ported = script.replace(task_symbol, root_qualify(real_name))
        probe = run_checked(
            server, Command(cmd=f"theorem _truth_probe_script : {truth_goal} := {ported}",
                            env=base_env), timeout=120.0)
        if probe.status is CheckStatus.PASSED:
            return True

    truth_stmt = statement.replace(task_symbol, root_qualify(real_name))
    budgets = dataclasses.replace(DEFAULT_LADDER_BUDGETS, tier2_tactics=(
        TacticBudget("push_neg <;> simp_all", 15.0),
        TacticBudget("push_neg <;> omega", 10.0),
        TacticBudget("decide", 10.0),
        TacticBudget("push_neg <;> aesop", 30.0, heavy=True),
    ))
    probe = adjudicate_tier2(server, base_env, "neg_truth_probe",
                             negation_goal(truth_stmt), budgets, imports=imports)
    return probe.winning is not None


PROVER_SYSTEM = "You are an expert Lean 4 and Mathlib prover."


def build_prover_prompt(record: dict, statement: str, direction: str) -> str:
    """Prover-native shape: a Lean file to complete, not a conversation. Goedel-Prover-V2's
    trained task is emitting the finished proof for a stated theorem; the candidate definition
    rides above the goal exactly as an auxiliary definition would in its training data."""
    goal = statement if direction == "forward" else negation_goal(statement)
    return (
        "Complete the following Lean 4 code:\n\n"
        f"```lean4\nimport Mathlib\n\n{record['extracted_code']}\n\n"
        f"theorem goal_to_prove : {goal} := by\n```\n"
    )


def _generate_converse(args) -> int:
    """Cross-vendor generation via Bedrock Converse (DeepSeek, Qwen, ...).

    Same resume/atomic-append contract as the Bedrock-Anthropic path: one row per goal keyed by
    `key`, errors counted and left absent so a re-run retries exactly them.
    """
    from bedrock.converse import ConverseClient
    from scoring.samples import load_task

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
        t = load_task(record["task_name"])
        statements = {f.id: f.statement for f in t["facts"]}
        for fid in unknown:
            key = key_of(record, fid, args.direction)
            if key in done_keys or fid not in statements:
                continue
            if args.arm != "all" and arm_of(record, fid) != args.arm:
                continue
            units.append((key, record, fid, statements[fid]))
    if args.limit:
        units = units[: args.limit]
    print(f"{len(units)} scripts to generate with {args.model_id} @ {args.region} "
          f"({len(done_keys)} already on disk)", flush=True)
    if not units:
        return 0

    client = ConverseClient(region=args.region, read_timeout_s=900.0)
    lock_path = out_path.with_suffix(".lock")
    assert not lock_path.exists(), f"another generator appears active ({lock_path})"
    lock_path.write_text(str(time.time()))
    done = errors = 0
    t0 = time.perf_counter()

    def one(unit):
        key, record, fid, stmt = unit
        prompt = build_prompt(record, stmt, args.direction)
        res = client.send(SYSTEM, prompt, model_id=args.model_id,
                          max_tokens=args.max_tokens, temperature=args.temperature)
        return key, res

    try:
        with ThreadPoolExecutor(max_workers=args.concurrency) as pool, \
                out_path.open("a", encoding="utf-8") as fh:
            futures = {pool.submit(one, u): u for u in units}
            for fut in as_completed(futures):
                key = futures[fut][0]
                try:
                    key, res = fut.result()
                    fh.write(json.dumps({
                        "key": key, "script": extract_script(res.text),
                        "output_tokens": res.output_tokens, "stop_reason": res.stop_reason,
                        "model_id": res.model_id}) + "\n")
                    fh.flush()
                    done += 1
                except Exception as e:  # noqa: BLE001 -- quota walls checkpoint, never crash
                    errors += 1
                    print(f"ERROR {key}: {type(e).__name__}: {str(e)[:140]}", flush=True)
                if (done + errors) % 20 == 0:
                    rate = (done + errors) / max(time.perf_counter() - t0, 1e-6)
                    print(f"{done+errors}/{len(units)} (err={errors}) "
                          f"eta {(len(units)-done-errors)/rate/60:.0f} min", flush=True)
    finally:
        lock_path.unlink(missing_ok=True)
    print(f"\nGENERATED {done}, errors {errors}")
    return 0 if errors == 0 else 1


def cmd_generate(args) -> int:
    if args.backend == "vllm":
        return _generate_vllm(args)
    if args.backend == "converse":
        return _generate_converse(args)
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
            if args.arm != "all" and arm_of(record, fid) != args.arm:
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


def _generate_vllm(args) -> int:
    """Prover-backend generation: k sampled attempts per goal against a vLLM endpoint.

    k separate calls rather than one n=k request: `prelim.client`'s SSE accumulator merges all
    choices into one string, and k calls parallelise across the pool anyway. Rows carry the same
    `key` with an `attempt` index; the check phase tries every attempt until one certifies.
    """
    from prelim.client import generate as vllm_generate

    scores_dir = cfg.scores_dir()
    out_path = Path(args.scripts)
    done = set()
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
                done.add((row["key"], row.get("attempt", 0)))
            except (json.JSONDecodeError, KeyError):
                continue

    units = []
    from scoring.samples import load_task
    for record, unknown in unresolved_facts(scores_dir):
        t = load_task(record["task_name"])
        statements = {f.id: f.statement for f in t["facts"]}
        for fid in unknown:
            if fid not in statements:
                continue
            if args.arm != "all" and arm_of(record, fid) != args.arm:
                continue
            key = key_of(record, fid, args.direction)
            for attempt in range(args.samples):
                if (key, attempt) not in done:
                    units.append((key, attempt, record, statements[fid]))
    if args.limit:
        units = units[: args.limit]
    print(f"{len(units)} attempts to generate (pass@{args.samples}, "
          f"{len(done)} already on disk)", flush=True)

    t0 = time.perf_counter()
    n_done = errors = 0

    def one(unit):
        key, attempt, record, stmt = unit
        prompt = build_prover_prompt(record, stmt, args.direction)
        res = vllm_generate(
            [{"role": "user", "content": prompt}], temperature=args.temperature,
            max_tokens=args.max_tokens, model_name=args.model_name, endpoint_style="chat",
            stream=True, timeout_s=1800.0, endpoint_url=args.endpoint)
        return key, attempt, res.text

    with ThreadPoolExecutor(max_workers=args.concurrency) as pool,             out_path.open("a", encoding="utf-8") as fh:
        futures = {pool.submit(one, u): u for u in units}
        for fut in as_completed(futures):
            key, attempt = futures[fut][0], futures[fut][1]
            try:
                key, attempt, text = fut.result()
                fh.write(json.dumps({"key": key, "attempt": attempt,
                                     "script": extract_script(text)}) + "\n")
                fh.flush()
                n_done += 1
            except Exception as e:  # noqa: BLE001
                errors += 1
                print(f"ERROR {key}#{attempt}: {type(e).__name__}: {str(e)[:100]}", flush=True)
            if (n_done + errors) % 50 == 0:
                rate = (n_done + errors) / max(time.perf_counter() - t0, 1e-6)
                print(f"{n_done+errors}/{len(units)} (err={errors}) "
                      f"eta {(len(units)-n_done-errors)/rate/60:.0f} min", flush=True)
    print(f"\nGENERATED {n_done}, errors {errors}")
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
    scripts = collections.defaultdict(list)
    for line in Path(args.scripts).read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
            if row.get("script") and row["script"] not in scripts[row["key"]]:
                scripts[row["key"]].append(row["script"])
        except json.JSONDecodeError:
            continue
    print(f"{sum(len(v) for v in scripts.values())} scripts over {len(scripts)} goals", flush=True)

    if getattr(args, "tag", None):
        # An explicit tag names the (model, arm) pass, so a SECOND model attacking the SAME arm's
        # goals gets its own stage and stamp. Without it the stamp from the first pass would make
        # `todo` skip every record, and the run would silently do nothing.
        stage, stamp = f"{args.tag}_{args.direction}", f"{args.tag}_{args.direction}_topup"
    elif args.arm in ("goedel", "goedel32b"):
        tag = "prover" if args.arm == "goedel" else "prover32b"
        stage, stamp = f"{tag}_{args.direction}", f"{tag}_{args.direction}_topup"
    else:
        stage, stamp = STAGE[args.direction], STAMP[args.direction]
    handle = ServerHandle()
    checked = certified = audit_rejected = 0
    by_fact = collections.Counter()
    suspect_facts = collections.Counter()
    t0 = time.perf_counter()
    try:
        todo = [(r, u) for r, u in unresolved_facts(scores_dir) if not r.get(stamp)]
        for record, unknown in todo:
            t = load_task(record["task_name"])
            statements = {f.id: f.statement for f in t["facts"]}
            in_arm = [fid for fid in unknown
                      if args.arm == "all" or arm_of(record, fid) == args.arm]
            if not in_arm:
                continue  # no goals of this record belong to this arm -- do not stamp it
            relevant = [(fid, scripts.get(key_of(record, fid, args.direction)) or [None])
                        for fid in in_arm]
            server, env = handle.get()
            outcome = splice_candidate_declaration(server, env, t["signature"],
                                                   record["extracted_code"])
            if outcome.result.status is not CheckStatus.PASSED:
                continue
            cand_env = outcome.result.env
            by_id = {fv["fact_id"]: fv for fv in record["fact_verdicts"]}
            for i, (fid, attempt_scripts) in enumerate(relevant):
                stages = by_id[fid].setdefault("unknown_after", [])
                goal = statements[fid] if args.direction == "forward" else negation_goal(statements[fid])
                ok, script = False, None
                for j, candidate_script in enumerate(attempt_scripts):
                    if candidate_script is None:
                        continue
                    script = candidate_script
                    name = f"llm_{args.direction}_{i}_{j}"
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
                        break
                if not any(attempt_scripts):
                    if stage not in stages:
                        stages.append(stage)
                    continue
                if ok and args.direction == "negation" and t.get("truth_real_name"):
                    # A refutation only indicts the CANDIDATE if the TRUTH survives the same
                    # attack. `scripts/negation_topup.py` has carried this countercheck since the
                    # pass's first-ever refutation turned out to be a defective fact
                    # (Nat.log/log_lt_of_lt_pow, missing `n ≠ 0`); this path did not, and shipped
                    # the identical failure again -- Nat.divisors/divisors_mem_iff, false of real
                    # `Nat.divisors` at n=0 because both it and the candidate give ∅ there.
                    # Without this, tier 5 manufactures FAILs against defective facts at scale.
                    if _refutes_truth_too(server, env, statements[fid], t["truth_real_name"],
                                          t["signature"].name, cfg.imports_for(t.get("imports")),
                                          script=script):
                        suspect_facts[f"{record['task_name']}/{fid}"] += 1
                        by_id[fid]["detail"] = ("refutation also proves against the truth -- "
                                                "suspect FACT, not a candidate FAIL")
                        by_id[fid].setdefault("unknown_after", []).append("neg_suspect_fact")
                        ok = False
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
          f"{audit_rejected} rejected by axiom audit, "
          f"{sum(suspect_facts.values())} withheld as SUSPECT FACTS (the refutation also proves "
          f"against the truth), {(time.perf_counter()-t0)/60:.1f} min")
    for k, v in by_fact.most_common(15):
        print(f"  {v:>3}x  {k}")
    for k, v in suspect_facts.most_common(15):
        print(f"  SUSPECT {v:>3}x  {k}")
    Path(f"scoring_output/llm_{args.direction}_summary.json").write_text(json.dumps({
        "checked": checked, "certified": certified, "audit_rejected": audit_rejected,
        "by_fact": dict(by_fact), "suspect_facts": dict(suspect_facts)}, indent=1), encoding="utf-8")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate")
    g.add_argument("--direction", choices=("forward", "negation"), required=True)
    g.add_argument("--arm", choices=("sonnet", "goedel", "goedel32b", "all"), default="all")
    g.add_argument("--backend", choices=("bedrock", "vllm", "converse"), default="bedrock")
    g.add_argument("--model-id", default=None, help="converse backend: Bedrock model id")
    g.add_argument("--region", default=None, help="converse backend: AWS region hosting it")
    g.add_argument("--tag", default=None,
                   help="names this (model, arm) pass; required when a second model attacks an "
                        "arm another model already stamped")
    g.add_argument("--endpoint", default=None, help="vllm backend: chat-completions URL")
    g.add_argument("--model-name", default="Goedel-LM/Goedel-Prover-V2-8B")
    g.add_argument("--samples", type=int, default=8, help="vllm backend: pass@k attempts/goal")
    g.add_argument("--temperature", type=float, default=1.0)
    g.add_argument("--scripts", default=None)
    g.add_argument("--concurrency", type=int, default=12)
    g.add_argument("--max-tokens", type=int, default=4096)
    g.add_argument("--limit", type=int, default=None)
    g.add_argument("--no-thinking", action="store_true")
    c = sub.add_parser("check")
    c.add_argument("--direction", choices=("forward", "negation"), required=True)
    c.add_argument("--arm", choices=("sonnet", "goedel", "goedel32b", "all"), default="all")
    c.add_argument("--scripts", default=None)
    c.add_argument("--tag", default=None, help="must match the tag used at generate time")
    args = ap.parse_args()
    if args.scripts is None:
        backend = getattr(args, "backend", None) or "check"
        suffix = "" if backend in ("bedrock", "check") else f"_{args.model_name.rsplit('/', 1)[-1].lower()}"
        args.scripts = f"scoring_output/llm_scripts_{args.direction}{suffix}.jsonl"
    return cmd_generate(args) if args.cmd == "generate" else cmd_check(args)


if __name__ == "__main__":
    sys.exit(main())
