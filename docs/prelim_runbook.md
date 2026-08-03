# Prelim testing — overnight run runbook

**What this does:** generates 7 open models × 41 task dossiers × 10 samples = **2,870 definitions**,
to pick the base model for training. One GPU pod, one evening of setup, unattended overnight.

**Expected:** ~4–6 pod-hours, **$6–10**. Two independent auto-terminations protect the meter.

Everything below is copy-paste. Read step 3's eyeball checklist carefully — it is the only
human judgement in the whole process, and it is what stops a bad night.

---

## Step 0 — Before you start (Mac, 2 min)

```bash
cd /Users/henryhayton/definition-verifier
uv run python scripts/prelim_dry_run.py
```

Must end with `DRY RUN PASSED`. If it does not, **stop** — do not rent a pod.

---

## Step 1 — Deploy the pod (RunPod web, ~5 min)

1. RunPod → **Secure Cloud** → **Deploy**.
2. GPU: **1× A100 80GB** (H100 80GB is fine if the same price or cheaper — both fit every model
   comfortably; 80GB is chosen so an 8B model at 8k context never comes near the limit).
3. Template: **PyTorch** (any recent CUDA 12.x image).
4. **Volume: 100 GB** mounted at `/workspace`. Seven models at ~15 GB each will not all be
   resident at once, but HF caches them as it goes and 100 GB avoids a mid-night disk-full.
5. **Expose HTTP ports: `8000,8001`.**
6. Deploy. Then copy down:
   - **Pod ID** (the short id in the dashboard, e.g. `a1b2c3d4e5`)
   - **Port 8000 proxy URL** → looks like `https://<podid>-8000.proxy.runpod.net`
   - **Port 8001 proxy URL** → looks like `https://<podid>-8001.proxy.runpod.net`
7. Get an API key: RunPod → Settings → **API Keys** → create (read+write). Needed for
   self-termination.

---

## Step 2 — Bootstrap the pod (Mac, then pod web terminal, ~10 min)

On the **Mac**, build the paste-ready bootstrap with your key and pod id baked in:

```bash
cd /Users/henryhayton/definition-verifier
uv run python scripts/make_pod_bundle.py \
  --key 'YOUR_RUNPOD_API_KEY' \
  --pod-id 'YOUR_POD_ID' | pbcopy
```

That is now on your clipboard. Open the pod's **web terminal** and:

```bash
cat > /workspace/bootstrap.sh   # then paste (Cmd-V), then press Ctrl-D
bash /workspace/bootstrap.sh
```

vLLM install takes several minutes. You should end up seeing the first model start downloading.
Watch it:

```bash
tail -f /workspace/pod_runner.log
```

Wait until the log shows vLLM has finished loading the **first** model
(`Goedel-LM/Goedel-Prover-V2-8B`) — look for vLLM's own "Application startup complete" or an
`Uvicorn running on http://0.0.0.0:8000` line. First model includes a ~16 GB download; **allow
5–10 minutes**.

Confirm from the pod terminal:

```bash
curl -s localhost:8001/status
curl -s localhost:8000/v1/models
```

The second must list `Goedel-LM/Goedel-Prover-V2-8B`.

---

## Step 3 — Smoke test (Mac, ~3 min) — **THE GO/NO-GO GATE**

```bash
cd /Users/henryhayton/definition-verifier
export PRELIM_ENDPOINT_URL='https://YOUR_POD_ID-8000.proxy.runpod.net/v1/chat/completions'
export PRELIM_CONTROL_URL='https://YOUR_POD_ID-8001.proxy.runpod.net'

# Reachability first — should print the model id:
curl -s "https://YOUR_POD_ID-8000.proxy.runpod.net/v1/models" | head -c 300; echo
```

Then the smoke run — **1 task × 1 sample × all 7 models**, advancing the pod through every model:

```bash
uv run python -m prelim.driver --smoke \
  --control-url "$PRELIM_CONTROL_URL" \
  --models-url "https://YOUR_POD_ID-8000.proxy.runpod.net/v1/models"
```

This takes ~10–20 minutes: it loads each of the 7 models once (that is the point — it proves
every model in the list actually serves).

### Eyeball checklist — do this, do not skip it

```bash
for f in prelim_testing/output/samples/*/Nat.clog/sample_00.json; do
  echo "=============================================================="
  uv run python -c "
import json,sys; d=json.load(open('$f'))
print(d['model_slug'], '| finish:', d['finish_reason'], '| extract_ok:', d['extra'].get('extraction_ok'))
print('--- completion (first 600 chars) ---')
print((d['completion'] or '')[:600])
"
done
```

For **each of the 7 models**, the sample is **plausible** if ALL of:

- [ ] it is **not empty** and not a refusal ("I can't", "I'm sorry", "As an AI")
- [ ] it contains the token **`def`** (or `abbrev`/`instance`)
- [ ] it contains **`:=`**
- [ ] it mentions **`VTask.clog`** *or* at least declares some named definition
- [ ] `extract_ok` is `true` for **at least 5 of the 7**

**ABORT CRITERIA — do not start the overnight run if:**

- **3 or more** models produce no plausible sample → something systemic is wrong (endpoint,
  prompt assembly, sampling params). Investigate before spending a night.
- **Any** model returns HTTP 400 → our request shape is wrong for it; fix the model table.
- The smoke run never advances past a model → the pod's model list is out of sync with
  `prelim/models.py`.

**One or two weak models is NOT an abort.** That is a real measurement (Kimina-Autoformalizer in
particular may emit theorem stubs rather than definitions — expected, and worth recording). The
run's own validity gate will halt any model that produces three unusable samples and continue
with the rest.

---

## Step 4 — Launch the overnight run, then go to bed

The pod is now sitting at model 7 after the smoke test. **Restart the pod runner** so it begins
again at model 1:

```bash
# In the POD web terminal:
pkill -f pod_runner.py; pkill -f "vllm serve"; sleep 5
cd /workspace && nohup python3 -u pod_runner.py > /workspace/pod_runner.log 2>&1 &
tail -f /workspace/pod_runner.log     # wait for model 1 to be serving again
```

Then on the **Mac** — `caffeinate -i` stops the Mac sleeping mid-run:

```bash
cd /Users/henryhayton/definition-verifier
caffeinate -i uv run python -m prelim.driver \
  --control-url "$PRELIM_CONTROL_URL" \
  --models-url "https://YOUR_POD_ID-8000.proxy.runpod.net/v1/models" \
  2>&1 | tee -a prelim_testing/output/console.log
```

Leave the terminal open. Expect **4–6 hours**. Go to bed.

> The smoke samples are *kept* — they are `sample_00` of `Nat.clog` for each model, and the run
> will skip regenerating them. That is the resume logic working, not a mistake.

---

## Step 5 — Morning checks (5 min)

```bash
cd /Users/henryhayton/definition-verifier

# 1. Did it finish? (want: 7 models, all "completed")
uv run python -c "
import json; d=json.load(open('prelim_testing/output/run_summary.json'))
print('stopped_reason:', d['stopped_reason'])
for m in d['models']: print(f\"  {m['slug']:28s} {m['status']:12s} {m['completed']}/{m['attempted']}  ext-fail={m['extraction_failures']}\")
print('totals:', json.dumps(d['totals'], indent=2))
"

# 2. Full expected count is 410 per model (41 tasks x 10 samples)
tail -40 prelim_testing/output/run_log.txt
```

**3. Confirm the pod is gone.** RunPod dashboard → the pod should be **terminated**. If it is
still running, terminate it manually now. (The idle watchdog terminates after 60 minutes of no
traffic, so even a crashed Mac stops the meter — but verify.)

### If it only partially completed

The run is resume-safe. Redeploy a pod (Steps 1–2), then repoint and **rerun the identical
command**:

```bash
export PRELIM_ENDPOINT_URL='https://NEW_POD_ID-8000.proxy.runpod.net/v1/chat/completions'
export PRELIM_CONTROL_URL='https://NEW_POD_ID-8001.proxy.runpod.net'
caffeinate -i uv run python -m prelim.driver \
  --control-url "$PRELIM_CONTROL_URL" \
  --models-url "https://NEW_POD_ID-8000.proxy.runpod.net/v1/models"
```

Completed samples are skipped; only the gaps are filled. Nothing is regenerated, nothing is lost.

To finish **one specific model** only:

```bash
caffeinate -i uv run python -m prelim.driver --models herald-7b \
  --control-url "$PRELIM_CONTROL_URL" \
  --models-url "https://NEW_POD_ID-8000.proxy.runpod.net/v1/models"
```

(A single-model rerun still advances the pod through the list to reach it — simplest is to let
the pod restart from model 1 and let the driver skip the finished ones.)

---

## Reference

| | |
|---|---|
| Sampling | 5 × temp 0.7 + 5 × temp 1.0, top_p 0.95, max_tokens 4096 |
| Total generations | 7 × 41 × 10 = **2,870** |
| Samples land in | `prelim_testing/output/samples/<slug>/<task>/sample_NN.json` |
| Progress log | `prelim_testing/output/run_log.txt` (one line/min per model) |
| Per-call provenance | `prelim_testing/output/call_log.jsonl` (every attempt, incl. retries) |
| Final summary | `prelim_testing/output/run_summary.json` |
| Pod log | `/workspace/pod_runner.log` |
| Pod status | `curl -s $PRELIM_CONTROL_URL/status` |

**Emergency stop:** Ctrl-C the Mac driver, then terminate the pod in the RunPod dashboard. Nothing
is corrupted — every completed sample is already on disk and a relaunch resumes from there.
