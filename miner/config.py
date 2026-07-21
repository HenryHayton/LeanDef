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


# --- Gate thresholds (design doc §3) ---

# (a) Full-corpus mention floor. Applied against `mention_count` (the raw full-Mathlib-tree
# text-occurrence count computed by `miner.harvest.compute_mention_counts` via `grep -r` over
# the whole `mathlib_root`, independent of `TARGET_MODULES` scope) rather than
# `theorem_mention_count` (which is scoped only to the scanned corpus, per that field's own
# docstring, and is *not* "full-corpus" in the sense this gate needs). On the batch-1 data,
# `mention_count < 30` alone excludes 89.5% of verified candidates -- flagged, not tuned away,
# per this task's instruction to report pathological attrition and let it stand for a human to
# read and adjust.
MENTION_FLOOR = 30

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
# (`VerifiedDef.referenced_constants`) must all resolve -- via `miner.depindex`'s best-effort
# name -> defining-module index over the full Mathlib tree -- to a module path starting with
# one of these prefixes. Deliberately directory-level prefixes, not an exhaustive file list,
# to keep this list itself small and auditable; a reference that resolves to no known module
# (almost always textual noise from `referenced_constants`' own known limitation -- local
# bound variables like `x`, `a_1` slipping through, see miner.verify's module docstring) does
# not count against a candidate, since the gate's purpose is to catch exotic *infrastructure*,
# not to penalize the extraction step's noise.
COMMON_VOCABULARY_MODULES: list[str] = [
    "Data/Nat",
    "Data/Int",
    "Data/List",
    "Data/Finset",
    "Data/Set",
    "Data/Multiset",
    "Data/Option",
    "Data/Prod",
    "Data/Sigma",
    "Data/Bool",
    "Data/Fin",
    "Logic",
    "Order",
    "Algebra/Group",
    "Algebra/Order",
    "Algebra/Ring",
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
