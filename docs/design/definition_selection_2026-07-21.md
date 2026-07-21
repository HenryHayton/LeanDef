# Definition Selection

*Design of record for miner definition selection · 21 July 2026*
*Supersedes the ranking design implicit in miner stage 1 — the weighted score of quality,
in-degree, and dependency-footprint that `miner/rank.py` computed for harvest batch 1. The
stage-1 measurement machinery (`miner/scan.py`, `miner/verify.py`, `miner/proxies.py`) is
retained as-is: this document changes what is done with the measurements, not how they are
taken.*

---

## 1 · What the first ranking got wrong

The batch-1 harvest (`docs/harvest_review_batch1.md`) surfaced a selection failure, not a
measurement failure. Every number the pipeline recorded was, after the round-2 fixes,
accurate; the problem was what the ranking formula did with those numbers. Dominance of
mention-count and dependency-minimality in a single additive score selected for **fundamental
vocabulary**: `Finset.range`, sitting at the top of the batch on the strength of 852 raw
mentions and zero recorded dependencies, and one-line delegations like `Nat.Prime := Irreducible
p`, cheap precisely because there is nothing there to be wrong about. Both are upstream of
essentially everything in the corpus — maximal mentions by construction, since anything this
foundational is used everywhere — and both are trivially shallow, minimal dependencies by the
same construction, since a definition this close to the axioms has nothing left to depend on.
Worse, both are exactly the kind of object a plausible base model has memorized verbatim: `range
n := ⟨_, nodup_range n⟩` is not a definition a model needs to *reason* its way to: it has almost
certainly seen this exact declaration, under this exact name, in this exact file, many times
over in pretraining.

The consequence is a task that produces a near-100% pass rate for reasons that have nothing to
do with the candidate's understanding of the mathematics. A task like that carries no selection
pressure: every plausible candidate solves it, so it distinguishes nothing and teaches nothing.
It is not that mention-count is a bad measurement — it was doing one legitimate job, standing in
for global-fact supply, since a definition mentioned often in theorem statements has a large
pool of candidate global facts sitting around it, ready to be pulled into a fact suite. The
failure was architectural: as a dominant *additive weight* in a scalar score, mention-count
ended up selecting for ubiquity in the corpus, not for richness of content. Ubiquity and content
are different axes, and the batch-1 score conflated them.

## 2 · The architectural change: gates and bands, not a weighted sum

A scalar weighted score has a structural property that no amount of re-tuning removes: any
metric with enough spread, given enough weight (or, symmetrically, any metric with enough
absolute range even at moderate weight), can dominate the ranking on its own. That is exactly
the failure mode §1 describes, and adjusting `MENTION_WEIGHT` or `DEPENDENCY_WEIGHT` up or down
would only move the dominance around — trade one blind spot for another — rather than remove
the mechanism that produces blind spots in the first place. A weighted sum lets a candidate
compensate for having no content of its own by being sufficiently well-connected in the
dependency graph; that compensation is precisely what must not be possible.

The redesign replaces the single weighted score with two separate mechanisms that cannot
compensate for one another:

- **Hard eligibility gates** define the includable set. Each gate is a yes/no test; a
  candidate that fails any gate is excluded, full stop, regardless of how it scores on every
  other axis. Gates are individually auditable — every exclusion in the manifest records
  *which* gate fired, not just that the candidate was excluded — so the reason a definition
  didn't make it into the corpus is always inspectable, never a difference-of-scores no one
  can read back out.
- **A small preference score** orders the set that survives the gates. It is deliberately
  minor relative to the gates in terms of what work it does: the gates have already done the
  job of ensuring every candidate that reaches the score has *some* minimum bar of content,
  supply, and tractability, so the score's only remaining job is to rank among
  already-acceptable candidates, not to rescue unacceptable ones.

No metric can compensate for another under this scheme — a candidate that is unusually rich in
theorem mentions still fails the length-band gate if it is a one-line delegation, and no amount
of richness-score credit can buy it past a docstring-floor gate it fails. This is the direct
fix for §1's failure: the batch-1 score let `Finset.range`'s dependency count of zero and
mention count of 852 add up to a rank-1 finish despite (not because of) its content being
trivial; under gates-and-bands, the length-band gate and the anti-plumbing filter are the
first line of defense against exactly that shape of candidate, and no mention-count credit
downstream can undo an exclusion decided upstream.

All thresholds introduced below are named config values, not literals buried in the ranking
logic, and none of them is expected to be correct on the first attempt. The expected workflow
is to run the harvest, read the exclusion report (which gate fired, and how often, for which
candidates), and adjust the thresholds — the same iterate-on-the-manifest workflow that
produced the round-2 fixes to the measurement layer, now applied to the selection layer.

## 3 · The gates

**(a) Full-corpus theorem mentions ≥ `MENTION_FLOOR`** (initial value: 30). This is
mention-count's legitimate job, demoted from a score contribution to a minimum requirement:
enough theorem-statement mentions across the corpus to guarantee that global-fact supply and
documentation actually exist for this object, not merely that they exist in profusion. Once a
candidate clears the floor, additional mentions buy it nothing further — ubiquity above the
floor is no longer rewarded, which is the direct fix for the part of §1's failure that put
`Finset.range`'s 852 mentions to work as a scoring advantage rather than a supply guarantee.

**(b) Length band `[LENGTH_MIN, LENGTH_MAX]`** on the normalized definition body. The floor
rejects one-liners and pure delegations — there is too little text, and therefore too little
independent content, to formalize a dossier around; the ceiling rejects definitions whose
dossier would be unmanageably large to author and review. Length is used as a band, not a
score, because it is a difficulty proxy that lies in *both* directions: recursion boilerplate
(a `where`-clause fuel-recursive auxiliary, a multi-case pattern match) inflates a body's raw
length without adding conceptual difficulty, while a clean one-line delegation to a
well-chosen helper deflates it without the object being simple — the two errors don't cancel,
they compound, which is why length gets a permissive band to screen out only the extremes
rather than a score that would reward or punish the middle for no good reason. The §4 richness
score is what actually measures difficulty within the band.

**(c) Docstring floor.** A docstring must exist and exceed a trivial length. This is not a
content-quality check — it is a raw-material check. The dossier is generated by
reverse-translating the docstring (and source) into prose; a definition with no docstring, or
a docstring too short to state anything beyond the name, gives the dossier generator nothing
to reverse-translate, and every downstream stage inherits that gap.

**(d) Dependency vocabulary tier.** Every dependency a candidate uses must lie within a
common-vocabulary tier of Mathlib — the basic `Nat`, `List`, `Finset`, order, and algebra
modules, given as a config list rather than hard-coded. This replaces dependency-*count*
scoring entirely, for a reason the batch-1 data made concrete: what makes a task hard on the
candidate side is exotic, unfamiliar infrastructure, not the sheer number of times a candidate
touches common vocabulary. Counting dependencies punished condition-rich definitions for the
wrong reason — a definition with several genuine side conditions legitimately references more
supporting lemmas and structures than a shallow one, so a naive count treated richness as a
penalty. Gating on *which* vocabulary tier the dependencies come from, rather than how many
there are, removes that perverse incentive while still keeping genuinely exotic candidates out
of scope for now.

**(e) Anti-plumbing name patterns.** Automatic exclusion of `Aux`/`aux`, `Impl`/`.go`,
tail-recursive `TR`-suffixed variants, and `decEq`/`beq`/instance-machinery names: these are
engineering artifacts of how Lean/Mathlib code is organized, not independent mathematical
objects with an informal identity of their own — there is nothing to write a dossier *about*.
`Nat.digitsAux1`, excluded by hand via `miner/curation.yaml` in the round-2 re-harvest because
its docstring says "(Impl.)", is exactly the class of candidate this gate mechanizes: the
curation file remains in place for genuine judgment calls (near-duplicate concepts, borderline
cases), while name-pattern matching now handles the mechanical, high-volume class so curation
doesn't have to be re-litigated by hand every batch.

**(f) At least one non-`none` fact-supply tier.** A definition supporting no fact of any type —
casework, membership, or global — under the stage-1 supply proxies would be an unscoreable
task by construction, regardless of what else is true about it. This is the weakest possible
floor in the set and is expected to rarely bind, since gate (a) alone (a mention floor of 30)
already implies some global-fact supply for almost every survivor; it is kept as an explicit,
separately-auditable gate rather than folded silently into (a) so that the rare candidate it
does catch is visible in the exclusion report under its own name.

## 4 · The preference score

Ordering among gate-survivors is governed by a small set of preferences, in weight order.

**(1) Structural richness — dominant.** A count, over the definition body and its binders, of
conjunctions, conditionals and match arms, quantifiers, comparison operators, and hypothesis
binders (side conditions). This is close to a direct measurement of how many distinguishable
ways a candidate definition can be *wrong*: a dropped conjunct, a flipped inequality, a missing
side condition, a swapped quantifier — these are precisely the misreading classes the verifier
exists to catch (`docs/design/verifier_architecture_2026-07-20.md` §2, mutant suites), and a
definition with more of this structure has more places for a plausible-but-wrong candidate to
diverge from it. Richness also directly attacks the delegation problem that dependency-count
scoring was standing in for, badly: a pure delegation (`toFinset l := Multiset.toFinset l`) has
approximately zero structure of its own — no conjunction, no conditional, no side condition, no
comparison — so it scores near zero on richness regardless of how many or how few things it
depends on. This replaces the old proxy (dependency-minimality, which measured the wrong thing
and happened to correlate with delegation only by accident) with a direct measurement of the
property dependency-count was only ever gesturing at.

**(2) Docstring substance.** Beyond the floor in gate (c), prefer docstrings that state
conditions or conventions in prose — the kind of sentence that tells a dossier author "this is
undefined at zero, by such-and-such Mathlib convention" rather than merely naming the object.
A docstring that states a condition is raw material the dossier generator can lift directly;
one that only names the function leaves the generator to infer everything from the signature
and source alone.

**(3) Supply breadth.** Well-rounded supply across the three fact types (casework, membership,
global) beats lopsided supply at equal quality — unchanged in substance from the previous
design's breadth term (`miner/rank.py`'s `BREADTH_WEIGHT`), and kept deliberately the smallest
weight in the score for the same reason it was smallest before: it is a soft, tie-breaking
preference, not a requirement. A candidate that is excellent on one fact type and absent on the
other two is still allowed to outrank a mediocre-but-well-rounded one; breadth only decides
between candidates that are otherwise close.

## 5 · What is deliberately absent

**Convention-presence detection (junk-value reliance) as its own gate or score term.** This was
considered and dropped. It is not ignored — it arrives for free as a byproduct of richness,
since the edge-case conditionals that encode a junk-value convention (`digits 0 0 = []`,
handled as a special case rather than falling out of the general recursion) are exactly the
kind of conditional structural richness already counts. Building a second, dedicated detector
for the same signal would duplicate machinery for no additional information, and — more to the
point — the system's actual leverage over convention problems is at dossier-authoring and
validation time (stating the convention correctly, checking the dossier against it), not at
selection time. Selection only needs to know that convention-bearing structure is present, which
richness already tells it.

**"Number of plausible misreadings" as a direct, standalone metric.** This is the actual
target this whole exercise is reaching for, and it is not mechanically measurable — counting
misreadings requires knowing what a plausible-but-wrong reader would get wrong, which requires
the kind of judgment only a reader (human or LLM) can supply. Structural richness is offered
here as its best available mechanical shadow: a proxy that correlates with the true target
without claiming to *be* it. The honest assessment of how many ways a given definition can be
misread belongs to stage 2's LLM difficulty estimate, made per-object with the dossier and
source in hand, not to a mechanical count made at selection time over a corpus of hundreds of
candidates.

## 6 · Corpus scope

The five module corners scanned in batch 1 (`Data/Nat`, `Data/List`, `Data/Finset`, `Data/Int`,
`Logic`) are structurally biased toward simplicity: they are foundational corners of Mathlib,
and foundations are, definitionally, full of simple things — the basic recursors, the basic
predicates, the basic constructors everything else is built from. Re-ranking within that set,
however good the ranking mechanism, re-ranks a pond; it cannot surface condition-rich objects
that were never scanned into the corpus to begin with. The re-mine that follows this document
widens `TARGET_MODULES` into condition-richer territory — `Mathlib/Order/`, the basics of
`Mathlib/Algebra/`, the basics of `Mathlib/Combinatorics/`, the shallows of
`Mathlib/NumberTheory/` — in addition to, not instead of, the original five corners. This is
accepted with the known cost that harvest time scales roughly linearly with corpus size (the
round-2 re-harvest over 782 candidates took on the order of 40 minutes; a wider corpus will
take proportionally longer), a cost judged worth paying because no amount of ranking
sophistication compensates for scanning the wrong set of modules in the first place.

## 7 · Retrieval policy (resolved question)

The definition-writer, at generation time, sees the dossier and the pinned signature only — no
retrieval over Mathlib source. Using the ambient Mathlib environment and its vocabulary
(importing `Mathlib`, calling existing lemmas and definitions, writing in the idioms Mathlib
already uses) is the job itself and is fully permitted; the candidate is, after all, meant to
produce a real Mathlib-style definition. What is not permitted is reading off the target
object's *own* source — doing so would collapse a mined task from "write a faithful definition
of the described object" into "locate and copy the declaration this dossier is paraphrasing,"
which is a lookup task, not a definition-writing task, and would certify nothing about the
candidate's ability to formalize.

Weights-memorization of Mathlib by the base model is a separate concern and is unavoidable:
any model trained on a corpus containing Mathlib source has already seen these declarations,
retrieval policy or no. That fact is already priced into how the mined corpus is used — it is
training and development material, not a clean capability measurement. Clean measurement of
whether a system can produce a faithful definition from a description alone belongs to the
held-out fresh-source set (`task.json`'s `heldout` field, `docs/design/task_schema_v1.md`),
where no equivalent of "the answer already exists verbatim in pretraining data" applies in the
same way.

This policy is recorded here, in a document about *selection*, because it bears directly on
which definitions are safe to select. Memorization risk is not uniform across the corpus: it is
strongest for short, famous, heavily-used definitions — precisely the shape of object §1
describes the old ranking as having promoted to the top. The length floor (§3b) and the
richness weighting (§4.1) both push selection away from that shape for their own, independent
reasons (too little content to formalize; too little structure to be wrong about); that they
also happen to push away from the objects most likely to be pure recall is a welcome
consequence of the same fixes, not a third, separate mechanism.

---

## Revision: 22 July 2026 — recalibration after batch 2

Batch 2 (`docs/harvest_review_batch2.md`) ran the gates-and-bands design of record above for
the first time, over a corpus widened per §6. It surfaced two measurement bugs and one
threshold miscalibration severe enough to shrink the eligible set to 52 candidates against a
requested top-100 — well below what §2's "already-acceptable candidates" framing intended. This
section is the second calibration pass the design always expected (§2: "none of them is
expected to be correct on the first attempt"), not a reversal of the architecture. Five changes
follow.

**(a) The raw mention floor is retired, replaced by a theorem-mention floor.** Gate (a) of §3
now reads: *full-corpus theorem mentions ≥ `THEOREM_MENTION_FLOOR`* (initial value: 2), measured
against the count of theorem/lemma *statements* mentioning the name — not, as before, a raw
text-occurrence count. Batch 2's Finding A traced the old floor's 87.5% attrition rate to a
category error: raw mention-count measures *ubiquity*, and ubiquity is systematically lower in
less-central territory almost by construction — the whole point of widening the corpus past the
original five foundational corners was to reach exactly that territory, so a floor tuned against
foundational-corner ubiquity was never going to survive contact with it. But ubiquity was never
actually what gate (a) needed to guarantee; §3's own original rationale said so explicitly ("enough
theorem-statement mentions... to guarantee that global-fact supply and documentation actually
exist," not "to guarantee prominence"). Theorem-mention count measures that requirement directly
instead of through the ubiquity proxy, so the floor can be set low — 2, not 30 — because its only
remaining job is confirming *some* supply exists, the same demotion-from-score-to-minimum logic
§3(a) always used, now applied to a metric that actually measures the thing being demoted to.

**(b) Structural richness gains a floor: `richness ≥ 1` is now a gate, not only a score term.**
Once the richness-counting bug in (e) below is fixed, a richness-zero definition is reliably a
pure delegation or projection — `toFinset l := Multiset.toFinset l`, `Equiv.symm := ...` — the
exact population this whole redesign has targeted since batch 1's `Finset.range`/`Nat.Prime`
finding (§1). The length band (§3b) was supposed to catch this population but demonstrably
doesn't catch all of it: batch 2 included 23 richness-zero candidates (44% of its eligible set)
that cleared the length band comfortably. Richness is a direct measurement of the thing length
only approximates, so it becomes the more precise gate for the same population, while remaining
(above the floor) the dominant preference-score term per §4.1 — a floor and a score term are not
redundant here, the same way the docstring floor (§3c) and docstring substance (§4.2) coexist
without conflict. Because richness's own counting had a real bug at the time of batch 2 (item
(e)), this gate is introduced only once that bug is fixed — gating on a miscounted metric would
have reintroduced exactly the kind of measurement-error-masquerading-as-selection-decision this
whole document exists to prevent. As a blind-spot watch going forward, each batch's review will
enumerate the richness-zero *exclusions* this gate produces with a one-line characterization of
each (pure delegation, projection, or genuinely notation-hidden structure the counter still can't
see) — the last category is the gate's known failure mode, and tracking its rate is how a future
recalibration would be triggered.

**(c) The top-N cutoff is abolished.** The manifest now contains exactly two populations:
*eligible* (passed every gate, ranked by the preference score in full — no cutoff) and *excluded*
(with the specific gate(s) that fired). Baking a batch size into the mining artifact was a
category confusion: how many tasks a downstream consumer wants is a *consumption* decision — made
by whoever draws from the ranked eligible set, at stage-2 slicing or corpus-assembly time, and
potentially different for different consumers of the same manifest — not a property of the
mining artifact itself. Under the old top-N design, a candidate could be gate-eligible and still
excluded for a reason that had nothing to do with it ("ranked 53rd, below top 52") purely because
of how many other candidates happened to also be eligible that batch, a fact §2's original
framing ("no metric can compensate for another... every exclusion records which gate fired") never
actually intended: outranking was never a gate, and it should never have looked like one in the
manifest. There is no "outranked" category anymore. This also resolves the awkwardness batch 2's
own review had to name explicitly (§4 there: "this edge list is empty... nothing was
ranked-and-cut") — a symptom of top-N answering a question the mining stage was never positioned
to answer.

**(d) The common-vocabulary list widens.** Batch 2 (Finding B and its own §5) found genuine
Combinatorics-territory candidates excluded by `dependency_vocabulary` because their natural
dependencies (`Multiset`, `Sym`, `Polynomial`-adjacent machinery for generating functions) simply
weren't on a list tuned against the original five foundational corners. `COMMON_VOCABULARY_MODULES`
now includes `Multiset`, `Sym`, basic `Polynomial`, and a broader `Order`/`Algebra` slice (see
`miner/config.py` for the exact entries this round added). This list is expected to keep growing
empirically, corner by corner, as each widened batch's review reports its `dependency_vocabulary`
exclusions — the same iterate-on-the-manifest workflow §2 established for every other threshold
here, not a one-time correction.

**(e) Two batch-2 measurement bugs, now fixed, cross-referenced here for the record.** First,
the `dependency_vocabulary` gate's false-failure mechanism (batch 2's Finding B): short,
unqualified, lowercase bound-variable tokens surviving in `referenced_constants` (a known noise
source of that extraction — see `miner.verify`'s module docstring) were colliding with unrelated
real Mathlib declarations that happen to share the same short bare name, so a definition's own
local variable names could resolve to an exotic module and fail the gate for a dependency it
never had. `Pairwise` and `Set.Pairwise` — both genuine, richly-mentioned candidates in batch
1 — were batch 2's clearest casualties of this bug. Second, richness's textual `=>`-counting
(batch 2's §5, item 3): `=>` was counted as a conditional/match-arm marker without distinguishing
a genuine pattern-match arm from a `where`-block field assignment or an anonymous-constructor
lambda body, so several `Equiv.*` equivalence-proof definitions (`Equiv.prodAssoc`,
`Equiv.Set.univ`, `Equiv.sumCongr`, `Equiv.swap`, among batch 2's own top 10) scored artificially
high on richness for structure that had nothing to do with their actual mathematical content.
Both are infrastructure fixes to existing measurements, not new design decisions, and are
implemented — not merely diagnosed — in the round that carries this revision.
