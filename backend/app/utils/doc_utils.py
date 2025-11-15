"""
Word document utility functions
"""
from docx import Document
import io


def extract_docx_text(docx_content: bytes) -> str:
    """
    Extract text from Word document

    Args:
        docx_content: DOCX file content as bytes

    Returns:
        Extracted text
    """
    text = ""
    doc = Document(io.BytesIO(docx_content))

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text.strip()
