"""Shared configuration for the authoring pipeline driver (`authoring.pipeline`)."""

# Per-task LLM call ceiling (contract §6: "a task consumes at most a bounded number of LLM
# calls (configuration), and a task that exhausts its call budget rotates out"). A dial, not a
# commitment, like every other threshold in this codebase.
#
# Distinct from `authoring.orchestrate.DEFAULT_MAX_CALLS_PER_TASK` (20) -- that one is
# `CallBudget`'s own bare fallback when nothing wires a budget in at all; this is the actual
# per-task default `authoring.pipeline.author_task` uses.
AUTHORING_MAX_CALLS_PER_TASK = 12
