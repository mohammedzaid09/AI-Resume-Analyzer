from app.services.skill_matcher import extract_skills


def analyze_professional_summary(summary: str) -> dict:
    """
    Analyze the quality of the professional summary.
    """

    if not summary or not summary.strip():
        return {
            "status": "missing",
            "score": 0,
            "feedback": [
                "Professional summary is missing."
            ]
        }

    summary = summary.strip()

    word_count = len(summary.split())

    score = 100
    feedback = []

    # Check if summary is too short
    if word_count < 20:
        score -= 30

        feedback.append(
            "Professional summary is too short. Add more details about your skills and career goals."
        )

    # Check if summary is too long
    elif word_count > 100:
        score -= 20

        feedback.append(
            "Professional summary is too long. Try to keep it concise and focused."
        )

    # Good length
    else:
        feedback.append(
            "Professional summary has a good length."
        )

    return {
        "status": "present",
        "score": max(score, 0),
        "feedback": feedback
    }

def analyze_detailed_section(
    content: str,
    section_name: str,
    short_feedback: str,
    medium_feedback: str
) -> dict:
    if not content or not content.strip():
        return {
            "status": "missing",
            "score": 0,
            "technologies": {},
            "feedback": [f"{section_name} section is missing."]
        }

    content = content.strip()
    word_count = len(content.split())
    technologies = extract_skills(content)

    score = 100
    feedback = []

    if word_count < 15:
        score -= 40
        feedback.append(short_feedback)
    elif word_count < 30:
        score -= 20
        feedback.append(medium_feedback)

    if not technologies:
        score -= 20
        feedback.append(
            f"Mention relevant technologies or tools used in your {section_name.lower()}."
        )

    if not feedback:
        feedback.append(
            f"{section_name} section contains a good amount of relevant detail."
        )

    return {
        "status": "present",
        "score": max(score, 0),
        "technologies": technologies,
        "feedback": feedback
    }

def analyze_projects(projects: str) -> dict:
    return analyze_detailed_section(
        projects,
        "Projects",
        "Project descriptions are too brief. Add more details about features and implementation.",
        "Consider adding more details about your project implementation."
    )

def analyze_experience(experience: str) -> dict:
    return analyze_detailed_section(
        experience,
        "Experience",
        "Experience details are too brief. Add your responsibilities and contributions.",
        "Consider adding more details about your responsibilities and achievements."
    )

def analyze_technical_skills(skills: str) -> dict:
    if not skills or not skills.strip():
        return {
            "status": "missing",
            "score": 0,
            "skills": {},
            "feedback": ["Technical Skills section is missing."]
        }

    detected_skills = extract_skills(skills)
    total_skills = sum(len(items) for items in detected_skills.values())

    score = min(total_skills * 10, 100)
    feedback = []

    if total_skills < 3:
        feedback.append(
            "Add more relevant technical skills."
        )
    elif total_skills < 6:
        feedback.append(
            "Technical skills section could include more relevant skills."
        )
    else:
        feedback.append(
            "Technical skills section contains a good range of skills."
        )

    return {
        "status": "present",
        "score": score,
        "skills": detected_skills,
        "feedback": feedback
    }

def analyze_education(education: str) -> dict:
    if not education or not education.strip():
        return {
            "status": "missing",
            "score": 0,
            "feedback": ["Education section is missing."]
        }

    word_count = len(education.split())
    score = 100
    feedback = []

    if word_count < 5:
        score -= 40
        feedback.append(
            "Education details are too brief. Add your degree, institution, and academic details."
        )
    elif word_count < 10:
        score -= 20
        feedback.append(
            "Consider adding institution, graduation details, or academic achievements."
        )

    if not feedback:
        feedback.append(
            "Education section contains sufficient information."
        )

    return {
        "status": "present",
        "score": score,
        "feedback": feedback
    }

def analyze_certifications(certifications: str) -> dict:
    if not certifications or not certifications.strip():
        return {
            "status": "missing",
            "score": 0,
            "feedback": ["Certifications section is missing."]
        }

    certification_count = len(
        [line for line in certifications.splitlines() if line.strip()]
    )

    score = min(certification_count * 25, 100)

    if certification_count == 1:
        feedback = [
            "Consider adding more relevant certifications or achievements."
        ]
    elif certification_count < 4:
        feedback = [
            "Certifications section contains relevant information."
        ]
    else:
        feedback = [
            "Certifications section contains a good range of achievements."
        ]

    return {
        "status": "present",
        "score": score,
        "feedback": feedback
    }

def calculate_resume_quality(section_analysis: dict) -> int:
    weights = {
        "professional_summary": 0.15,
        "technical_skills": 0.20,
        "projects": 0.25,
        "experience": 0.20,
        "education": 0.10,
        "certifications": 0.10
    }

    return round(
        sum(
            section_analysis.get(section, {}).get("score", 0) * weight
            for section, weight in weights.items()
        )
    )

def generate_improvement_suggestions(
    missing_skills: list,
    missing_sections: list,
    section_analysis: dict
) -> list:

    suggestions = []

    if missing_skills:
        suggestions.append(
            f"Add relevant missing skills: {', '.join(missing_skills)}."
        )

    if missing_sections:
        suggestions.append(
            f"Consider adding missing sections: {', '.join(missing_sections)}."
        )

    for analysis in section_analysis.values():
        suggestions.extend(analysis.get("feedback", []))

    return suggestions