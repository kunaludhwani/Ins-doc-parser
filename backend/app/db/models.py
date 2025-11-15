"""
Database models
"""
from datetime import datetime


class RequestLog:
    """Model for request logging"""

    def __init__(self, file_type: str, page_count: int, text_length: int, explanation: str):
        self.file_type = file_type
        self.page_count = page_count
        self.text_length = text_length
        self.explanation = explanation
        self.timestamp = datetime.now()
