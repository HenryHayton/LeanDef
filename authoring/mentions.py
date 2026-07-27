"""Mention-sidecar retrieval helper (contract §1.4, §8 item 4): cap + rank the full, unranked
per-definition mention list `miner.harvest.write_mention_names` persists into a short excerpt
worth spending prompt tokens on.

Relevance heuristic (deliberately simple -- per the task that added this module, "a relevance
heuristic, not a retrieval system," and a named tuning point): prefer statements that read as
self-contained when shown out of context, approximated by how many fully-qualified
`Namespace.name` references they contain (a statement leaning on qualified names needs less
ambient context to make sense on its own than one relying on bare names resolved by an open
namespace); prefer shorter statements as a tiebreak (less to read, less room for noise);
dedupe by exact statement text before capping (the sidecar can match the same statement twice
under a namespace-qualified and a bare-name variant, per
`miner.harvest.compute_theorem_mentions`'s own matching rule).
"""

import re

from miner.harvest import MentionRecord

DEFAULT_MENTION_CAP = 15

# A fully-qualified reference: an identifier starting with an uppercase letter (Mathlib
# namespace convention), followed by at least one `.segment` -- e.g. `Nat.clog`, `List.Sorted`.
# Deliberately crude (a real Lean parser would do better) -- this is a ranking heuristic, not a
# correctness check, and the module docstring says so.
_QUALIFIED_REF_RE = re.compile(r"\b[A-Z][A-Za-z0-9_']*(?:\.[A-Za-z0-9_']+)+\b")


def _qualified_ref_count(statement_text: str) -> int:
    return len(_QUALIFIED_REF_RE.findall(statement_text))


def rank_mentions(records: list[MentionRecord], *, cap: int = DEFAULT_MENTION_CAP) -> list[MentionRecord]:
    """Cap + rank one definition's mention list: sort by (more fully-qualified references
    first, shorter statement first), dedupe by `statement_text` keeping the highest-ranked
    copy, then truncate to `cap`. `cap` is a configuration knob, not a fixed constant --
    callers tune it per prompt-budget needs."""
    ranked = sorted(records, key=lambda r: (-_qualified_ref_count(r.statement_text), len(r.statement_text)))
    seen: set[str] = set()
    deduped: list[MentionRecord] = []
    for record in ranked:
        if record.statement_text in seen:
            continue
        seen.add(record.statement_text)
        deduped.append(record)
    return deduped[:cap]


def render_mention_excerpt(records: list[MentionRecord], *, cap: int = DEFAULT_MENTION_CAP) -> str:
    """Render a capped+ranked mention list as the prompt-ready excerpt text every generation
    call's input includes (contract §1.4)."""
    ranked = rank_mentions(records, cap=cap)
    if not ranked:
        return "(no mentioning theorems found in the mention sidecar)"
    return "\n".join(f"- {r.theorem_name}: {r.statement_text}  ({r.source_file})" for r in ranked)
