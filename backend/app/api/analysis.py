from fastapi import APIRouter

from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.resume_analyzer import analyze_resume
from app.services.section_detector import detect_sections

from app.services.section_analyzer import (analyze_professional_summary, analyze_projects, analyze_experience, analyze_technical_skills, analyze_education, analyze_certifications, calculate_resume_quality)

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
    section_result = detect_sections(request.resume_text)
    sections = section_result["sections"]

    result["sections"] = sections
    result["missing_sections"] = section_result["missing_sections"]

    result["section_analysis"] = {
        "professional_summary": analyze_professional_summary(
            sections.get("professional_summary", "")
        ),
        "projects": analyze_projects(
            sections.get("projects", "")
        ),
        "experience": analyze_experience(
            sections.get("experience", "")
        ),
        "technical_skills": analyze_technical_skills(
            sections.get("technical_skills", "")
        ),
        "education": analyze_education(
            sections.get("education", "")
        ),
        "certifications": analyze_certifications(
            sections.get("certifications", "")
        )
    }

    result["resume_quality_score"] = calculate_resume_quality(
        result["section_analysis"]
    )

    return result