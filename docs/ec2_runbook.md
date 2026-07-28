# EC2 Hammer Environment Runbook

Rebuild recipe for the rented x86 box that holds LeanHammer working against our pin. Written
so a fresh session — or a fresh box, if this one is ever terminated rather than
stopped/restarted — needs only this file plus valid AWS credentials. See
`docs/design/reward_structure_2026-07-21.md` §3 for why this exists: tier 3 of the adjudication
ladder is LeanHammer, and it needs x86 (bundled Zipperposition binary) and large memory
(premise-selection spikes >30GB) that the dev Mac (ARM) cannot provide.

## Why a rented box, not the Mac

- Hammer's bundled Zipperposition ATP binary is x86-only; Apple Silicon needs Rosetta and the
  LeanHammer README itself warns of "significant slowdown" from process-spawning overhead on
  Mac even with Rosetta.
- Premise selection has memory spikes the dev Mac isn't provisioned for.

## Current instance (as of 2026-07-24)

- Instance `i-009b37b6b652f67dc`, r6i.2xlarge, `eu-west-1`, 150GB gp3 root volume, tag
  `Name=verifier-hammer`.
- Security group `verifier-hammer-sg` (`sg-07dee4fbf43bade67`): SSH/22 only, locked to
  whichever Mac IP was current when last updated — **check/update this before every session**
  (Phase A step 2 below), not just at first creation.
- Key pair `verifier-hammer`, private key at `~/.ssh/verifier-hammer.pem` on the Mac,
  `chmod 400`. Never re-create if it exists on one side but not the other — that means
  something is out of sync; stop and investigate rather than deleting/recreating.
- CloudWatch alarm `verifier-hammer-idle-autostop`: CPUUtilization < 5% for 30 consecutive
  minutes → stop the instance. A safety net, not a substitute for the explicit stop in Phase D.
- AMI lineage: Ubuntu 24.04 LTS amd64, resolved via the SSM public parameter (below) at
  provisioning time — `ami-08c7a4b4f234dfa77` as of 2026-07-24. Re-resolve if rebuilding from
  scratch; Canonical rotates the concrete AMI id under that parameter over time.
- Public IP **changes on every stop/start** (no Elastic IP — deliberately not provisioned, see
  `docs/deferred.md`). Always re-fetch after starting, never assume the last-used IP still
  applies.

---

## Phase A — provision from scratch (only if the instance/key/SG don't already exist)

Skip straight to Phase B if `i-009b37b6b652f67dc` (or its successor) already exists — this
phase is for a full from-scratch rebuild only.

0. `aws sts get-caller-identity` (no `--profile`) — must show the assumed-role ARN in account
   `297433794164`, region `eu-west-1`. If not, reload credentials (see the repo's own
   session-start convention: quit VS Code, `aws sts get-caller-identity --profile verifier`
   with MFA, `eval "$(aws configure export-credentials --profile verifier --format env)"`,
   relaunch VS Code from that terminal).
1. Key pair (only if `~/.ssh/verifier-hammer.pem` doesn't already exist):
   ```
   aws ec2 create-key-pair --key-name verifier-hammer --region eu-west-1 \
     --query 'KeyMaterial' --output text > ~/.ssh/verifier-hammer.pem
   chmod 400 ~/.ssh/verifier-hammer.pem
   ```
2. Security group (create once; update the IP rule every session thereafter):
   ```
   MY_IP=$(curl -s https://checkip.amazonaws.com)
   # create (first time only):
   aws ec2 create-security-group --group-name verifier-hammer-sg \
     --description "SSH access for verifier-hammer EC2 box" --vpc-id <default-vpc-id> \
     --region eu-west-1
   # authorize/update (every session the IP has changed):
   aws ec2 authorize-security-group-ingress --group-id <sg-id> --protocol tcp --port 22 \
     --cidr ${MY_IP}/32 --region eu-west-1
   # if a stale rule exists for the old IP, revoke it first:
   aws ec2 revoke-security-group-ingress --group-id <sg-id> --protocol tcp --port 22 \
     --cidr <old-ip>/32 --region eu-west-1
   ```
3. AMI:
   ```
   aws ssm get-parameter \
     --name /aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id \
     --region eu-west-1 --query 'Parameter.Value' --output text
   ```
4. Launch:
   ```
   aws ec2 run-instances --image-id <ami-id> --instance-type r6i.2xlarge \
     --key-name verifier-hammer --security-group-ids <sg-id> \
     --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":150,"VolumeType":"gp3"}}]' \
     --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=verifier-hammer}]' \
     --region eu-west-1
   aws ec2 wait instance-running --instance-ids <id> --region eu-west-1
   aws ec2 wait instance-status-ok --instance-ids <id> --region eu-west-1
   ```
5. Idle auto-stop alarm (guardrail, not a gate — note in the report if permission-denied and
   continue):
   ```
   aws cloudwatch put-metric-alarm --alarm-name verifier-hammer-idle-autostop \
     --alarm-description "Stop verifier-hammer if CPU < 5% for 30 consecutive minutes" \
     --namespace AWS/EC2 --metric-name CPUUtilization \
     --dimensions Name=InstanceId,Value=<id> --statistic Average --period 300 \
     --evaluation-periods 6 --threshold 5 --comparison-operator LessThanThreshold \
     --alarm-actions arn:aws:automate:eu-west-1:ec2:stop --region eu-west-1
   ```
6. Gate: `ssh -i ~/.ssh/verifier-hammer.pem -o StrictHostKeyChecking=accept-new ubuntu@<ip> 'uname -m'`
   returns `x86_64`.

---

## Phase B — start an existing box and reconnect

```
aws ec2 start-instances --instance-ids i-009b37b6b652f67dc --region eu-west-1
aws ec2 wait instance-running --instance-ids i-009b37b6b652f67dc --region eu-west-1
aws ec2 wait instance-status-ok --instance-ids i-009b37b6b652f67dc --region eu-west-1
aws ec2 describe-instances --instance-ids i-009b37b6b652f67dc --region eu-west-1 \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text
```

Re-check the security group's IP rule against the Mac's *current* public IP (Phase A step 2)
before SSHing — it will be stale if the Mac's IP changed since last session.

```
ssh -i ~/.ssh/verifier-hammer.pem -o StrictHostKeyChecking=accept-new ubuntu@<fresh-ip>
```

---

## Phase C — Lean/Hammer environment (only needed on a genuinely fresh box)

### C.1 — base packages

```
sudo apt-get update && sudo apt-get install -y git curl build-essential unzip
```

**`unzip` is required, not optional** — Hammer's build downloads and unzips two prebuilt
binary bundles (the Zipperposition ATP binary from `sneeuwballen/zipperposition`'s GitHub
releases, and the cvc5 static-library bundle from `abdoo8080/cvc5`'s releases). The base
Ubuntu 24.04 AMI does not include it. Without it, `lake build Hammer` fails with `external
command 'unzip' exited with code 255` on the Zipperposition and cvc5 download steps, and (see
the stale-cache trap below) can leave the box in a state where re-running the build silently
skips the parts that actually needed fixing.

### C.2 — elan (Lean toolchain manager)

```
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y
```

Non-interactive (`-y`). Adds `export PATH="$HOME/.elan/bin:$PATH"` to `~/.profile`
automatically — every subsequent SSH command that needs `lake`/`lean` on PATH must either be a
login shell or explicitly `source ~/.profile` first (non-interactive SSH commands are not login
shells by default).

### C.3 — get the Lean project onto the box

From the Mac, **excluding `.lake/`** (the build cache is huge — ~7GB for this project — and
machine-specific; never sync it):

```
rsync -avz --exclude='.lake/' -e "ssh -i ~/.ssh/verifier-hammer.pem" \
  /Users/henryhayton/definition-verifier/lean/ ubuntu@<ip>:~/verifier-lean/
```

### C.4 — the Hammer lakefile edit (box-local, never the Mac's `lean/lakefile.toml`)

The repo tracks the box's variant at `lean/lakefile.ec2.toml` (see that file's own header
comment). Deploy it by overwriting the synced copy on the box:

```
scp -i ~/.ssh/verifier-hammer.pem /Users/henryhayton/definition-verifier/lean/lakefile.ec2.toml \
  ubuntu@<ip>:~/verifier-lean/lakefile.toml
```

The only structural change from the Mac's `lean/lakefile.toml` is one `[[require]]` block for
Hammer, inserted **before** the `mathlib` require block (documented LeanHammer practice — both
share a dependency on `batteries`, and listing Hammer first avoids an unnecessary Mathlib
recompile):

```toml
[[require]]
name = "Hammer"
git = "https://github.com/JOSHCLUNE/LeanHammer"
rev = "v4.32.0"

[[require]]
name = "mathlib"
scope = "leanprover-community"
rev = "v4.32.0"
```

`v4.32.0` is a real release tag on the Hammer repo (not `main` — the README's own generic
example uses `rev = "main"`, but we pin to the tag matching our toolchain, consistent with
every other pin in this project).

### C.5 — build

```
cd ~/verifier-lean
lake update                 # resolves Hammer + transitive deps (Duper, aesop, lean-smt,
                             # premise-selection, Cli, cvc5, auto); also runs Mathlib's
                             # post-update cache-fetch hook
lake exe cache get          # confirms/completes the Mathlib prebuilt cache (mandatory --
                             # never let a from-source Mathlib build start; it takes hours)
nohup lake build > ~/lake_build.log 2>&1 &   # our project's own default target; long-running,
                                              # survives SSH drops
```

Poll `~/lake_build.log` for `Build completed successfully` or an `error:` line rather than
blocking the SSH session on it.

**Gate:** `lake env lean` can elaborate a file importing Mathlib:
```
printf 'import Mathlib\nexample : (2:Nat) + 2 = 4 := by decide\n' > /tmp/gate_test.lean
lake env lean /tmp/gate_test.lean
```

### C.6 — build Hammer explicitly (do not skip this)

**`lake build`'s default target does not build Hammer.** Our `lakefile.toml`'s
`defaultTargets = ["DefinitionVerifier"]` only builds what our own project transitively
imports, and nothing in `DefinitionVerifier.lean`/`DefinitionVerifier/Basic.lean` imports
`Hammer` — so the Phase C.5 gate above passes fully without Hammer's own library ever being
compiled. This is easy to miss since `lake build` reports "Build completed successfully" with
no hint that an entire required package was skipped. Build it explicitly:

```
nohup lake build Hammer > ~/lake_build_hammer.log 2>&1 &
```

Same polling/nohup discipline as C.5. Expect on the order of 1300+ build jobs (Duper, lean-smt,
premise-selection, Hammer itself, and their C shims).

### The stale-cache trap (encountered, real, not hypothetical)

If a `lake build Hammer` attempt fails partway through a download+extract step (e.g. because
`unzip` was missing, per C.1), **do not assume a clean retry will redo that step correctly.**
Observed failure mode: the download half of the step (a `curl` to fetch a `.zip`) had already
succeeded and left a valid zip file on disk before the `unzip` call failed; on retry (after
installing `unzip`), lake's incremental build tracking treated the step as already
up-to-date (because its tracked output file — the zip — already existed) and **never re-ran
the extraction**, so the build failed again downstream with `no such file or directory` errors
for files that should have come out of that zip (for us: `libcadical.a`, `libcvc5.a`,
`libcvc5parser.a`, `libgmp.a`, `libgmpxx.a`, `libpicpoly.a`, `libpicpolyxx.a` under
`.lake/packages/cvc5/cvc5-Linux-x86_64-static/lib/`).

**Symptom:** `lake build Hammer` fails with `error: no such file or directory (error code:
4294967294)` naming files under an extracted-bundle directory that doesn't exist, even though
the corresponding `.zip` is present and valid (`file <path>.zip` reports "Zip archive data").

**Fix:** don't trust the incremental tracking for that one step — extract the bundle by hand,
then rebuild:
```
cd ~/verifier-lean/.lake/packages/cvc5
unzip -q -d . cvc5-Linux-x86_64-static.zip
cd ~/verifier-lean
nohup lake build Hammer > ~/lake_build_hammer.log 2>&1 &
```
This generalizes: if any other download+extract dependency step fails after a `unzip`-missing
(or similarly transient) first failure, check whether the archive already exists on disk before
assuming a plain retry will re-extract it — it may not.

### C.7 — cvc5 FFI fix (`--load-dynlib`, required for every hammer invocation)

**Symptom:** any goal whose `hammer` search reaches the cvc5/SMT route crashes the whole `lean`
process with SIGABRT: `libc++abi: terminating due to uncaught exception of type
lean::exception: Could not find native implementation of external declaration
'cvc5.TermManager.new' (symbols 'lp_cvc5_cvc5_TermManager_new___boxed' or
'lp_cvc5_cvc5_TermManager_new')`.

**Root cause, confirmed by direct inspection (`nm -D` on every built `.so`, cross-referenced
against where the `extern_def`s actually live in source):**

- `TermManager.new` (and every other cvc5 FFI entry point) is declared via `extern_def` directly
  in the cvc5 package's top-level `cvc5.lean` (`.lake/packages/cvc5/cvc5.lean:360` and
  throughout that file) — not in any of its submodules (`cvc5/{Init,Kind,ProofRule,SkolemId,
  Types}.lean`).
- The cvc5 package's `lakefile.lean` sets `precompileModules := true` and `moreLinkObjs := libs`
  (the downloaded `libcadical.a`/`libcvc5.a`/`libgmp.a`/etc. plus the compiled `ffi.o` FFI glue)
  on the `cvc5` `lean_lib` target. This correctly produces a combined native shared library,
  `.lake/packages/cvc5/.lake/build/lib/libcvc5_cvc5.so` — confirmed to contain the missing
  symbol (`nm -D libcvc5_cvc5.so | grep TermManager_new` finds it).
- But `precompileModules := true` *also* generates a **separate, per-submodule** interpreter
  plugin `.so` for each of the five submodules (`cvc5_cvc5_{Kind,ProofRule,SkolemId,Types,
  Init}.so` under `.lake/build/lib/lean/`) — and critically, **no equivalent plugin `.so` is
  generated for the top-level `cvc5` module itself**, which is the one that actually declares
  the FFI symbols. None of the five submodule plugins contain `TermManager_new` either
  (confirmed empty via the same `nm` search) — they're pure-Lean re-exports/enum wrappers with
  no native code of their own.
- `lake env lean <file>` (plain interpreted-script invocation, not a declared `lean_exe`
  target) has no way to know it needs `libcvc5_cvc5.so` — Lake only auto-wires
  `--load-dynlib`/rpath flags for targets it knows about at build time (declared `lean_exe`s),
  not for ad-hoc script files. So the aggregate `.so` that has the symbol never gets loaded, and
  the interpreter aborts the process outright (not a catchable Lean-level error) the moment it
  hits the first `@[extern]` call.
- This did **not** match a documented upstream issue — checked the `abdoo8080/lean-cvc5`,
  `ufmg-smite/lean-smt`, and `JOSHCLUNE/LeanHammer` issue trackers for this exact error string;
  nothing found. The generic Lean error hint ("set `supportInterpreter := true` in the relevant
  `lean_exe` statement") pointed at the right *mechanism* (interpreter-mode native-symbol
  loading) but not a directly applicable fix, since we have no `lean_exe` of our own in this
  invocation path.

**Fix applied (our own invocation convention — zero changes to any dependency source):** pass
Lean's own `--load-dynlib` flag (`lean --help`: "load shared library to make its symbols
available to the interpreter") pointing at the aggregate `.so`, on every `lake env lean`
invocation that might reach the SMT route (i.e., every hammer smoke-test/goal invocation —
cheap and harmless to include unconditionally even for goals that don't need it):

```
DYNLIB=$(pwd)/.lake/packages/cvc5/.lake/build/lib/libcvc5_cvc5.so
lake env lean --load-dynlib="$DYNLIB" <file>.lean
```

No rebuild was required — `libcvc5_cvc5.so` already existed from the original `lake build
Hammer`; this is purely an invocation-layer fix. **Anyone driving hammer from Python (the real
ladder-worker, eventually) must pass this flag on every subprocess invocation** — it is not
optional and not automatic.

**Secondary, unrelated bug this surfaced:** the original smoke-test goal files only had
`import Hammer`, not `import Mathlib`. Under the SIGABRT, this was invisible — the crash fired
before any "unknown identifier" diagnostics could flush to stdout (fully-buffered stdio when
redirected to a file loses unflushed output on abnormal process termination; stderr's abort
message survived because C++'s `std::cerr`/`libc++abi`'s termination handler write
unbuffered/immediately). Once the crash was fixed, goals referencing Mathlib identifiers
(`Monotone`, etc.) without `import Mathlib` surfaced their *real*, mundane failure: unresolved
identifiers, unrelated to cvc5. Fixed by adding `import Mathlib` to the goal files that need it.

### Versions to confirm after any rebuild

```
lean --version          # must read 4.32.0
```
Hammer's resolved commit is recorded in `~/verifier-lean/lake-manifest.json` under the
`"Hammer"` package entry's `"rev"` field (distinct from `"inputRev"`, which is the tag
`v4.32.0` we requested — `"rev"` is the concrete commit that tag pointed to when resolved).

---

## Phase D — premise selection

No self-hosting setup needed for now: the default is a hosted server at `http://leanpremise.net`
(LeanHammer's own README describes this as intended for individual use, with automatic
caching). `hammer` uses it automatically — no config file, no environment variable, no
box-local server process to start. Confirmed working from this box (goals reaching the
premise-selection/Zipperposition route completed in ~3s each in the first smoke test).

Self-hosting (`hanwenzhu/lean-premise-server`, a separate repo with its own setup) is
deliberately deferred — see `docs/deferred.md`.

---

## Phase E — smoke test

Test files live at `~/verifier-lean/smoke_goals/goal<N>.lean` on the box (recreate them if the
box was rebuilt — see the original smoke-test task for the exact 6 goals, or the follow-up
task for the 7th). Run each with a wall-clock budget rather than relying on any built-in
timeout (Hammer's `by hammer [lemmas] {options}` syntax has no timeout option of its own):

```
cd ~/verifier-lean
DYNLIB=$(pwd)/.lake/packages/cvc5/.lake/build/lib/libcvc5_cvc5.so
timeout 60 lake env lean --load-dynlib="$DYNLIB" smoke_goals/goal1.lean
```

**`--load-dynlib` is required, not optional** — see Phase C.7 above. Without it, any goal whose
`hammer` search reaches the cvc5/SMT route crashes the whole process with SIGABRT instead of
failing gracefully. Every goal file that references Mathlib identifiers also needs its own
`import Mathlib` (not just `import Hammer`) — easy to miss since the SIGABRT (before the fix)
masked this as a separate-looking crash rather than a plain unresolved-identifier error.

Expect real run-to-run timing variance from `hammer` — it's a portfolio search hitting an
external, network-dependent premise-selection server plus multiple solver backends in
parallel/race fashion. One goal (a plain `Monotone (fun n => n + 1)` fact) timed out at the
full 60s budget on one run and proved in 6.5s on an immediate repeat, with no other change.
Don't treat a single timeout as a hard failure without at least one retry.

---

## Phase G — Python/ladder-worker bootstrap (Session B onward)

Separate from Phase C's Lean/Hammer project (`~/verifier-lean/`, left in place, never renamed):
the `ladder/`/`harness/` Python side lives in its own sync target, `~/definition-verifier/`, so
the two never collide and the expensive Hammer build in `~/verifier-lean/.lake/` is never
threatened by a Python-side resync. Every ladder-worker script that touches Lean explicitly
passes `lean_project_dir=~/verifier-lean` (`harness.repl.get_warm_environment`'s own parameter)
and `repo_root=~/verifier-lean` (`ladder.cache.toolchain_pin`'s own parameter) at the call site
-- no source changes needed, both already accept overrides.

### G.1 — sync the Python side

From the Mac, excluding everything Lean/Hammer-specific (that stays in `~/verifier-lean/`),
`bedrock/` (no bedrock work happens on this box, ever), and local-only clutter:

```
rsync -avz \
  --exclude='.git/' --exclude='.venv/' --exclude='__pycache__/' --exclude='.pytest_cache/' \
  --exclude='.ruff_cache/' --exclude='.DS_Store' \
  --exclude='lean/.lake/' --exclude='lean/build/' \
  --exclude='pickles/' --exclude='scratch/' --exclude='bedrock/' --exclude='archive/' \
  --exclude='authoring/' --exclude='tasks/' \
  -e "ssh -i ~/.ssh/verifier-hammer.pem" \
  /Users/henryhayton/definition-verifier/ ubuntu@<ip>:~/definition-verifier/
```

`lean/` is included (minus `.lake/`) purely so `ladder.cache.toolchain_pin()`'s *default*
(no-override) code path has real `lean/lean-toolchain` + `lean/lake-manifest.json` files to
read on box, matching every other test that doesn't pass an explicit `repo_root` -- it is not
built or used as a Lean project on the box; `~/verifier-lean/` is the one that actually runs.

### G.1b — the --load-dynlib resolution (Session B, `docs/deferred.md` fired)

`ladder.tier3`'s hammer calls need the cvc5 FFI fix (Phase C.7) applied to invocations driven
through **LeanInteract**, not just raw `lake env lean` shell calls. Diagnosis, confirmed by
reading the actual source (not assumed): `lean_interact.server.LeanServer.start()` launches the
REPL binary with a hardcoded `Popen` argv (`[lake_path, "env", repl_binary_path]`, no room for
extra flags) -- and even if it could pass extra argv, the REPL project's own `REPL/Main.lean`
(`augustepoiroux/repl`, the fork LeanInteract drives) discards its `args` parameter entirely
(`unsafe def main (_ : List String) : IO Unit`). **No CLI-flag injection path exists through
LeanInteract at all.**

**Fix**: `Lean.loadDynlib` (`Lean/LoadDynlib.lean` in core Lean -- "Equivalent to passing
`--load-dynlib=path` to `lean`", the exact primitive `lean`'s own flag handler calls
internally) is a plain `IO Unit` function, callable directly. `lean/repl_main.ec2.lean` (tracked
in this repo, mirrors `lakefile.ec2.toml`'s own box-local-override convention) is a full
replacement for `REPL/Main.lean` whose `main` calls it, reading the path from the
`LEAN_INTERACT_LOAD_DYNLIB` environment variable (a no-op when unset, so this patched REPL is
safe to use for every ladder tier, not just tier 3):

```
git clone https://github.com/augustepoiroux/repl.git ~/patched-repl
cd ~/patched-repl
git checkout v1.3.18_lean-toolchain-v4.32.0   # the exact per-Lean-version tag LeanInteract
                                                # resolves for our pin -- NOT the bare `v1.3.18`
                                                # tag, which points at a v4.8.0-rc1 toolchain
cp ~/definition-verifier/lean/repl_main.ec2.lean REPL/Main.lean
lake build
```

Python side -- set the env var before constructing the server, and point `local_repl_path` at
the patched checkout:

```python
import os
os.environ["LEAN_INTERACT_LOAD_DYNLIB"] = str(Path.home() / "verifier-lean" / ".lake" /
    "packages" / "cvc5" / ".lake" / "build" / "lib" / "libcvc5_cvc5.so")
config = LeanREPLConfig(
    project=LocalProject(directory=str(Path.home() / "verifier-lean")),
    local_repl_path=str(Path.home() / "patched-repl"),
    build_repl=False,  # already built above
)
```

**Verified empirically (2026-07-27, Session B)**: `Monotone (fun n => n + 1) := by hammer` --
the exact goal that SIGABRTed pre-fix (Phase C.7) -- completed cleanly through this path, driven
from Python, no crash, hammer found a real proof (`apply add_left_mono`).

### G.2 — bootstrap `uv` and the Python env

```
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv python install 3.12
cd ~/definition-verifier && uv sync
```

### G.3 — re-sync after every Mac-side edit

Same `rsync` command as G.1, re-run after any Mac-side change to `ladder/`/`harness/`/`tests/`
before running anything on the box — the box's copy is a snapshot, not live.

### G.4 — box-only test marker convention

New tier-3/tier-4 tests that need the box's Hammer-enabled Lean project are marked
`@pytest.mark.box_only` (registered in `pyproject.toml`'s `[tool.pytest.ini_options]`). The
Mac's regular `uv run pytest` run **deselects** them (`-m "not box_only"`); on the box, the
same tests run with `-m box_only` (or no `-m` filter at all, since the box never runs the
Mac-oriented default-`repo_root` tests that need `~/definition-verifier/lean` to be a *built*
project).

---

## Phase F — shutdown (always end here)

```
aws ec2 stop-instances --instance-ids i-009b37b6b652f67dc --region eu-west-1
aws ec2 wait instance-stopped --instance-ids i-009b37b6b652f67dc --region eu-west-1
```

If AWS credentials expire before this runs, the instance is left running and costs real money
— this must be flagged prominently to the human with the exact command to run, not silently
left for "next time."

---

## Changelog

- **2026-07-24 (smoke test)** — box provisioned, Hammer built, `unzip`-missing and stale-cache
  issues found and fixed, first smoke test run: 2/6 goals proved via the Zipperposition/premise
  route, 2/6 crashed with a cvc5 FFI SIGABRT, 2/6 failed to elaborate (expected — context-
  stripped real Mathlib statements).
- **2026-07-24 (cvc5 FFI fix)** — root cause: `lake env lean` never auto-loads the aggregate
  cvc5 shared library for ad-hoc script interpretation (Phase C.7). Fixed by always passing
  `--load-dynlib=.../libcvc5_cvc5.so`. Re-test: 4/7 goals proved (including the two
  previously-crashing `Monotone`-shaped goals and a new linear-arithmetic goal added to confirm
  cvc5 genuinely proves things when healthy, not merely stops crashing), 1/7 failed gracefully
  with a clean "unsolved goals" message (no crash — a genuinely hard fact, not a defect), 2/7
  still fail elaboration as expected (context-stripped real Mathlib statements, out of scope).
  Zero SIGABRTs.
- **2026-07-27 (Ladder worker Session B)** — Python side bootstrapped (`uv`, Phase G), the
  `--load-dynlib` fix ported to LeanInteract via a patched local REPL checkout (Phase G.1b,
  `lean/repl_main.ec2.lean`), tiers 3-4 made real and wired into `ladder.adjudicate`. Existing
  `~/verifier-lean`/Hammer build reused unchanged (survived the stop/start intact — confirmed
  before doing any rebuild work). One real bug found and fixed during the tier-cascade
  measurement: `#print axioms`'s pretty-printer wraps the axiom list across multiple lines once
  it's long enough, and `_AXIOM_LIST_RE` (both `ladder.axiom_audit` and its duplicate in
  `harness.admissibility`) used `.` without `re.DOTALL`, silently failing to parse wrapped lists
  and demoting genuinely CERTIFIED facts to UNKNOWN — fixed in both places, regression-tested.
  60-statement tier-cascade measurement run: see `docs/tier_cascade_measurement_2026-07.md`.
  **Idle-autostop fired mid-session** (real, not simulated — `verifier-hammer-idle-autostop`,
  ~20 min of Mac-side-only work between box interactions triggered it): confirms the alarm works
  as designed; the box was simply restarted and work continued, IP re-fetched, no data lost
  (`~/verifier-lean`/`~/patched-repl` persisted on the EBS volume through the stop/start).
