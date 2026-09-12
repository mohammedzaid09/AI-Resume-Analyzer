import io

import fitz
from docx import Document


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
}


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a PDF resume.
    """

    try:
        pdf = fitz.open(
            stream=file_bytes,
            filetype="pdf"
        )

        pages = []

        for page in pdf:
            text = page.get_text()

            if text:
                pages.append(text)

        pdf.close()

        return "\n".join(pages).strip()

    except Exception as exc:
        raise ValueError(
            f"Unable to read PDF file: {exc}"
        )


def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    Extract text from a DOCX resume.
    """

    try:
        document = Document(
            io.BytesIO(file_bytes)
        )

        paragraphs = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return "\n".join(paragraphs).strip()

    except Exception as exc:
        raise ValueError(
            f"Unable to read DOCX file: {exc}"
        )


def extract_resume_text(
    filename: str,
    file_bytes: bytes
) -> str:
    """
    Extract resume text based on the file extension.
    """

    filename_lower = filename.lower()

    if filename_lower.endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)

    elif filename_lower.endswith(".docx"):
        text = extract_text_from_docx(file_bytes)

    else:
        raise ValueError(
            "Unsupported file type. "
            "Only PDF and DOCX files are supported."
        )

    if not text.strip():
        raise ValueError(
            "No readable text was found in the resume."
        )

    return text