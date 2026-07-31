# Batch report: batch-41 completion session (2026-07-31)

*First entry in `docs/batch_reports/` — new convention established this date (see
`docs/batch_reports/2026-07-31_failure_forensics.md`'s Part 0.3 for why: the prior session's
prediction/vocabulary/anchor tracking lived only in chat output and was unrecoverable one
session later. Batch reports are repo artifacts from now on, not chat-only observations.*

## Context

This is the retroactive first entry: the report below was produced live, in chat, at the end
of the "Harness Fixes (Splice, REPL Recovery, Signature Injection) → Complete the Batch"
session (2026-07-31), and is transcribed here verbatim (structure preserved) rather than
rewritten, per the instruction that motivated this file's creation.

Four harness/pipeline fixes landed that session (commits `b412c6a`, `bccd64d`, `404b04d`,
`6ac7767`, `5bea85a`): the truth-splice self-reference/noncomputable bug (Items 0-1), REPL-death
detect/recover in the batch runner (Item 2), mechanical signature injection replacing the
signature-substring check (Item 3), and repair-loop infra-failure exemption (Item 4). The batch
completion phase then re-ran everything those fixes were meant to unblock: 6 `not_agent_fixable`
names, 6 `escalate_to_human` names, and the 16 previously-unattempted names from the 41-name
batch. Total real spend: $4.03 of a $10 session ceiling.

## Aggregate table, all 41 names, final status (as of 2026-07-31, end of completion session)

| Status | Count | Names |
|---|---|---|
| Shipped clean | 24 | Nat.clog, Nat.ModEq, Nat.choose, Function.Bijective, Relation.Map, Nat.divisors, Int.greatestOfBdd, Finset.strongDownwardInduction, Nat.log, Pi.Lex, Function.extend, Equiv.piEquivPiSubtypeProd, Relation.Fibration, Multiset.strongDownwardInduction, Filter.comk, Nat.nthRoot, Multiset.noncommFoldr, Equiv.piCongrRight, Matroid.map, Set.PartiallyWellOrderedOn.IsBadSeq, Nat.evenOddRec, Relation.CutExpand, Finset.strongInduction, Nat.bitCasesOn |
| Repaired & shipped (cleanup loop) | 6 | Int.leastOfBdd, Finset.sumLexLift, OrderHom.prevFixed (pre-session), Nat.findGreatest, Nat.binaryRec, List.prev (this session) |
| Still rotated — harness bug fixed, new distinct failure | 4 | Monotone (dossier_consistency), DependsOn (dossier_consistency), Set.PartiallyWellOrderedOn.IsMinBadSeq (mechanical_validation), Equiv.ofLeftInverse (dossier_consistency) |
| Still escalate_to_human | 3 | Function.Embedding.setValue (round_trip_scoring, compile), SimpleGraph.replaceVertex (mechanical_validation, no facts survived), Equiv.subtypePreimage (new: REPL death during cleanup setup) |
| New rotations, never before attempted | 4 | Filter.Germ.IsConstant (round_trip_scoring), Graph.banana (round_trip_scoring), memPartition (dossier_consistency, real-name leak), Multiset.Pi.cons (mechanical_validation) |

**30/41 shipped, 11/41 unresolved.**

## Problems found, not fixed (as reported that session)

1. `authoring/cleanup.py` had no REPL-death recovery (Item 2 only wired `authoring/batch.py`) —
   live-confirmed: `Equiv.subtypePreimage`'s cleanup attempt died with "Unknown environment"
   during truth-splice setup, escalating with 0 attempts used. **Fixed 2026-07-31, Part 0.1 of
   the immediately-following Failure Forensics session** — see that report.
2. `Function.Embedding.setValue` — reproducible `Invalid ⟨...⟩ notation` compile failure across
   5 repair attempts.
3. `SimpleGraph.replaceVertex` — signature-substring class dissolved as predicted (Item 3), but
   now fails "no facts survived mechanical validation."
4. 8 new rotations (4 phase A + 4 phase C) were never queued (the completion session used
   `author_task` directly, not `run_batch`, so automatic queuing never fired). **Backfilled
   2026-07-31, Part 0.2 of the Failure Forensics session.**
5. 4 names still rotate after Items 1-2, but now for ordinary (non-harness) reasons, confirming
   the fixes worked.

## Note on data this entry does NOT have

The predecessor session (before the one that produced this report) had pre-registered
predictions (referenced as "P2/P4/P5"), a membership-vocabulary baseline, seeded-anchor
tracking, and a "deferred-gap watch" — none of which were ever written to a file. That data was
requested for this report and found to be genuinely unrecoverable (checked `docs/`, scratchpad,
grepped for the relevant terms — nothing). This is the exact loss this new `docs/batch_reports/`
convention exists to prevent going forward.
