"""Tests for `authoring.task_symbol.task_symbol_for` -- pure, no REPL/Bedrock."""

import pytest

from authoring.task_symbol import task_symbol_for


def test_dotted_name_uses_last_component():
    assert task_symbol_for("Nat.clog") == "VTask.clog"


def test_deeply_dotted_name_uses_last_component():
    assert task_symbol_for("Order.Frame.MinimalAxioms.foo") == "VTask.foo"


def test_bare_name_unchanged_as_base():
    assert task_symbol_for("Monotone") == "VTask.Monotone"


def test_deterministic_same_input_same_output():
    assert task_symbol_for("Nat.clog") == task_symbol_for("Nat.clog")


def test_rejects_a_base_component_that_is_not_a_valid_identifier():
    with pytest.raises(ValueError):
        task_symbol_for("Nat.")
