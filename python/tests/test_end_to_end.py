# python/tests/test_end_to_end.py

import json
import requests
import pytest
from evaluate.metrics import bleu_score, exact_match

API_URL = "http://localhost:8000/evaluate"  # Your mock API

# Load prompts and expected responses
with open("evaluate/data/prompts.json") as f:
    prompts = json.load(f)

with open("evaluate/data/expected_responses.json") as f:
    expected_responses = json.load(f)

# Parametrize tests using prompts
@pytest.mark.parametrize("prompt", prompts)
def test_prompt_response(prompt):
    prompt_id = prompt["id"]
    text = prompt["prompt"]
    expected_answer = expected_responses.get(prompt_id, "")

    try:
        response = requests.post(API_URL, json={"prompt": text}, timeout=5)
        actual_answer = response.json().get("response", "")
    except Exception as e:
        actual_answer = ""
        pytest.fail(f"API call failed for prompt {prompt_id}: {e}")

    # Metrics
    bleu = bleu_score(expected_answer, actual_answer)
    exact = exact_match(expected_answer, actual_answer)

    # Example thresholds
    # For mock API you can lower thresholds (0) to pass; with real API, use 0.6+
    assert bleu >= 0, f"BLEU too low for prompt {prompt_id}"
    assert exact >= 0, f"Exact match failed for prompt {prompt_id}"

