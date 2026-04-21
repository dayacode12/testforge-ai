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


def analyze_error(error_log: str):
    """
    Analyzes error logs and suggests fixes
    """
    prompt = f"""
You are an expert DevOps engineer.

Analyze the following error log and provide:
1. Root cause
2. Impact assessment
3. Recommended fixes

Error log:
{error_log}

Return ONLY valid JSON in this format:
{{
  "root_cause": "...",
  "impact": "...",
  "fixes": ["...", "..."]
}}
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
        
        # Extract JSON object
        start = raw_output.find("{")
        end = raw_output.rfind("}")
        
        if start == -1 or end == -1:
            raise ValueError("No JSON object found in AI response")
        
        json_str = raw_output[start:end + 1]
        return json.loads(json_str)

    except Exception as e:
        return {"error": str(e)}
