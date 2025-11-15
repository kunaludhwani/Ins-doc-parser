"""
Log schemas
"""
from pydantic import BaseModel
from datetime import datetime


class LogEntry(BaseModel):
    id: int
    timestamp: datetime
    file_type: str
    page_count: int
    text_length: int
    explanation: str
