"""Preflight for the cross-vendor tier-5 arms: prove the models are reachable before spending.

    uv run python scripts/converse_preflight.py

Bedrock model access is granted PER MODEL per account, and a model the account has not enabled
fails at the first call with AccessDeniedException -- indistinguishable, in a 200-goal run's log,
from a credentials problem. One cheap call each, up front, converts that into a clear answer.

Also probes the DeepSeek V3.1 fallback the operator named, so a V3.2 refusal comes with its
remedy already tested rather than needing a second round trip.
"""

import sys

from bedrock.converse import (DEEPSEEK_V31, DEEPSEEK_V32, DEFAULT_REGION,
                              QWEN3_CODER_480B, ConverseClient, ConverseError)

PROBE = ("Reply with only a fenced lean block containing exactly: by simp")


def probe(model_id: str, region: str) -> tuple[bool, str]:
    try:
        client = ConverseClient(region=region, max_attempts=1, read_timeout_s=120.0)
        res = client.send("You are a Lean 4 prover.", PROBE, model_id=model_id, max_tokens=64)
        got = (res.text or "").strip().replace("\n", " ")[:70]
        return True, f"OK  out_tokens={res.output_tokens} stop={res.stop_reason}  text={got!r}"
    except ConverseError as e:
        return False, str(e)[:220]
    except Exception as e:  # noqa: BLE001 -- boto/credential errors must read clearly too
        return False, f"{type(e).__name__}: {str(e)[:200]}"


def main() -> int:
    targets = [(DEEPSEEK_V32, DEFAULT_REGION),
               (DEEPSEEK_V31, DEFAULT_REGION),
               (QWEN3_CODER_480B, DEFAULT_REGION)]
    results = {}
    for model_id, region in targets:
        ok, detail = probe(model_id, region)
        results[model_id] = ok
        print(f"{'PASS' if ok else 'FAIL'}  {model_id:<34} @ {region}\n      {detail}", flush=True)

    print()
    if results.get(DEEPSEEK_V32):
        print("deepseek arm -> deepseek.v3.2")
    elif results.get(DEEPSEEK_V31):
        print("deepseek arm -> deepseek.v3.1 (V3.2 unavailable; operator-approved fallback)")
    else:
        print("deepseek arm BLOCKED: neither V3.2 nor V3.1 reachable")
    print("qwen arm -> " + ("qwen3-coder-480b" if results.get(QWEN3_CODER_480B) else "BLOCKED"))
    return 0 if any(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
