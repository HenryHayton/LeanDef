"""Three-arm dossier sufficiency probe against Claude Sonnet 4.6.

**The confound this exists to break.** Every measurement so far reads a failure as "8B models
cannot construct definitions". It could equally be "our dossiers under-determine the object, so
NO model could recover it". Nothing run to date separates those, and they imply opposite next
steps: one says get better models or train; the other says the corpus is the bug and every
downstream number is measuring our own writing.

    A  dossier + pinned signature          exactly what the 8B models got
    B  A + the real Mathlib name           ceiling: can it write the thing when told what it is?
    C  pinned signature only, no dossier   floor: is the dossier contributing anything at all?

Reading, fixed before the run:

    A high                -> dossiers are fine; it is a small-model capability gap
    A low, B high         -> the model can produce the object but not from OUR description.
                             The dossiers are the bug.
    A low, B low          -> the task framing itself (pinned type, binder style) is broken
    A ~= C                -> the dossier is decorative and models are reading the signature

**Arm B deliberately defeats the leak guard.** Every other generation path in this repo refuses
to run if a task's real Mathlib name appears in the prompt, because a leak would silently turn a
construction measurement into a recall measurement. Arm B leaks on purpose -- that is the whole
control -- so its samples are quarantined in their own directory, marked `leaked_real_name` in
every stored record, and must never be pooled with arm A or used as training data.

Arm B also asks for the definition to be written out rather than aliased. `:= Nat.clog` would
type-check and prove only that the model can copy a name we just handed it; the question is
whether it can produce the OBJECT. Aliasing is still detected and reported rather than blocked,
since an alias is itself evidence about what the model understood.
"""

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from bedrock import config as bedrock_cfg
from bedrock.client import BedrockClient
from prelim import store
from prelim.prompts import available_tasks, load_task
from pretuning.glossary import render_glossary

ARMS = ("A_dossier", "B_named", "C_signature_only")

SYSTEM = (
    "You are an expert Lean 4 and Mathlib user. You write definitions that are mathematically "
    "faithful to an informal specification and that compile against the given signature."
)

CONFORMANCE = (
    "The definition must have exactly the pinned signature above. Do not change binder style or "
    "explicitness, do not bundle or unbundle arguments, and do not add or drop typeclass "
    "assumptions. Reply with a single fenced ```lean4 block containing only the definition."
)

_SIG_MARKER = "<!-- PINNED-SIGNATURE:"


def _strip_markers(dossier_md: str) -> str:
    return "\n".join(ln for ln in dossier_md.splitlines() if _SIG_MARKER not in ln)


def build_prompt(arm: str, dossier_md: str, pinned_signature: str, real_name: str | None) -> str:
    symbol = pinned_signature.split(" : ", 1)[0]
    pinned_type = pinned_signature.split(" : ", 1)[1] if " : " in pinned_signature else pinned_signature
    blocks: list[str] = []

    if arm != "C_signature_only":
        blocks += [
            "# Your task",
            "",
            "The following is a complete informal specification of a single mathematical object.",
            "",
            _strip_markers(dossier_md).strip(),
            "",
        ]
    else:
        # The floor arm: nothing but the type. If this scores like arm A, the dossier is
        # decorative and the models have been reading the signature all along.
        blocks += [
            "# Your task",
            "",
            "Write the Lean 4 definition with exactly the signature below. No further "
            "specification is provided; infer the intended object from the signature alone.",
            "",
        ]

    blocks += [
        f"Write the complete Lean 4 definition of `{symbol}`. It must have exactly this type:",
        "",
        "```lean",
        pinned_signature,
        "```",
        "",
        CONFORMANCE,
        "",
    ]

    if arm == "B_named":
        blocks += [
            f"For reference, the object being specified is Mathlib's `{real_name}`.",
            "",
            f"Write the definition out in full. Do NOT answer with `{real_name}` itself or with "
            f"a thin alias of it -- reproduce the construction, so that the answer would still "
            f"be correct if that declaration did not exist.",
            "",
        ]

    glossary = render_glossary(pinned_type)
    if glossary:
        blocks += [glossary, ""]
    blocks += ["Mathlib is already imported."]
    return "\n".join(blocks).strip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples-dir", default="prelim_testing/output/dossier_probe")
    ap.add_argument("--samples-per-task", type=int, default=3)
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--concurrency", type=int, default=16)
    # Measured: 281s for one adaptive-thinking call (2700 thinking tokens) on a real task. The
    # client's 60s default read timeout turns every such call into three timed-out retries and
    # then a hard failure -- which reads as a credentials or model-id problem, not a timeout.
    ap.add_argument("--read-timeout", type=float, default=900.0)
    ap.add_argument("--arms", nargs="*", default=list(ARMS))
    ap.add_argument("--tasks", nargs="*", default=None)
    ap.add_argument("--no-thinking", action="store_true",
                    help="disable extended thinking (a hobbled ceiling is not a ceiling; "
                         "use only for a cost-bounded pilot)")
    args = ap.parse_args()

    tasks = args.tasks or available_tasks()
    reals = {p.parent.name: (json.loads(p.read_text()).get("provenance") or {}).get("mathlib_name")
             for p in Path("prelim_testing/tasks").glob("*/task.json")}
    missing = [t for t in tasks if not reals.get(t)]
    if "B_named" in args.arms and missing:
        print(f"refusing to run arm B: {len(missing)} task(s) have no recorded Mathlib name: "
              f"{missing[:5]}", flush=True)
        return 1

    thinking = None if args.no_thinking else {"type": "adaptive"}
    client = BedrockClient(read_timeout_s=args.read_timeout)
    samples_dir = Path(args.samples_dir)
    model_id = bedrock_cfg.AUTHORING_MODEL_ID

    print(f"{'=' * 78}\nDOSSIER PROBE\n{'=' * 78}")
    print(f"model={model_id}  region={bedrock_cfg.REGION}  thinking={thinking}")
    print(f"arms={args.arms}  tasks={len(tasks)}  samples/task={args.samples_per_task}")
    print(f"total calls = {len(args.arms) * len(tasks) * args.samples_per_task}\n", flush=True)

    units = [(arm, t, i) for arm in args.arms for t in tasks
             for i in range(args.samples_per_task)]
    done = generated = errors = skipped = 0
    t0 = time.perf_counter()

    def one(unit):
        nonlocal generated, errors, skipped
        arm, task, idx = unit
        if store.is_complete(arm, task, idx, samples_dir=samples_dir):
            skipped += 1
            return
        dossier, pinned = load_task(task)
        prompt = build_prompt(arm, dossier, pinned, reals.get(task))
        started = time.perf_counter()
        try:
            res = client.send(SYSTEM, prompt, model_id=model_id, max_tokens=args.max_tokens,
                              thinking=thinking)
        except Exception as e:  # noqa: BLE001 -- one sample must never sink the run
            errors += 1
            print(f"[{arm}] {task}/{idx} ERROR {type(e).__name__}: {str(e)[:140]}", flush=True)
            return
        usage = res.usage or {}
        sample = store.build_sample(
            model_name=model_id, task_name=task, sample_index=idx,
            temperature=1.0, max_tokens=args.max_tokens,
            prompt_messages=[{"role": "system", "content": SYSTEM},
                             {"role": "user", "content": prompt}],
            completion=res.text, finish_reason=getattr(res, "stop_reason", None),
            prompt_tokens=usage.get("input_tokens"),
            completion_tokens=usage.get("output_tokens"),
            wall_time_s=time.perf_counter() - started,
            extra={
                "arm": arm,
                "cell_id": arm,
                "task": task,
                "thinking": thinking,
                # Arm B is the only path in this repo that puts a task's real Mathlib name in a
                # prompt. Marked on every record so a later consumer cannot pool it by accident.
                "leaked_real_name": reals.get(task) if arm == "B_named" else None,
                "thinking_tokens": (usage.get("output_tokens_details") or {}).get("thinking_tokens"),
            },
        )
        sample.model_slug = arm
        store.write_sample(sample, samples_dir=samples_dir)
        generated += 1

    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = [pool.submit(one, u) for u in units]
        for _ in as_completed(futures):
            done += 1
            if done % 25 == 0:
                rate = done / max(time.perf_counter() - t0, 1e-6)
                eta = (len(units) - done) / rate if rate else float("inf")
                print(f"{done}/{len(units)} (gen={generated} skip={skipped} err={errors}) "
                      f"eta {eta/60:.0f} min", flush=True)

    print(f"\nDONE generated={generated} skipped={skipped} errors={errors} "
          f"{(time.perf_counter()-t0)/60:.1f} min")
    return 0


if __name__ == "__main__":
    sys.exit(main())
