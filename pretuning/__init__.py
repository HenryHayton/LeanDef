"""Pre-tuning prompt experiment: 4 anti-sorry levels x 2 reasoning scaffolds, one model.

Measures whether Goedel-Formalizer's 33% `sorry` rate is a task-interpretation artefact (it
stopped at ~700 of 8192 tokens with competent reasoning and miniF2F boilerplate) rather than a
capability ceiling. The three worked exemplars are permanent: whatever they demonstrate, the
model drifts toward.
"""
