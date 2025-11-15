"""
Text extraction service
Extracts text from PDF, Word documents, and images (OCR)
"""
import io
from PyPDF2 import PdfReader
from docx import Document


async def extract_text(file_content: bytes, file_extension: str) -> str:
    """
    Extract text from various file formats

    Args:
        file_content: File content as bytes
        file_extension: File extension (.pdf, .docx, .jpg, etc.)

    Returns:
        Extracted text as string
    """
    text = ""

    try:
        if file_extension == ".pdf":
            # Extract text from PDF
            pdf_reader = PdfReader(io.BytesIO(file_content))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        elif file_extension in [".doc", ".docx"]:
            # Extract text from Word document
            doc = Document(io.BytesIO(file_content))
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"

        elif file_extension in [".jpg", ".jpeg", ".png"]:
            # For images, try OCR but gracefully fail
            try:
                from app.utils.ocr import extract_text_from_image
                text = await extract_text_from_image(file_content)
            except ImportError:
                raise Exception(
                    "Image OCR requires Tesseract. Please upload a PDF or Word document instead.")
            except Exception as ocr_error:
                raise Exception(
                    f"Could not extract text from image: {str(ocr_error)}")

        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        return text.strip()

    except Exception as e:
        raise Exception(f"Error extracting text: {str(e)}")
