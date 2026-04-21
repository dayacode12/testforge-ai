import requests
from app.config import TESTFORGE_URL

ANALYZE_URL = f"{TESTFORGE_URL}/analyze"


def send_logs_to_ai(log_text: str):
    """
    Sends Jenkins logs to TestForge AI for analysis
    """
    try:    
        response = requests.post(
            ANALYZE_URL,
            data=log_text,
            headers={"Content-Type": "text/plain"},
            timeout=30
        )

        response.raise_for_status()  # 🚀 ensures HTTP errors are caught

        return response.json()

    except Exception as e:
        return {
            "error": "Pipeline AI call failed",
            "details": str(e)
        }


def read_logs_from_file(file_path: str):
    """
    Reads logs from Jenkins output file
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except FileNotFoundError:
        return None

    except Exception as e:
        return None


def process_pipeline_failure(log_file_path: str):
    """
    Full pipeline flow:
    1. Read logs
    2. Send to AI
    3. Return structured analysis
    """

    logs = read_logs_from_file(log_file_path)

    if logs is None:
        return {
            "status": "failed",
            "error": f"Log file not found or unreadable: {log_file_path}"
        }

    analysis = send_logs_to_ai(logs)

    return {
        "status": "processed",
        "log_source": log_file_path,
        "analysis": analysis
    }