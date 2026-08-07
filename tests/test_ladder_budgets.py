

def test_tier3_can_be_disabled_without_disabling_tier4():
    """Tier 4 runs AFTER tier 3 in the cascade, so an early return when the hammer is off would
    silently take the equivalence fast path with it. The flag must skip tier 3 only.

    The flag exists because "no Hammer build" and "the hammer tried and lost" are different
    facts that look identical in the attempt log: without `$SCORING_EXTRA_IMPORTS` the tactic is
    simply unknown and the attempt fails in ~0ms.
    """
    import inspect

    from ladder import adjudicate as A
    from ladder.budgets import LadderBudgets

    assert LadderBudgets().tier3_enabled is True
    assert LadderBudgets(tier3_enabled=False).tier3_enabled is False

    src = inspect.getsource(A.adjudicate_fact)
    guard = src.index("if budgets.tier3_enabled:")
    tier4 = src.index("# Tier 4 (real, narrow scope")
    assert guard < tier4, "the tier-3 guard must precede tier 4"
    # The tier-4 block must NOT be inside the tier-3 guard: it starts at function-body indent.
    assert "\n    # Tier 4 (real, narrow scope" in src
