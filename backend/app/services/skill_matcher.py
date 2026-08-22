import re

from app.core.skills import SKILL_CATEGORIES


def normalize_text(text: str) -> str:
    """
    Normalize text for consistent skill matching.
    """

    text = text.lower()

    # Replace special characters with spaces,
    # but preserve + and # for skills like C++ and C#
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)

    # Normalize multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def skill_exists(text: str, alias: str) -> bool:
    """
    Check whether a skill alias exists as a whole phrase.
    """

    pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"

    return bool(re.search(pattern, text))


def extract_skills(text: str) -> dict:
    """
    Extract skills from text and group them by category.
    """

    normalized_text = normalize_text(text)

    extracted_skills = {}

    for category, skills in SKILL_CATEGORIES.items():

        category_skills = []

        for canonical_skill, aliases in skills.items():

            for alias in aliases:

                normalized_alias = normalize_text(alias)

                if skill_exists(normalized_text, normalized_alias):

                    category_skills.append(canonical_skill)

                    # Stop checking aliases once one matches
                    break

        if category_skills:

            extracted_skills[category] = sorted(category_skills)

    return extracted_skills


def flatten_skills(categorized_skills: dict) -> set:
    """
    Convert categorized skills into a set.
    """

    skills = set()

    for category_skills in categorized_skills.values():
        skills.update(category_skills)

    return skills


def match_skills(resume_text: str, job_description: str) -> dict:
    """
    Compare resume skills with job description skills.
    """

    resume_skills_by_category = extract_skills(resume_text)

    job_skills_by_category = extract_skills(job_description)

    resume_skills = flatten_skills(resume_skills_by_category)

    job_skills = flatten_skills(job_skills_by_category)

    matched_skills = sorted(
        resume_skills.intersection(job_skills)
    )

    missing_skills = sorted(
        job_skills.difference(resume_skills)
    )

    return {
        "resume_skills_by_category": resume_skills_by_category,

        "job_skills_by_category": job_skills_by_category,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "total_resume_skills": len(resume_skills),

        "total_job_skills": len(job_skills),

        "matched_count": len(matched_skills)
    }