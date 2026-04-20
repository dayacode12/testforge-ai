import requests
import json

OLLAMA_URL = "http://ollama:11434/api/generate"

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

        # Try to extract JSON safely
        start = raw_output.find("[")
        end = raw_output.rfind("]") + 1
        json_str = raw_output[start:end]

        return json.loads(json_str)

    except Exception as e:
        return [{"error": str(e)}]