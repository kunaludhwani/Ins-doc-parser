"""
OCR utility using Tesseract
Extracts text from images
"""
import io
from PIL import Image
import pytesseract


async def extract_text_from_image(image_content: bytes) -> str:
    """
    Extract text from image using OCR

    Args:
        image_content: Image file content as bytes

    Returns:
        Extracted text
    """
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(image_content))

        # Perform OCR
        text = pytesseract.image_to_string(image)

        return text.strip()

    except Exception as e:
        raise Exception(f"OCR extraction failed: {str(e)}")
