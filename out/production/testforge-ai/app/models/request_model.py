from pydantic import BaseModel

class TestRequest(BaseModel):
    feature_description: str