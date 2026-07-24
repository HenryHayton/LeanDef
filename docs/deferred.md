# Deferred

A running list of known, deliberately-not-yet-done items. Each entry has a **trigger**: the
specific event or milestone that makes it time to act. An entry is not a priority ranking and
not a promise of when it'll happen — it's a tripwire, so that when the trigger fires, the item
gets picked up rather than re-discovered from scratch. Remove an entry once it's actioned;
don't leave it checked off in place.

- **`harness.config.PROOF_TIMEOUT` retirement.** Unused placeholder (`harness/config.py:39`),
  superseded by the tiered adjudication ladder's per-tier budgets.
  **Trigger:** the unified ladder-budget config (`docs/design/reward_structure_2026-07-21.md`
  §7) lands.
- **`docs/decidability_bias_survey.md` line ~137 prover-retry phrasing.** Describes retry cost
  in terms of "a prover agent's retry," pre-dating the adjudication ladder.
  **Trigger:** the next edit of that doc.
- **Sonnet 5 re-pin.** `AUTHORING_MODEL_ID` / `FLAGSHIP_MODEL_ID` (`bedrock/config.py`) are
  pinned to `eu.anthropic.claude-sonnet-4-6`; `eu.anthropic.claude-sonnet-5` is catalogued
  in-region (`eu-west-1`) but not yet entitled to the account.
  **Trigger:** Bedrock entitlement for `eu.anthropic.claude-sonnet-5` lands.
- **Flagship-model residue comparison.** Pre-registered follow-up: re-run the hammer-failed
  residue with a flagship-class model for comparison
  (`docs/design/reward_structure_2026-07-21.md` §6).
  **Trigger:** the pilot (§11 of that doc) shows a fat residue of hammer-failed facts that the
  pinned model also cannot close.
- **Stub-fixture parity with the real Bedrock response shape.** `tests/test_bedrock_client.py`'s
  `_success_body()` fixture doesn't model prompt-caching `usage` fields or `stop_details`,
  which the real Bedrock response carries (confirmed 2026-07-24).
  **Trigger:** the next `bedrock/`-touching task that edits its tests.
- **Archived τ probe → schema-v1 golden fixture.** `archive/n1_tau/` is the one worked example
  from the n=1 probe; converting it into a golden fixture under the frozen task schema would
  give the harness a known-answer regression test.
  **Trigger:** task schema v1.1 lands.
- **Self-host the premise-selection server** (`hanwenzhu/lean-premise-server`). The EC2 hammer
  box currently uses the public default (`http://leanpremise.net`, per the LeanHammer README —
  documented as intended for individual use); self-hosting is a separate repo with its own
  setup, materially more complex than using the default (`docs/ec2_runbook.md` Phase D).
  **Trigger:** before the first real training round; until then the public server is used for
  search only — cached-script replay (reward doc §3.2) has no server dependency, so nothing
  downstream of a certified proof depends on the public server staying up.
- **Elastic IP or SSM Session Manager for stable EC2 box addressing.** The hammer box's public
  IP changes on every stop/start (`docs/ec2_runbook.md`), requiring a re-fetch (and a security-
  group rule update) every session.
  **Trigger:** if IP-refetch friction becomes a recurring cost (e.g. once sessions on this box
  become frequent enough that the manual re-fetch/re-authorize steps add up).
