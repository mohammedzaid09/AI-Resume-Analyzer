import re


SECTION_ALIASES = {

    "professional_summary": [
        "professional summary",
        "summary",
        "profile",
        "career objective",
        "objective"
    ],

    "education": [
        "education",
        "academic background",
        "academic qualifications",
        "qualifications"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "internship",
        "internships"
    ],

    "projects": [
        "projects",
        "personal projects",
        "academic projects",
        "project experience"
    ],

    "technical_skills": [
        "technical skills",
        "skills",
        "core competencies",
        "technical competencies",
        "technical expertise"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "certifications & achievements",
        "certifications and achievements",
        "licenses",
        "achievements"
    ]
}

REQUIRED_SECTIONS = [
    "professional_summary",
    "education",
    "experience",
    "projects",
    "technical_skills"
]


def normalize_heading(text: str) -> str:
    """
    Normalize a possible section heading.
    """

    text = text.lower().strip()

    text = re.sub(r"\s+", " ", text)

    return text


def identify_heading(line: str):
    """
    Check whether a line is a known section heading.

    Returns:
        (section_name, inline_content)
    """

    original_line = line.strip()
    normalized_line = normalize_heading(original_line)

    for section, aliases in SECTION_ALIASES.items():

        sorted_aliases = sorted(
            aliases,
            key=len,
            reverse=True
        )

        for alias in sorted_aliases:

            # Exact heading
            if normalized_line == alias:
                return section, ""

            # Heading followed by : or -
            pattern = (
                r"^" +
                re.escape(alias) +
                r"\s*[:\-–—]\s*(.+)$"
            )

            match = re.match(
                pattern,
                original_line,
                flags=re.IGNORECASE
            )

            if match:
                return section, match.group(1).strip()

    return None, None


def detect_sections(resume_text: str) -> dict:
    """
    Detect common resume sections and extract their content.
    Supports:

    - TECHNICAL SKILLS
    - Technical Skills:
    - Technical Skills: Python, FastAPI
    - Projects - Resume Analyzer
    """

    lines = resume_text.splitlines()

    sections = {}

    current_section = None
    current_content = []

    for line in lines:

        cleaned_line = line.strip()

        if not cleaned_line:

            if current_section:
                current_content.append("")

            continue

        section_name, inline_content = identify_heading(cleaned_line)

        # New section found
        if section_name:

            # Save the previous section
            if current_section:

                content = "\n".join(
                    current_content
                ).strip()

                if content:
                    sections[current_section] = content

            # Start new section
            current_section = section_name
            current_content = []

            # If content exists on the same line as heading
            if inline_content:
                current_content.append(inline_content)

        else:

            # Normal content belonging to current section
            if current_section:
                current_content.append(cleaned_line)

    # Save the last section
    if current_section:

        content = "\n".join(
            current_content
        ).strip()

        if content:
            sections[current_section] = content

    missing_sections = []

    for section in REQUIRED_SECTIONS:
        if section not in sections:
            missing_sections.append(section)

    return {
        "sections": sections,
        "missing_sections": missing_sections
    }