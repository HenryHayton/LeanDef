#!/usr/bin/env bash
# Prelim testing -- pod bootstrap. Paste this whole file into the RunPod web terminal.
#
# Deliberately does NOT pre-download any weights: vLLM fetches each model when it first serves
# it, so pre-pulling would double the disk use and delay the first model behind six others it
# does not need yet.
set -euo pipefail

# --- Hugging Face cache MUST live on the volume, and MUST be set before anything downloads ----
# The 110 GB volume mounts at /workspace; the container's own disk is ~30 GB and HF's default
# cache (~/.cache/huggingface) sits on it. Seven models at ~15 GB each would fill that disk and
# kill the run mid-night. Set first, before pip and before any model is fetched.
export HF_HOME=/workspace/hf
export HUGGINGFACE_HUB_CACHE=/workspace/hf/hub
mkdir -p "$HF_HOME" "$HUGGINGFACE_HUB_CACHE"
echo "=== HF cache -> $HF_HOME (on the volume) ==="
df -h /workspace | tail -1

# --- FILL THESE IN before pasting -------------------------------------------------------------
export RUNPOD_API_KEY="${RUNPOD_API_KEY:-PASTE_KEY_HERE}"
export RUNPOD_POD_ID="${RUNPOD_POD_ID:-PASTE_YOUR_POD_ID_HERE}"
# ----------------------------------------------------------------------------------------------

if [[ "$RUNPOD_API_KEY" == "PASTE_KEY_HERE" || "$RUNPOD_POD_ID" == "PASTE_YOUR_POD_ID_HERE" ]]; then
  echo "!!! RUNPOD_API_KEY / RUNPOD_POD_ID not set -- the pod will NOT self-terminate."
  echo "!!! It will still run; you must terminate it manually from the dashboard."
  echo "!!! Ctrl-C now if you would rather set them first."
  sleep 10
fi

echo "=== installing vllm (several minutes) ==="
pip install --upgrade pip
pip install "vllm>=0.6.0"

echo "=== writing pod_runner.py ==="
# Paste the contents of scripts/pod_runner.py into the heredoc below, OR fetch it if the repo is
# reachable from the pod. The heredoc form is the reliable one -- no auth, no network assumptions.
cat > /workspace/pod_runner.py <<'PYEOF'
__POD_RUNNER_PY__
PYEOF

echo "=== starting pod_runner (control port 8001, vLLM port 8000) ==="
cd /workspace
# nohup + & so closing the web terminal does not kill the run.
nohup python3 -u pod_runner.py > /workspace/pod_runner.log 2>&1 &
echo "pod_runner started; pid $!"
sleep 5
echo "=== first 40 log lines ==="
head -40 /workspace/pod_runner.log || true
echo
echo "Watch progress with:  tail -f /workspace/pod_runner.log"
echo "Check status with:    curl -s localhost:8001/status"
