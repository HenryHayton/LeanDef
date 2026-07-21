"""REPL session management, warm-environment setup, and the timeout/watchdog layer.

Every REPL interaction in this package goes through `run_checked` (single command, timeout +
one retry) or `start_server_with_watchdog` (server construction, timeout + one retry). Neither
existed anywhere in the codebase before this module -- see `docs/repo_audit.md` observation 2:
no call site anywhere ever passed a timeout, and a genuine multi-minute hang during this
project's own `archive/n1_tau/` work had to be killed by hand.

Output from any diagnostic prints in this module is flushed immediately (`flush=True`) rather
than left to Python's default buffering, since buffered output previously masked how far a
stuck process had actually gotten while debugging that hang.
"""

import concurrent.futures
import os
import time
from pathlib import Path

import psutil
from lean_interact import AutoLeanServer, Command, LeanREPLConfig, LocalProject
from lean_interact.interface import BaseREPLQuery, LeanError

from harness import config as cfg
from harness.results import CheckResult, CheckStatus


class WarmupTimeoutError(RuntimeError):
    """Raised when LeanREPLConfig/AutoLeanServer setup didn't complete within the warmup
    timeout, even after one retry against a freshly-cleared process tree."""


def _kill_stray_children(wait_timeout: float = 5.0) -> list[int]:
    """Kill every child process of the current process.

    Used to recover from a stuck `LeanREPLConfig` setup call. `LeanREPLConfig.__init__` has
    no timeout parameter of its own and blocks on internal `git`/`lake` subprocess calls with
    no limit -- this is exactly the call that hung for 20+ minutes during this project's own
    calibration work and had to be killed by hand (see `docs/repo_audit.md` observation 2).
    Mirrors that manual recovery: find every child of our own process and kill it, the same
    way `lean_interact.server.LeanServer.kill()` kills the REPL subprocess and its children.
    """
    me = psutil.Process(os.getpid())
    children = me.children(recursive=True)
    pids = [c.pid for c in children]
    for child in children:
        try:
            child.kill()
        except psutil.NoSuchProcess:
            pass
    if children:
        psutil.wait_procs(children, timeout=wait_timeout)
    return pids


def _build_server(lean_project_dir: Path, max_total_memory: float, verbose: bool) -> AutoLeanServer:
    lean_config = LeanREPLConfig(project=LocalProject(directory=str(lean_project_dir)), verbose=verbose)
    return AutoLeanServer(lean_config, max_total_memory=max_total_memory)


def start_server_with_watchdog(
    lean_project_dir: Path | None = None,
    max_total_memory: float | None = None,
    warmup_timeout: float | None = None,
    verbose: bool = False,
) -> AutoLeanServer:
    """Build a `LeanREPLConfig` + `AutoLeanServer`, bounding the otherwise-unbounded setup
    call to `warmup_timeout` seconds. On timeout: kill every stray child process, retry once
    from scratch. If the retry also exceeds the timeout, raises `WarmupTimeoutError` rather
    than hanging forever.

    Implementation note: `LeanREPLConfig`'s internal subprocess calls give us no handle to
    cancel them directly, so the construction runs in a background thread and we bound it
    with `Future.result(timeout=...)`. A timed-out thread cannot be forcibly stopped by
    Python, but killing the subprocess it's blocked on (`_kill_stray_children`) makes its
    blocking call raise and the thread exit shortly after; we don't wait for that to happen
    before starting the retry.
    """
    lean_project_dir = lean_project_dir if lean_project_dir is not None else cfg.LEAN_PROJECT_DIR
    max_total_memory = max_total_memory if max_total_memory is not None else cfg.MAX_TOTAL_MEMORY
    warmup_timeout = warmup_timeout if warmup_timeout is not None else cfg.DEFAULT_WARMUP_TIMEOUT

    last_error: BaseException | None = None
    for attempt in range(2):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        future = executor.submit(_build_server, lean_project_dir, max_total_memory, verbose)
        try:
            server = future.result(timeout=warmup_timeout)
            executor.shutdown(wait=False)
            return server
        except concurrent.futures.TimeoutError as e:
            last_error = e
            print(
                f"[harness.repl] warmup exceeded {warmup_timeout}s on attempt {attempt + 1}/2; "
                "killing stray subprocesses" + (" and retrying" if attempt == 0 else " -- giving up"),
                flush=True,
            )
            executor.shutdown(wait=False)
            _kill_stray_children()
        except Exception as e:  # pragma: no cover - defensive
            last_error = e
            executor.shutdown(wait=False)
            break

    raise WarmupTimeoutError(
        f"LeanREPLConfig/AutoLeanServer setup did not complete within {warmup_timeout}s "
        f"(after one retry). Last error: {last_error!r}"
    )


def run_checked(
    server: AutoLeanServer,
    request: BaseREPLQuery,
    timeout: float | None = None,
    retries: int = 1,
) -> CheckResult:
    """Run a single REPL request with a timeout and (by default) one retry.

    `lean_interact`'s per-call `timeout=` already kills the underlying REPL subprocess on
    timeout (`LeanServer.run_dict`), and `AutoLeanServer` self-heals on the *next* call
    because it checks `is_alive()` and restarts if needed -- that's what makes "retry the
    call" meaningful without any extra bookkeeping here. If the retry also fails (timeout,
    connection error, an unparseable `LeanError` response, or any other unexpected
    exception), the check is recorded as ERRORED rather than silently folded into FAILED or
    left to raise and stall the batch.

    Caveat, documented rather than hidden: if the server actually died and restarted, every
    environment id from before the restart (base env, any spliced candidate env) is gone.
    Retrying the *same* request against the fresh server will itself fail fast (the REPL
    reports an unknown environment) rather than hang again, so this still satisfies "a single
    wedged call must never stall a batch" -- but it does not transparently recover the lost
    warm state. Recovering full context (re-import, re-splice) after a mid-run crash is not
    implemented; out of scope for this task.
    """
    timeout = timeout if timeout is not None else cfg.DECIDE_TIMEOUT
    attempts_left = 1 + max(retries, 0)
    last_detail = ""

    for attempt in range(attempts_left):
        start = time.perf_counter()
        try:
            response = server.run(request, timeout=timeout)
        except (TimeoutError, ConnectionAbortedError, ChildProcessError) as e:
            elapsed = time.perf_counter() - start
            last_detail = f"{type(e).__name__}: {e}"
            if attempt == attempts_left - 1:
                return CheckResult(status=CheckStatus.ERRORED, elapsed_s=elapsed, detail=last_detail)
            continue
        except Exception as e:  # pragma: no cover - defensive catch-all
            elapsed = time.perf_counter() - start
            last_detail = f"unexpected {type(e).__name__}: {e}"
            if attempt == attempts_left - 1:
                return CheckResult(status=CheckStatus.ERRORED, elapsed_s=elapsed, detail=last_detail)
            continue

        elapsed = time.perf_counter() - start
        if isinstance(response, LeanError):
            last_detail = f"LeanError: {response.message}"
            if attempt == attempts_left - 1:
                return CheckResult(status=CheckStatus.ERRORED, elapsed_s=elapsed, detail=last_detail)
            continue

        status = CheckStatus.FAILED if response.has_errors() else CheckStatus.PASSED
        detail = "; ".join(m.data for m in response.get_errors()) if status is CheckStatus.FAILED else ""
        return CheckResult(
            status=status, elapsed_s=elapsed, detail=detail,
            env=getattr(response, "env", None), raw_response=response,
        )

    return CheckResult(status=CheckStatus.ERRORED, elapsed_s=0.0, detail=last_detail)  # pragma: no cover


def warm_import(
    server: AutoLeanServer,
    imports: list[str] | None = None,
    timeout: float | None = None,
) -> CheckResult:
    """Send the task's import list as a single cold command, establishing the base warm
    environment every candidate will be spliced against. Generalizes the single hardcoded
    `"import Mathlib"` used throughout the codebase before this package (see
    `docs/repo_audit.md` §4, "Import list")."""
    imports = imports if imports is not None else ["Mathlib"]
    timeout = timeout if timeout is not None else cfg.DEFAULT_WARMUP_TIMEOUT
    cmd = "\n".join(f"import {module}" for module in imports)
    return run_checked(server, Command(cmd=cmd), timeout=timeout, retries=1)


def get_warm_environment(
    lean_project_dir: Path | None = None,
    imports: list[str] | None = None,
    max_total_memory: float | None = None,
    warmup_timeout: float | None = None,
    verbose: bool = False,
) -> tuple[AutoLeanServer, CheckResult]:
    """Build a server and import the task's dependencies in one call.

    Returns `(server, import_result)`; `import_result.env` is the base environment id every
    candidate should be spliced against. Raises `WarmupTimeoutError` if server construction
    itself doesn't complete in time. Does not raise if the import command times out --
    returns an ERRORED `import_result` instead, so the caller decides how to handle it.
    """
    server = start_server_with_watchdog(
        lean_project_dir=lean_project_dir,
        max_total_memory=max_total_memory,
        warmup_timeout=warmup_timeout,
        verbose=verbose,
    )
    import_result = warm_import(server, imports=imports, timeout=warmup_timeout)
    return server, import_result
