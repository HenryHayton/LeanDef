"""Driving `score_candidate_body` across a task's samples: dedup, fan-out, resume, hygiene.

Sequential by design for now. The pool interface is sketched in `ScoringWorker` (per-worker env
ownership, per-worker re-warm, per-worker cache file) but deliberately not built: 5.7 GB of
resident Mathlib per worker is what bounds parallelism, and the pilot's arithmetic should decide
the count rather than a guess made before any timing data exists.

**Dedup is the main lever.** The prelim field sampled 5x at temperature 0.7 and 12 of the 41
tasks carry `RECALLED_TARGET`, so identical bodies recur heavily within a task. One distinct body
is scored once; every other sample sharing its hash gets the same verdicts with `scored_as` set,
so an inherited verdict is always distinguishable from a computed one.

**Resume is file-existence over the scores tree**, the same contract `prelim/store.py` proved
under a real mid-run kill. Both the representative and its fan-out targets are checked, so an
interrupted run resumes without recomputing and without leaving a group half-written.
"""

import sys
import time
from dataclasses import dataclass, field

from lean_interact import Command

from harness.repl import get_warm_environment, is_unknown_environment_error, run_checked
from harness.results import CheckStatus
from ladder.budgets import DEFAULT_LADDER_BUDGETS, LadderBudgets
from scoring import config as cfg
from scoring import dedup, store
from scoring.candidate import score_candidate_body
from scoring.samples import load_samples, load_task


@dataclass
class TaskOutcome:
    task_name: str
    model_slug: str
    scored: int = 0          # bodies actually put through the kernel
    fanned_out: int = 0      # samples that inherited a verdict
    skipped: int = 0         # already complete on disk
    unextractable: int = 0   # no definition to score
    equivalence_hits: int = 0
    admissibility: dict = field(default_factory=dict)  # failure kind -> count (None = admitted)
    wall_s: float = 0.0
    per_candidate_s: float = 0.0
    errors: list[str] = field(default_factory=list)


class ServerHandle:
    """Owns one warm Mathlib server and knows when to replace it.

    Same growth-relative rule as `tests/conftest.py` -- recycle at 1.5x the post-warm baseline
    rather than at a flat GB figure, because a healthy warm server reads ~5.7 GB (Mathlib mmaps
    its `.olean` files and RSS counts those pages), so any absolute cap set from intuition sits
    below the baseline and recycles constantly. Plus a candidate-count belt, because a full pass
    is a far longer server lifetime than any test session that has yet been observed.
    """

    def __init__(self, *, recycle_every: int = cfg.RECYCLE_EVERY_N_CANDIDATES):
        self._server = None
        self._env = None
        self._baseline_gb = None
        self._since_recycle = 0
        self._recycle_every = recycle_every
        self.recycles = 0
        # Counted and surfaced, not merely handled. A nonzero value is the early warning that a
        # run's ERROR population may be contaminated: a mid-run restart invalidates every
        # environment id, so verdicts recorded around one say nothing about their candidates.
        # Free to record; on the box it is the difference between trusting a number and not.
        self.env_probe_fires = 0

    @staticmethod
    def _rss_gb() -> float:
        try:
            import os

            import psutil

            proc = psutil.Process(os.getpid())
            return sum(c.memory_info().rss for c in proc.children(recursive=True)) / (1024**3)
        except Exception:  # noqa: BLE001 -- an unreadable measurement must not force a recycle
            return 0.0

    def _reason_to_recycle(self) -> str | None:
        if self._server is None:
            return "first use"
        try:
            if not self._server.is_alive():
                return "server died"
        except Exception:  # noqa: BLE001
            return "server unresponsive"

        # Liveness alone is not enough: `AutoLeanServer` self-heals by restarting, so it reports
        # alive again while every pre-restart environment id has become invalid ("Unknown
        # environment"). Over a multi-hour pass that would silently turn every subsequent
        # candidate into an ERROR -- a whole run's worth of verdicts that say nothing. A trivial
        # probe against the stored env is sub-millisecond and catches it immediately.
        probe = run_checked(
            self._server, Command(cmd="example : True := trivial", env=self._env), timeout=30.0
        )
        if is_unknown_environment_error(probe.detail or ""):
            self.env_probe_fires += 1
            return "environment invalidated by a server restart"
        if self._since_recycle >= self._recycle_every:
            return f"{self._since_recycle} candidates since last recycle"
        rss = self._rss_gb()
        if rss > cfg.SERVER_ABSOLUTE_CAP_GB:
            return f"RSS {rss:.1f}GB over the {cfg.SERVER_ABSOLUTE_CAP_GB}GB backstop"
        if self._baseline_gb and rss > self._baseline_gb * cfg.SERVER_GROWTH_FACTOR:
            return f"RSS {rss:.1f}GB is {rss / self._baseline_gb:.1f}x baseline"
        return None

    def get(self):
        reason = self._reason_to_recycle()
        if reason is not None:
            self.close()
            print(f"[scoring] fresh Mathlib server ({reason})", file=sys.stderr, flush=True)
            server, imported = get_warm_environment()
            if imported.status is not CheckStatus.PASSED:
                raise RuntimeError(f"could not warm Mathlib: {imported.detail}")
            self._server, self._env = server, imported.env
            self._baseline_gb = self._rss_gb()
            self._since_recycle = 0
            self.recycles += 1
        return self._server, self._env

    def note_candidate(self):
        self._since_recycle += 1

    def close(self):
        if self._server is not None:
            try:
                self._server.kill()
            except Exception:  # noqa: BLE001
                pass
        self._server, self._env, self._baseline_gb = None, None, None


def score_task(
    model_slug: str,
    task_name: str,
    handle: ServerHandle,
    *,
    budgets: LadderBudgets = DEFAULT_LADDER_BUDGETS,
    cache=None,
    scores_dir=None,
    tasks_root=None,
    samples_root=None,
    try_equivalence: bool = True,
    limit: int | None = None,
) -> TaskOutcome:
    """Score every distinct candidate for one (model, task), fanning verdicts out to duplicates."""
    started = time.perf_counter()
    outcome = TaskOutcome(task_name=task_name, model_slug=model_slug)
    task = load_task(task_name, tasks_root=tasks_root)
    samples = load_samples(model_slug, task_name, samples_root=samples_root)
    if limit is not None:
        samples = samples[:limit]

    outcome.unextractable = sum(1 for s in samples if not s.get("extracted_code"))
    groups = dedup.group_by_hash(samples)

    for body_hash, members in groups.items():
        representative = members[0]
        body = representative["extracted_code"]

        if all(
            store.is_complete(model_slug, task_name, m["sample_index"], scores_dir=scores_dir)
            for m in members
        ):
            outcome.skipped += len(members)
            continue

        server, base_env = handle.get()
        handle.note_candidate()
        try:
            payload = score_candidate_body(
                server, base_env, task["signature"], body, task["facts"],
                truth_real_name=task["truth_real_name"] if try_equivalence else None,
                budgets=budgets, cache=cache, imports=task["imports"],
                try_equivalence=try_equivalence,
            )
        except Exception as e:  # noqa: BLE001 -- one candidate must never sink the run
            outcome.errors.append(f"{task_name}/sample_{representative['sample_index']}: {e}")
            continue

        outcome.scored += 1
        kind = payload.get("admissibility_failure") or "admitted"
        outcome.admissibility[kind] = outcome.admissibility.get(kind, 0) + 1
        if payload.get("equivalence_certified"):
            outcome.equivalence_hits += 1

        for member in members:
            record = dict(payload)
            record.update(
                model_slug=model_slug,
                task_name=task_name,
                sample_index=member["sample_index"],
                candidate_hash=body_hash,
                # Provenance: computed for the representative, inherited for the rest. An
                # inherited verdict must never be mistaken for an independent measurement.
                scored_as=None if member is representative else representative["sample_index"],
                extraction_disagreed=member.get("extraction_disagreed", False),
                extracted_code=member.get("extracted_code"),
                temperature=member.get("temperature"),
            )
            store.write_verdict(record, scores_dir=scores_dir)
            if member is not representative:
                outcome.fanned_out += 1

    outcome.wall_s = time.perf_counter() - started
    outcome.per_candidate_s = outcome.wall_s / outcome.scored if outcome.scored else 0.0
    return outcome


def score_model_tasks(
    model_slug: str,
    task_names: list[str],
    *,
    budgets: LadderBudgets = DEFAULT_LADDER_BUDGETS,
    cache=None,
    scores_dir=None,
    tasks_root=None,
    samples_root=None,
    try_equivalence: bool = True,
    limit_per_task: int | None = None,
) -> list[TaskOutcome]:
    """Sequential pass over tasks, sharing one server handle across all of them."""
    handle = ServerHandle()
    outcomes = []
    try:
        for task_name in task_names:
            outcome = score_task(
                model_slug, task_name, handle, budgets=budgets, cache=cache,
                scores_dir=scores_dir, tasks_root=tasks_root, samples_root=samples_root,
                try_equivalence=try_equivalence, limit=limit_per_task,
            )
            outcomes.append(outcome)
            print(
                f"[scoring] {model_slug}/{task_name}: scored={outcome.scored} "
                f"fanned={outcome.fanned_out} skipped={outcome.skipped} "
                f"equiv={outcome.equivalence_hits} {outcome.wall_s:.1f}s "
                f"({outcome.per_candidate_s:.1f}s/cand) adm={outcome.admissibility} "
                f"env_probe_fires={handle.env_probe_fires}",
                file=sys.stderr, flush=True,
            )
    finally:
        handle.close()
    return outcomes
