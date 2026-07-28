"""Shared configuration for the authoring pipeline driver (`authoring.pipeline`)."""

# Per-task LLM call ceiling (contract §6: "a task consumes at most a bounded number of LLM
# calls (configuration), and a task that exhausts its call budget rotates out"). A dial, not a
# commitment, like every other threshold in this codebase.
#
# Distinct from `authoring.orchestrate.DEFAULT_MAX_CALLS_PER_TASK` (20) -- that one is
# `CallBudget`'s own bare fallback when nothing wires a budget in at all; this is the actual
# per-task default `authoring.pipeline.author_task` uses.
AUTHORING_MAX_CALLS_PER_TASK = 12

# Per-call output-token ceilings, one per contract call. A dial, not a commitment -- like every
# other threshold in this codebase. Confirmed necessary, not precautionary: `BedrockClient
# .send`'s own bare default (1024) is what the real 2026-07-28 slice run used for EVERY call,
# and every one of 4 real dossier-generation attempts hit `stop_reason: max_tokens` at exactly
# that ceiling and got cut off mid-JSON-string -- a six-section dossier with worked examples
# genuinely needs more room than a one-paragraph classification rationale does. Values here are
# a first real-world-informed pass (dossier sized to comfortably clear the ~2300-character,
# still-truncated real response observed; fact_proposal and round_trip sized by the same
# "genuinely more content, more room" reasoning, not independently measured against a real
# truncation the way dossier's number is).
AUTHORING_MAX_TOKENS = {
    "classification": 1024,
    "dossier": 4096,
    "fact_proposal": 8192,
    "round_trip": 2048,
}

# Round-trip compile-failure retry cap (decided 2026-07-28, replacing the prior blind-single-
# repair design -- see `authoring/pipeline.py`'s module docstring, decision 2, and
# `docs/design/llm_io_contract_v1.md` §5). A dial, not a commitment.
ROUND_TRIP_MAX_COMPILE_ATTEMPTS = 4
