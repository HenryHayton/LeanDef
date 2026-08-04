"""Find and (on request) kill ORPHANED Lean REPL servers.

Fills the gap `harness.repl._kill_stray_children` structurally cannot: that function reaps
children of the *current* process, which is exactly the set that no longer exists once the
owning Python process has been killed. An orphaned REPL reparents to launchd/init and keeps its
full ~2.5 GB resident forever. On 2026-08-04 six of them reached 15.8 GB of a 16 GB machine and
forced a hard restart.

    uv run python scripts/reap_repls.py            # LIST only -- never kills
    uv run python scripts/reap_repls.py --kill     # actually kill what was listed

**Listing is the default and killing requires an explicit flag.** This will eventually run on a
box hosting several legitimate concurrent scoring workers, where killing a live worker's server
would destroy hours of work.

Two conditions must BOTH hold before a process is even a candidate, which is what makes that
safe:

1. **It is a lean_interact REPL.** Its command line names a `repl` binary living under a
   `lean_interact` cache directory (`.../lean_interact/cache/.../build/bin/repl`), or it is the
   `lake env <that binary>` wrapper. Matching the bare string "repl" is explicitly not enough --
   `replayd` is a normal macOS process, and this repo's own directories are full of the word.
2. **It is orphaned.** Its parent is PID 1 (launchd on macOS, init/systemd on Linux) or its
   parent no longer exists. A live worker's server is a child of that worker's live Python
   process, so it can never match. This is the condition that makes the tool safe to run on a
   busy box, and it is deliberately not overridable by a flag.

Killing takes the whole subtree of each orphan, parent-first-then-children, because `lake env
repl` means the orphan may be the `lake` wrapper with the real REPL as its child -- reaping only
the wrapper would leave the memory behind, which is the entire problem this exists to solve.
"""

import argparse
import os
import sys

import psutil

# Path fragments that together identify a lean_interact-managed REPL. Both must appear in the
# process's command line: the package's cache directory AND the binary name.
_CACHE_MARKER = os.path.join("lean_interact", "cache")
_BINARY_MARKER = "repl"


def _cmdline(proc: psutil.Process) -> str:
    try:
        return " ".join(proc.cmdline())
    except (psutil.Error, OSError):
        return ""


def _is_lean_repl(proc: psutil.Process) -> bool:
    """Condition 1: this is a lean_interact REPL process, not merely something named 'repl'."""
    cmd = _cmdline(proc)
    if _CACHE_MARKER not in cmd:
        return False
    # The binary marker must appear as a path component, not as a substring of some longer
    # word -- `.../build/bin/repl` qualifies, a directory merely called `replay` does not.
    return any(part == _BINARY_MARKER or part.endswith(os.sep + _BINARY_MARKER) for part in cmd.split())


def _is_orphan(proc: psutil.Process) -> bool:
    """Condition 2: reparented to init/launchd, or its parent is already gone.

    A REPL owned by a live worker has that worker's Python process as its parent and therefore
    never satisfies this. Not overridable -- it is the whole safety story.
    """
    try:
        ppid = proc.ppid()
    except (psutil.Error, OSError):
        return False
    if ppid == 1:
        return True
    return not psutil.pid_exists(ppid)


def find_orphans() -> list[psutil.Process]:
    orphans = []
    for proc in psutil.process_iter(["pid", "ppid"]):
        try:
            if proc.pid == os.getpid():
                continue
            if _is_lean_repl(proc) and _is_orphan(proc):
                orphans.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return orphans


def _rss_gb(proc: psutil.Process) -> float:
    """RSS of the process plus its children -- an orphaned `lake env repl` wrapper holds almost
    nothing itself while its REPL child holds the gigabytes."""
    try:
        total = proc.memory_info().rss
        for child in proc.children(recursive=True):
            try:
                total += child.memory_info().rss
            except (psutil.Error, OSError):
                pass
        return total / (1024**3)
    except (psutil.Error, OSError):
        return 0.0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--kill", action="store_true", help="actually kill (default is to list only)")
    parser.add_argument("--timeout", type=float, default=5.0, help="seconds to wait for each kill")
    args = parser.parse_args()

    orphans = find_orphans()
    if not orphans:
        print("no orphaned Lean REPL servers found")
        return 0

    reclaimable = sum(_rss_gb(p) for p in orphans)
    print(f"{len(orphans)} orphaned Lean REPL process(es), holding ~{reclaimable:.2f} GB:\n")
    for proc in orphans:
        print(f"  pid={proc.pid:<8} ppid={proc.ppid():<6} rss={_rss_gb(proc):.2f}GB")
        print(f"    {_cmdline(proc)[:160]}")

    if not args.kill:
        print("\nLISTED ONLY. Re-run with --kill to terminate these.")
        return 0

    victims: list[psutil.Process] = []
    for proc in orphans:
        # Children first in the list, but kill parent-first below so the wrapper cannot respawn.
        try:
            victims.extend([proc, *proc.children(recursive=True)])
        except (psutil.Error, OSError):
            victims.append(proc)

    killed = 0
    for proc in victims:
        try:
            proc.kill()
            killed += 1
        except psutil.NoSuchProcess:
            pass  # already gone -- a child died with its parent
        except psutil.AccessDenied:
            print(f"  ! access denied killing pid={proc.pid}", file=sys.stderr)
    psutil.wait_procs(victims, timeout=args.timeout)

    survivors = [p for p in victims if p.is_running()]
    print(f"\nkilled {killed} process(es), reclaimed ~{reclaimable:.2f} GB")
    if survivors:
        print(f"WARNING: {len(survivors)} still running: {[p.pid for p in survivors]}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
