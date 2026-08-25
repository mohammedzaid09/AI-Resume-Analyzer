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