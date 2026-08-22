from fastapi import FastAPI
from app.api import resume
from app.api.analysis import router as analysis_router

app = FastAPI(
    title="ResumeIQ API",
    description="AI-Powered Resume Analyzer API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to ResumeIQ API"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "success",
        "message": "ResumeIQ API is running"
    }

app.include_router(resume.router)
app.include_router(analysis_router)