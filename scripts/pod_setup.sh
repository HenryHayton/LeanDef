#!/usr/bin/env bash
# Prelim testing -- pod bootstrap. Paste this whole file into the RunPod web terminal.
#
# Deliberately does NOT pre-download any weights: vLLM fetches each model when it first serves
# it, so pre-pulling would double the disk use and delay the first model behind six others it
# does not need yet.
set -euo pipefail

# --- FILL THESE IN before pasting -------------------------------------------------------------
export RUNPOD_API_KEY="${RUNPOD_API_KEY:-PASTE_YOUR_API_KEY_HERE}"
export RUNPOD_POD_ID="${RUNPOD_POD_ID:-PASTE_YOUR_POD_ID_HERE}"
# ----------------------------------------------------------------------------------------------

if [[ "$RUNPOD_API_KEY" == "PASTE_YOUR_API_KEY_HERE" || "$RUNPOD_POD_ID" == "PASTE_YOUR_POD_ID_HERE" ]]; then
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

echo "=== hugging face cache on the volume (survives pod restarts) ==="
export HF_HOME=/workspace/hf
mkdir -p "$HF_HOME"

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
