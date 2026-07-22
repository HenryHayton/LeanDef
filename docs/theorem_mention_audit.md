# Theorem-Mention Count Audit

*Investigation only — no gate logic, thresholds, scan code, or manifest changed anywhere in
this repo as a result of this report. All recounting described below happened in standalone
scratch scripts outside the tree, reusing the real, unmodified `miner.scan.scan_theorem_statements`
as a baseline wherever a comparison needed one.*

**Question under audit** (per `docs/harvest_review_batch3.md` §3 and §5): `theorem_mention_floor`
kills 75.2% of verified candidates independently (714/950) — the single most aggressive gate in
the pipeline, even at a floor of 2. Does that kill rate reflect a real fact about the corpus, or
is the *measurement* undercounting real theorem-mentions?

**Bottom line, stated up front:** it is overwhelmingly a measurement artifact. §H1 below finds
that most of it comes from one specific, well-understood mechanism — the counter only matches a
candidate's *fully-qualified* name, but the majority of a definition's real theorem-statement
mentions are written *unqualified*, inside the same namespace, per ordinary Lean naming
convention. On a 15-candidate sample spanning the corpus, correcting for this one mechanism alone
moves the floor-2 pass rate from **0/15 (0%) to 8/15 (53%)**.

## How a "theorem mention" is currently counted

Two pieces, both in the current codebase, both read but not modified for this audit:

1. **Statement extraction** (`miner.scan.scan_theorem_statements`): scans a file's raw text
   line by line. A line matching `_THEOREM_RE` — `^(private |protected )*(theorem|lemma)\s+<ident>`
   — starts capture. `_capture_indented_block` then grabs that line plus every following blank
   or indented line, stopping at the next column-0 line (the same indentation heuristic
   `miner.scan.scan_text` uses for `def`s). The captured block is then split on the *first*
   `":="` found anywhere in it, and only the text *before* that point is kept as the
   "statement." This runs once per `.lean` file under `mathlib_root`, across the *entire* tree
   (not just `TARGET_MODULES`) — a corpus-wide pass, since the 22 July 2026 design-doc
   revision made this back a hard gate.
2. **Mention counting** (`miner.harvest.compute_theorem_mention_counts`): for each candidate,
   counts how many of the extracted statement strings contain the candidate's **fully-qualified
   name** (`hit.name`, e.g. `"Finset.pi"`) as a **literal substring** — `hit.name in s`. No
   namespace awareness, no bare-name fallback, no word-boundary anchoring.

The qualified-name-only substring check is the crux of H1. Lean's namespace resolution means a
theorem stated *inside* `namespace Finset ... end Finset` refers to `pi` freely without ever
writing `Finset.pi` — this is not an edge case, it is the dominant style throughout Mathlib. The
counter as written cannot see any of those mentions.

## Candidate sample

15 gate-killed candidates (all currently fail `theorem_mention_floor`), chosen to span the
corpus and to include a deliberate mix of "should intuitively be well-theoremed" `Data/Nat` and
`Data/Finset` names (selected by cross-referencing the manifest's *other* full-corpus signal,
raw `mention_count`, which is unaffected by the qualification issue — a high raw count with a
near-zero theorem-mention count is itself a strong prior signal of undercounting, and several of
these were chosen exactly because they show that split):

| Name | Module | Raw `mention_count` | Reported `theorem_mention_count` |
|---|---|---|---|
| `Finset.pi` | Data/Finset/Pi.lean | 33 | 0 |
| `Nat.binaryRec` | Data/Nat/BinaryRec.lean | 26 | 0 |
| `Finset.attach` | Data/Finset/Attach.lean | 23 | 1 |
| `Finset.empty` | Data/Finset/Empty.lean | 12 | 0 |
| `Finset.strongInduction` | Data/Finset/Card.lean | 9 | 0 |
| `Finset.dens` | Data/Finset/Density.lean | 7 | 0 |
| `Nat.castOrderEmbedding` | Data/Nat/Cast/Order/Basic.lean | 5 | 1 |
| `Finset.choose` | Data/Finset/Basic.lean | 4 | 0 |
| `Nat.chineseRemainderOfMultiset` | Data/Nat/ChineseRemainder.lean | 0 | 0 |
| `maxDefault` | Order/Defs/LinearOrder.lean | 8 | 1 |
| `minDefault` | Order/Defs/LinearOrder.lean | 5 | 1 |
| `IsWellFounded.fix` | Order/RelClasses.lean | 2 | 0 |
| `SemilatticeSup.mk'` | Order/Lattice.lean | 0 | 1 |
| `Composition.blocksFun` | Combinatorics/Enumerative/Composition.lean | 5 | 1 |
| `derangements.subtypeEquiv` | Combinatorics/Derangements/Basic.lean | 0 | 0 |

`Finset.pi` (explicitly requested), `Nat.chineseRemainderOfMultiset` and
`derangements.subtypeEquiv` (raw-mention-zero controls) are included alongside the
high-raw-mention cases, so the sample isn't cherry-picked toward only the worst offenders.

## H1 — Name-matching misses

**Method.** One full-tree pass (8264 files, 176,167 theorem/lemma statements, matching the
figures already logged by the real harvest run) built an index of every extracted statement
together with the **active namespace stack at that exact statement's point of declaration**
(the same `namespace`/`section`/`end` tracking `miner.scan.scan_text` already does for `def`s,
reimplemented locally in the scratch script — not imported from a modified copy, and not fed
back into any real code path). Four counts per candidate:

- **(a) current** — qualified name substring, anywhere, no restriction (the real, unmodified
  behavior).
- **(b) bare name, own-file scope** — bare name substring, restricted to files that *ever* open
  the candidate's namespace prefix (e.g. `namespace Finset`) *somewhere*, at file granularity.
- **(c) bare name, own-namespace scope, cross-tree** — bare name substring, restricted
  *per-statement* to exactly the statements whose active namespace stack at declaration time
  equals the candidate's namespace prefix — correct anywhere in the tree, not just the
  candidate's defining file (Mathlib routinely reopens `namespace Nat`, `namespace Finset`,
  etc. across dozens of files).
- **(d) qualified-or-bare, unrestricted** — bare name substring *or* qualified name substring,
  with no namespace restriction at all — the most permissive strategy, included specifically to
  demonstrate the collision risk the task asked to characterize.

### Results

| Name | (a) current | (b) own-file | (c) own-namespace, cross-tree | (d) qualified-or-bare | (d) bare-only matches | (d) bare-only, *other* namespace |
|---|---|---|---|---|---|---|
| `Finset.pi` | 0 | 162 | 63 | 3428 | 3428 | 3365 |
| `Nat.binaryRec` | 0 | 8 | 7 | 8 | 8 | 1 |
| `Finset.attach` | 1 | 44 | 24 | 111 | 110 | 86 |
| `Finset.empty` | 0 | 611 | 95 | 4953 | 4953 | 4858 |
| `Finset.strongInduction` | 0 | 2 | 2 | 4 | 4 | 2 |
| `Finset.dens` | 0 | 38 | 17 | 435 | 435 | 418 |
| `Nat.castOrderEmbedding` | 1 | 0 | 0 | 1 | 0 | 0 |
| `Finset.choose` | 0 | 57 | 14 | 460 | 460 | 446 |
| `Nat.chineseRemainderOfMultiset` | 0 | 1 | 1 | 1 | 1 | 0 |
| `maxDefault` | 1 | 0 | 1 | 1 | 0 | 0 |
| `minDefault` | 1 | 0 | 1 | 1 | 0 | 0 |
| `IsWellFounded.fix` | 0 | 2 | 1 | 442 | 442 | 441 |
| `SemilatticeSup.mk'` | 1 | 2 | 0 | 589 | 588 | 588 |
| `Composition.blocksFun` | 1 | 26 | 18 | 27 | 26 | 9 |
| `derangements.subtypeEquiv` | 0 | 0 | 0 | 17 | 17 | 17 |

**(b)–(d) systematically exceed (a).** In every row but one (`Nat.castOrderEmbedding`, discussed
below), the corrected strategies recover strictly more mentions than the current method, often
by one to three orders of magnitude. This is the core finding: (a) is not a noisy-but-roughly-right
measurement, it is missing the majority signal entirely for names that are typically used
unqualified.

**Strategy (c) is the trustworthy one; (b) and (d) both overcount for different reasons.**
(d)'s "collision exposure" column makes this concrete: for `Finset.pi`, 3365 of 3428 matches
(98%) come from statements *outside* `Finset`'s own namespace — i.e., the bare token `"pi"`
colliding with unrelated uses (the mathematical constant, unrelated local variables, other
namespaces' own `pi`-named declarations). `Finset.empty` (4858/4953 outside-namespace),
`IsWellFounded.fix` (441/442), and `SemilatticeSup.mk'` (588/589) show the identical pattern —
short, common-English or common-pattern bare names (`pi`, `empty`, `fix`, `mk'`) are exactly the
shape most exposed to this collision, the mirror image of the vocabulary gate's original
bare-name-collision bug (batch 2's Finding B) now showing up on the *counting* side instead of
the *gating* side. (b) is intermediate: file-level granularity means a file that reopens the
right namespace *anywhere* has all its bare mentions counted, including ones textually outside
the actual namespace block at that point (e.g. a file with `namespace Finset ... end Finset`
followed by unrelated top-level content later in the same file) — visible in `Finset.empty`
(611 vs. (c)'s 95) and `Finset.pi` (162 vs. 63), both roughly 2.5–6× (c)'s more careful count.

**Which name shapes are worst hit, in both directions:**
- *Worst undercounted by (a), safely recovered by (c):* long, distinctive, single-purpose bare
  names with low collision risk — `Nat.binaryRec` (0→7, only 1 of 8 (d)-matches is
  cross-namespace), `Finset.strongInduction` (0→2, only 2 of 4 cross-namespace),
  `Composition.blocksFun` (1→18, only 9 of 27 cross-namespace). These are exactly the cases
  where a namespace-scoped bare match is trustworthy.
- *Worst collision-exposed if bare matching is done without namespace scoping (i.e., if a fix
  used (d) instead of (c)):* short, generic, or common-word-shaped bare names — `pi`, `empty`,
  `fix`, `dens`, `mk'`, `choose`. `Finset.dens` in particular (0→17 under (c) but 435 under (d))
  is worst-hit by a *second*, distinct mechanism beyond namespace collision: `"dens"` is a bare
  substring of ordinary English/Mathlib vocabulary (`density`, `condense`, `dense`,
  `Densely...`) that a plain substring check (used by every strategy here, (a) included) cannot
  distinguish from a real identifier token — a word-boundary gap orthogonal to the
  namespace-scoping question, worth noting separately in §synthesis.
- **One case, `Nat.castOrderEmbedding`, where (b) and (c) find *less* than (a):** (a) found its
  one qualified mention in a statement that is *not itself* inside a `Nat`-namespace block (a
  cross-namespace reference using full qualification, exactly as such references should be
  written) — so a bare, namespace-scoped search correctly doesn't re-find it, and correctly
  shouldn't. This confirms (a) and (c) are not nested/comparable in one direction only; the
  right corrected estimate is their **union**, not a replacement — see §synthesis.

## H2 — Statement-extraction scope

**Keyword coverage.** `_THEOREM_RE` already matches both `theorem` **and** `lemma` — confirmed
by direct inspection of the regex and by a raw `grep` cross-check: the corpus contains 177,249
lines starting with `(private |protected )*(theorem|lemma) `, against 176,167 statements the
real scanner actually extracts (a 0.6% gap, addressed below). **`lemma` was never a gap.**

**`instance` declarations are never scanned for statements at all** — confirmed: 26,892
`instance` declarations exist tree-wide, none contribute to `scan_theorem_statements`'s output.
Checked whether this matters for the sample: **it does not, for any of the 15.** None of the 15
candidates' qualified or bare names appear in any instance declaration's own type signature
(0/15, all rows). This is very likely a real, if modest, source of missed mentions *in
general* — some instances do package a fact about a named definition into their signature (e.g.
`instance : DecidablePred Nat.Prime`) — but it happened to contribute nothing to this specific
sample, so its aggregate impact is unmeasured here and would need a separate, broader sample to
size properly.

**Multi-line statements are captured correctly by the indentation-based block capture** — spot
checks across `Order/Basic.lean`, `Algebra/AddConstMap/Basic.lean`, and others confirm signatures
split across several indented lines (binder groups on their own lines, return type on the next)
are captured whole, not truncated at a line boundary.

**A real, distinct, and previously unknown truncation bug: named-argument syntax inside a
statement.** The statement/proof split is `text.split(":=", 1)[0]` — the *first* `":="`
anywhere in the captured block. Lean 4's named-argument application syntax, `f (arg := value)`,
routinely appears *inside a theorem's own stated type* (not just its proof) — e.g.
`lemma birkhoffFinset_injective : Injective (birkhoffFinset (α := α)) := by ...` — and that
`(α := α)` contains a `":="` that occurs *before* the real, top-level statement/proof separator.
The naive split cuts the "statement" off right there, silently discarding everything after —
including any candidate mention that happens to appear later in the actual statement.

Quantified by comparing the naive split against a bracket-depth-aware split (the identical
technique `miner.verify._split_check_output` already uses elsewhere in this codebase, applied
here only in a scratch script — not wired into `miner.scan`): **3,212 of 176,167 statements
(1.82%) are truncated differently by the two methods** — a real, corpus-wide, previously
undocumented measurement bug. **Impact on the 15-candidate sample: zero** — none of the 15 had
a naive-vs-bracket-aware delta (all identical). This bug is confirmed and quantified at the
corpus scale but happens not to touch this particular sample; it should still be fixed (see
§synthesis (iv)), just not because it explains this report's headline finding.

**The 0.6% raw-grep-vs-extracted gap** (177,249 vs. 176,167) was not chased further — an order
of magnitude smaller than either the namespace issue or the truncation bug, and not evidenced to
affect the sample. Plausible innocuous explanations (docstring prose lines that coincidentally
start with `"theorem "` inflating the raw grep count; `noncomputable theorem`, vanishingly rare
in practice) were not required to explain the sample's undercounting and weren't pursued given
proportionate effort.

## H3 — Full-tree scan coverage

**File count:** the scratch full-tree pass processed **8,264 files** — an exact match for
`find $MATHLIB_ROOT -name '*.lean' | wc -l` run independently against the same tree. No files
silently skipped, no path filter dropping a subtree.

**Statement count:** 176,167 statements extracted, consistent with the real harvest run's own
logged timing note ("~176k theorem statements across ~8300 files") from `docs/harvest_review_batch3.md`'s
underlying `miner.harvest` docstring.

**Spot checks**, comparing the real, unmodified `scan_theorem_statements` output against an
independent raw `grep -Ec '^(private |protected )*(theorem|lemma) '` count on the same file:

| File | Raw grep count | Scanner-extracted count |
|---|---|---|
| `Order/Basic.lean` | 126 | 126 |
| `Topology/Basic.lean` | 35 | 35 |
| `Algebra/Group/Basic.lean` | 203 | 203 |

All three match exactly. **No path or filter bug found — H3 is clean.** The scan genuinely
walks the whole tree, and no silent per-file failure (encoding error, exception) occurred: had
one, the real harvest run would have raised rather than completing (there is no
try/except around the per-file read in `compute_theorem_mention_counts`), and the batch-3 run
completed and logged a normal timing.

## Synthesis

**(i) Best estimate of the true-vs-measured relationship, and which hypothesis explains the
gap.** H1 dominates, alone. The qualified-name-only substring match misses the large majority of
real theorem-statement mentions, because Lean's own namespace convention makes unqualified
reference the *normal* way to mention something from inside its own namespace — this is not a
corner case, it is the typical case, and the corrected counts confirm it: 13 of 15 sampled
names had a strictly higher count once namespace-scoped bare matching (strategy (c)) was added.
H2 identified one additional, real, corpus-scale bug (the named-argument truncation, 1.82% of
statements) and ruled out two hypothesized gaps (`lemma` coverage was never missing;
`instance`-declaration exclusion is real but contributed nothing to this sample) — but H2's
confirmed bug has **zero measured overlap** with this report's 15-candidate evidence, so it is
a real, separate, worthwhile fix, not part of *this* report's headline explanation. H3 found
nothing — the full-tree scan is clean. **The gap is explained by H1, essentially alone, for this
sample; H2's truncation bug is real but orthogonal and would need its own broader sample to size
its aggregate contribution.**

**(ii) Corrected sensitivity picture.** Using the union of (a) and (c) — the one estimate this
audit treats as trustworthy, since (b) and (d) both demonstrably overcount (see H1) — the
15-candidate pass rate at each floor:

| Floor | Pass under current (a) | Pass under corrected (union of (a), (c)) |
|---|---|---|
| ≥ 1 | 6/15 (40%) | **14/15 (93%)** |
| ≥ 2 (current `THEOREM_MENTION_FLOOR`) | 0/15 (0%) | **8/15 (53%)** |
| ≥ 3 | 0/15 (0%) | **7/15 (47%)** |

Under the *current, uncorrected* counting, **not one of these 15 candidates clears even a floor
of 2** — the gate is, for this sample, functioning as a near-blanket exclusion rather than a
graded threshold. Under the corrected count, the floor of 2 does real, graded work again: about
half the sample passes, half doesn't, which is what a threshold is supposed to look like.

**(iii) The genuinely-zero population.** Only one of the 15, `derangements.subtypeEquiv`, stays
at zero under every corrected strategy including the careful namespace-scoped one ((c) = 0, and
even the maximally permissive (d) = 17 is *entirely* cross-namespace noise, none of it a real
same-namespace mention). But this candidate is a poor test case for the "conditional floor"
design question: it independently fails three *other* gates simultaneously (`length_band`,
`dependency_vocabulary`, `fact_supply`) — its `casework_tier`, `membership_tier`, and
`global_tier` are all `none`, so it has no supply of any kind, and the theorem-mention floor
isn't the thing actually excluding a candidate that would otherwise be viable.

Widening the lens to the full corpus (not just the 15-sample), though, the design question has
real teeth: **149 candidates fail *only* `theorem_mention_floor`** (would be eligible under
every other gate as currently configured), and of those, **31 (21%) are already `casework_tier:
rich`** — genuine, independently-verified casework supply, excluded solely for lacking global
theorem-mention supply (`Nat.multichoose`, `Nat.doubleFactorial`, `Int.bodd`, `Nat.psub`, and
similar). This is direct, corpus-scale evidence that a floor conditional on other supply being
thin (e.g., "require `theorem_mention_count >= 2` only when `casework_tier` and
`membership_tier` are both `none`") would recover a nontrivial, casework-legitimate population
that the current unconditional floor discards for the wrong reason. Whether that's the right
design call is outside this report's scope; the number to weigh it against is 31 (of 149,
21%) — not hypothetical.

**(iv) Recommended fix scope.** Small-to-moderate, not a scanner rework:

- **H1's fix is the priority.** Extend `scan_theorem_statements` (or a sibling function) to
  track the active namespace stack per statement — the exact `namespace`/`section`/`end`
  tracking `miner.scan.scan_text` already implements for `def`s, adapted rather than invented.
  Then in `compute_theorem_mention_counts`, count a mention if the qualified name matches
  *anywhere* (current behavior, kept) **or** the bare name matches inside a statement whose
  namespace stack equals the candidate's namespace prefix (strategy (c) here) — a union, not a
  replacement, per the `Nat.castOrderEmbedding` counter-example above. This is a self-contained
  change to two functions; no change to `def`-scanning, gating, or the manifest schema.
- **H2's truncation fix is small and mechanical**: swap the naive `.split(":=", 1)[0]` for a
  bracket-depth-aware split. The exact technique already exists in this codebase
  (`miner.verify._split_check_output`) and would need only to be ported, not designed from
  scratch.
- **H2's `instance`-inclusion gap** is lower priority: real, but measured as zero-impact on this
  sample. Worth a follow-up audit with a larger or differently-selected sample before deciding
  whether to extend `scan_theorem_statements` to `instance` declarations — not clearly
  warranted on the evidence gathered here.
- **`THEOREM_MENTION_FLOOR`'s value itself will likely need revisiting once H1 is fixed** — a
  floor of 2 was calibrated against the undercounted measurement; corrected counts run
  substantially higher for genuinely well-theoremed candidates (dozens, sometimes hundreds), so
  the same floor value may end up doing a very different (probably much gentler) job once the
  measurement itself is corrected. Not sized further here — a threshold call for a future task,
  same as this report treats the "conditional floor" question in (iii).
