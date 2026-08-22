from fastapi import APIRouter, UploadFile, File, HTTPException
import pymupdf

router = APIRouter(
    prefix="/api/resumes",
    tags=["Resumes"]
)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    try:
        # Read uploaded PDF
        contents = await file.read()

        # Open PDF from memory
        pdf_document = pymupdf.open(
            stream=contents,
            filetype="pdf"
        )

        # Extract text from all pages
        resume_text = ""

        for page in pdf_document:
            resume_text += page.get_text()

        pdf_document.close()

        # Check if text was extracted
        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from this PDF."
            )

        return {
            "success": True,
            "filename": file.filename,
            "text": resume_text
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF: {str(e)}"
        )