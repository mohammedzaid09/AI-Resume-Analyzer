from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    resume_text: str
    job_description: str


class AnalysisResponse(BaseModel):
    success: bool
    scores: dict
    skill_analysis: dict
    section_analysis: dict
    job_analysis: dict
    improvement_suggestions: list[str]
    ai_feedback: str

class RewriteSectionRequest(BaseModel):
    section_name: str
    content: str


class RewriteSectionResponse(BaseModel):
    success: bool
    section_name: str
    original_content: str
    improved_content: str

class ImproveResumeRequest(BaseModel):
    resume_text: str
    job_description: str


class ImproveResumeResponse(BaseModel):
    success: bool
    sections_improved: list[dict]
    missing_sections: list[str]
    missing_skills: list[str]
    suggestions: list[str]