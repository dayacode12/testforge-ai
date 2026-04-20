import requests
import json
from app.config import OLLAMA_URL


def safe_extract_json(raw_output: str):
    """
    Safely extracts JSON from LLM response
    """
    try:
        return json.loads(raw_output)
    except:
        pass

    start = raw_output.find("[")
    end = raw_output.rfind("]")

    if start == -1 or end == -1:
        raise ValueError("No JSON array found in AI response")

    json_str = raw_output[start:end + 1]

    return json.loads(json_str)


def generate_test_cases(feature_description: str):
    prompt = f"""
You are a senior QA engineer.

Generate test cases for the following feature:

Feature: {feature_description}

Return ONLY valid JSON in this format:
[
  {{
    "id": "TC_001",
    "description": "...",
    "steps": ["...", "..."],
    "expected": "..."
  }}
]
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        raw_output = response.json().get("response", "")

        return safe_extract_json(raw_output)

    except Exception as e:
        return [{"error": str(e)}]