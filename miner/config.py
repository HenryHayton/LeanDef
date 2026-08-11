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

# --- Batch 5 "full-math widening" (9 Aug 2026) ---------------------------------------------
#
# Tranche A: the large majority of mathematical Mathlib, as whole top-level subtrees. This
# REPLACES the batch-1..4 entry list wholesale -- every prior entry was a corner of one of
# these subtrees (Data/Nat under Data, Algebra/Ring/* under Algebra, Topology/Order/* under
# Topology, ...), and keeping both granularities would double-scan those files exactly as the
# batch-4 note that used to sit above the old Order/Combinatorics entries warned. The batch-4
# manifest is the archived record of the old scope; git history holds the old list.
#
# Geometry is entered per-subdirectory because Geometry/Manifold is tranche-B deferred; the
# pin has no loose Geometry/*.lean files (checked 9 Aug 2026), so the subdirectory list IS the
# subtree minus Manifold.
TARGET_MODULES: list[str] = [
    "Algebra",
    "Analysis",
    "Combinatorics",
    "Computability",
    "Control",
    "Data",
    "Dynamics",
    "FieldTheory",
    "Geometry/Convex",
    "Geometry/Diffeology",
    "Geometry/Euclidean",
    "Geometry/Group",
    "Geometry/Polygon",
    "Geometry/RingedSpace",
    "GroupTheory",
    "InformationTheory",
    "LinearAlgebra",
    "Logic",
    "ModelTheory",
    "NumberTheory",
    "Order",
    "RingTheory",
    "SetTheory",
    "Topology",
]

# Excluded PERMANENTLY (infrastructure/meta, not mathematics -- one-line reason each):
#   Tactic      -- tactic implementations; no mathematical objects to mine
#   Util        -- build/CI/doc tooling
#   Lean        -- compiler/meta-level bindings
#   Testing     -- test scaffolding (slim profile checks etc.)
#   Deprecated  -- retired declarations kept for migration; mining them would select dead names
# (No `Init` directory exists at this pin -- checked 9 Aug 2026.)
#
# DEFERRED, tranche B (do not scan this batch; trigger recorded in docs/deferred.md):
#   CategoryTheory, AlgebraicGeometry, AlgebraicTopology, Condensed, RepresentationTheory,
#   MeasureTheory, Probability, Geometry/Manifold
# Reason: expected near-total attrition at the dependency-vocabulary / self-containment gates
# (heavy abstract infrastructure; dossiers not self-containable at current depth standards).
# Trigger to revisit: eligible pool still short of target after vocabulary round 2, or a strata
# need only this territory supplies (e.g. the MeasurableSet predicate layer).

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
    "Algebra/Polynomial",    # --- Batch 5 round 1 (9 Aug 2026): conservative seeds for the widened territory, per
    # area; every directory existence-checked at the pin. Round 2 grows from the review's
    # grouped exclusion evidence, not guesswork. Deliberately NOT added in round 1:
    # Real/NNReal/ENNReAL, Filter beyond what Order carries, and all topology vocabulary --
    # the exclusion tables must argue for those.
    "Data/Rat",             # rationals as common vocabulary alongside Nat/Int
    "Data/Fintype",         # finiteness typeclass -- ubiquitous hypothesis vocabulary
    "Data/ZMod",            # modular arithmetic carrier
    "Data/Vector",          # fixed-length vectors
    "Data/Array",           # array primitives (Computability/Control territory)
    "Data/PNat",            # positive naturals
    "Data/Sum",             # sum types (Prod/Option/Sigma already present)
    "Data/Matrix",          # matrix basics -- LinearAlgebra territory's natural carrier
    "GroupTheory/Perm",     # Equiv.Perm basics
    "GroupTheory/Subgroup", # subgroup lattice vocabulary
    "RingTheory/Ideal",     # ideal basics
    "Algebra/GCDMonoid",    # divisibility/gcd vocabulary
    # --- Batch 5 round 2 (11 Aug 2026): EVIDENCE-DRIVEN, from the round-1 exclusion table.
    # Every entry below was the sole gate failing for a named block of definitions; the count is
    # blocked references observed, and the test for inclusion was the brief's: would a dossier
    # using this vocabulary still be writable to the depth standard, self-contained?
    "Analysis/Normed",          # 538 refs -- normed spaces (ZSpan.fundamentalDomain, ZLattice.covolume).
                                # The boldest entry: it transitively admits Real. Kept because "V is a
                                # normed space, ‖·‖ its norm" is one dossier sentence, not an edifice.
    "Algebra/Module",           # 365 -- modules over a ring; the natural successor to Group/Ring/Field
    "Algebra/Algebra",          # 243 -- R-algebras (AlgEquiv.piCongrLeft, AlgEquiv.prodCongr)
    "Topology/Defs",            # 261 -- IsOpen/IsClosed/Continuous, the basic topological vocabulary
    "Computability/Partrec",    # 124 -- partial recursive functions; Computability is a scanned area
    "Topology/MetricSpace",     #  55 -- metric spaces; standard vocabulary, self-contained in a line
    "Combinatorics/SimpleGraph",#  46 -- simple graphs (SimpleGraph.mulCayley, adjMatrix)
    "Data/Seq",                 #  45 -- sequences/streams (GenContFract.squashSeq, Stream'.Seq1.map)
    "LinearAlgebra/Matrix",     #  45 -- matrix basics (Matrix.gram, Matrix.compl)
    #
    # Deliberately REJECTED despite high reference counts -- these are the heavy abstract
    # infrastructure the gate exists to catch, and are tranche-B in character:
    #   Algebra/Homology (501), CategoryTheory/* (375), Algebra/Category (193),
    #   AlgebraicTopology/* (156), AlgebraicGeometry/* (115), Algebra/Lie (81), Data/QPF (46).
    # A dossier for an object over chain complexes or a subfunctor is not self-containable at the
    # current depth standard, which is precisely what tranche B defers.
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

# --- Tier-2 discharge measurement (batch 4 "wide mine", new 22 July 2026) ---
# `miner.discharge`: for each eligible definition with theorem_mention_count >= 1, sample up
# to DISCHARGE_SAMPLE_SIZE of its mentioning theorem statements and attempt each with this
# deterministic tactic ladder, in order, stopping at the first success. A measurement, not a
# gate -- nothing here excludes a candidate or changes its score (see miner.discharge's module
# docstring). Order matters: cheapest/most-specific first (rfl, omega -- fast, narrow), then
# broader automation (simp), then the two search-based tactics (exact?, aesop) last, since
# they're the most expensive and most likely to find something the earlier tactics can't.
TACTIC_LADDER: list[str] = ["rfl", "omega", "simp", "exact?", "aesop"]

# Per-attempt budget. Task instructions suggested 30s; revised down after the batch-4 run
# itself: statements extracted standalone (outside their original file's context -- see
# `miner.discharge.attempt_statement`'s docstring) routinely fail to elaborate as a goal at
# all, and `exact?`/`aesop` genuinely search rather than failing fast when a goal *does*
# elaborate but the ladder can't close it -- at 30s/attempt this made the full 727-definition,
# ~2,000-statement measurement run past 7 hours without finishing. 8s keeps real successes and
# fast failures (the overwhelming majority) essentially unaffected while bounding the worst
# case for a genuinely slow search to a third of what it was. See
# DISCHARGE_MAX_WALL_CLOCK_S below for the second half of the fix: a hard cap so a slow corpus
# can't turn an "overnight run" into an unbounded one regardless of this value.
DISCHARGE_TACTIC_TIMEOUT = 8.0

# How many mentioning statements to sample per definition (task instructions: "up to 3").
DISCHARGE_SAMPLE_SIZE = 3

# Overall wall-clock budget for one full discharge-measurement run (new after the batch-4
# run's own 7+-hour, still-incomplete first attempt at DISCHARGE_TACTIC_TIMEOUT=30.0):
# `miner.discharge.measure_discharge` stops after completing whichever definition is in
# progress when this elapses, rather than continuing indefinitely -- guarantees an overnight
# run terminates with a usable (possibly partial) manifest. 8 hours: a full overnight window.
DISCHARGE_MAX_WALL_CLOCK_S = 8 * 60 * 60.0
