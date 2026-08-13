"""
Exception Handling Module

Defines custom exceptions for the application and their HTTP status codes.
These exceptions are caught by FastAPI exception handlers for consistent error responses.

Exceptions:
    - AppException: Base application exception
    - ValidationException: Input validation errors
    - NotFound: Resource not found
    - DuplicateError: Duplicate resource (email already registered)
    - AuthenticationError: Authentication failures
    - FaceMatchingError: Face matching operation errors
"""

from fastapi import status
from typing import Optional, Dict, Any

class AppException(Exception):
    """
    Base application exception.
    
    All custom exceptions inherit from this base class.
    
    Attributes:
        message: Error message
        error_code: Error code for client-side handling
        status_code: HTTP status code
        details: Additional error details
    """
    
    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(AppException):
    """
    Validation error exception.
    
    Raised when input validation fails (invalid format, out of range, etc.)
    
    HTTP Status: 422 Unprocessable Entity
    """
    
    def __init__(
        self,
        message: str = "Validation failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class NotFoundError(AppException):
    """
    Resource not found exception.
    
    Raised when a requested resource doesn't exist.
    
    HTTP Status: 404 Not Found
    """
    
    def __init__(
        self,
        message: str = "Resource not found",
        resource_type: str = "Resource",
        resource_id: Optional[Any] = None
    ):
        details = {
            "resource_type": resource_type,
            "resource_id": resource_id
        } if resource_id else {"resource_type": resource_type}
        
        super().__init__(
            message=message,
            error_code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )


class DuplicateError(AppException):
    """
    Duplicate resource exception.
    
    Raised when attempting to create a resource that already exists
    (e.g., email already registered).
    
    HTTP Status: 409 Conflict
    """
    
    def __init__(
        self,
        message: str = "Resource already exists",
        field: str = "",
        value: Optional[Any] = None
    ):
        details = {}
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = value
        
        super().__init__(
            message=message,
            error_code="DUPLICATE_RESOURCE",
            status_code=status.HTTP_409_CONFLICT,
            details=details
        )


class AuthenticationError(AppException):
    """
    Authentication error exception.
    
    Raised when authentication fails or is required but missing.
    
    HTTP Status: 401 Unauthorized
    """
    
    def __init__(
        self,
        message: str = "Authentication failed",
        reason: str = ""
    ):
        details = {"reason": reason} if reason else {}
        
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details
        )


class FaceMatchingError(AppException):
    """
    Face matching operation error exception.
    
    Raised when face matching fails or no match is found.
    
    HTTP Status: 400 Bad Request
    """
    
    def __init__(
        self,
        message: str = "Face matching failed",
        reason: str = "",
        confidence: Optional[float] = None
    ):
        details = {}
        if reason:
            details["reason"] = reason
        if confidence is not None:
            details["confidence"] = confidence
        
        super().__init__(
            message=message,
            error_code="FACE_MATCHING_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class InternalServerError(AppException):
    """
    Internal server error exception.
    
    Raised for unexpected application errors.
    
    HTTP Status: 500 Internal Server Error
    """
    
    def __init__(
        self,
        message: str = "An unexpected error occurred",
        error_type: Optional[str] = None
    ):
        details = {"error_type": error_type} if error_type else {}
        
        super().__init__(
            message=message,
            error_code="INTERNAL_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


__all__ = [
    "AppException",
    "ValidationException",
    "NotFoundError",
    "DuplicateError",
    "AuthenticationError",
    "FaceMatchingError",
    "InternalServerError"
]
