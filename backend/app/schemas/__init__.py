"""
Schemas Module

Exports all Pydantic models for request/response validation.
These schemas provide type safety and automatic validation for API operations.

Exports:
    - User schemas: UserCreate, UserResponse, LoginRequest, LoginResponse
    - Response schemas: ErrorResponse, SuccessResponse, MessageResponse
    - Validation schemas: ValidationErrorDetail, ValidationErrorResponse
"""

from app.schemas.user import (
    UserCreate,
    UserResponse,
    LoginRequest,
    LoginResponse
)
from app.schemas.response import (
    ErrorResponse,
    SuccessResponse,
    MessageResponse,
    ValidationErrorDetail,
    ValidationErrorResponse
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserResponse",
    "LoginRequest",
    "LoginResponse",
    # Response schemas
    "ErrorResponse",
    "SuccessResponse",
    "MessageResponse",
    "ValidationErrorDetail",
    "ValidationErrorResponse"
]
