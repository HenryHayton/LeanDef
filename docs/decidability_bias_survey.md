# Decidability-bias survey

Read-only survey of `harness/` for places the current implementation structurally assumes
"every fact resolves via `decide`," per the task that requested it. **No code was changed as
part of this survey** — findings only. See `docs/design/reward_structure_2026-07-21.md` §2 for
the three-fact-type model (decidable casework, membership facts, global theorem facts) and
`docs/design/verifier_architecture_2026-07-20.md` §4 for the tri-state TRUE/FALSE/UNKNOWN
adjudication protocol proof-based facts need. `archive/n1_tau/` (this repo's only worked
example) is fully decidable-fact-shaped; everything below is the gap between what that example
needed and what §2.2 (proof-requiring membership) / §2.3 (global theorems) will need.

---

## 1. `CheckStatus` has no `UNKNOWN` — and the current call pattern couldn't produce one anyway

**`harness/results.py:14-17`**

```python
class CheckStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    ERRORED = "errored"
```

Three states, none of them `UNKNOWN`. Per the architecture doc §4, a proof-based fact
(membership facts that need a proof, §2.2; every global fact, §2.3) is adjudicated by
attempting the fact *and independently attempting its negation* under a fixed budget: proof of
the fact → TRUE, proof of the negation → FALSE, neither → UNKNOWN, "reported as its own
category and never folded into failure." There is no fourth state to report it into. Today a
genuinely-uncertain proof outcome would have to be miscoded as either `ERRORED` (wrong: that
means the check-infrastructure failed, not that the prover tried and honestly couldn't decide)
or `FAILED` (explicitly forbidden by the design doc's "never folded into failure").

This compounds with a second, sharper gap: **nothing currently attempts the negation at all.**
`run_facts` (`harness/scoring.py:51-61`) sends exactly one REPL command per fact and reads
PASSED/FAILED off `response.has_errors()`. For `decide` this is sound — a decidable
proposition's truth value is fully determined by whether `decide` closes the goal, so one
command is enough. It is not sound for a general tactic/proof attempt: `has_errors() == True`
on a submitted proof conflates three different situations ("the proof script is wrong but the
statement might be true," "the statement is actually false," "no proof was found in the
budget") that `decide`'s binary result never has to distinguish, because `decide` doesn't fail
for lack of trying. Producing a real TRUE/FALSE/UNKNOWN verdict needs at minimum two REPL
round-trips per obligation (attempt the fact, attempt the negation) plus logic to combine the
two outcomes — a different call shape than `run_facts`' current one-command-per-fact loop, not
just an extra enum value.

**Generalizing this would involve:** adding `CheckStatus.UNKNOWN`; changing the proof-fact
adjudication path (wherever it's built) to attempt both directions and combine the results,
rather than reusing `run_facts`' single-command-per-fact loop; deciding what "detail" means for
an UNKNOWN result (there is no error message to report — both attempts simply ran out of
budget).

## 2. `CandidateScore.fidelity` has no policy for a fact that isn't PASSED or FAILED

**`harness/results.py:54-59`**

```python
def fidelity(self) -> float | None:
    if not self.admissible or not self.fact_results:
        return None
    n_passed = sum(1 for r in self.fact_results if r.status is CheckStatus.PASSED)
    return n_passed / len(self.fact_results)
```

Fidelity is `passed / total`, where `total` is unconditionally `len(self.fact_results)`. This
is fine while every result is PASSED or FAILED. Once `UNKNOWN` exists (finding 1), this formula
needs an explicit decision that isn't made anywhere today: does an UNKNOWN fact count in the
denominator (penalizing a candidate for a fact the *prover* couldn't resolve, which reads like
exactly the "folded into failure" the design doc forbids), or is it excluded (shrinking the
suite the candidate is actually scored against, which changes what "fidelity" means suite to
suite)? Both are defensible; neither is currently chosen, because the type that would force the
choice doesn't exist yet.

**Generalizing this would involve:** deciding and implementing an explicit UNKNOWN-handling
policy in `fidelity` once `CheckStatus.UNKNOWN` exists, rather than letting whatever the
denominator does by default become the policy by accident.

## 3. The fact representation has no adjudication-mechanism slot — `decide` is implicit

**`harness/scoring.py:51-61`** (`run_facts`), and the `facts: list[str]` parameter shared by
`run_facts`, `score_candidate` (`harness/scoring.py:64-69`), and `score_spliced_candidate`
(`harness/scoring.py:90-95`)

A fact is a bare Python string — raw Lean source text, sent as-is via
`Command(cmd=fact, env=candidate_env)`. There is no field, tag, or wrapper type indicating
*how* a given fact should be adjudicated. This works only because every fact string in the
codebase today happens to end in `:= by decide`, so "run it, check `has_errors()`" is correct
by convention, not by any check the code performs. Nothing stops (or flags) a caller from
passing a fact string that needs a real proof search — it would simply be sent as a normal
command, and `has_errors()` would almost always come back `True` for a nontrivial theorem
attempted with no tactic at all, silently scoring as FAILED rather than routing to a prover
agent. The three-type model (§2) is not represented in the data at all: there's no way to look
at a `facts: list[str]` and know which of the three mechanisms an entry needs without reading
its source text and guessing.

**Generalizing this would involve:** replacing the bare-string fact representation with a
structured type carrying at least an adjudication-mechanism tag (decidable / membership-proof /
global-proof) alongside the statement text, and branching `run_facts` (or its replacement) on
that tag rather than assuming `decide` for everything.

## 4. `DEFAULT_CHECK_TIMEOUT` is one tier, tuned for decidable-scale cost, applied to every fact

**`harness/config.py:22`** (`DEFAULT_CHECK_TIMEOUT = 60.0`) and **`harness/admissibility.py:101`**
(a second, independent hardcoded `60.0` fallback inside `check_admissibility`, not sourced from
`harness.config` at all — the same assumption duplicated in a second place)

`run_facts` uses this single default for every fact it runs, with no distinction by fact type.
60 seconds is generous for a decidable check (milliseconds observed in practice) and roughly
the right order of magnitude for a shallow membership proof, but the architecture doc puts
global/proof-based facts at "seconds to minutes" *per attempt* — and with finding 1's
two-attempts-per-obligation requirement, potentially two budgets of that size per fact. A
global fact that would have been provable given a real budget would instead come back
`ERRORED` (timeout) under the current default, indistinguishable in the result from a candidate
that actually wedged the REPL. This is exactly the scenario the task asked about directly:
**yes, something in the current result flow would misbehave if a fact took minutes instead of
milliseconds** — not by crashing, but by silently misclassifying a slow-but-correct proof
attempt as an infrastructure error.

**Generalizing this would involve:** giving proof-based fact adjudication its own budget
parameter (plausibly minutes, not extending `DEFAULT_CHECK_TIMEOUT`), and reconciling the
duplicate hardcoded `60.0` in `admissibility.py` with the one in `config.py` regardless (the
duplication itself is a smaller, orthogonal issue, but it's the same "one number for every
check" assumption showing up twice).

## 5. The watchdog's retry semantics are shaped for infrastructure flakiness, not proof search

**`harness/repl.py`** (`run_checked`, described in its own docstring as: kill on timeout,
"retry the call once against a fresh REPL")

`run_checked`'s one retry exists to recover from a wedged REPL subprocess — the same command,
resent, after a restart. That is the right response to infrastructure flakiness (the hang this
module was built to survive) and the wrong response to "the prover didn't find a proof this
time": a prover agent's retry (different strategy, a different LLM call, possibly a larger
internal budget) is a different operation from resending an identical Lean command, not a
degenerate case of it. Nothing in the current code conflates these yet, because nothing calls
`run_checked` for a proof attempt today — but a naive extension that routed prover-agent calls
through the same retry path would silently do so.

**Generalizing this would involve:** keeping `run_checked`'s retry-after-restart mechanism for
what it's for (REPL infrastructure recovery) and giving a future prover-agent adjudication path
its own, semantically distinct retry/budget logic rather than reusing this one.

---

## Summary table

| # | Location | Assumes | Needed for §2.2/§2.3 |
|---|---|---|---|
| 1 | `harness/results.py:14-17`, `harness/scoring.py:51-61` | Every check is TRUE/FALSE (PASSED/FAILED); one REPL command settles it | `UNKNOWN` state; two-attempt (fact + negation) adjudication |
| 2 | `harness/results.py:54-59` | Every fact result counts identically toward fidelity | An explicit UNKNOWN-handling policy in the denominator |
| 3 | `harness/scoring.py:51-95` (`facts: list[str]`) | `decide` is the only adjudication mechanism; it's implicit in the fact string, not declared | A per-fact adjudication-mechanism tag |
| 4 | `harness/config.py:22`, `harness/admissibility.py:101` | 60s is enough for any check | A separate, larger budget for proof-based facts |
| 5 | `harness/repl.py` (`run_checked`) | Retry = resend the same command after a restart | Separate retry/budget semantics for prover-agent calls |
