/-
n=1 calibration probe: divisor-counting function τ (tau).
Scratch file only — see scratch/n1_tau/README.md. Not part of the permanent project.
-/
import Mathlib

/-- The divisor-counting function: the number of positive divisors of `n`.
Hand-written body (not Mathlib's `Nat.divisors`), so the fact suite below is checked by
kernel computation over this body, not by library lemmas. -/
def tau : ℕ → ℕ := fun n => ((Finset.Icc 1 n).filter (· ∣ n)).card

-- Sanity check: `tau` agrees with Mathlib's own divisor-counting function for n < 40.
-- (`Nat.divisors n = {d ∈ Finset.Ico 1 (n + 1) | d ∣ n}`, which is the same range as our
-- `Finset.Icc 1 n` for `ℕ`, so this should hold for ALL n, not just n < 40 — the bounded
-- check is just what we can `decide` cheaply.)
example : ∀ n, n < 40 → tau n = n.divisors.card := by decide

-- Fact suite (10 two-sided facts), each decided by kernel computation over `tau`'s body.
example : tau 1 = 1 := by decide
example : tau 2 = 2 := by decide
example : tau 6 = 4 := by decide
example : tau 7 = 2 := by decide
example : tau 12 = 6 := by decide
example : tau 16 = 5 := by decide
example : tau 28 = 6 := by decide

-- Refuting facts: the values the proper-divisor mutant (`tau_mutant` below) would produce.
example : tau 6 ≠ 3 := by decide
example : tau 12 ≠ 5 := by decide
example : tau 16 ≠ 4 := by decide

-- Mutant candidate: proper-divisor near-miss (excludes n itself, shifting every value down
-- by one for n ≥ 1).
def tau_mutant : ℕ → ℕ := fun n => ((Finset.Icc 1 (n - 1)).filter (· ∣ n)).card

-- Junk candidate: the vacuous/empty definition.
def tau_junk : ℕ → ℕ := fun _ => 0
