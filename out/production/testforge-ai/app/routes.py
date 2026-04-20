from fastapi import APIRouter, Request
from app.models.request_model import TestRequest
from app.services.ai_service import generate_test_cases, analyze_error

router = APIRouter()

# Existing: Test case generation
@router.post("/generate-tests")
def generate_tests(request: TestRequest):
    result = generate_test_cases(request.feature_description)
    return {"test_cases": result}


# NEW: Pipeline error analysis
@router.post("/analyze")
async def analyze(request: Request):
    log_text = await request.body()
    result = analyze_error(log_text.decode("utf-8"))
    return {"analysis": result}