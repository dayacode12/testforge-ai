from fastapi import APIRouter
from app.models.request_model import TestRequest
from app.services.ai_service import generate_test_cases

router = APIRouter()
@router.post("/generate-tests")
def generate_tests(request: TestRequest):
    result=generate_test_cases(request.feature_description)
    return {"test_cases":result}
