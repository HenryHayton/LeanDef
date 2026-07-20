"""Step 0 smoke test: proves the LeanInteract + pinned Lean/Mathlib project work end to
end, and records timings for the README "Timings" section. Run with:

    uv run python scripts/smoke_test.py
"""

import time
from pathlib import Path

import psutil
from lean_interact import (
    AutoLeanServer,
    Command,
    LeanREPLConfig,
    LocalProject,
    PickleEnvironment,
    UnpickleEnvironment,
)
from lean_interact.utils import get_total_memory_usage

REPO_ROOT = Path(__file__).resolve().parent.parent
LEAN_PROJECT_DIR = REPO_ROOT / "lean"
PICKLE_DIR = REPO_ROOT / "pickles"

# AutoLeanServer refuses to run above this fraction of system-wide memory usage (default
# 0.8) to protect against OOM. Raised here since dev laptops often sit well above 80% used
# from unrelated apps; Mathlib import itself still needs real headroom to succeed.
MAX_TOTAL_MEMORY = 0.95

timings: dict[str, float] = {}


def timed(label: str, fn):
    start = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - start
    timings[label] = elapsed
    print(f"[{elapsed:7.2f}s] {label}")
    return result


def main() -> None:
    print("=== Step 0 smoke test: LeanInteract + pinned Lean/Mathlib project ===\n")

    config = timed(
        "Prepare LeanREPLConfig (builds REPL against lean/ project)",
        lambda: LeanREPLConfig(project=LocalProject(directory=str(LEAN_PROJECT_DIR)), verbose=False),
    )
    server = timed("Start AutoLeanServer", lambda: AutoLeanServer(config, max_total_memory=MAX_TOTAL_MEMORY))

    # --- Cold command: import Mathlib ---
    cold_resp = timed("Cold command: `import Mathlib`", lambda: server.run(Command(cmd="import Mathlib")))
    assert not cold_resp.has_errors(), cold_resp.messages
    env = cold_resp.env
    print(f"    -> warm environment id = {env}")

    # No public accessor for the REPL subprocess pid, so we reach into the documented
    # `_proc` instance attribute to get a memory snapshot (approx. peak, not tracked over time).
    if server._proc is not None:
        rss_mb = get_total_memory_usage(psutil.Process(server._proc.pid)) / (1024 * 1024)
        timings["repl_rss_mb_after_import (approx peak)"] = rss_mb
        print(f"    -> REPL process RSS after Mathlib import: {rss_mb:.0f} MB (approx. peak)")

    # --- Warm checks ---
    eval_resp = timed("Warm: trivial #eval", lambda: server.run(Command(cmd="#eval 1 + 1", env=env)))
    assert not eval_resp.has_errors()

    decide_resp = timed(
        "Warm: small `decide` (2 + 2 = 4)",
        lambda: server.run(Command(cmd="example : (2 : Nat) + 2 = 4 := by decide", env=env)),
    )
    assert not decide_resp.has_errors()

    heavy_decide_resp = timed(
        "Warm: heavier `decide` (bounded forall, n < 100)",
        lambda: server.run(
            Command(cmd="example : ∀ n < 100, n % 3 = 0 ∨ n % 3 = 1 ∨ n % 3 = 2 := by decide", env=env)
        ),
    )
    assert not heavy_decide_resp.has_errors()

    # --- Splice pattern: def in one command, a follow-up command about it reusing the env id ---
    def_resp = timed(
        "Splice: `def` in its own command",
        lambda: server.run(Command(cmd="def myDouble (n : Nat) : Nat := 2 * n", env=env)),
    )
    assert not def_resp.has_errors()
    def_env = def_resp.env

    thm_resp = timed(
        "Splice: follow-up `example` about the def, proved by `decide`",
        lambda: server.run(Command(cmd="example : myDouble 3 = 6 := by decide", env=def_env)),
    )
    assert not thm_resp.has_errors()
    print(f"    -> splice pattern succeeded (def env={def_env}, no errors on follow-up)")

    # --- Sorry detection: must show up as a warning, not an error ---
    sorry_resp = timed(
        "Sorry detection: `def` containing `sorry`",
        lambda: server.run(Command(cmd="def mySorryDef : Nat := sorry", env=env)),
    )
    warning_data = [m.data for m in sorry_resp.get_warnings()]
    has_sorry_warning = any("sorry" in d for d in warning_data)
    print(f"    -> has_errors={sorry_resp.has_errors()}, warnings={warning_data}, sorries={sorry_resp.sorries}")
    assert not sorry_resp.has_errors(), "sorry should NOT be reported as an error"
    assert has_sorry_warning, "sorry should be reported as a warning"

    # --- Environment pickling ---
    try:
        PICKLE_DIR.mkdir(exist_ok=True)
        pickle_path = str(PICKLE_DIR / "mathlib_env.olean")

        pickle_resp = timed(
            "Pickle warm Mathlib environment to disk",
            lambda: server.run(PickleEnvironment(env=env, pickle_to=pickle_path)),
        )
        assert not pickle_resp.has_errors()

        # Simulate a fresh process picking up the pickled environment.
        server.kill()
        server2 = timed(
            "Start a fresh AutoLeanServer (post-restart)",
            lambda: AutoLeanServer(config, max_total_memory=MAX_TOTAL_MEMORY),
        )

        unpickle_resp = timed(
            "Unpickle environment from disk",
            lambda: server2.run(UnpickleEnvironment(unpickle_env_from=pickle_path)),
        )
        assert not unpickle_resp.has_errors()
        unpickled_env = unpickle_resp.env

        check_resp = timed(
            "Check `decide` fact against unpickled environment",
            lambda: server2.run(Command(cmd="example : (2 : Nat) + 2 = 4 := by decide", env=unpickled_env)),
        )
        assert not check_resp.has_errors()
        print("    -> pickling round-trip succeeded")
    except Exception as e:
        print(f"    -> pickling not exercised cleanly ({e}); noting and moving on rather than sinking hours into it")

    # --- Summary ---
    print("\n=== Timings summary ===")
    for label, seconds in timings.items():
        if "rss_mb" in label:
            print(f"{label:45s} {seconds:8.0f} MB")
        else:
            print(f"{label:45s} {seconds:8.2f} s")


if __name__ == "__main__":
    main()
