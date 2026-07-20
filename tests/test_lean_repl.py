from lean_interact import Command


def test_decide_proves_arithmetic(lean_server):
    response = lean_server.run(Command(cmd="example : (2 : Nat) + 2 = 4 := by decide"))
    assert not response.has_errors()


def test_sorry_is_reported_as_warning_not_error(lean_server):
    response = lean_server.run(Command(cmd="def mySorryDef : Nat := sorry"))
    assert not response.has_errors()
    warning_data = [m.data for m in response.get_warnings()]
    assert any("sorry" in d for d in warning_data)
