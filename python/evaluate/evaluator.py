import os
import json
import requests
from .metrics import bleu_score, exact_match, semantic_similarity

API_URL = "http://localhost:8000/evaluate"

# Load prompts
with open("evaluate/data/prompts.json") as f:
    prompts = json.load(f)

with open("evaluate/data/expected_responses.json") as f:
    expected_responses = json.load(f)

results = []

for prompt in prompts:
    prompt_id = prompt["id"]
    text = prompt["prompt"]

    try:
        response = requests.post(API_URL, json={"prompt": text}, timeout=10)
        actual_answer = response.json().get("answer", "")
    except Exception as e:
        actual_answer = ""
        print(f"Error calling API for prompt {prompt_id}: {e}")

    expected_answer = expected_responses.get(prompt_id, "")

    # Compute metrics
    bleu = bleu_score(expected_answer, actual_answer)
    exact = exact_match(expected_answer, actual_answer)
    semantic = semantic_similarity(expected_answer, actual_answer)

    results.append({
        "id": prompt_id,
        "prompt": text,
        "expected": expected_answer,
        "actual": actual_answer,
        "bleu": bleu,
        "exact_match": exact,
        "semantic_similarity": semantic
    })

# Save results
os.makedirs("evaluate/reports", exist_ok=True)
report_path = "evaluate/reports/latest_metrics.json"
with open(report_path, "w") as f:
    json.dump(results, f, indent=4)

print(f"Evaluation complete. Results saved to {report_path}")

