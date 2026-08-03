#!/usr/bin/env python3
"""Run a command on the RunPod pod over its SSH proxy, from a non-interactive context.

RunPod's `ssh.runpod.io` proxy refuses connections without a PTY ("Your SSH client doesn't
support PTY"), and an automation shell has no controlling terminal to give it: `ssh -t` declines
("stdin is not a terminal"), `ssh -tt` hangs, and `script` cannot attach because stdout is a
socket. So this allocates a real PTY with `pty.openpty()` and runs ssh against it -- which is
what the proxy actually wants -- while still capturing output programmatically.

Usage:
    python3 scripts/podssh.py 'command to run on the pod'
    python3 scripts/podssh.py --timeout 600 'long command'
    python3 scripts/podssh.py --put LOCAL REMOTE      # transfer a file (base64, sha256-verified)

The pod target is read from $POD_SSH_TARGET (e.g. jp244e0qdworad-64411275@ssh.runpod.io).
Exit code is the remote command's, where recoverable.
"""

import argparse
import base64
import hashlib
import os
import pty
import re
import select
import subprocess
import sys
import time
from pathlib import Path

SSH_OPTS = [
    # `-t` is required even though stdin is a real PTY: ssh does not REQUEST a remote pty when
    # invoked with a command argument, and RunPod's proxy rejects any session without one.
    "-t",
    "-o", "StrictHostKeyChecking=no",
    "-o", "UserKnownHostsFile=/dev/null",
    "-o", "LogLevel=ERROR",
    "-o", "ConnectTimeout=20",
    "-o", "ServerAliveInterval=15",
    "-o", "ServerAliveCountMax=4",
    "-i", os.path.expanduser("~/.ssh/id_ed25519"),
]

# Marker wrapping so we can separate the remote command's real output from the proxy's own
# banner/MOTD noise and from PTY echo of the command line itself.
BEGIN = "___POD_BEGIN___"
END = "___POD_END___"


def target() -> str:
    t = os.environ.get("POD_SSH_TARGET", "").strip()
    if not t:
        sys.exit("POD_SSH_TARGET is not set (e.g. jp244e0qdworad-64411275@ssh.runpod.io)")
    return t


_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]|\x1b\][^\x07]*\x07|\x1b[=>]")


def _clean(text: str) -> str:
    return _ANSI_RE.sub("", text.replace("\r\n", "\n").replace("\r", ""))


def run_remote(command: str, timeout: float = 120.0, quiet: bool = False,
               secret: bool = False) -> tuple[int, str]:
    """Run `command` on the pod and return (exit_code, cleaned_output).

    RunPod's proxy DISCARDS any command passed as an ssh argument and always drops the session
    into an interactive login shell, so the command is typed into that shell's stdin instead and
    delimited by markers. Everything before BEGIN (RunPod's ASCII-art banner, the shell prompt,
    the PTY's echo of what we typed) is discarded; the exit status rides back on the END marker.
    """
    master, slave = pty.openpty()
    proc = subprocess.Popen(
        ["ssh", *SSH_OPTS, target()],
        stdin=slave, stdout=slave, stderr=slave, close_fds=True,
    )
    os.close(slave)

    chunks: list[bytes] = []
    deadline = time.time() + timeout
    sent = False
    settled = time.time() + 4.0  # let the banner/prompt arrive before typing

    while True:
        if time.time() > deadline:
            chunks.append(b"\n[podssh] TIMEOUT\n")
            break
        try:
            ready, _, _ = select.select([master], [], [], 0.5)
        except (OSError, ValueError):
            break

        if not sent and time.time() >= settled:
            # `secret=True` disables the REMOTE pty's echo before the command is typed, so a
            # command carrying a credential never comes back down the wire and therefore never
            # reaches our captured output, the transcript, or a log. Echo is restored after.
            # (Disabling echo locally would not help: what we see echoed is the remote
            # interactive shell rendering the line, not our own pty.)
            if secret:
                os.write(master, b" stty -echo\n")
                time.sleep(0.4)
            os.write(master, f" echo {BEGIN}\n".encode())
            os.write(master, f" {{ {command} ; }} 2>&1\n".encode())
            os.write(master, f" echo {END}:$?\n".encode())
            if secret:
                time.sleep(0.4)
                os.write(master, b" stty echo\n")
            sent = True

        if ready:
            try:
                data = os.read(master, 65536)
            except OSError:
                break
            if not data:
                break
            chunks.append(data)
            if not quiet:
                sys.stdout.write(_clean(data.decode("utf-8", "replace")))
                sys.stdout.flush()
            if END in _clean(b"".join(chunks).decode("utf-8", "replace")):
                break
        elif proc.poll() is not None:
            break

    try:
        os.write(master, b" exit\n")
        time.sleep(0.3)
    except OSError:
        pass
    proc.kill()
    try:
        os.close(master)
    except OSError:
        pass
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        pass

    raw = _clean(b"".join(chunks).decode("utf-8", "replace"))
    code = 0
    if BEGIN in raw:
        # Take the LAST occurrence: the first is the PTY echoing our own `echo BEGIN` line back.
        raw = raw.rsplit(BEGIN, 1)[1]
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw
    if END in raw:
        body, _, tail = raw.split(END)[0], "", raw.rsplit(END, 1)[1]
        raw = body
        try:
            code = int(tail.lstrip(":").split()[0])
        except (ValueError, IndexError):
            code = 0
    # Drop the trailing echo of the `echo END` line itself.
    lines = [ln for ln in raw.split("\n") if END not in ln and BEGIN not in ln]
    return code, "\n".join(lines).strip("\n")


def put_file(local: Path, remote: str, *, chunk: int = 40000, timeout: float = 180.0) -> bool:
    """Copy a local file to the pod. scp/sftp are not available through the PTY-only proxy, so
    the content goes as base64 in shell commands and is verified by sha256 afterwards -- a
    silently truncated bootstrap would be far worse than a failed transfer."""
    data = local.read_bytes()
    want = hashlib.sha256(data).hexdigest()
    b64 = base64.b64encode(data).decode()
    print(f"[podssh] sending {local} -> {remote}  ({len(data)} bytes, sha256 {want[:12]}...)")

    code, _ = run_remote(f"rm -f {remote}.b64 {remote}", timeout=30, quiet=True)
    parts = [b64[i:i + chunk] for i in range(0, len(b64), chunk)]
    for n, part in enumerate(parts, 1):
        code, out = run_remote(f"printf '%s' '{part}' >> {remote}.b64", timeout=timeout, quiet=True)
        if code != 0:
            print(f"[podssh] chunk {n}/{len(parts)} failed: {out}")
            return False
        print(f"[podssh]   chunk {n}/{len(parts)} ok")

    code, out = run_remote(
        f"base64 -d {remote}.b64 > {remote} && rm -f {remote}.b64 && sha256sum {remote}",
        timeout=60, quiet=True,
    )
    got = ""
    for tok in out.split():
        if len(tok) == 64 and all(c in "0123456789abcdef" for c in tok):
            got = tok
            break
    if got == want:
        print(f"[podssh] transfer verified: sha256 matches ({want[:12]}...)")
        return True
    print(f"[podssh] CHECKSUM MISMATCH -- wanted {want}, got {got or out!r}")
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", nargs="?", default=None)
    ap.add_argument("--timeout", type=float, default=120.0)
    ap.add_argument("--put", nargs=2, metavar=("LOCAL", "REMOTE"))
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--secret", action="store_true",
                    help="disable remote echo; for commands carrying a credential")
    ap.add_argument("--stdin-cmd", action="store_true",
                    help="read the command from stdin so it never appears in argv/ps")
    args = ap.parse_args()

    if args.put:
        return 0 if put_file(Path(args.put[0]), args.put[1], timeout=args.timeout) else 1
    cmd = sys.stdin.read() if args.stdin_cmd else args.command
    if not cmd:
        ap.error("give a command, --stdin-cmd, or --put")
    code, out = run_remote(cmd, timeout=args.timeout,
                           quiet=args.quiet or args.secret, secret=args.secret)
    if args.secret:
        print("[podssh] secret command completed (output suppressed by design)")
    elif args.quiet:
        print(out)
    return code


if __name__ == "__main__":
    sys.exit(main())
