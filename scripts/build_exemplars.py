"""Build and VERIFY the three few-shot exemplar declarations.

An exemplar that does not compile, or does not have its own pinned type, would teach the model
exactly the failure we are trying to remove -- and it would do so in every prompt of every future
run. So each one is put through the real machinery here: spliced against Mathlib, checked for
admissibility, and type-probed against the pinned signature. Anything that fails is not shipped.

**Why the declaration is rebuilt rather than reused verbatim.** Mathlib source relies on
file-scoped `variable` declarations (`SimpleGraph.LocallyLinear`'s `α` is never bound in its own
`def` line), so pasting the source text standalone does not elaborate. The manifest records
`binder_groups`, so the header is reconstructed mechanically: implicit `{}`, instance `[]` and
explicit `()` groups in their original order, then the return type, then the original body. That
is also the shape a correct ANSWER takes -- binders in the header, not a pi-type -- which is what
the exemplar needs to demonstrate.
"""

import json
from pathlib import Path

from harness.admissibility import check_admissibility, type_probe_command
from harness.repl import get_warm_environment, run_checked
from harness.scoring import splice_candidate
from harness.signature import PinnedSignature
from harness.results import CheckStatus
from lean_interact import Command

CHOSEN = [("Nat.ceilRoot", 1), ("SimpleGraph.LocallyLinear", 2), ("Filter.limsSup", 3)]
OUT = Path("pretuning/exemplars.json")


def render_binders(groups) -> str:
    parts = []
    for g in groups:
        names = " ".join(g.get("names") or [])
        t = g.get("type_text", "")
        kind = g.get("kind")
        if kind == "implicit":
            parts.append(f"{{{names} : {t}}}")
        elif kind == "instance":
            parts.append(f"[{t}]" if not names else f"[{names} : {t}]")
        elif kind == "strict_implicit":
            parts.append(f"⦃{names} : {t}⦄")
        else:
            parts.append(f"({names} : {t})")
    return " ".join(parts)


def main() -> int:
    recs = {json.loads(x)["name"]: json.loads(x)
            for x in Path("miner/output/harvest_manifest.jsonl").read_text().splitlines() if x.strip()}
    bundles = {b["name"]: b for b in json.loads(Path("scoring_output/exemplar_bundles.json").read_text())}
    prose = json.loads(Path("scoring_output/exemplar_r1_prose.json").read_text())

    server, imported = get_warm_environment()
    assert imported.status is CheckStatus.PASSED, imported.detail
    env = imported.env

    out, all_ok = [], True
    for name, slot in CHOSEN:
        b = bundles[name]
        v = recs[name]["verified"]
        sym = b["pinned_signature"].split(" : ", 1)[0]
        src = v["source_text"]
        body = src.split(":=", 1)[1].strip() if ":=" in src else src
        binders = render_binders(v.get("binder_groups") or [])
        decl = f"def {sym} {binders} : {v['return_type']} :=\n  {body}".replace("  :", " :")

        sig = PinnedSignature(name=sym, type_sig=b["pinned_type"])
        sp = splice_candidate(server, env, f"@[reducible] {decl}", timeout=90.0)
        ok_compile = sp.status is CheckStatus.PASSED
        verdict = None
        ok_type = False
        if ok_compile:
            verdict = check_admissibility(server, sp.env, sig, splice_response=sp.raw_response, timeout=90.0)
            probe = run_checked(server, Command(cmd=type_probe_command(sig), env=sp.env), timeout=90.0)
            ok_type = probe.status is CheckStatus.PASSED

        status = "OK" if (ok_compile and verdict and verdict.passed and ok_type) else "FAILED"
        print(f"[slot {slot}] {sym:<24} compile={ok_compile} "
              f"admissible={verdict.passed if verdict else None} type_ok={ok_type}  -> {status}")
        if status != "OK":
            all_ok = False
            print(f"    splice : {(sp.detail or '')[:200]}")
            if verdict and not verdict.passed:
                print(f"    verdict: {verdict.failure.value}: {verdict.detail[:200]}")
        out.append({
            "slot": slot, "source_name": name, "task_symbol": sym,
            "pinned_signature": b["pinned_signature"], "pinned_type": b["pinned_type"],
            "dossier_md": b["dossier_md"], "definition": decl, "r1_prose": prose[name],
            "verified_compiles": ok_compile,
            "verified_admissible": bool(verdict and verdict.passed),
            "verified_type_matches": ok_type,
        })

    server.kill()
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\n{'ALL THREE VERIFIED' if all_ok else '*** NOT ALL VERIFIED -- do not ship ***'} -> {OUT}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
