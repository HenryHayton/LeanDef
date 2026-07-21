"""scratch/n1_tau/score.py — throwaway calibration probe scorer.

NOT part of the permanent `harness/` package. Scores a battery of candidate bodies for `tau`
(the divisor-counting function) — the true definition, seven mutants representing distinct
categories of plausible misreading, and a junk/vacuous candidate — against the 7 positive
exact-value facts, using the same LeanREPLConfig/AutoLeanServer pattern already proven in
scripts/smoke_test.py (copied here, not imported, to keep this scratch probe self-contained).

The 3 `≠`-refuting facts from the first probe run are dropped from scoring: they were shown to
leak free passes to constant candidates (junk scored 3/10 by luck, not by tracking anything).
This run only scores the 7 positive facts.

True values at the tested inputs (hand-computed, for reference):
  n     : 1  2  6  7  12 16 28
  tau(n): 1  2  4  2  6  5  6      (divisor count)
  omega : 0  1  2  1  2  1  2      (distinct prime factors, for m6)
  sigma : 1  3  12 8  28 31 56     (divisor sum, for m7)

Run with: uv run python scratch/n1_tau/score.py
"""

import time
from pathlib import Path

from lean_interact import AutoLeanServer, Command, LeanREPLConfig, LocalProject

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LEAN_PROJECT_DIR = REPO_ROOT / "lean"
MAX_TOTAL_MEMORY = 0.95  # see scripts/smoke_test.py / CLAUDE.md for why this is raised

# The 7 positive exact-value facts from the original suite (the 3 `!=` refuting facts are
# dropped — see module docstring).
FACTS: list[str] = [
    "example : tau 1 = 1 := by decide",
    "example : tau 2 = 2 := by decide",
    "example : tau 6 = 4 := by decide",
    "example : tau 7 = 2 := by decide",
    "example : tau 12 = 6 := by decide",
    "example : tau 16 = 5 := by decide",
    "example : tau 28 = 6 := by decide",
]

# Candidates are spliced under the pinned name `tau`, so FACTS (written in terms of `tau`)
# apply unchanged to whichever candidate is currently defined.
CANDIDATES: dict[str, str] = {
    "true": "def tau : ℕ → ℕ := fun n => ((Finset.Icc 1 n).filter (· ∣ n)).card",
    # m1: proper divisors (excludes n itself). Shifts every value down by 1.
    "m1_proper_divisors": "def tau : ℕ → ℕ := fun n => ((Finset.Icc 1 (n - 1)).filter (· ∣ n)).card",
    # m2: counts from 0 instead of 1. 0 ∣ n only when n = 0, so this agrees with true tau for
    # every n >= 1 and differs only at n = 0, which none of our facts test.
    "m2_include_zero": "def tau : ℕ → ℕ := fun n => ((Finset.range (n + 1)).filter (· ∣ n)).card",
    # m3: half-open Ico 1 n instead of Icc 1 n — mathematically identical to m1 (Icc 1 (n-1)
    # = Ico 1 n for n : ℕ), just a different Finset spelling of the same set.
    "m3_strict_bound": "def tau : ℕ → ℕ := fun n => ((Finset.Ico 1 n).filter (· ∣ n)).card",
    # m4: range extended past n. (n+1) never divides n for n >= 1, so this agrees with true
    # tau for every n >= 1 and differs only at n = 0.
    "m4_off_by_one_up": "def tau : ℕ → ℕ := fun n => ((Finset.Icc 1 (n + 1)).filter (· ∣ n)).card",
    # m5: divisibility direction flipped (counts d in [1,n] with n ∣ d, i.e. multiples of n in
    # that range). For n >= 1 the only such d is n itself, so this is the constant 1.
    "m5_multiples_confusion": "def tau : ℕ → ℕ := fun n => ((Finset.Icc 1 n).filter (n ∣ ·)).card",
    # m6: counts only prime divisors — confuses tau (divisor count) with omega (count of
    # distinct prime factors).
    "m6_count_primes": (
        "def tau : ℕ → ℕ := fun n => ((Finset.Icc 1 n).filter (fun d => d ∣ n ∧ Nat.Prime d)).card"
    ),
    # m7: sums divisors instead of counting them — confuses tau with sigma.
    "m7_sum_not_count": "def tau : ℕ → ℕ := fun n => ((Finset.Icc 1 n).filter (· ∣ n)).sum id",
    "junk": "def tau : ℕ → ℕ := fun _ => 0",
}

# Predictions, hand-computed before running (see module docstring for the raw tau/omega/sigma
# tables). True = predicted to PASS that fact, in FACTS order (n = 1,2,6,7,12,16,28).
PREDICTIONS: dict[str, list[bool]] = {
    "true": [True, True, True, True, True, True, True],
    # values 0,1,3,1,5,4,5 vs true 1,2,4,2,6,5,6 -- no matches
    "m1_proper_divisors": [False, False, False, False, False, False, False],
    # agrees with true tau at every n >= 1 -- expected to slip through entirely
    "m2_include_zero": [True, True, True, True, True, True, True],
    # identical function to m1
    "m3_strict_bound": [False, False, False, False, False, False, False],
    # agrees with true tau at every n >= 1 -- expected to slip through entirely
    "m4_off_by_one_up": [True, True, True, True, True, True, True],
    # constant 1 for n >= 1; matches true tau only at n = 1 (tau(1) = 1)
    "m5_multiples_confusion": [True, False, False, False, False, False, False],
    # omega values 0,1,2,1,2,1,2 vs true 1,2,4,2,6,5,6 -- no matches
    "m6_count_primes": [False, False, False, False, False, False, False],
    # sigma values 1,3,12,8,28,31,56 vs true 1,2,4,2,6,5,6 -- matches only at n = 1 (coincidence: sigma(1) = tau(1) = 1)
    "m7_sum_not_count": [True, False, False, False, False, False, False],
    "junk": [False, False, False, False, False, False, False],
}


def main() -> None:
    config = LeanREPLConfig(project=LocalProject(directory=str(LEAN_PROJECT_DIR)), verbose=False)
    server = AutoLeanServer(config, max_total_memory=MAX_TOTAL_MEMORY)

    wall_start = time.perf_counter()

    print("Importing Mathlib (cold, one-time; reused as the base env for all candidates)...")
    t0 = time.perf_counter()
    base_resp = server.run(Command(cmd="import Mathlib"))
    assert not base_resp.has_errors(), base_resp.messages
    base_env = base_resp.env
    cold_import_s = time.perf_counter() - t0
    print(f"  done in {cold_import_s:.1f}s (env={base_env})\n")

    results: dict[str, list[bool]] = {}
    fact_check_times: list[float] = []
    for label, def_body in CANDIDATES.items():
        def_resp = server.run(Command(cmd=def_body, env=base_env))
        assert not def_resp.has_errors(), f"candidate {label!r} failed to even compile: {def_resp.messages}"
        candidate_env = def_resp.env

        passed = []
        for fact in FACTS:
            t_fact = time.perf_counter()
            fact_resp = server.run(Command(cmd=fact, env=candidate_env))
            fact_check_times.append(time.perf_counter() - t_fact)
            passed.append(not fact_resp.has_errors())
        results[label] = passed

    wall_total_s = time.perf_counter() - wall_start

    # --- Results table ---
    print(f"{'candidate':24s} {'fidelity':10s} facts (✓=passed ✗=failed, in fact-suite order)")
    for label, passed in results.items():
        n_pass = sum(passed)
        marks = "".join("✓" if p else "✗" for p in passed)
        print(f"{label:24s} {n_pass:2d}/{len(FACTS)}      {marks}")

    # --- Prediction vs actual ---
    print("\n=== Prediction vs actual ===")
    any_mismatch = False
    for label in CANDIDATES:
        predicted = PREDICTIONS[label]
        actual = results[label]
        if predicted == actual:
            print(f"{label:24s} MATCH")
        else:
            any_mismatch = True
            pred_marks = "".join("✓" if p else "✗" for p in predicted)
            actual_marks = "".join("✓" if p else "✗" for p in actual)
            print(f"{label:24s} MISMATCH  predicted={pred_marks}  actual={actual_marks}")
    if any_mismatch:
        print("\n*** At least one prediction did not match reality — see MISMATCH lines above. ***")
    else:
        print("\nAll predictions matched actual results.")

    # --- Candidates that slipped through entirely ---
    print("\n=== Candidates passing ALL facts ===")
    slipped = [label for label, passed in results.items() if all(passed) and label != "true"]
    if slipped:
        for label in slipped:
            print(f"  {label}")
    else:
        print("  (none besides 'true')")

    # --- Per-fact discrimination: how many candidates (excluding 'true') each fact fails ---
    print("\n=== Per-fact discrimination (mutants+junk failed, out of {}) ===".format(len(CANDIDATES) - 1))
    non_true_labels = [label for label in CANDIDATES if label != "true"]
    for i, fact in enumerate(FACTS):
        n_failed = sum(1 for label in non_true_labels if not results[label][i])
        print(f"  fact {i} ({fact.split(':')[1].split(':=')[0].strip()}): failed by {n_failed}/{len(non_true_labels)}")

    # --- Timing summary ---
    n_checks = len(fact_check_times)
    avg_fact_s = sum(fact_check_times) / n_checks if n_checks else 0.0
    print("\n=== Timing ===")
    print(f"cold `import Mathlib`:        {cold_import_s:.1f}s")
    print(f"total wall clock:             {wall_total_s:.1f}s")
    print(f"fact checks run:              {n_checks} ({len(CANDIDATES)} candidates x {len(FACTS)} facts)")
    print(f"avg time per fact check:      {avg_fact_s:.3f}s")
    print(f"min/max fact check time:      {min(fact_check_times):.3f}s / {max(fact_check_times):.3f}s")


if __name__ == "__main__":
    main()
