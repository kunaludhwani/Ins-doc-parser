"""
Response schemas for API endpoints
"""
from pydantic import BaseModel
from typing import Optional


class UploadResponse(BaseModel):
    status: str
    is_insurance: bool
    summary: str


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
