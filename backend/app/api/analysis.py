from fastapi import APIRouter

from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.resume_analyzer import analyze_resume
from app.services.section_detector import detect_sections

router = APIRouter(
    prefix="/api",
    tags=["Resume Analysis"]
)


@router.post(
    "/analyze",
    response_model=AnalysisResponse
)
async def analyze(request: AnalysisRequest):

    result = analyze_resume(
        resume_text=request.resume_text,
        job_description=request.job_description
    )
    sections = detect_sections(request.resume_text)
    result["sections"] = sections["sections"]
    result["missing_sections"] = sections["missing_sections"]

    return result