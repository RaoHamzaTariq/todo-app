"""
Error response schemas for the Todo API.
"""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response format."""

    detail: str


class ValidationErrorResponse(BaseModel):
    """Validation error response format."""

    detail: str
    errors: list[dict]
