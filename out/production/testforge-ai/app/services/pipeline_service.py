import requests

TESTFORGE_ANALYZE_URL = "http://localhost:8000/analyze"


def send_logs_to_ai(log_text: str):
    """
    Sends Jenkins logs to TestForge AI for analysis
    """
    try:
        response = requests.post(
            TESTFORGE_ANALYZE_URL,
            data=log_text,
            headers={"Content-Type": "text/plain"},
            timeout=30
        )

        return response.json()

    except Exception as e:
        return {"error": f"Pipeline AI call failed: {str(e)}"}


def read_logs_from_file(file_path: str):
    """
    Reads logs from a file (e.g., logs.txt from Jenkins)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Error reading log file: {str(e)}"


def process_pipeline_failure(log_file_path: str):
    """
    Full pipeline flow:
    1. Read logs
    2. Send to AI
    3. Return analysis
    """
    logs = read_logs_from_file(log_file_path)

    if "Error reading" in logs:
        return {"error": logs}

    analysis = send_logs_to_ai(logs)

    return {
        "status": "processed",
        "analysis": analysis
    }