"""Miner stage 1: mechanical harvest of Mathlib definitions.

Pure filtering and measurement -- no LLM calls, no fact generation, no dossier writing, no
task directories. Output is a ranked harvest manifest (`miner/output/harvest_manifest.jsonl`)
for a human/agent to work from in a later stage. See `docs/design/task_schema_v1.md` and both
design docs in `docs/design/` for the target shape this harvest feeds into.
"""
