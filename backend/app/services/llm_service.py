import os
import re

from dotenv import load_dotenv
from ollama import chat


load_dotenv()

# Keep the model configurable through .env
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:0.6b")


# ============================================================
# AI FEEDBACK
# ============================================================

def generate_ai_feedback(
    ats_score: int,
    resume_quality_score: int,
    missing_skills: list[str],
    missing_sections: list[str],
    section_analysis: dict,
    job_title: str = ""
) -> str:
    """
    Generate personalized and actionable resume feedback
    using a local Ollama model.
    """

    weak_sections = []
    section_feedback = []

    for section_name, analysis in section_analysis.items():

        score = analysis.get("score", 100)

        if score < 70:
            weak_sections.append(
                f"{section_name.replace('_', ' ')} ({score}/100)"
            )

        feedback = analysis.get("feedback", [])

        if feedback:
            section_feedback.append(
                f"{section_name.replace('_', ' ')}: "
                + " ".join(feedback)
            )

    prompt = f"""
/no_think

You are a professional resume reviewer.

Your task is to generate personalized resume improvement
recommendations based ONLY on the analysis data provided below.

RESUME ANALYSIS DATA

Target Job Title:
{job_title or "Not specified"}

ATS Score:
{ats_score}/100

Resume Quality Score:
{resume_quality_score}/100

Missing Skills:
{", ".join(missing_skills) if missing_skills else "None"}

Missing Resume Sections:
{", ".join(missing_sections) if missing_sections else "None"}

Weak Sections:
{", ".join(weak_sections) if weak_sections else "None"}

Section Feedback:
{" | ".join(section_feedback) if section_feedback else "None"}

STRICT RULES

1. Use ONLY the information provided above.

2. NEVER invent or assume:
   - years of experience
   - projects
   - achievements
   - certifications
   - technical skills
   - job responsibilities
   - numbers
   - percentages
   - metrics

3. If recommending a missing skill, clearly say:
   "only if you have practical experience with it."

4. Do NOT recommend creating a separate section
   for an individual technical skill.

5. Do NOT repeat the same recommendation.

6. Prioritize the most important weaknesses.

7. Give practical recommendations that explain WHAT
   should be improved and WHERE it should be improved.

8. Do not mention that you are an AI.

9. Do not repeat the scores.

10. Keep every recommendation aligned with the
    specific resume section mentioned in the analysis.

11. Do not recommend adding technical skills
    to the Education section.

12. Do not use claims such as achievements,
    accomplishments, impact, or performance unless
    explicitly supported by the analysis data.

13. For the Experience section, only recommend improving
    responsibilities and contributions if those are
    mentioned in the section feedback.

14. For Technical Skills, recommend adding or improving
    skills only within the Technical Skills section or
    relevant project/experience descriptions.

15. Do not combine unrelated resume sections.

OUTPUT FORMAT

Return only a numbered list containing 3 to 5 recommendations.
Do not add an introduction or conclusion.
"""

    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.2
        }
    )

    return response.message.content.strip()


# ============================================================
# RESUME SECTION REWRITING
# ============================================================

def _build_rewrite_prompt(
    section_name: str,
    content: str
) -> str:
    """
    Build a prompt for substantially improving resume wording
    while preserving all original information.
    """

    return f"""
/no_think

You are a professional resume editor.

Rewrite the resume content below to make it significantly
more professional, clear, concise, and polished.

Make a MAJOR improvement to the wording and sentence structure.
Do not simply make minor grammar corrections.

IMPORTANT:
Change the wording and structure, NOT the information.

You MUST preserve:
- every skill
- every technology
- every project feature
- every responsibility
- every fact
- every number
- every date
- the original meaning

You MUST NOT:
- add new skills
- remove skills
- replace skills with different skills
- add technologies
- remove technologies
- invent achievements
- invent responsibilities
- invent metrics
- invent numbers
- invent dates
- invent users, scale, performance, impact, or results
- add information that is not present
- change project titles
- change section titles
- change labels such as "Tech Stack"
- add a section heading
- add an introduction
- add a conclusion
- explain your changes
- summarize what you changed
- mention these instructions

Improve:
- grammar
- sentence structure
- word choice
- clarity
- readability
- professional resume language

You may completely restructure sentences when needed,
but every statement must remain supported by the original content.

The goal is to make the existing content sound substantially
better while keeping exactly the same factual information.

OUTPUT RULES:

Return ONLY the rewritten resume content.

Do NOT include:
- explanations
- comments
- summaries
- notes
- analysis
- statements about preserving information
- statements about improving the content
- statements about what you changed

Do not write anything before the rewritten content.
Do not write anything after the rewritten content.

The response must end immediately after the final
rewritten sentence or bullet point.

SECTION:
{section_name}

CONTENT:
{content}
"""


def _extract_numbers(text: str) -> list[str]:
    """
    Extract numbers and percentages that should be preserved.
    """

    return re.findall(
        r"\b\d+(?:\.\d+)?%?\b",
        text
    )


def _extract_technical_terms(text: str) -> list[str]:
    """
    Find technical terms that are already present in the
    original content.
    """

    technical_terms = [
        "python",
        "java",
        "c++",
        "c#",
        "javascript",
        "typescript",
        "sql",
        "html",
        "css",
        "react",
        "angular",
        "vue",
        "fastapi",
        "django",
        "flask",
        "spring",
        "spring boot",
        "node",
        "nodejs",
        "express",
        "postgresql",
        "mysql",
        "mongodb",
        "redis",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "git",
        "github",
        "machine learning",
        "deep learning",
        "data science",
        "data analysis",
        "pandas",
        "numpy",
        "tensorflow",
        "pytorch",
    ]

    original_lower = text.lower()

    return [
        term
        for term in technical_terms
        if term in original_lower
    ]


def _remove_unwanted_heading(
    section_name: str,
    text: str
) -> str:
    """
    Remove an accidental section heading generated by the model.

    Example:

        Projects
        Built an AI Resume Analyzer...

    becomes:

        Built an AI Resume Analyzer...
    """

    lines = text.strip().splitlines()

    if not lines:
        return text.strip()

    first_line = lines[0].strip().lower()

    section_titles = {
        "professional summary",
        "summary",
        "projects",
        "project",
        "experience",
        "work experience",
        "technical skills",
        "skills",
        "education",
        "certifications",
        "certification",
    }

    if first_line in section_titles:
        lines = lines[1:]

    return "\n".join(lines).strip()


def _validate_rewrite(
    original: str,
    rewritten: str
) -> bool:
    """
    Validate rewritten resume content.

    Rejects empty output, AI commentary, unwanted headings,
    and changes to important factual information.
    """

    if not original.strip():
        return False

    if not rewritten.strip():
        return False

    rewritten_lower = rewritten.lower()

    # --------------------------------------------------------
    # Reject obvious AI explanations / commentary
    # --------------------------------------------------------

    forbidden_phrases = [
        "analysis:",
        "explanation:",
        "changes made:",
        "rewritten version:",
        "here is the rewritten",
        "here's the rewritten",
        "improved version:",
        "no changes made",
        "each skill and fact",
        "this restructure",
        "this rewrite",
        "this version",
        "this revised version",
        "maintains all original",
        "while enhancing clarity",
        "end.",
    ]

    for phrase in forbidden_phrases:
        if phrase in rewritten_lower:
            return False

    # --------------------------------------------------------
    # Reject model-generated section headings
    # --------------------------------------------------------

    unwanted_headings = [
        "professional_summary",
        "professional summary",
        "technical skills:",
        "experience:",
        "projects:",
        "education:",
        "certifications:",
    ]

    for heading in unwanted_headings:
        if heading in rewritten_lower:
            return False

    # --------------------------------------------------------
    # Preserve numbers
    # --------------------------------------------------------

    original_numbers = _extract_numbers(original)

    for number in original_numbers:
        if number not in rewritten:
            return False

    # --------------------------------------------------------
    # Preserve existing technical skills
    # --------------------------------------------------------

    original_terms = _extract_technical_terms(original)

    for term in original_terms:
        if term not in rewritten_lower:
            return False

    # --------------------------------------------------------
    # Prevent common skill hallucinations
    # --------------------------------------------------------

    # If the original contains C but not C++, the model must
    # not introduce C++ as a new skill.
    if (
        "c++" not in original.lower()
        and "c++" in rewritten_lower
    ):
        return False

    return True


def rewrite_resume_section(
    section_name: str,
    content: str
) -> str:
    """
    Improve a selected resume section.

    The model is intentionally given a simple task:
    improve the wording while keeping the original information.
    """

    # --------------------------------------------------------
    # Empty content
    # --------------------------------------------------------

    if not content or not content.strip():
        return content

    # --------------------------------------------------------
    # Build prompt
    # --------------------------------------------------------

    prompt = _build_rewrite_prompt(
        section_name=section_name,
        content=content
    )

    # --------------------------------------------------------
    # Call Ollama
    # --------------------------------------------------------

    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional resume editor. "
                    "Substantially improve the wording and sentence "
                    "structure of the provided resume content. Correct "
                    "grammar and make the writing more professional "
                    "while preserving the original information and skills. "
                    "Do not invent information or add new skills. "
                    "Return only the rewritten resume content."                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.1
        }
    )

    rewritten = response.message.content.strip()

    # --------------------------------------------------------
    # Remove accidental section heading
    # --------------------------------------------------------

    rewritten = _remove_unwanted_heading(
        section_name=section_name,
        text=rewritten
    )

    # --------------------------------------------------------
    # Validate the result
    # --------------------------------------------------------

    if _validate_rewrite(
        original=content,
        rewritten=rewritten
    ):
        return rewritten

    # --------------------------------------------------------
    # Safe fallback
    # --------------------------------------------------------

    return content

