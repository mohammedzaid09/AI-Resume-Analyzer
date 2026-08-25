import re

from app.services.skill_matcher import extract_skills


def extract_experience_requirement(text: str) -> str:
    patterns = [
        r"\b\d+\+?\s*(?:-\s*\d+)?\s+years?\b",
        r"\bfresher[s]?\b",
        r"\bentry[- ]level\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return match.group()

    return ""

def extract_education_requirement(text: str) -> str:
    patterns = [
        r"\b(?:b\.?e\.?|b\.?tech|bachelor'?s?|bsc)\b",
        r"\b(?:m\.?e\.?|m\.?tech|master'?s?|msc)\b",
        r"\bcomputer science\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return match.group()

    return ""

def extract_job_title(text: str) -> str:
    patterns = [
        r"(?:looking for|hiring|seeking)\s+(?:an?\s+)?([a-z\s]+?(?:developer|engineer|analyst))",
        r"role[:\s]+([a-z\s]+?(?:developer|engineer|analyst))"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return match.group(1).strip().title()

    return ""


def analyze_job_description(job_description: str) -> dict:
    return {
        "job_title": extract_job_title(job_description),
        "skills": extract_skills(job_description),
        "experience_requirement": extract_experience_requirement(job_description),
        "education_requirement": extract_education_requirement(job_description)
    }