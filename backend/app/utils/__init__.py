"""
Utils Module

Provides utility functions, validators, custom exceptions, helpers, and constants
for the entire application.

Exports:
    - Exceptions: Custom exception classes
    - Validators: Input validation functions
    - Helpers: Helper functions for common operations
    - Constants: Application-wide constants
"""

from app.utils.exceptions import (
    AppException,
    ValidationException,
    NotFoundError,
    DuplicateError,
    AuthenticationError,
    FaceMatchingError,
    InternalServerError
)
from app.utils.validators import (
    validate_email,
    validate_face_embedding,
    validate_age,
    validate_name
)
from app.utils.helpers import (
    format_error_response,
    format_success_response,
    PaginatedResponse,
    get_pagination_params
)
from app.utils import constants

__all__ = [
    # Exceptions
    "AppException",
    "ValidationException",
    "NotFoundError",
    "DuplicateError",
    "AuthenticationError",
    "FaceMatchingError",
    "InternalServerError",
    # Validators
    "validate_email",
    "validate_face_embedding",
    "validate_age",
    "validate_name",
    # Helpers
    "format_error_response",
    "format_success_response",
    "PaginatedResponse",
    "get_pagination_params",
    # Constants
    "constants"
]
