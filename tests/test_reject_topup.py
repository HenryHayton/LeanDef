"""The reject-floor top-up: one focused re-ask, never a discard.

Measured on the 50-task run (11-12 Aug 2026): the prompt calls the reject floor "hard" and only
15 of 29 suites met it, 7 shipping with ZERO reject facts -- while the mechanically enforced
decide cap held 29/29. This is the narrow second ask, and the point is as much to measure how
well re-prompting works as to raise the floor.
"""

from dataclasses import dataclass

from authoring.reject_topup import RejectTopupOutcome, topup_reject_facts


@dataclass
class F:
    id: str
    mechanism: str = "proof"
    statement: str = "P x"
    polarity: str | None = None


def _positive(n):
    return [F(id=f"g{i}") for i in range(n)]


def test_not_attempted_when_the_floor_is_already_met():
    facts = _positive(5) + [F(id="r1", polarity="reject"), F(id="r2", statement="¬ P w")]
    out = topup_reject_facts(client=None, model_id="m", system="s", facts=facts,
                             parse_fn=lambda t: ([], []))
    assert out.needed is False and out.attempted is False
    assert out.gained == []


def test_attempted_and_counted_when_short(monkeypatch):
    new = [F(id="r_new", polarity="reject")]
    monkeypatch.setattr("authoring.orchestrate._call_llm_json", lambda *a, **k: (new, []))
    out = topup_reject_facts(client=None, model_id="m", system="s", facts=_positive(6),
                             parse_fn=lambda t: (new, []))
    assert out.needed and out.attempted
    assert out.before == 0 and out.after == 1
    assert [f.id for f in out.gained] == ["r_new"]


def test_duplicate_ids_from_the_topup_are_discarded(monkeypatch):
    facts = _positive(3)
    monkeypatch.setattr("authoring.orchestrate._call_llm_json",
                        lambda *a, **k: ([F(id="g0", polarity="reject")], []))
    out = topup_reject_facts(client=None, model_id="m", system="s", facts=facts,
                             parse_fn=lambda t: ([], []))
    assert out.gained == [], "a fact reusing an existing id must not be added twice"


def test_a_failed_topup_never_loses_the_task(monkeypatch):
    def _boom(*a, **k):
        raise RuntimeError("bedrock said no")
    monkeypatch.setattr("authoring.orchestrate._call_llm_json", _boom)
    out = topup_reject_facts(client=None, model_id="m", system="s", facts=_positive(4),
                             parse_fn=lambda t: ([], []))
    assert out.attempted and out.gained == []
    assert "bedrock said no" in out.detail


def test_still_short_is_reported_not_fatal():
    """The floor of 2 is not yet known to be right; a short suite must still ship."""
    out = RejectTopupOutcome(needed=True, attempted=True, before=0, after=1)
    assert out.met_after is False  # reported, and the caller ships anyway
