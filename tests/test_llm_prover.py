"""Tier-5 LLM prover: the pure pieces. Kernel checking is exercised live on the box."""

from scripts.llm_prover import build_prompt, extract_script, negation_goal


def test_negation_wraps_in_parens_so_binders_cannot_capture():
    assert negation_goal("∀ n : ℕ, n = 0") == "¬ (∀ n : ℕ, n = 0)"


def test_script_extraction_takes_the_last_fenced_by_block():
    text = "Reasoning...\n```lean\nexample : True := trivial\n```\nFinal:\n```lean\nby push_neg\n  exact ⟨1, by simp⟩\n```"
    assert extract_script(text).startswith("by push_neg")


def test_a_reply_with_no_by_script_is_rejected_not_guessed():
    assert extract_script("I cannot prove this.") is None
    assert extract_script("```lean\ntheorem x : True := trivial\n```") is None


def test_prompts_carry_the_candidate_and_the_right_goal_direction():
    record = {"extracted_code": "def VTask.f : ℕ := 3"}
    fwd = build_prompt(record, "VTask.f = 3", "forward")
    neg = build_prompt(record, "VTask.f = 3", "negation")
    assert "def VTask.f" in fwd and "VTask.f = 3" in fwd and "NEGATION" not in fwd
    assert "¬ (VTask.f = 3)" in neg and "counterexample" in neg


def test_prover_native_theorem_shape_extracts_from_the_last_assignment():
    text = ("```lean4\nimport Mathlib\ndef VTask.f : ℕ := 3\n"
            "theorem goal_to_prove : VTask.f = 3 := by\n  rfl\n```")
    from scripts.llm_prover import extract_script
    s = extract_script(text)
    assert s is not None and s.startswith("by")
    assert "rfl" in s and "theorem" not in s


def test_prover_prompt_is_a_file_completion_not_a_conversation():
    from scripts.llm_prover import build_prover_prompt
    p = build_prover_prompt({"extracted_code": "def VTask.f : ℕ := 3"}, "VTask.f = 3", "forward")
    assert "Complete the following Lean 4 code" in p
    assert "theorem goal_to_prove : VTask.f = 3 := by" in p
    n = build_prover_prompt({"extracted_code": "def VTask.f : ℕ := 3"}, "VTask.f = 3", "negation")
    assert "¬ (VTask.f = 3)" in n


def test_arm_assignment_is_deterministic_direction_blind_and_balanced():
    from scripts.llm_prover import arm_of
    rec = lambda i: {"model_slug": "m", "task_name": "T", "sample_index": i}
    arms = [arm_of(rec(i), f"fact_{j}") for i in range(10) for j in range(30)]
    assert arms == [arm_of(rec(i), f"fact_{j}") for i in range(10) for j in range(30)]
    share = arms.count("goedel") / len(arms)
    assert 0.4 < share < 0.6, f"hash split badly unbalanced: {share}"


class TestTruthCountercheckUsesTheWitness:
    """Regression: the countercheck must reuse the model's OWN refutation script.

    Observed twice on Nat.divisors/divisors_mem_iff (a fact missing `n ≠ 0`, false of the real
    Nat.divisors at n=0). A refutation is a WITNESS -- `refine ⟨0, 1, ?_⟩` -- and the generic
    push_neg/simp_all/aesop ladder never rediscovers which witness, so it returned False and a
    FAIL was certified against a fact already known to be defective.
    """

    def test_script_is_ported_to_the_truth_and_tried_first(self, monkeypatch):
        import scripts.llm_prover as lp

        seen = {}

        class _Passed:
            status = __import__("harness.results", fromlist=["CheckStatus"]).CheckStatus.PASSED

        def fake_run_checked(server, command, timeout=None):
            seen["cmd"] = command.cmd
            return _Passed()

        monkeypatch.setattr("harness.repl.run_checked", fake_run_checked)
        out = lp._refutes_truth_too(
            server=object(), base_env=0,
            statement="∀ (n d : ℕ), d ∈ VTask.divisors n ↔ d ∣ n ∧ 0 < d",
            real_name="Nat.divisors", task_symbol="VTask.divisors", imports=None,
            script="by\n  push_neg\n  refine ⟨0, 1, ?_⟩\n  simp",
        )
        assert out is True, "a script that proves the truth's negation must flag a suspect fact"
        assert "VTask.divisors" not in seen["cmd"], "task symbol must be rewritten to the truth"
        assert "Nat.divisors" in seen["cmd"]
        assert "refine ⟨0, 1, ?_⟩" in seen["cmd"], "the witness must survive the port"
