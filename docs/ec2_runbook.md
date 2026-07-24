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

### C.7 — cvc5 FFI fix

<!-- Filled in by the 2026-07-24 follow-up task (cvc5 SIGABRT fix). See that task's report /
     this file's own changelog for what was found and applied. Placeholder kept here so a
     from-scratch rebuild knows a fix step exists at this point in the sequence, even before
     reading the details below. -->

**[to be completed by Part 2/3 of this task below]**

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
timeout 60 lake env lean smoke_goals/goal1.lean
```

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
