"""Prelim testing: running several open models over the task dossiers to select a training
base model.

Stage 1 (this package's initial contents) is Mac-side plumbing only -- `prelim.client` (an
OpenAI-compatible HTTP client, which is what vLLM serves) and `prelim.store` (the on-disk
sample store), both exercised against `prelim.stubserver` rather than any real endpoint.

Naming note: this effort was called "bake-off" in early discussion; that term is retired.
Everything here says "prelim testing". The package is `prelim/`; its on-disk output tree is
`prelim_testing/output/` (see `prelim.config`).
"""
