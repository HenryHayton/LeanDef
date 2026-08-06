# Corpus finding: every mining gate selects against characterization-style definitions (2026-08-07)

Surfaced while sourcing few-shot exemplars for the Formalizer prompt. This is a **corpus
finding**, not an exemplar footnote: it describes what the mining pipeline systematically
removes before any human or model ever sees the pool.

## Measurement

Of the **680** eligible definitions outside the current 41 tasks, only **16 (2.4%)** are
characterization-flavoured — bodies naming `sInf`/`sSup`/`⨅`/`⨆`/`Classical.*`/`.choose`/
`Nat.find`. Of those 16, only **3** clear the exemplar filter's 60-character body floor.

The survivors and their body lengths make the shape of the problem obvious:

| body | chars |
|---|--:|
| `sInf { a \| ∀ᶠ n in f, n ≤ a }` (`Filter.limsSup`) | 29 |
| `sInf { a \| ∀ᶠ x in f, p x → u x ≤ a }` (`Filter.blimsup`) | 37 |
| `Nat.find <| μ.exists_notMem_row i` (`YoungDiagram.rowLen`) | 33 |
| `sInf { a \| f a ≤ a }` (`OrderHom.lfp`) | ~20 |

## Two independent gates, same casualty

**The length floor.** A floor exists to exclude *delegation-thinness* — bodies that are short
because they hand the work to one library function. But a characterization is short **because a
characterization is compact**: `sInf { a | ∀ᶠ n in f, n ≤ a }` states the entire mathematical
content in 29 characters. The floor cannot distinguish "short because it delegates" from "short
because it characterizes", and silently discards the second.

**The richness counter.** `richness` counts conditionals, quantifiers, connectives and
comparisons at the top level of the body. In a characterization the logical structure lives
**inside the set-builder**, where the counter cannot see it: `sInf { a | ∀ᶠ n in f, n ≤ a }`
contains a quantifier and a relation, and scores as though it contained neither. `OrderHom.lfp`
— the canonical Knaster–Tarski least fixed point, arguably the purest characterization in
Mathlib — scores `richness_total = 1`.

So the two gates fail **independently and in the same direction**. Passing either does not
rescue a definition from the other.

## Why this matters beyond the exemplar exercise

This is the **mining-side twin of the scoring-side bias** recorded in the 2026-08-07
pre-registration amendment. There, the decide-mechanism component turned out to be a
16-of-41-task instrument that cannot evaluate noncomputable candidates at all (their `decide`
facts are correctly UNKNOWN), so a definition-by-characterization goes unscored while an
algorithm-by-reduction scores cleanly.

The pattern is the same at both ends of the pipeline: **infrastructure built around computable
arithmetic quietly deletes characterization-shaped mathematics at every gate that does not
explicitly account for it.** Mining removes it from the pool; scoring cannot measure it if it
survives. Neither gate was designed to do this and neither records that it did.

Observed downstream in the prelim run, the same asymmetry appears in model outputs: for
`Nat.clog`, one model produced `sInf {k : ℕ | n ≤ b^k}` — the honest characterization — and was
penalized with UNKNOWN coverage, while another produced a wrapper around the existing `Nat.log`
primitive and scored cleanly.

## Recorded requirement on the pilot-100 selection spec (not built now)

The pilot-100 selection must carry a **characterization stratum with shape-aware gates**:

- the length floor is **waived** for characterization-flavoured bodies (detected by the marker
  set above), since the floor's stated purpose — excluding delegation-thinness — does not apply
  to them;
- **richness is assessed on the set-builder's internal structure**, not only at the top level,
  so `{ a | ∀ᶠ n in f, n ≤ a }` is scored for the quantifier and relation it actually contains.

Without both, the pilot-100 will reproduce the current corpus's composition — short famous
computable definitions — and the verifier will continue to have almost nothing to say about the
class of objects that admit no algorithm.

## Precedent recorded

The slot-3 floor exception adopted for `Filter.limsSup` is the first instance of a **per-slot
filter exception**. It was approved on the reasoning that it *corrects a measured misfire of a
rule against that rule's own stated purpose*, rather than bending the contract — and on the
condition that such exceptions are surfaced for decision rather than adopted silently. That is
the standing precedent for filter exceptions generally.
