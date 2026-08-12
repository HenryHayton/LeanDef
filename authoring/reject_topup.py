"""One extra call asking specifically for REJECT facts, when a suite comes up short.

Measured on the 50-task run (11-12 Aug 2026): the reject floor of 2 was stated in the prompt as
"hard", and only **15 of 29** suites met it -- **7 shipped with zero reject facts**. The decide
cap, which is enforced mechanically rather than requested, held 29/29. Asking does not work; the
question is whether asking a SECOND time, narrowly, does.

Deliberate design, per the operator:

* **Once.** One top-up call per task, never a loop. If the model cannot produce reject facts on a
  focused second ask, that is itself the finding.
* **Never discards the task.** A suite still short after the top-up ships anyway. The floor of 2
  is not yet known to be the right number -- this run is partly to find out -- so it must not
  silently delete tasks that would inform that question.
* **Recorded either way.** `RejectTopupOutcome` carries before/after counts and whether the call
  was even needed, so the batch report can say how well the re-prompt works rather than only
  whether the floor was met.

Top-up facts go through the SAME parse and the same validation ladder as first-pass facts; this
adds a call, not a shortcut.
"""

from dataclasses import dataclass, field

from authoring.composition import REJECT_FLOOR, _is_reject

REJECT_TOPUP_PROMPT = """\
The fact suite you proposed for this object contains {n_reject} fact(s) that assert the \
definition does NOT hold of something, but this suite needs at least {floor}.

Propose {n_needed} ADDITIONAL fact(s), each of which asserts a NON-example: an object the \
definition should REJECT. Shapes that qualify: a `polarity: "reject"` membership fact, or a \
global fact of the form `¬ ...`, `... ∉ ...`, `... ≠ ...`.

Prefer NEAR-MISSES: an object satisfying every defining condition except one, violating exactly \
that one, with `near_miss_clause` naming the violated clause. A group is pinned down by a monoid \
that is not a group. These are what distinguish the intended object from a vacuous definition \
that accepts everything.

Do not repeat or restate facts you already proposed. Respond with a strict JSON array only, in \
the same format as before, containing ONLY the new facts."""


@dataclass
class RejectTopupOutcome:
    needed: bool = False
    attempted: bool = False
    before: int = 0
    after: int = 0
    gained: list = field(default_factory=list)
    detail: str = ""

    @property
    def met_after(self) -> bool:
        return self.after >= REJECT_FLOOR


def topup_reject_facts(client, model_id, system: str, facts: list, parse_fn, *,
                       budget=None, max_tokens: int | None = None) -> RejectTopupOutcome:
    """One focused re-ask for reject facts. Returns the outcome; caller appends `gained`."""
    from authoring.orchestrate import _call_llm_json

    before = sum(1 for f in facts if _is_reject(f))
    out = RejectTopupOutcome(needed=before < REJECT_FLOOR, before=before, after=before)
    if not out.needed:
        return out

    out.attempted = True
    prompt = REJECT_TOPUP_PROMPT.format(n_reject=before, floor=REJECT_FLOOR,
                                        n_needed=REJECT_FLOOR - before)
    try:
        new_facts, _rejections = _call_llm_json(client, system, prompt, model_id=model_id,
                                                parse_fn=parse_fn, budget=budget,
                                                max_tokens=max_tokens)
    except Exception as e:  # noqa: BLE001 -- a failed top-up must never lose the task
        out.detail = f"top-up call failed: {type(e).__name__}: {str(e)[:120]}"
        return out

    existing = {getattr(f, "id", None) for f in facts}
    fresh = [f for f in new_facts if getattr(f, "id", None) not in existing]
    out.gained = fresh
    out.after = before + sum(1 for f in fresh if _is_reject(f))
    out.detail = (f"top-up returned {len(new_facts)} fact(s), {len(fresh)} new, "
                  f"{out.after - before} of them reject-shaped")
    return out
