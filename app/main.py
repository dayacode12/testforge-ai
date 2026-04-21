from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="TestForge-AI", version="1.0.0")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "testforge-ai"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "TestForge-AI API", "endpoints": ["/health", "/generate-tests", "/analyze"]}

app.include_router(router)
