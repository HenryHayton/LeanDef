"""Read the Lean that models actually produced, from the samples on disk.

The store is append-only and written as each generation lands, so this is safe to run against
a LIVE run -- it only reads, and a partially-finished run just shows fewer samples.

    uv run python scripts/show_samples.py                       # what exists so far, one line each
    uv run python scripts/show_samples.py --task Nat.clog        # every model's answer to one task
    uv run python scripts/show_samples.py --model goedel-prover-v2-8b --full
    uv run python scripts/show_samples.py --failures             # only the ones extraction rejected
    uv run python scripts/show_samples.py --raw --task Nat.clog  # the complete completion text

By default it prints the EXTRACTED definition (what scoring will actually see). `--raw` prints
the model's whole reply including its reasoning, which is what you want when the extraction
looks wrong and you need to see whether the model or the extractor is at fault.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from prelim.extract import Extraction, extract_definition  # noqa: E402

SAMPLES = Path(__file__).resolve().parent.parent / "prelim_testing" / "output" / "samples"

BOLD, DIM, RESET = "\033[1m", "\033[2m", "\033[0m"
GREEN, RED, YELLOW = "\033[32m", "\033[31m", "\033[33m"


def load_all(root: Path) -> list[dict]:
    out = []
    for path in sorted(root.rglob("sample_*.json")):
        try:
            d = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            continue  # a sample being written right now; it will be there next time
        d["_path"] = path
        out.append(reextract(d))
    return out


def reextract(d: dict) -> dict:
    """Recompute extraction from the stored completion instead of trusting the stored verdict.

    The sample files record whatever the extractor decided AT GENERATION TIME, and that verdict
    goes stale the moment the extractor is fixed -- as it was on 2026-08-03, when a fence
    pair-matching bug was found mid-run. Those samples are never regenerated (the store's
    resume-safety correctly treats them as complete), so the frozen `extraction_ok` on disk can
    disagree with what the current code would say.

    Extraction is a pure, deterministic, millisecond-cheap function of `completion`, so the
    honest thing is to recompute it on read. Nothing here writes: the raw completion is the
    durable artifact, and the extraction is a view over it.
    """
    result = extract_definition(
        d.get("model_slug", ""), d.get("completion") or "", finish_reason=d.get("finish_reason")
    )
    extra = dict(d.get("extra") or {})
    was = extra.get("extraction_ok")
    if isinstance(result, Extraction):
        extra.update(
            extraction_ok=True, extracted_code=result.code, declared_name=result.declared_name,
            renamed_symbol=result.renamed_symbol, from_fence=result.from_fence,
            n_candidates=result.n_candidates,
        )
    else:
        extra.update(
            extraction_ok=False, extraction_reason=result.reason, extraction_detail=result.detail,
            n_candidates=result.n_candidates,
        )
    extra["_stale_on_disk"] = was is not None and was != extra["extraction_ok"]
    d["extra"] = extra
    return d


def one_line(d: dict) -> str:
    extra = d.get("extra") or {}
    ok = extra.get("extraction_ok")
    mark = f"{GREEN}ok {RESET}" if ok else f"{RED}FAIL{RESET}"
    code = (extra.get("extracted_code") or "").replace("\n", " ⏎ ")
    if not ok:
        code = f"{DIM}{extra.get('extraction_reason', 'no definition extracted')}{RESET}"
    flags = []
    if extra.get("renamed_symbol"):
        flags.append("renamed")
    if d.get("finish_reason") == "length":
        flags.append("hit-token-cap")
    if (extra.get("n_candidates") or 1) > 1:
        flags.append(f"{extra['n_candidates']} candidates")
    if extra.get("_stale_on_disk"):
        flags.append("stale verdict on disk")
    tag = f" {YELLOW}[{', '.join(flags)}]{RESET}" if flags else ""
    return (
        f"{mark} {d['model_slug']:<32} {d['task_name']:<22} "
        f"s{d['sample_index']:02d} T={d['temperature']}{tag}\n     {code[:150]}"
    )


def detailed(d: dict, *, raw: bool) -> str:
    extra = d.get("extra") or {}
    head = (
        f"{BOLD}{'=' * 92}{RESET}\n"
        f"{BOLD}{d['task_name']}{RESET} — {d['model_slug']}  "
        f"(sample {d['sample_index']}, temperature {d['temperature']}, "
        f"{d.get('completion_tokens')} tokens, {d.get('wall_time_s', 0):.0f}s"
        f", finish={d.get('finish_reason')})\n{BOLD}{'=' * 92}{RESET}\n"
    )
    if raw:
        return head + (d.get("completion") or "(empty)") + "\n"
    if not extra.get("extraction_ok"):
        return (
            head
            + f"{RED}extraction failed:{RESET} {extra.get('extraction_reason', '?')}\n"
            + f"{DIM}{extra.get('extraction_detail', '')}{RESET}\n"
            + f"{DIM}--- rerun with --raw to see the full reply ---{RESET}\n"
        )
    return head + (extra.get("extracted_code") or "") + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--task", help="only this task (e.g. Nat.clog)")
    p.add_argument("--model", help="only this model slug (substring match is fine)")
    p.add_argument("--sample", type=int, help="only this sample index")
    p.add_argument("--full", action="store_true", help="print each definition in full, not one line")
    p.add_argument("--raw", action="store_true", help="print the model's ENTIRE reply (implies --full)")
    p.add_argument("--failures", action="store_true", help="only samples where extraction failed")
    p.add_argument("--root", type=Path, default=SAMPLES)
    args = p.parse_args()

    if not args.root.exists():
        print(f"no samples yet at {args.root}", file=sys.stderr)
        return 1

    rows = load_all(args.root)
    if args.task:
        rows = [d for d in rows if d["task_name"] == args.task]
    if args.model:
        rows = [d for d in rows if args.model in d["model_slug"]]
    if args.sample is not None:
        rows = [d for d in rows if d["sample_index"] == args.sample]
    if args.failures:
        rows = [d for d in rows if not (d.get("extra") or {}).get("extraction_ok")]

    if not rows:
        print("no samples match that filter (yet)", file=sys.stderr)
        return 1

    for d in rows:
        print(detailed(d, raw=args.raw) if (args.full or args.raw) else one_line(d))

    ok = sum(1 for d in rows if (d.get("extra") or {}).get("extraction_ok"))
    print(f"\n{BOLD}{len(rows)} samples — {ok} extracted, {len(rows) - ok} failed{RESET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
