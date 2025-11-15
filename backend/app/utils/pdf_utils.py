"""
PDF utility functions
"""
from PyPDF2 import PdfReader
import io


def get_pdf_page_count(pdf_content: bytes) -> int:
    """
    Get number of pages in PDF

    Args:
        pdf_content: PDF file content as bytes

    Returns:
        Number of pages
    """
    pdf_reader = PdfReader(io.BytesIO(pdf_content))
    return len(pdf_reader.pages)


def extract_pdf_text(pdf_content: bytes) -> str:
    """
    Extract all text from PDF

    Args:
        pdf_content: PDF file content as bytes

    Returns:
        Extracted text
    """
    text = ""
    pdf_reader = PdfReader(io.BytesIO(pdf_content))

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()
