"""Miner configuration.

`TARGET_MODULES` is the config list of Mathlib corners scanned by the harvest -- easily
widened later, not a structural limit of the scanner. Everything else here is a named
threshold for the gates-then-preference-score selection design (see
`docs/design/definition_selection_2026-07-21.md`), each one a dial expected to be re-tuned
after reading a harvest's gate-attrition report, not a value fixed for all time.
"""

from pathlib import Path

from harness import config as harness_cfg

MATHLIB_ROOT = harness_cfg.LEAN_PROJECT_DIR / ".lake" / "packages" / "mathlib" / "Mathlib"

TARGET_MODULES: list[str] = [
    # Original five corners (miner stage 1 / harvest batch 1).
    "Data/Nat",
    "Data/List",
    "Data/Finset",
    "Data/Int",
    "Logic",
    # Widened for batch 2 (design doc §6): condition-richer territory beyond the
    # foundational corners, deliberately kept to "basics"/"shallows" scope -- individual
    # Defs/Basic files and small subdirectories, not whole (100+-file) subtrees -- to bound
    # harvest cost. 69 files, 182 scanned `def` hits confirmed by a dry scan before the full
    # harvest ran; see the batch-2 review doc's corpus-scope section for the count and the
    # per-area file list this comment summarizes.
    "Order/Basic.lean",
    "Order/Defs",
    "Order/Bounds",
    "Order/BoundedOrder",
    "Order/Monotone",
    "Order/Lattice.lean",
    "Order/Directed.lean",
    "Order/Disjoint.lean",
    "Order/RelClasses.lean",
    "Order/SetNotation.lean",
    "Order/SymmDiff.lean",
    "Order/Antisymmetrization.lean",
    "Order/Cover.lean",
    "Algebra/Group/Defs.lean",
    "Algebra/Group/Basic.lean",
    "Algebra/Ring/Defs.lean",
    "Algebra/Ring/Basic.lean",
    "Algebra/GroupWithZero/Defs.lean",
    "Algebra/GroupWithZero/Basic.lean",
    "Algebra/Field/Basic.lean",
    "Algebra/Order/Monoid/Defs.lean",
    "Algebra/Order/Ring/Defs.lean",
    "Algebra/Order/Group/Defs.lean",
    "Combinatorics/Pigeonhole.lean",
    "Combinatorics/Colex.lean",
    "Combinatorics/Derangements",
    "Combinatorics/Enumerative/Bell.lean",
    "Combinatorics/Enumerative/Catalan.lean",
    "Combinatorics/Enumerative/Composition.lean",
    "Combinatorics/Enumerative/DoubleCounting.lean",
    "Combinatorics/Enumerative/Stirling.lean",
    "Combinatorics/Enumerative/Pentagonal.lean",
    "Combinatorics/Enumerative/DyckWord.lean",
    "Combinatorics/Enumerative/Schroder.lean",
    "NumberTheory/Basic.lean",
    "NumberTheory/Divisors.lean",
    "NumberTheory/Fermat.lean",
    "NumberTheory/FermatPsp.lean",
    "NumberTheory/LucasLehmer.lean",
    "NumberTheory/LucasPrimality.lean",
    "NumberTheory/Bertrand.lean",
    "NumberTheory/AlmostPrime.lean",
    "NumberTheory/Multiplicity.lean",
    "NumberTheory/Wilson.lean",
    "NumberTheory/ArithmeticFunction",
]


def target_dirs(mathlib_root: Path | None = None) -> list[Path]:
    mathlib_root = mathlib_root if mathlib_root is not None else MATHLIB_ROOT
    return [mathlib_root / m for m in TARGET_MODULES]


# --- Gate thresholds (design doc §3, recalibrated 22 July 2026 after batch 2) ---

# (a) Full-corpus THEOREM-mention floor (recalibrated 22 July 2026 -- see the design doc's
# "Revision: 22 July 2026" section for the full rationale). Retires the raw mention-count
# floor: raw `mention_count` measures ubiquity, not the actual requirement (global-fact
# supply), and batch 2 showed a floor tuned against the foundational corners' ubiquity
# excludes 87.5% of a corpus deliberately widened into less-central territory (batch 2's
# Finding A). `theorem_mention_count` (full-corpus, scanned once over all of Mathlib by
# `miner.harvest.compute_theorem_mention_counts`) measures supply directly, so the floor can
# be set low -- its only remaining job is confirming *some* supply exists, not selecting for
# prominence. `mention_count` (the old raw metric) is retained as recorded metadata on
# `VerifiedDef` only; nothing gates on it anymore.
THEOREM_MENTION_FLOOR = 2

# (b) Length band on the normalized definition body (see `miner.gates.normalize_body` for the
# exact normalization: comments stripped, whitespace collapsed). Chosen by inspecting the
# batch-1 length distribution (768 elaborating candidates): LENGTH_MIN=40 excludes exactly the
# cluster of one-line delegations/renames at the bottom of the distribution (9 candidates,
# 1.2% -- `Int.pred`/`Int.succ` at 25 chars, `Cycle.nil`/`Denumerable.pair`/`Nat.Prime` at 34,
# `Nat.dist` at 37, `Nat.gcdA`/`Nat.gcdB` at 38 -- confirming `Nat.Prime := Irreducible p`
# fails the floor as required) while keeping short-but-genuinely-structured predicates just
# above it (`Relator.LeftTotal` at 39, `Nat.ModEq`/`Int.ModEq` at 42). LENGTH_MAX=500 excludes
# 24 candidates (3.1%, just past the p97 mark of 514) -- the "top few percent" the task asked
# for, catching the handful of very large multi-case/heavily-binder definitions without
# touching the bulk of the distribution (median 123, p90 306).
LENGTH_MIN = 40
LENGTH_MAX = 500

# (c) Docstring floor: minimum normalized-docstring length to count as "exists and exceeds a
# trivial length" (design §3c). A dial, not a measurement -- 20 characters is enough to rule
# out a docstring that's just the bare name restated, not enough to demand real prose.
DOCSTRING_MIN_LENGTH = 20

# (d) Dependency vocabulary tier (design §3d): a candidate's direct references
# (`VerifiedDef.referenced_constants`, filtered per `miner.gates._looks_like_bound_variable` --
# see that function's docstring for batch 2's Finding B and its fix) must all resolve -- via
# `miner.depindex`'s best-effort name -> defining-module index over the full Mathlib tree --
# to a module path starting with one of these prefixes. Deliberately directory-level prefixes,
# not an exhaustive file list, to keep this list itself small and auditable; a reference that
# resolves to no known module does not count against a candidate, since the gate's purpose is
# to catch exotic *infrastructure*, not to penalize the extraction step's noise.
#
# Widened 22 July 2026 (design doc revision, item (d)): added `Data/Sym`, `Algebra/Polynomial`,
# `Algebra/BigOperators`, `Algebra/GroupWithZero`, `Algebra/Field` -- batch 2 showed genuine
# Combinatorics-territory candidates dying on `dependency_vocabulary` because their natural
# dependencies (symmetric-power types, generating-function polynomials, big-operator sums)
# simply weren't on a list tuned against the original five foundational corners. Expected to
# keep growing empirically, corner by corner, as each batch's review reports this gate's
# exclusions -- not a one-time correction.
COMMON_VOCABULARY_MODULES: list[str] = [
    "Data/Nat",
    "Data/Int",
    "Data/List",
    "Data/Finset",
    "Data/Set",
    "Data/Multiset",
    "Data/Sym",
    "Data/Option",
    "Data/Prod",
    "Data/Sigma",
    "Data/Bool",
    "Data/Fin",
    "Logic",
    "Order",
    "Algebra/Group",
    "Algebra/GroupWithZero",
    "Algebra/Order",
    "Algebra/Ring",
    "Algebra/Field",
    "Algebra/BigOperators",
    "Algebra/Polynomial",
]

# (e) Anti-plumbing name patterns (design §3e): a candidate whose bare name (last dotted
# component) matches any of these is excluded as an engineering artifact with no independent
# mathematical identity. Each entry is a compiled-at-use regex string, matched against the
# bare name only (not the full dotted path) so e.g. `Nat.digitsAux1` is tested as
# `digitsAux1`. Curation (`miner/curation.yaml`) remains for judgment calls the patterns can't
# mechanize -- this list is deliberately narrow and mechanical.
ANTI_PLUMBING_PATTERNS: list[str] = [
    r"(?i)aux\d*$",  # e.g. digitsAux1, fooAux2 -- internal auxiliary helper
    r"(?i)^aux",  # e.g. auxHelper
    r"Impl$",  # e.g. FooImpl
    r"(?:^|\.)go$",  # e.g. Nat.log.go -- where-clause fuel-recursion helper
    r"TR$",  # e.g. List.iterateTR -- tail-recursive variant of a named def
    r"(?i)decEq$",  # e.g. instDecidableEqFoo, fooDecEq -- decidable-equality machinery
    r"(?i)beq$",  # e.g. fooBeq, instBEqFoo -- boolean-equality machinery
]

# (g) Richness floor (new 22 July 2026, design doc revision item (b)): `richness_total >= this`
# is now a hard gate, not only the dominant preference-score term (design §4.1). Introduced
# only once `miner.richness`'s `=>`/`:=` counting bug (batch 2's §5 item 3) was fixed --
# gating on a miscounted metric would have reintroduced exactly the kind of
# measurement-error-masquerading-as-selection-decision the whole design exists to prevent.
# Set to the lowest possible value (1) since its job is only to catch the richness-zero
# population (pure delegations/projections) the length band demonstrably misses -- batch 2
# included 23 richness-zero candidates (44% of its eligible set) despite the length band.
RICHNESS_FLOOR = 1
