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
    #
    # NOTE (batch 4 "wide mine"): the batch-2 Order/* and Combinatorics/* entries that used
    # to live here are gone -- not dropped, *subsumed* -- now that "Order" and "Combinatorics"
    # below scan those same subtrees in full. Keeping both would double-scan every file in
    # them (two ScanHit lists for the same declarations), so the narrower entries were removed
    # rather than left redundant. `Algebra/GroupWithZero/*` and `Algebra/Order/*` are
    # untouched -- outside batch 4's requested Algebra scope, unrelated to the change below.
    "Algebra/GroupWithZero/Defs.lean",
    "Algebra/GroupWithZero/Basic.lean",
    "Algebra/Order/Monoid/Defs.lean",
    "Algebra/Order/Ring/Defs.lean",
    "Algebra/Order/Group/Defs.lean",
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
    # --- Batch 4 "wide mine" (22 July 2026): corpus expansion for composition statistics.
    # Measurement-purpose mine -- selection machinery is unchanged, only corpus scope grows.
    # See docs/harvest_review_batch4.md for the dry-scan breakdown and the report's own note
    # on `Algebra/GroupPower` (requested but does not exist in this Mathlib version -- skipped,
    # not substituted) and the `Logic/Relation`+`Logic/Function` request (already fully covered
    # by the bare "Logic" entry above -- a no-op, not re-added).
    "Order",  # full subtree (was 13 individual batch-2 entries above)
    "Combinatorics",  # full subtree (was 11 individual batch-2 entries above)
    "Algebra/Group/AddChar.lean",
    "Algebra/Group/Basic.lean",
    "Algebra/Group/Center.lean",
    "Algebra/Group/Commutator.lean",
    "Algebra/Group/Conj.lean",
    "Algebra/Group/ConjFinite.lean",
    "Algebra/Group/Defs.lean",
    "Algebra/Group/Embedding.lean",
    "Algebra/Group/End.lean",
    "Algebra/Group/Even.lean",
    "Algebra/Group/EvenFunction.lean",
    "Algebra/Group/Ext.lean",
    "Algebra/Group/Finsupp.lean",
    "Algebra/Group/ForwardDiff.lean",
    "Algebra/Group/Graph.lean",
    "Algebra/Group/Ideal.lean",
    "Algebra/Group/Idempotent.lean",
    "Algebra/Group/Indicator.lean",
    "Algebra/Group/InjSurj.lean",
    "Algebra/Group/MinimalAxioms.lean",
    "Algebra/Group/ModEq.lean",
    "Algebra/Group/NatPowAssoc.lean",
    "Algebra/Group/Opposite.lean",
    "Algebra/Group/PNatPowAssoc.lean",
    "Algebra/Group/PUnit.lean",
    "Algebra/Group/Prod.lean",
    "Algebra/Group/Shrink.lean",
    "Algebra/Group/Support.lean",
    "Algebra/Group/Torsion.lean",
    "Algebra/Group/TransferInstance.lean",
    "Algebra/Group/Translate.lean",
    "Algebra/Group/ULift.lean",
    "Algebra/Ring/AddAut.lean",
    "Algebra/Ring/Associated.lean",
    "Algebra/Ring/Associator.lean",
    "Algebra/Ring/Aut.lean",
    "Algebra/Ring/Basic.lean",
    "Algebra/Ring/BooleanRing.lean",
    "Algebra/Ring/Center.lean",
    "Algebra/Ring/Centralizer.lean",
    "Algebra/Ring/CentroidHom.lean",
    "Algebra/Ring/CharZero.lean",
    "Algebra/Ring/Commute.lean",
    "Algebra/Ring/CompTypeclasses.lean",
    "Algebra/Ring/Defs.lean",
    "Algebra/Ring/Equiv.lean",
    "Algebra/Ring/Ext.lean",
    "Algebra/Ring/Fin.lean",
    "Algebra/Ring/GeomSum.lean",
    "Algebra/Ring/GrindInstances.lean",
    "Algebra/Ring/Idempotent.lean",
    "Algebra/Ring/Identities.lean",
    "Algebra/Ring/InjSurj.lean",
    "Algebra/Ring/Invertible.lean",
    "Algebra/Ring/IsFormallyReal.lean",
    "Algebra/Ring/MinimalAxioms.lean",
    "Algebra/Ring/Nat.lean",
    "Algebra/Ring/NegOnePow.lean",
    "Algebra/Ring/NonZeroDivisors.lean",
    "Algebra/Ring/Opposite.lean",
    "Algebra/Ring/PUnit.lean",
    "Algebra/Ring/Parity.lean",
    "Algebra/Ring/Periodic.lean",
    "Algebra/Ring/Pi.lean",
    "Algebra/Ring/Prod.lean",
    "Algebra/Ring/Rat.lean",
    "Algebra/Ring/Regular.lean",
    "Algebra/Ring/Semiconj.lean",
    "Algebra/Ring/Shrink.lean",
    "Algebra/Ring/Subgroup.lean",
    "Algebra/Ring/SumsOfSquares.lean",
    "Algebra/Ring/Torsion.lean",
    "Algebra/Ring/TransferInstance.lean",
    "Algebra/Ring/ULift.lean",
    "Algebra/Ring/Units.lean",
    "Algebra/Ring/WithZero.lean",
    "Algebra/Field/Basic.lean",
    "Algebra/Field/Defs.lean",
    "Algebra/Field/Equiv.lean",
    "Algebra/Field/GeomSum.lean",
    "Algebra/Field/IsField.lean",
    "Algebra/Field/MinimalAxioms.lean",
    "Algebra/Field/ModEq.lean",
    "Algebra/Field/NegOnePow.lean",
    "Algebra/Field/Opposite.lean",
    "Algebra/Field/Periodic.lean",
    "Algebra/Field/Power.lean",
    "Algebra/Field/Rat.lean",
    "Algebra/Field/Shrink.lean",
    "Algebra/Field/TransferInstance.lean",
    "Algebra/Field/ULift.lean",
    "Algebra/Field/ZMod.lean",
    "Algebra/BigOperators/Associated.lean",
    "Algebra/BigOperators/Balance.lean",
    "Algebra/BigOperators/Expect.lean",
    "Algebra/BigOperators/Field.lean",
    "Algebra/BigOperators/Fin.lean",
    "Algebra/BigOperators/Finprod.lean",
    "Algebra/BigOperators/Intervals.lean",
    "Algebra/BigOperators/ModEq.lean",
    "Algebra/BigOperators/Module.lean",
    "Algebra/BigOperators/NatAntidiagonal.lean",
    "Algebra/BigOperators/Option.lean",
    "Algebra/BigOperators/Pi.lean",
    "Algebra/BigOperators/RingEquiv.lean",
    "Algebra/BigOperators/Sym.lean",
    "Algebra/BigOperators/WithTop.lean",
    "Algebra/Module/Basic.lean",
    "Algebra/Module/BigOperators.lean",
    "Algebra/Module/Bimodule.lean",
    "Algebra/Module/Card.lean",
    "Algebra/Module/CharacterModule.lean",
    "Algebra/Module/DedekindDomain.lean",
    "Algebra/Module/Defs.lean",
    "Algebra/Module/End.lean",
    "Algebra/Module/FinitePresentation.lean",
    "Algebra/Module/GradedModule.lean",
    "Algebra/Module/Hom.lean",
    "Algebra/Module/Injective.lean",
    "Algebra/Module/Lattice.lean",
    "Algebra/Module/MinimalAxioms.lean",
    "Algebra/Module/NatInt.lean",
    "Algebra/Module/Opposite.lean",
    "Algebra/Module/PID.lean",
    "Algebra/Module/PUnit.lean",
    "Algebra/Module/Pi.lean",
    "Algebra/Module/PointwisePi.lean",
    "Algebra/Module/Prod.lean",
    "Algebra/Module/Projective.lean",
    "Algebra/Module/Rat.lean",
    "Algebra/Module/RingHom.lean",
    "Algebra/Module/Shrink.lean",
    "Algebra/Module/SnakeLemma.lean",
    "Algebra/Module/SpanRank.lean",
    "Algebra/Module/SpanRankOperations.lean",
    "Algebra/Module/TransferInstance.lean",
    "Algebra/Module/ULift.lean",
    "Algebra/Module/ZMod.lean",
    "NumberTheory/Primorial.lean",
    "NumberTheory/Padics/AddChar.lean",
    "NumberTheory/Padics/Complex.lean",
    "NumberTheory/Padics/HeightOneSpectrum.lean",
    "NumberTheory/Padics/Hensel.lean",
    "NumberTheory/Padics/MahlerBasis.lean",
    "NumberTheory/Padics/PadicIntegers.lean",
    "NumberTheory/Padics/PadicNorm.lean",
    "NumberTheory/Padics/PadicNumbers.lean",
    "NumberTheory/Padics/ProperSpace.lean",
    "NumberTheory/Padics/RingHoms.lean",
    "NumberTheory/Padics/ValuativeRel.lean",
    "NumberTheory/Padics/WithVal.lean",
    "Topology/Basic.lean",
    "Topology/Order/AtTopBotIxx.lean",
    "Topology/Order/Basic.lean",
    "Topology/Order/Bornology.lean",
    "Topology/Order/Compact.lean",
    "Topology/Order/Completion.lean",
    "Topology/Order/CountableSeparating.lean",
    "Topology/Order/DenselyOrdered.lean",
    "Topology/Order/ExtendFrom.lean",
    "Topology/Order/ExtrClosure.lean",
    "Topology/Order/Filter.lean",
    "Topology/Order/HullKernel.lean",
    "Topology/Order/IntermediateValue.lean",
    "Topology/Order/IsLUB.lean",
    "Topology/Order/IsLocallyClosed.lean",
    "Topology/Order/IsNormal.lean",
    "Topology/Order/Lattice.lean",
    "Topology/Order/LawsonTopology.lean",
    "Topology/Order/LeftRight.lean",
    "Topology/Order/LeftRightLim.lean",
    "Topology/Order/LeftRightNhds.lean",
    "Topology/Order/LiminfLimsup.lean",
    "Topology/Order/LocalExtr.lean",
    "Topology/Order/LowerUpperTopology.lean",
    "Topology/Order/Monotone.lean",
    "Topology/Order/MonotoneContinuity.lean",
    "Topology/Order/MonotoneConvergence.lean",
    "Topology/Order/NhdsSet.lean",
    "Topology/Order/OrderClosed.lean",
    "Topology/Order/OrderClosedExtr.lean",
    "Topology/Order/PartialSups.lean",
    "Topology/Order/Priestley.lean",
    "Topology/Order/ProjIcc.lean",
    "Topology/Order/Real.lean",
    "Topology/Order/Rolle.lean",
    "Topology/Order/ScottTopology.lean",
    "Topology/Order/SuccPred.lean",
    "Topology/Order/T5.lean",
    "Topology/Order/UpperLowerSetTopology.lean",
    "Topology/Order/WithTop.lean",
    "Topology/Separation",  # full (flat) dir -- Hausdorff/regular/normal-type separation axioms
    "Topology/Connected",  # full (flat) dir
    "Topology/Compactness",  # full (flat) dir -- "compactness-related files" read as this directory
    "Analysis/SpecialFunctions/Arcosh.lean",
    "Analysis/SpecialFunctions/ArithmeticGeometricMean.lean",
    "Analysis/SpecialFunctions/Arsinh.lean",
    "Analysis/SpecialFunctions/Artanh.lean",
    "Analysis/SpecialFunctions/Bernstein.lean",
    "Analysis/SpecialFunctions/BinaryEntropy.lean",
    "Analysis/SpecialFunctions/Choose.lean",
    "Analysis/SpecialFunctions/CompareExp.lean",
    "Analysis/SpecialFunctions/Exp.lean",
    "Analysis/SpecialFunctions/ExpDeriv.lean",
    "Analysis/SpecialFunctions/Exponential.lean",
    "Analysis/SpecialFunctions/ImproperIntegrals.lean",
    "Analysis/SpecialFunctions/JapaneseBracket.lean",
    "Analysis/SpecialFunctions/MulExpNegMulSq.lean",
    "Analysis/SpecialFunctions/MulExpNegMulSqIntegral.lean",
    "Analysis/SpecialFunctions/NonIntegrable.lean",
    "Analysis/SpecialFunctions/OrdinaryHypergeometric.lean",
    "Analysis/SpecialFunctions/Pochhammer.lean",
    "Analysis/SpecialFunctions/PolarCoord.lean",
    "Analysis/SpecialFunctions/PolynomialExp.lean",
    "Analysis/SpecialFunctions/Sigmoid.lean",
    "Analysis/SpecialFunctions/SmoothTransition.lean",
    "Analysis/SpecialFunctions/Sqrt.lean",
    "Analysis/SpecialFunctions/Stirling.lean",
    "Dynamics",  # full subtree
    # "Data/Set/ core": read as top-level files only (excludes the Card/, Finite/, Lattice/,
    # Pairwise/, Pointwise/ subdirectories -- deeper, more specialized machinery than "core"
    # suggests; a judgment call, flagged in the batch-4 report).
    "Data/Set/Accumulate.lean",
    "Data/Set/Basic.lean",
    "Data/Set/BoolIndicator.lean",
    "Data/Set/BooleanAlgebra.lean",
    "Data/Set/Card.lean",
    "Data/Set/CoeSort.lean",
    "Data/Set/Constructions.lean",
    "Data/Set/Countable.lean",
    "Data/Set/Defs.lean",
    "Data/Set/Disjoint.lean",
    "Data/Set/Dissipate.lean",
    "Data/Set/Enumerate.lean",
    "Data/Set/Equitable.lean",
    "Data/Set/FiniteExhaustion.lean",
    "Data/Set/Function.lean",
    "Data/Set/Functor.lean",
    "Data/Set/Image.lean",
    "Data/Set/Inclusion.lean",
    "Data/Set/Insert.lean",
    "Data/Set/Lattice.lean",
    "Data/Set/List.lean",
    "Data/Set/MemPartition.lean",
    "Data/Set/Monotone.lean",
    "Data/Set/MulAntidiagonal.lean",
    "Data/Set/NAry.lean",
    "Data/Set/Notation.lean",
    "Data/Set/Operations.lean",
    "Data/Set/Opposite.lean",
    "Data/Set/Order.lean",
    "Data/Set/Piecewise.lean",
    "Data/Set/PowersetCard.lean",
    "Data/Set/Prod.lean",
    "Data/Set/Restrict.lean",
    "Data/Set/SMulAntidiagonal.lean",
    "Data/Set/Semiring.lean",
    "Data/Set/Sigma.lean",
    "Data/Set/Subset.lean",
    "Data/Set/Subsingleton.lean",
    "Data/Set/Sups.lean",
    "Data/Set/SymmDiff.lean",
    "Data/Set/UnionLift.lean",
    "Data/Rat",  # full subtree
    "Data/Real",  # full subtree (happens to be flat -- no subdirectories exist)
    "Data/Multiset",  # full subtree
    "Data/Sym",  # full subtree
    "Data/Fin",  # full subtree
    "Data/Bool",  # full subtree
    "Data/Prod",  # full subtree
    "Data/Sum",  # full subtree
    "Data/Option",  # full subtree
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
