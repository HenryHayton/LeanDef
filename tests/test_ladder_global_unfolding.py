"""Tier 2 must unfold the candidate's own definition on GLOBAL (proof-mechanism) facts.

Both cases below were kernel-verified as UNKNOWN-before / PASS-after on 11 Aug 2026, against
real candidates from the 32B scoring corpus. Before this change tier 2 attacked ∀-quantified
facts with `rfl, omega, norm_num, positivity, simp, exact?, aesop` -- not one of which can see
inside a non-reducible `def` -- so 579 of the corpus's 731 UNKNOWNs were global facts that no
attempted tactic was permitted to look at.

These are `mathlib`-marked: they need a real Mathlib environment, and they assert an END-TO-END
adjudication outcome rather than the shape of a tactic list, because the tactic list was already
"right" in the sense that it existed -- it just was not reachable from this code path.
"""

import pytest

from harness.scoring import splice_candidate_declaration
from harness.results import CheckStatus
from harness.facts import Fact
from ladder.adjudicate import adjudicate_fact
from ladder.statuses import AdjudicationStatus
from scoring.samples import load_task


def _splice(server, base_env, task_name, body):
    t = load_task(task_name)
    outcome = splice_candidate_declaration(server, base_env, t["signature"], body)
    assert outcome.result.status is CheckStatus.PASSED, outcome.result.detail
    return t, outcome.result.env


@pytest.mark.parametrize(
    "task_name,body,fact_id,statement",
    [
        # A correct Nat.divisors candidate (qwen3-32b s9). `simp` and `aesop` both FAIL here;
        # `simp [VTask.divisors, Finset.mem_filter, Finset.mem_range]` closes it.
        (
            "Nat.divisors",
            "def VTask.divisors (n : ℕ) : Finset ℕ :=\n"
            "  if n = 0 then ∅ else Finset.filter (· ∣ n) (Finset.range (n + 1))",
            "divisors_n_mem_self",
            "∀ n : ℕ, 0 < n → n ∈ VTask.divisors n",
        ),
        # A Nat.choose candidate that is character-for-character Mathlib's definition
        # (goedel-prover-v2-32b s7). The fact restates its OWN FIRST CLAUSE and was UNKNOWN.
        (
            "Nat.choose",
            "def VTask.choose : ℕ → ℕ → ℕ\n"
            "  | _, 0 => 1\n"
            "  | 0, _ + 1 => 0\n"
            "  | n + 1, k + 1 => VTask.choose n k + VTask.choose n (k + 1)",
            "choose_global_zero_right",
            "∀ n : ℕ, VTask.choose n 0 = 1",
        ),
    ],
)
def test_global_fact_is_certified_once_the_definition_can_be_unfolded(
    mathlib_env, task_name, body, fact_id, statement
):
    server, base_env = mathlib_env
    t, env = _splice(server, base_env, task_name, body)
    fact = Fact(id=fact_id, type="global", mechanism="proof", statement=statement)
    adjudication, _ = adjudicate_fact(
        fact, env, server, imports=t.get("imports"), truth_name=t.get("truth_real_name"),
    )
    assert adjudication.status is AdjudicationStatus.CERTIFIED, (
        f"{task_name}/{fact_id} should now be certified by tier 2 with unfolding; "
        f"got {adjudication.status.name}: {adjudication.detail}"
    )
    assert adjudication.tier == 2
