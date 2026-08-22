from pydantic import BaseModel


class AnalysisRequest(BaseModel):

    resume_text: str
    job_description: str

class AnalysisResponse(BaseModel):

    success: bool
    ats_score: int

    matched_skills: list[str]
    missing_skills: list[str]

    resume_skills_by_category: dict[str, list[str]]
    job_skills_by_category: dict[str, list[str]]

    total_resume_skills: int
    total_job_skills: int
    matched_count: int

    strengths: list[str]
    suggestions: list[str]
    
    sections: dict[str, str]
    missing_sections: list[str]