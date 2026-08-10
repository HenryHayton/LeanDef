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
