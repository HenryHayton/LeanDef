"""Step 1 of exemplar sourcing: mechanical filter over the eligible pool. No LLM.

Selects a shortlist of candidate few-shot exemplars for the Formalizer prompt. These will sit in
every prompt of every future run, so the filter is deliberately conservative -- it is cheaper to
hand-read 30 survivors than to discover mid-training that an exemplar taught the wrong lesson.

The body is the demonstration, so every structural condition is checked on the BODY, not on the
signature: a definition with a rich type and a one-line delegating body teaches delegation.

Attrition is reported per condition (cumulative), because which condition does the cutting is
itself a finding about the pool -- see the batch-report note on slot-3 scarcity.
"""

import json
import re
from pathlib import Path

MANIFEST = Path("miner/output/harvest_manifest.jsonl")
TASKS_DIR = Path("prelim_testing/tasks")
OUT = Path("scoring_output/exemplar_shortlist.json")

LEN_MIN, LEN_MAX = 60, 250
LEN_MIN_TIGHT, LEN_MAX_TIGHT = 80, 220

# Disqualifiers (spec): incidental machinery that would dominate an example.
WHERE_OR_FUEL = re.compile(r"\bwhere\b|\bfuel\b|termination_by|decreasing_by")
CONDITIONAL = re.compile(r"\bif\b|\bmatch\b|\bthen\b")
QUANTIFIER = re.compile(r"∀|∃|⦃")
CONNECTIVE = re.compile(r"∧|∨|→|↔|¬")


def body_of(source_text: str) -> str:
    """Text after the top-level `:=`. Equation-style definitions (`| pat => …`) have no `:=`,
    so they return the match block, which is the right thing to measure."""
    if ":=" not in source_text:
        return source_text.strip()
    return source_text.split(":=", 1)[1].strip()


def normalized(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def task_collision_keys():
    """Final-two name components of every current task, plus their task symbols.

    Two-component matching (not just the leaf) because `Nat.log`/`Nat.clog` style families share
    idiom and vocabulary; an exemplar from the same family would leak the shape of a live task
    into every prompt.
    """
    keys, symbols = set(), set()
    for p in TASKS_DIR.glob("*/task.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        real = (d.get("provenance") or {}).get("mathlib_name") or p.parent.name
        parts = real.split(".")
        keys.add(".".join(parts[-2:]) if len(parts) >= 2 else parts[-1])
        keys.add(parts[-1])
        symbols.add(d["signature"]["name"])
        symbols.add(real)
    return keys, symbols


def main() -> int:
    recs = [json.loads(x) for x in MANIFEST.read_text(encoding="utf-8").splitlines() if x.strip()]
    elig = [r for r in recs if r.get("eligible")]
    coll_keys, coll_syms = task_collision_keys()
    task_reals = {(json.loads(p.read_text()).get("provenance") or {}).get("mathlib_name")
                  for p in TASKS_DIR.glob("*/task.json")}

    steps, cur = [], elig
    steps.append(("eligible pool", len(cur)))

    cur = [r for r in cur if r["name"] not in task_reals]
    steps.append(("minus the 41 current tasks", len(cur)))

    def keep(r, lo, hi):
        return lo <= len(normalized(body_of(r["verified"]["source_text"]))) <= hi

    cur = [r for r in cur if keep(r, LEN_MIN, LEN_MAX)]
    steps.append((f"body length {LEN_MIN}-{LEN_MAX} chars", len(cur)))

    def structural(r, min_total):
        rich = r.get("richness") or {}
        if (rich.get("total") or 0) < min_total:
            return False
        body = body_of(r["verified"]["source_text"])
        if CONDITIONAL.search(body):
            return True
        return bool(QUANTIFIER.search(body) and CONNECTIVE.search(body))

    strict = [r for r in cur if structural(r, 2)]
    relaxed_used = False
    cur = strict
    steps.append(("richness>=2 AND (conditional/match OR quantifier+connective) in BODY", len(cur)))

    cur = [r for r in cur if (r["verified"].get("docstring") or "").strip()
           and (r.get("docstring_substance") or {}).get("score", 0) > 0]
    steps.append(("substantive docstring", len(cur)))

    def collides(r):
        parts = r["name"].split(".")
        two = ".".join(parts[-2:]) if len(parts) >= 2 else parts[-1]
        if two in coll_keys or parts[-1] in coll_keys:
            return True
        body = r["verified"]["source_text"]
        return any(re.search(rf"(?<![A-Za-z0-9_.]){re.escape(s)}(?![A-Za-z0-9_'])", body) for s in coll_syms)

    cur = [r for r in cur if not collides(r)]
    steps.append(("no namespace-family collision with a task", len(cur)))

    cur = [r for r in cur if not WHERE_OR_FUEL.search(r["verified"]["source_text"])]
    steps.append(("no where-clause / fuel recursion (disqualifier)", len(cur)))

    # Relax or tighten per the spec's own thresholds.
    note = ""
    if len(cur) < 12:
        relaxed_used = True
        note = "RELAXED richness to >=1 (shortlist was under 12)"
        cur = [r for r in elig if r["name"] not in task_reals and keep(r, LEN_MIN, LEN_MAX)
               and structural(r, 1)
               and (r["verified"].get("docstring") or "").strip()
               and (r.get("docstring_substance") or {}).get("score", 0) > 0
               and not collides(r) and not WHERE_OR_FUEL.search(r["verified"]["source_text"])]
        steps.append(("[relaxed] richness>=1", len(cur)))
    elif len(cur) > 60:
        note = f"TIGHTENED length to {LEN_MIN_TIGHT}-{LEN_MAX_TIGHT} (shortlist was over 60)"
        cur = [r for r in cur if keep(r, LEN_MIN_TIGHT, LEN_MAX_TIGHT)]
        steps.append((f"[tightened] length {LEN_MIN_TIGHT}-{LEN_MAX_TIGHT}", len(cur)))

    print(f"{'condition':<62}{'surviving':>10}{'cut':>8}")
    prev = None
    for label, n in steps:
        cut = "" if prev is None else f"-{prev - n}"
        print(f"{label:<62}{n:>10}{cut:>8}")
        prev = n
    if note:
        print(f"\n** {note} **")

    for r in cur:
        v = r["verified"]
        r["_body"] = normalized(body_of(v["source_text"]))
        r["_body_len"] = len(r["_body"])
        r["_exec"] = v.get("exec_mechanism")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cur, indent=1, ensure_ascii=False), encoding="utf-8")

    import collections
    print(f"\nshortlist: {len(cur)}  ->  {OUT}")
    print(f"  return_shape : {dict(collections.Counter(r.get('return_shape') for r in cur))}")
    print(f"  exec_mechanism: {dict(collections.Counter(r.get('_exec') for r in cur))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
