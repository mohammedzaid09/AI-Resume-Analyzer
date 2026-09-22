from fastapi import FastAPI
from app.api import resume
from fastapi.middleware.cors import CORSMiddleware
from app.api.analysis import router as analysis_router

app = FastAPI(
    title="ResumeIQ API",
    description="AI-Powered Resume Analyzer API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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