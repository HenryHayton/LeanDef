"""Step 3 of exemplar sourcing: dossier generation for the six candidates.

Dossier stage only -- no facts, no round-trip. The classification call precedes it because
`run_dossier_call` takes the classification as input; that is the pipeline's normal path, not an
addition. Two Bedrock calls per candidate, twelve total.

**No hand-repair.** An exemplar dossier must exemplify the pipeline's own register: if it comes
out thin, or the leak guard fires, the candidate is disqualified and the slot's backup is used.
Repairing one by hand would produce an exemplar that the pipeline could not itself have written,
which teaches the model a standard the corpus does not meet.

The leak guard is the same `authoring.consistency.check_no_real_name_leak` the batch pipeline
uses, run over the generated dossier against the real Mathlib name.
"""

import argparse
import json
from pathlib import Path

from authoring.consistency import check_no_real_name_leak, extract_sections, inject_pinned_signature
from authoring.orchestrate import run_classification_call, run_dossier_call
from authoring.preflight import check_output_to_pinned_type
from authoring.task_symbol import task_symbol_for
from bedrock import config as bc
from bedrock.client import BedrockClient
from harness.repl import get_warm_environment, run_checked
from harness.results import CheckStatus
from lean_interact import Command

CANDIDATES = [
    ("Fin.contractNth", 1, "A"), ("Nat.ceilRoot", 1, "B"),
    ("SimpleGraph.LocallyLinear", 2, "A"), ("Set.InjOn", 2, "B"),
    ("Filter.limsSup", 3, "A"), ("SuccChain", 3, "B"),
]
OUT = Path("scoring_output/exemplar_bundles.json")


def pinned_signature_for(server, env, real_name: str) -> tuple[str, str]:
    """Print-then-reparse: `#check <real>` -> pi-type -> pin under the task symbol. The same
    machinery the tasks use, so the exemplar shows the signature exactly as a task would."""
    chk = run_checked(server, Command(cmd=f"#check {real_name}", env=env), timeout=60.0)
    if chk.status is not CheckStatus.PASSED or chk.raw_response is None:
        raise RuntimeError(f"#check failed for {real_name}: {chk.detail}")
    text = ""
    for m in chk.raw_response.messages:
        if m.severity == "info":
            text = m.data.strip()
            break
    # `#check <name>` (not `@<name>`): the helper parses Lean's binder-group rendering
    # (`Monotone.{u, v} {a} [b] (c) : Prop`), which is also how the 41 tasks were pinned, so the
    # exemplar's signature line looks exactly like a task's rather than like an arrow type.
    pi = check_output_to_pinned_type(text.lstrip("@"), real_name)
    return f"{task_symbol_for(real_name)} : {pi}", pi


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.parse_args()

    recs = [json.loads(x) for x in Path("miner/output/harvest_manifest.jsonl")
            .read_text(encoding="utf-8").splitlines() if x.strip()]
    manifest = {r["name"]: r for r in recs}

    client = BedrockClient()
    server, imported = get_warm_environment()
    assert imported.status is CheckStatus.PASSED, imported.detail
    env = imported.env

    bundles = []
    for real_name, slot, tag in CANDIDATES:
        rec = manifest[real_name]
        v = rec["verified"]
        print(f"\n=== [{slot}{tag}] {real_name} ===", flush=True)
        try:
            pinned, pi_type = pinned_signature_for(server, env, real_name)
        except Exception as e:  # noqa: BLE001
            print(f"  PIN FAILED: {e}")
            bundles.append({"name": real_name, "slot": slot, "tag": tag, "status": "pin_failed",
                            "error": str(e)[:400]})
            continue
        print(f"  pinned: {pinned[:110]}")

        try:
            classification = run_classification_call(
                client, bc.AUTHORING_MODEL_ID, pinned_signature=pinned,
                definition_source=v["source_text"], docstring=v.get("docstring") or "",
                mention_sidecar_excerpt="", return_shape=rec.get("return_shape") or "value",
            )
            cls_text = json.dumps(classification.__dict__ if hasattr(classification, "__dict__")
                                  else classification, default=str)[:4000]
            payload = run_dossier_call(
                client, bc.FLAGSHIP_MODEL_ID, pinned_signature=pinned,
                definition_source=v["source_text"], docstring=v.get("docstring") or "",
                mention_sidecar_excerpt="", classification=cls_text,
                decidability=None if rec.get("return_shape") != "prop" else "unknown",
            )
        except Exception as e:  # noqa: BLE001
            print(f"  CALL FAILED: {type(e).__name__}: {str(e)[:200]}")
            bundles.append({"name": real_name, "slot": slot, "tag": tag, "status": "call_failed",
                            "error": f"{type(e).__name__}: {str(e)[:400]}"})
            continue

        dossier = inject_pinned_signature(payload.dossier_md, pinned)
        leak_ok, leak_detail = check_no_real_name_leak(dossier, real_name)
        sections = extract_sections(dossier)
        print(f"  dossier: {len(dossier)} chars, {len(sections)} sections, leak_ok={leak_ok}")
        if not leak_ok:
            print(f"    LEAK: {leak_detail[:160]}")

        bundles.append({
            "name": real_name, "slot": slot, "tag": tag, "status": "ok",
            "pinned_signature": pinned, "pinned_type": pi_type,
            "real_body": v["source_text"], "docstring": v.get("docstring") or "",
            "dossier_md": dossier, "dossier_chars": len(dossier),
            "sections": sorted(sections.keys()), "leak_ok": leak_ok, "leak_detail": leak_detail[:400],
            "manifest": {"richness": rec["richness"], "return_shape": rec.get("return_shape"),
                         "exec_mechanism": v.get("exec_mechanism"),
                         "docstring_substance": rec.get("docstring_substance"),
                         "module_path": rec.get("module_path"), "rank": rec.get("rank")},
        })

    server.kill()
    OUT.write_text(json.dumps(bundles, indent=1, ensure_ascii=False), encoding="utf-8")
    ok = [b for b in bundles if b.get("status") == "ok"]
    print(f"\n{'='*70}\nbundles: {len(ok)}/{len(CANDIDATES)} generated -> {OUT}")
    for b in bundles:
        if b.get("status") != "ok":
            print(f"  FAILED {b['name']}: {b['status']} {b.get('error','')[:120]}")
        elif not b["leak_ok"]:
            print(f"  LEAK   {b['name']}: disqualified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
