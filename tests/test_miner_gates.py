"""Unit tests for miner.gates -- the six hard eligibility gates, on synthetic VerifiedDef/
SupplyProxies instances. No REPL, no real Mathlib data."""

from miner.gates import (
    GateConfig,
    anti_plumbing_gate,
    bare_name,
    dependency_vocabulary_gate,
    docstring_floor_gate,
    evaluate_gates,
    fact_supply_gate,
    length_band_gate,
    looks_like_prop_type,
    mention_floor_gate,
    normalize_body,
)
from miner.proxies import SupplyProxies, SupplyTier
from miner.verify import BinderGroup, VerifiedDef

_ANTI_PLUMBING_PATTERNS = [
    r"(?i)aux\d*$",
    r"(?i)^aux",
    r"Impl$",
    r"(?:^|\.)go$",
    r"TR$",
    r"(?i)decEq$",
    r"(?i)beq$",
]


def _verified(**overrides) -> VerifiedDef:
    defaults = dict(
        name="Test.foo",
        module_path="Test.lean",
        source_text="def foo (n : Nat) : Nat := n + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1",
        docstring="A perfectly ordinary docstring describing what foo computes.",
        mention_count=100,
        included=True,
        elaborates=True,
        binder_groups=[BinderGroup(kind="explicit", names=["n"], type_text="ℕ")],
        explicit_arg_types=["ℕ"],
        return_type="ℕ",
        executable=True,
        exec_mechanism="eval",
        output_decidable_eq=True,
        referenced_constants=[],
        axioms=[],
    )
    defaults.update(overrides)
    return VerifiedDef(**defaults)


def _proxies(**overrides) -> SupplyProxies:
    defaults = dict(
        casework_tier=SupplyTier.RICH,
        membership_tier=SupplyTier.NONE,
        global_tier=SupplyTier.NONE,
        mention_count=100,
        theorem_mention_count=None,
        enumerable_arg_count=1,
        is_predicate_shaped=False,
        classifies_structure=False,
    )
    defaults.update(overrides)
    return SupplyProxies(**defaults)


def _config(**overrides) -> GateConfig:
    defaults = dict(
        mention_floor=30,
        length_min=40,
        length_max=500,
        docstring_min_length=20,
        vocabulary_modules=["Data/Nat", "Data/List", "Data/Finset", "Logic"],
        anti_plumbing_patterns=_ANTI_PLUMBING_PATTERNS,
    )
    defaults.update(overrides)
    return GateConfig(**defaults)


# --- normalize_body ---


def test_normalize_body_strips_comments_and_collapses_whitespace():
    src = "def foo -- a line comment\n  (n : ℕ) : ℕ :=\n  /- a\n  block comment -/ n + 1"
    assert normalize_body(src) == "def foo (n : ℕ) : ℕ := n + 1"


# --- bare_name ---


def test_bare_name_takes_last_dotted_component():
    assert bare_name("Nat.digitsAux1") == "digitsAux1"
    assert bare_name("foo") == "foo"


# --- (a) mention_floor_gate ---


def test_mention_floor_gate_passes_at_or_above_floor():
    v = _verified(mention_count=30)
    assert mention_floor_gate(v, floor=30) is True


def test_mention_floor_gate_fails_definition_mentioned_five_times():
    """Explicit acceptance case: a definition mentioned 5 times must fail the mention floor."""
    v = _verified(mention_count=5)
    assert mention_floor_gate(v, floor=30) is False


# --- (b) length_band_gate ---


def test_length_band_gate_fails_nat_prime_style_delegation():
    """Explicit acceptance case: `Nat.Prime := Irreducible p` must fail the length floor."""
    v = _verified(source_text="def Prime (p : ℕ) := Irreducible p")
    assert length_band_gate(v, length_min=40, length_max=500) is False


def test_length_band_gate_passes_within_band():
    v = _verified(source_text="def " + "x" * 60 + " : ℕ := 0")
    assert length_band_gate(v, length_min=40, length_max=500) is True


def test_length_band_gate_fails_above_ceiling():
    v = _verified(source_text="def foo : ℕ := " + "0 + " * 200 + "0")
    assert length_band_gate(v, length_min=40, length_max=500) is False


# --- (c) docstring_floor_gate ---


def test_docstring_floor_gate_fails_missing_docstring():
    v = _verified(docstring=None)
    assert docstring_floor_gate(v, min_length=20) is False


def test_docstring_floor_gate_fails_trivial_docstring():
    v = _verified(docstring="foo.")
    assert docstring_floor_gate(v, min_length=20) is False


def test_docstring_floor_gate_passes_substantial_docstring():
    v = _verified(docstring="Computes the thing that foo is supposed to compute, in detail.")
    assert docstring_floor_gate(v, min_length=20) is True


# --- (d) dependency_vocabulary_gate ---


def test_dependency_vocabulary_gate_passes_when_all_resolve_in_vocabulary():
    v = _verified(referenced_constants=["Nat.succ", "List.map"])
    index = {"Nat.succ": "Data/Nat/Basic.lean", "List.map": "Data/List/Basic.lean"}
    assert dependency_vocabulary_gate(v, index, ["Data/Nat", "Data/List"]) is True


def test_dependency_vocabulary_gate_fails_on_exotic_dependency():
    v = _verified(referenced_constants=["Nat.succ", "Analysis.Exotic.thing"])
    index = {
        "Nat.succ": "Data/Nat/Basic.lean",
        "Analysis.Exotic.thing": "Analysis/Exotic/Thing.lean",
    }
    assert dependency_vocabulary_gate(v, index, ["Data/Nat", "Data/List"]) is False


def test_dependency_vocabulary_gate_ignores_unresolvable_references():
    """referenced_constants noise (bound variables like 'x', 'a_1') that resolves to no known
    module must not block the gate -- see the gate's own docstring."""
    v = _verified(referenced_constants=["x", "a_1", "Nat.succ"])
    index = {"Nat.succ": "Data/Nat/Basic.lean"}
    assert dependency_vocabulary_gate(v, index, ["Data/Nat"]) is True


# --- (e) anti_plumbing_gate ---


def test_anti_plumbing_gate_fails_digitsaux1():
    """Explicit acceptance case: Nat.digitsAux1 must fail anti-plumbing."""
    v = _verified(name="Nat.digitsAux1")
    assert anti_plumbing_gate(v, _ANTI_PLUMBING_PATTERNS) is False


def test_anti_plumbing_gate_fails_tr_suffixed_name():
    """Explicit acceptance case: a TR-suffixed name must fail anti-plumbing."""
    v = _verified(name="List.iterateTR")
    assert anti_plumbing_gate(v, _ANTI_PLUMBING_PATTERNS) is False


def test_anti_plumbing_gate_fails_impl_suffix():
    v = _verified(name="Foo.BarImpl")
    assert anti_plumbing_gate(v, _ANTI_PLUMBING_PATTERNS) is False


def test_anti_plumbing_gate_fails_dot_go_helper():
    v = _verified(name="Nat.log.go")
    assert anti_plumbing_gate(v, _ANTI_PLUMBING_PATTERNS) is False


def test_anti_plumbing_gate_fails_dec_eq_and_beq_machinery():
    assert anti_plumbing_gate(_verified(name="Foo.instDecidableEqFooDecEq"), _ANTI_PLUMBING_PATTERNS) is False
    assert anti_plumbing_gate(_verified(name="Foo.instBeq"), _ANTI_PLUMBING_PATTERNS) is False


def test_anti_plumbing_gate_passes_ordinary_name():
    v = _verified(name="Nat.Prime")
    assert anti_plumbing_gate(v, _ANTI_PLUMBING_PATTERNS) is True


def test_anti_plumbing_gate_only_matches_bare_name_not_namespace():
    # "Aux" appearing in a namespace segment, not the leaf, must not trigger the pattern.
    v = _verified(name="AuxNamespace.realDefinition")
    assert anti_plumbing_gate(v, _ANTI_PLUMBING_PATTERNS) is True


# --- (f) fact_supply_gate ---


def test_fact_supply_gate_fails_all_none():
    p = _proxies(casework_tier=SupplyTier.NONE, membership_tier=SupplyTier.NONE, global_tier=SupplyTier.NONE)
    assert fact_supply_gate(p) is False


def test_fact_supply_gate_passes_one_non_none_tier():
    p = _proxies(casework_tier=SupplyTier.THIN, membership_tier=SupplyTier.NONE, global_tier=SupplyTier.NONE)
    assert fact_supply_gate(p) is True


# --- looks_like_prop_type ---


def test_looks_like_prop_type_true_for_relation_type():
    assert looks_like_prop_type("a ≠ b") is True
    assert looks_like_prop_type("∀ x, p x") is True


def test_looks_like_prop_type_false_for_plain_data_type():
    assert looks_like_prop_type("ℕ") is False
    assert looks_like_prop_type("Finset α") is False


# --- evaluate_gates aggregation ---


def test_evaluate_gates_empty_list_when_all_pass():
    v = _verified()
    p = _proxies()
    assert evaluate_gates(v, p, declaration_index={}, config=_config()) == []


def test_evaluate_gates_records_every_failing_gate_not_just_the_first():
    v = _verified(
        name="Nat.digitsAux1",  # fails anti_plumbing
        mention_count=5,  # fails mention_floor
        source_text="def Prime (p : ℕ) := Irreducible p",  # fails length_band
        docstring=None,  # fails docstring_floor
    )
    p = _proxies(casework_tier=SupplyTier.NONE, membership_tier=SupplyTier.NONE, global_tier=SupplyTier.NONE)
    failed = evaluate_gates(v, p, declaration_index={}, config=_config())
    assert set(failed) == {"mention_floor", "length_band", "docstring_floor", "anti_plumbing", "fact_supply"}
