"""Deduplicating identical candidate definitions within a task.

Why this is not an optimisation but a necessity: the prelim field sampled 5x at temperature 0.7,
and 12 of the 41 tasks carry the `RECALLED_TARGET` flag (famous definitions the models reproduce
close to verbatim). Both push hard toward the same text appearing many times per task. Scoring
one distinct text costs the full fact suite -- for a task with proof facts, potentially minutes
-- so re-scoring a byte-identical body is pure waste.

**Normalisation is deliberately conservative.** Only whitespace is collapsed: two bodies that
differ by indentation or a trailing newline are the same definition to Lean and to us. Anything
beyond that -- alpha-renaming bound variables, reordering `if`/`match` arms, normalising `fun`
vs `λ` -- would be claiming a semantic equivalence we have not proved, and if the claim were
wrong we would fan one candidate's verdicts out onto a genuinely different definition and
silently record a fabricated result. The tier-4 equivalence path is where semantic sameness gets
established, by the kernel, with a proof.

Fan-out records `scored_as` on every derived file so provenance stays visible: no verdict ever
appears without saying whether it was computed or inherited.
"""

import hashlib
import re

_WHITESPACE = re.compile(r"\s+")


def normalize(body: str) -> str:
    """Collapse runs of whitespace and strip the ends. Nothing else -- see the module docstring
    on why this stops well short of semantic normalisation."""
    return _WHITESPACE.sub(" ", (body or "").strip())


def candidate_hash(body: str) -> str:
    """A short, stable key for a normalised body. 16 hex chars of SHA-256: collision-free at any
    corpus size we will ever have, short enough to read in a filename or a log line."""
    return hashlib.sha256(normalize(body).encode("utf-8")).hexdigest()[:16]


def group_by_hash(samples: list[dict]) -> dict[str, list[dict]]:
    """`{hash: [sample, ...]}` for samples carrying an `extracted_code`.

    Order within each group is input order, so the representative chosen downstream (the first)
    is deterministic -- which matters for resume: a re-run must pick the same representative or
    it would score a second member of the group and write a computed verdict where an inherited
    one already sits.
    """
    groups: dict[str, list[dict]] = {}
    for sample in samples:
        code = sample.get("extracted_code")
        if not code:
            continue
        groups.setdefault(candidate_hash(code), []).append(sample)
    return groups
