from app.services.skill_matcher import match_skills


def analyze_resume(resume_text: str, job_description: str) -> dict:
    """
    Analyze resume skills against the job description.
    """

    # Get categorized skill matching results
    skill_results = match_skills(
        resume_text,
        job_description
    )

    matched_skills = skill_results["matched_skills"]
    missing_skills = skill_results["missing_skills"]

    total_job_skills = skill_results["total_job_skills"]

    # Calculate ATS score
    if total_job_skills > 0:
        ats_score = int(
            (len(matched_skills) / total_job_skills) * 100
        )
    else:
        ats_score = 0

    # Generate strengths
    strengths = []

    if matched_skills:
        strengths.append(
            f"Your resume matches {len(matched_skills)} relevant skills."
        )

    if len(resume_text) > 1000:
        strengths.append(
            "Your resume contains a good amount of detailed information."
        )

    # Generate suggestions
    suggestions = []

    if missing_skills:
        suggestions.append(
            "Consider adding relevant missing skills if you have experience with them."
        )

    if ats_score < 50:
        suggestions.append(
            "Your resume has a low keyword match with this job description."
        )

    elif ats_score < 75:
        suggestions.append(
            "Add more relevant keywords from the job description."
        )

    else:
        suggestions.append(
            "Your resume has a strong keyword match for this role."
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
            skill_results["matched_count"],

        "strengths": strengths,

        "suggestions": suggestions
    }