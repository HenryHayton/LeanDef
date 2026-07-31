# Batch report: batch-41 CLOSING RECORD (2026-07-31)

*Third and final entry for this batch. Supersedes the completion and forensics entries as the
statement of record for where batch-41 ended up.*

## Final scoreboard: 41/41 shipped

| Route | Count |
|---|---|
| Shipped clean on first pass (never rotated) | 22 |
| Shipped after repair (rotation queue → cleanup runner) | 19 |
| **Total shipped** | **41 / 41** |
| Unresolved | 0 |

The batch closed at 100%. That number should be read carefully: it is **not** evidence that every
definition was easy. Of the 19 repaired names, the majority were unblocked by fixing checks that
were rejecting correct work — three separate self-triggering name matchers, an ERRORED/FAILED
conflation, a truth-splice self-reference — and the final seven shipped only because round-trip
compile exhaustion became a *flag* rather than a rotation (the "harder" decision, contract §5).
Those seven are retained deliberately as corpus-hardness signal.

## Flag counts

| Flag | Count | Notes |
|---|---|---|
| clean (no flag) | 10 | of the 22 first-pass names |
| `RECALLED_TARGET` | 12 | of the 22 first-pass names; famous definitions accumulate this |
| `UNVERIFIED_TERMINATION_ONLY` | 0 | none in this batch |
| **`ROUND_TRIP_UNVERIFIED_COMPILE` ("harder")** | **6 (inferred, not persisted)** | see the gap below |
| not persisted | 19 | every cleanup-repaired name |

**Known gap in this table.** `authoring.cleanup.CleanupResult` does not carry
`round_trip_flags`, and neither does the emitted `task.json` — flags live only on an in-memory
`TaskResult` and in the batch review. So for all 19 repaired names the flags are **unrecoverable
from persisted data**. The 6 "harder" count is a sound inference, not a measurement. Those six are
exactly `Function.Embedding.setValue`, `Filter.Germ.IsConstant`, `Graph.banana`,
`Equiv.ofLeftInverse`, `SimpleGraph.replaceVertex` and `Equiv.subtypePreimage`: each had
previously exhausted every repair attempt on round-trip compile failure, and each shipped on
attempt 1 immediately after the flag landed with no other change — and the only path from
4-attempt compile exhaustion to SHIPPED is the new flag.

Deliberately NOT counted as "harder": `Set.PartiallyWellOrderedOn.IsMinBadSeq`, which also
shipped on attempt 1 this session but was never a round-trip failure — it rotated at
`mechanical_validation` and was unblocked by the namespace-qualification prompt guidance (Item 4).
Also not counted: `Int.leastOfBdd`, `Finset.sumLexLift`, `OrderHom.prevFixed` and `List.prev`,
which were round-trip compile exhaustions repaired *before* the flag existed — they shipped by
eventually producing a compiling body, so their round trips are verified.

This gap matters now in a way it did not before: "harder" is a population we specifically want to
count. Listed as found-not-fixed.

## Per-name final status

| Name | Route | Round-trip flags |
|---|---|---|
| `Nat.clog` | clean first pass | RECALLED_TARGET |
| `Nat.choose` | clean first pass | RECALLED_TARGET |
| `Nat.ModEq` | clean first pass | clean |
| `Monotone` | repaired | not persisted |
| `Function.Bijective` | clean first pass | clean |
| `Relation.Map` | clean first pass | clean |
| `Function.extend` | repaired | not persisted |
| `Nat.findGreatest` | repaired | not persisted |
| `Nat.divisors` | clean first pass | RECALLED_TARGET |
| `DependsOn` | repaired | not persisted |
| `Int.greatestOfBdd` | clean first pass | RECALLED_TARGET |
| `Nat.binaryRec` | repaired | not persisted |
| `Int.leastOfBdd` | repaired | not persisted |
| `List.prev` | repaired | not persisted |
| `Finset.strongDownwardInduction` | clean first pass | RECALLED_TARGET |
| `Finset.sumLexLift` | repaired | not persisted |
| `Nat.log` | clean first pass | RECALLED_TARGET |
| `OrderHom.prevFixed` | repaired | not persisted |
| `Pi.Lex` | clean first pass | clean |
| `Function.Embedding.setValue` | repaired | not persisted |
| `SimpleGraph.replaceVertex` | repaired | not persisted |
| `Equiv.subtypePreimage` | repaired | not persisted |
| `Set.PartiallyWellOrderedOn.IsMinBadSeq` | repaired | not persisted |
| `Equiv.piEquivPiSubtypeProd` | repaired | not persisted |
| `Equiv.ofLeftInverse` | repaired | not persisted |
| `Filter.Germ.IsConstant` | repaired | not persisted |
| `Graph.banana` | repaired | not persisted |
| `Relation.Fibration` | clean first pass | clean |
| `Multiset.strongDownwardInduction` | clean first pass | RECALLED_TARGET |
| `Filter.comk` | clean first pass | RECALLED_TARGET |
| `Nat.nthRoot` | clean first pass | clean |
| `memPartition` | repaired | not persisted |
| `Multiset.noncommFoldr` | clean first pass | RECALLED_TARGET |
| `Equiv.piCongrRight` | clean first pass | RECALLED_TARGET |
| `Matroid.map` | clean first pass | RECALLED_TARGET |
| `Set.PartiallyWellOrderedOn.IsBadSeq` | clean first pass | clean |
| `Nat.evenOddRec` | clean first pass | clean |
| `Relation.CutExpand` | clean first pass | clean |
| `Finset.strongInduction` | clean first pass | clean |
| `Nat.bitCasesOn` | clean first pass | RECALLED_TARGET |
| `Multiset.Pi.cons` | repaired | not persisted |

## What closed this batch

| Session | Change |
|---|---|
| Harness fixes | truth-splice `_root_.` qualification + noncomputable retry; REPL-death recovery in the batch runner; mechanical signature injection (retiring the signature-substring check); repair-loop infra-failure exemption |
| Failure forensics | per-name verdicts for all 11 then-unresolved names; survivorship analysis; repair-drift check (no content loss found); REPL-death recovery in the cleanup runner; `docs/batch_reports/` established |
| Quick fixes | `validate_global_fact` ERRORED/FAILED conflation; leak-check task-symbol self-trigger; `repair_one` truth-splice; raw-name fact-check task-symbol exclusion |
| Closing (this) | "harder" flag; name-matcher consolidation into `authoring/namematch.py`; `mechanical_validation` → agent-fixable; namespace-qualification prompt guidance |

## Standing caveats for whoever reads this next

1. **100% is a ceiling artifact, not a quality claim.** Seven tasks ship with the reconstruction
   unverified. They are good tasks with an unverified round trip, which is exactly what the flag
   says — but a downstream consumer that ignores flags will over-trust this corpus.
2. **Flags are not persisted for repaired tasks** (above). Fix before the flag counts matter
   quantitatively — i.e. before the mini-trial.
3. **The three-matcher bug class cost four separate discoveries.** They are now one helper
   (`authoring/namematch.py`); a future "compare a name against text" site must call it.
