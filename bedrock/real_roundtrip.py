"""Manual, one-off check of a real round trip against actual AWS Bedrock. Deliberately a
standalone script, not a pytest test, so it can never be collected or run by the automated
suite or CI -- run it by hand once real Bedrock access is confirmed:

    uv run python bedrock/real_roundtrip.py

It refuses to run against a stub (`config.ENDPOINT_URL` set) or with a placeholder model ID,
sends one short prompt to the pinned model, asserts the response text is non-empty, and
prints both the response text and the provenance record this call wrote to the call log.
"""

import json

from bedrock import config as cfg
from bedrock.client import BedrockClient


def main() -> None:
    if cfg.ENDPOINT_URL is not None:
        raise RuntimeError(
            "bedrock.config.ENDPOINT_URL is set -- this script is for a REAL round trip against "
            "AWS Bedrock. Leave ENDPOINT_URL at its default (None) before running this."
        )
    if cfg.AUTHORING_MODEL_ID.startswith("PLACEHOLDER"):
        raise RuntimeError(
            "bedrock.config.AUTHORING_MODEL_ID is still a placeholder -- fill in the real pinned "
            "model ID before running this script."
        )

    client = BedrockClient()
    response = client.send(
        system="You are a terse test assistant.",
        user_message="Reply with exactly one short sentence confirming you received this message.",
        model_id=cfg.AUTHORING_MODEL_ID,
        max_tokens=64,
        temperature=0.0,
    )

    assert response.text.strip(), "expected a non-empty response from a real round trip"

    print("=== response text ===")
    print(response.text)
    print()
    print("=== provenance record (last line of the call log) ===")
    with cfg.CALL_LOG_PATH.open(encoding="utf-8") as f:
        last_line = f.readlines()[-1]
    print(json.dumps(json.loads(last_line), indent=2))


if __name__ == "__main__":
    main()
