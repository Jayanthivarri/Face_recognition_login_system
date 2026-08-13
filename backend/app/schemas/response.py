"""
Common Response Schemas Module

Defines reusable response schemas for consistent API responses.
These schemas are used for error responses, success messages, and generic data wrapping.

Schemas:
    - ErrorResponse: Standard error response format
    - SuccessResponse: Standard success response format
    - MessageResponse: Simple message-only response
"""

from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from datetime import datetime

class ErrorResponse(BaseModel):
    """
    Standard error response schema.
    
    Used for all error responses across the API for consistency.
    
    Attributes:
        success: Always False for error responses
        message: Human-readable error message
        error_code: Error code for client-side handling
        details: Additional error details or validation errors
        timestamp: When the error occurred
    """
    
    success: bool = False
    message: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code for client handling")
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional error details"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of error"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Email already registered",
                "error_code": "DUPLICATE_EMAIL",
                "details": {
                    "field": "email",
                    "value": "john@example.com"
                },
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class SuccessResponse(BaseModel):
    """
    Standard success response schema.
    
    Wraps successful operation responses with metadata.
    
    Attributes:
        success: Always True for success responses
        message: Operation result message
        data: Response data (generic, can be any object)
        timestamp: When the response was generated
    """
    
    success: bool = True
    message: str = Field(..., description="Success message")
    data: Optional[Any] = Field(
        None,
        description="Response data"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "User created successfully",
                "data": {
                    "user_id": 1,
                    "email": "john@example.com"
                },
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class MessageResponse(BaseModel):
    """
    Simple message-only response schema.
    
    Used for simple acknowledgments and status messages.
    
    Attributes:
        message: Response message
        status: Operation status (success, error, pending, etc.)
    """
    
    message: str = Field(..., description="Message content")
    status: str = Field(
        "success",
        description="Response status"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation completed",
                "status": "success"
            }
        }


class ValidationErrorDetail(BaseModel):
    """
    Detail of a validation error.
    
    Used in error responses for form/input validation.
    
    Attributes:
        field: Name of the field with error
        message: Error message for this field
        value: The invalid value (optional)
    """
    
    field: str
    message: str
    value: Optional[Any] = None


class ValidationErrorResponse(ErrorResponse):
    """
    Validation error response with detailed field errors.
    
    Extends ErrorResponse with field-level validation details.
    
    Attributes:
        validation_errors: List of field-level errors
    """
    
    validation_errors: list[ValidationErrorDetail] = Field(
        default_factory=list,
        description="Field-level validation errors"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Validation failed",
                "error_code": "VALIDATION_ERROR",
                "validation_errors": [
                    {
                        "field": "email",
                        "message": "Invalid email format",
                        "value": "invalid-email"
                    },
                    {
                        "field": "age",
                        "message": "Age must be between 18 and 120",
                        "value": 150
                    }
                ],
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


__all__ = [
    "ErrorResponse",
    "SuccessResponse",
    "MessageResponse",
    "ValidationErrorDetail",
    "ValidationErrorResponse"
]
