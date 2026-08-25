from app.services.skill_matcher import match_skills


def analyze_resume(resume_text: str, job_description: str) -> dict:
    skill_results = match_skills(resume_text, job_description)

    matched_skills = skill_results["matched_skills"]
    missing_skills = skill_results["missing_skills"]
    total_job_skills = skill_results["total_job_skills"]

    ats_score = (
        int(len(matched_skills) / total_job_skills * 100)
        if total_job_skills else 0
    )

    return {
        "success": True,
        "ats_score": ats_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_skills_by_category":
            skill_results["resume_skills_by_category"],
        "job_skills_by_category":
            skill_results["job_skills_by_category"],
        "total_resume_skills":
            skill_results["total_resume_skills"],
        "total_job_skills":
            skill_results["total_job_skills"],
        "matched_count":
            skill_results["matched_count"]
    }