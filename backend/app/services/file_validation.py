"""
File validation service
Validates file type, size, and page count
"""
import io
from PyPDF2 import PdfReader
from app.config import settings


async def validate_file(file_content: bytes, file_extension: str, filename: str) -> dict:
    """
    Validate uploaded file

    Returns:
        dict with 'valid' boolean and optional 'error' message and 'page_count'
    """
    # Check file extension
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        return {
            "valid": False,
            "error": f"File type {file_extension} not supported. Please upload PDF, DOC, DOCX, JPG, or PNG files."
        }

    # Check file size (10 MB limit)
    file_size_mb = len(file_content) / (1024 * 1024)
    if file_size_mb > settings.MAX_FILE_SIZE_MB:
        return {
            "valid": False,
            "error": f"File size ({file_size_mb:.2f} MB) exceeds the maximum allowed size of {settings.MAX_FILE_SIZE_MB} MB."
        }

    # Check page count for PDFs
    page_count = 1
    if file_extension == ".pdf":
        try:
            pdf_reader = PdfReader(io.BytesIO(file_content))
            page_count = len(pdf_reader.pages)

            if page_count > settings.MAX_PAGES:
                return {
                    "valid": False,
                    "error": f"PDF has {page_count} pages, which exceeds the maximum allowed limit of {settings.MAX_PAGES} pages."
                }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Error reading PDF file: {str(e)}"
            }

    return {
        "valid": True,
        "page_count": page_count
    }
