from app.services.llm_service import generate_ai_feedback


feedback = generate_ai_feedback(
    ats_score=80,
    resume_quality_score=56,
    missing_skills=["docker"],
    missing_sections=[],
    section_analysis={
        "professional_summary": {
            "status": "present",
            "score": 70
        },
        "projects": {
            "status": "present",
            "score": 60
        },
        "experience": {
            "status": "present",
            "score": 60
        },
        "technical_skills": {
            "status": "present",
            "score": 40
        },
        "education": {
            "status": "present",
            "score": 80
        },
        "certifications": {
            "status": "present",
            "score": 25
        }
    },
    job_title="Python Developer"
)

print(feedback)