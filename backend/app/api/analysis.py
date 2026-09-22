from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas.analysis import AnalysisRequest, AnalysisResponse, RewriteSectionRequest, RewriteSectionResponse,  ImproveResumeRequest, ImproveResumeResponse
    

from app.services.resume_analyzer import analyze_resume
from app.services.section_detector import detect_sections
from app.services.llm_service import generate_ai_feedback, rewrite_resume_section
from app.services.job_analyzer import analyze_job_description
from app.services.resume_parser import extract_resume_text
from app.services.section_analyzer import (
    analyze_professional_summary,
    analyze_projects,
    analyze_experience,
    analyze_technical_skills,
    analyze_education,
    analyze_certifications,
    calculate_resume_quality,
    generate_improvement_suggestions
)


router = APIRouter(
    prefix="/api",
    tags=["Resume Analysis"]
)


@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):
    """
    Upload a PDF or DOCX resume and extract its text.
    """

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

    # --------------------------------------------------------
    # Validate filename
    # --------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was provided."
        )

    filename = file.filename.lower()

    # --------------------------------------------------------
    # Validate file type
    # --------------------------------------------------------

    if not (
        filename.endswith(".pdf")
        or filename.endswith(".docx")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    # --------------------------------------------------------
    # Read file
    # --------------------------------------------------------

    file_bytes = await file.read()

    # --------------------------------------------------------
    # Validate file size
    # --------------------------------------------------------

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must not exceed 5 MB."
        )

    # --------------------------------------------------------
    # Validate empty file
    # --------------------------------------------------------

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    # --------------------------------------------------------
    # Extract resume text
    # --------------------------------------------------------

    try:
        resume_text = extract_resume_text(
            filename=file.filename,
            file_bytes=file_bytes
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    # --------------------------------------------------------
    # Return extracted resume
    # --------------------------------------------------------

    return {
        "success": True,
        "filename": file.filename,
        "resume_text": resume_text
    }



@router.post(
    "/analyze",
    response_model=AnalysisResponse
)
async def analyze(request: AnalysisRequest):

    # Analyze resume skills against job description
    result = analyze_resume(
        resume_text=request.resume_text,
        job_description=request.job_description
    )

    # Detect resume sections
    section_result = detect_sections(request.resume_text)

    sections = section_result["sections"]

    result["sections"] = sections

    result["missing_sections"] = (
        section_result["missing_sections"]
    )

    # Analyze individual resume sections
    result["section_analysis"] = {

        "professional_summary":
            analyze_professional_summary(
                sections.get("professional_summary", "")
            ),

        "projects":
            analyze_projects(
                sections.get("projects", "")
            ),

        "experience":
            analyze_experience(
                sections.get("experience", "")
            ),

        "technical_skills":
            analyze_technical_skills(
                sections.get("technical_skills", "")
            ),

        "education":
            analyze_education(
                sections.get("education", "")
            ),

        "certifications":
            analyze_certifications(
                sections.get("certifications", "")
            )
    }

    # Calculate overall resume quality
    resume_quality_score = calculate_resume_quality(
        result["section_analysis"]
    )

    # Analyze job description
    job_analysis = analyze_job_description(
        request.job_description
    )

    # Prepare skill analysis
    skill_analysis = {
        "matched": result["matched_skills"],
        "missing": result["missing_skills"],
        "match_percentage": result["ats_score"]
    }

    # Generate rule-based improvement suggestions
    improvement_suggestions = generate_improvement_suggestions(
        result["missing_skills"],
        result["missing_sections"],
        result["section_analysis"]
    )

    # Generate AI-powered personalized feedback
    ai_feedback = generate_ai_feedback(
        ats_score=result["ats_score"],
        resume_quality_score=resume_quality_score,
        missing_skills=result["missing_skills"],
        missing_sections=result["missing_sections"],
        section_analysis=result["section_analysis"],
        job_title=job_analysis.get("job_title", "")
    )

    # Return final structured response
    return {
        "success": True,

        "scores": {
            "ats_score": result["ats_score"],
            "resume_quality_score": resume_quality_score
        },

        "skill_analysis": skill_analysis,

        "section_analysis": {
            "missing_sections": result["missing_sections"],
            "analysis": result["section_analysis"]
        },

        "job_analysis": job_analysis,

        "improvement_suggestions": improvement_suggestions,

        "ai_feedback": ai_feedback
    }

@router.post(
    "/rewrite-section",
    response_model=RewriteSectionResponse
)
async def rewrite_section(request: RewriteSectionRequest):

    improved_content = rewrite_resume_section(
        section_name=request.section_name,
        content=request.content,
    )

    return {
        "success": True,
        "section_name": request.section_name,
        "original_content": request.content,
        "improved_content": improved_content
    }


@router.post(
    "/improve-resume",
    response_model=ImproveResumeResponse
)
async def improve_resume(request: ImproveResumeRequest):

    # Analyze the resume against the job description
    result = analyze_resume(
        resume_text=request.resume_text,
        job_description=request.job_description
    )

    # Detect resume sections
    section_result = detect_sections(request.resume_text)

    sections = section_result["sections"]

    # Analyze individual sections
    section_analysis = {
        "professional_summary":
            analyze_professional_summary(
                sections.get("professional_summary", "")
            ),

        "projects":
            analyze_projects(
                sections.get("projects", "")
            ),

        "experience":
            analyze_experience(
                sections.get("experience", "")
            ),

        "technical_skills":
            analyze_technical_skills(
                sections.get("technical_skills", "")
            ),

        "education":
            analyze_education(
                sections.get("education", "")
            ),

        "certifications":
            analyze_certifications(
                sections.get("certifications", "")
            )
    }

    # Identify important sections to improve
    priority_sections = [
        "professional_summary",
        "experience",
        "projects",
    ]

    sections_to_improve = [
        section_name
        for section_name in priority_sections
        if section_analysis.get(section_name, {}).get("status") == "present"
    ]

    # Rewrite the selected sections
    sections_improved = []

    for section_name in sections_to_improve:

        original_content = sections.get(
            section_name,
            ""
        )

        if not original_content:
            continue

        improved_content = rewrite_resume_section(
            section_name=section_name,
            content=original_content
        )

        sections_improved.append({
            "section_name": section_name,
            "original_content": original_content,
            "improved_content": improved_content
        })

    # Return improvement result
    return {
        "success": True,
        "sections_improved": sections_improved,
        "missing_sections": section_result["missing_sections"],
        "missing_skills": result["missing_skills"],
        "suggestions": generate_improvement_suggestions(
            result["missing_skills"],
            section_result["missing_sections"],
            section_analysis
        )
    }