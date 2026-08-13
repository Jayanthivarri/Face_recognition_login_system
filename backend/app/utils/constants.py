"""
Application Constants Module

Defines all constant values used throughout the application.
These include thresholds, limits, and configuration values.

Constants:
    - Face recognition thresholds
    - Field length limits
    - API constraints
    - Error messages
"""

import os

# ============================================================================
# Face Recognition Configuration
# ============================================================================

# Euclidean distance threshold for face matching
# If distance < FACE_MATCH_THRESHOLD -> Same person
# If distance >= FACE_MATCH_THRESHOLD -> Different person
FACE_MATCH_THRESHOLD = float(os.getenv("FACE_MATCH_THRESHOLD", "0.4"))

# Face embedding dimensions (FaceRecognitionNet output)
FACE_EMBEDDING_DIMENSION = 128

# Valid range for face embedding values
FACE_EMBEDDING_MIN = -2.0
FACE_EMBEDDING_MAX = 2.0

# ============================================================================
# User Data Constraints
# ============================================================================

# First Name constraints
FIRST_NAME_MIN_LENGTH = 2
FIRST_NAME_MAX_LENGTH = 100

# Last Name constraints
LAST_NAME_MIN_LENGTH = 2
LAST_NAME_MAX_LENGTH = 100

# Email constraints
EMAIL_MAX_LENGTH = 255

# Age constraints
AGE_MIN = 18
AGE_MAX = 120

# ============================================================================
# Pagination Settings
# ============================================================================

# Default number of items per page
DEFAULT_PAGE_SIZE = 50

# Maximum items per page
MAX_PAGE_SIZE = 100

# ============================================================================
# API Response Messages
# ============================================================================

# Success messages
MSG_REGISTRATION_SUCCESS = "User registered successfully"
MSG_LOGIN_SUCCESS = "Login successful! Face matched."
MSG_USER_RETRIEVED = "User retrieved successfully"
MSG_USERS_RETRIEVED = "Users retrieved successfully"
MSG_HEALTH_OK = "API is healthy and running"

# Error messages
MSG_EMAIL_EXISTS = "Email already registered"
MSG_USER_NOT_FOUND = "User not found"
MSG_FACE_MATCH_FAILED = "No matching face found"
MSG_INVALID_EMBEDDING = "Invalid face embedding provided"
MSG_VALIDATION_ERROR = "Validation error"
MSG_INTERNAL_ERROR = "An unexpected error occurred"
MSG_DATABASE_ERROR = "Database operation failed"

# ============================================================================
# Error Codes
# ============================================================================

ERROR_CODE_VALIDATION = "VALIDATION_ERROR"
ERROR_CODE_DUPLICATE = "DUPLICATE_EMAIL"
ERROR_CODE_NOT_FOUND = "NOT_FOUND"
ERROR_CODE_FACE_MATCH = "FACE_MATCHING_ERROR"
ERROR_CODE_AUTH = "AUTHENTICATION_ERROR"
ERROR_CODE_INTERNAL = "INTERNAL_ERROR"

# ============================================================================
# Database Settings
# ============================================================================

# Database URL (from environment or default)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./face_recognition.db")

# SQLAlchemy pool settings for SQLite
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_MAX_OVERFLOW = 10
SQLALCHEMY_POOL_TIMEOUT = 30

# ============================================================================
# Application Settings
# ============================================================================

# Application name
APP_NAME = os.getenv("APP_NAME", "Face Recognition Login System")

# Application version
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# Debug mode
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# API host and port
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# ============================================================================
# CORS Settings
# ============================================================================

# Allowed origins for CORS
CORS_ORIGINS = [
    "http://localhost:5173",      # Frontend dev server (Vite)
    "http://localhost:3000",      # Alternative frontend
    "http://localhost:8080",      # Another alternative
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
]

# Allow credentials in CORS requests
CORS_ALLOW_CREDENTIALS = True

# Allowed methods in CORS
CORS_ALLOW_METHODS = ["*"]

# Allowed headers in CORS
CORS_ALLOW_HEADERS = ["*"]

# ============================================================================
# Validation Regex Patterns
# ============================================================================

# Email pattern (RFC 5322 simplified)
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Name pattern (letters, spaces, hyphens, apostrophes)
NAME_PATTERN = r'^[a-zA-Z\s\-\']{2,100}$'

# ============================================================================
# HTTP Status Codes (for reference)
# ============================================================================

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_UNPROCESSABLE_ENTITY = 422
HTTP_INTERNAL_SERVER_ERROR = 500

__all__ = [
    # Face recognition
    "FACE_MATCH_THRESHOLD",
    "FACE_EMBEDDING_DIMENSION",
    "FACE_EMBEDDING_MIN",
    "FACE_EMBEDDING_MAX",
    # User constraints
    "FIRST_NAME_MIN_LENGTH",
    "FIRST_NAME_MAX_LENGTH",
    "LAST_NAME_MIN_LENGTH",
    "LAST_NAME_MAX_LENGTH",
    "EMAIL_MAX_LENGTH",
    "AGE_MIN",
    "AGE_MAX",
    # Pagination
    "DEFAULT_PAGE_SIZE",
    "MAX_PAGE_SIZE",
    # Messages
    "MSG_REGISTRATION_SUCCESS",
    "MSG_LOGIN_SUCCESS",
    "MSG_USER_RETRIEVED",
    "MSG_USERS_RETRIEVED",
    "MSG_HEALTH_OK",
    "MSG_EMAIL_EXISTS",
    "MSG_USER_NOT_FOUND",
    "MSG_FACE_MATCH_FAILED",
    "MSG_INVALID_EMBEDDING",
    "MSG_VALIDATION_ERROR",
    "MSG_INTERNAL_ERROR",
    "MSG_DATABASE_ERROR",
    # Error codes
    "ERROR_CODE_VALIDATION",
    "ERROR_CODE_DUPLICATE",
    "ERROR_CODE_NOT_FOUND",
    "ERROR_CODE_FACE_MATCH",
    "ERROR_CODE_AUTH",
    "ERROR_CODE_INTERNAL",
    # Database
    "DATABASE_URL",
    "SQLALCHEMY_POOL_SIZE",
    "SQLALCHEMY_MAX_OVERFLOW",
    "SQLALCHEMY_POOL_TIMEOUT",
    # Application
    "APP_NAME",
    "APP_VERSION",
    "DEBUG",
    "API_HOST",
    "API_PORT",
    # CORS
    "CORS_ORIGINS",
    "CORS_ALLOW_CREDENTIALS",
    "CORS_ALLOW_METHODS",
    "CORS_ALLOW_HEADERS",
    # Patterns
    "EMAIL_PATTERN",
    "NAME_PATTERN",
    # Status codes
    "HTTP_OK",
    "HTTP_CREATED",
    "HTTP_BAD_REQUEST",
    "HTTP_UNAUTHORIZED",
    "HTTP_NOT_FOUND",
    "HTTP_CONFLICT",
    "HTTP_UNPROCESSABLE_ENTITY",
    "HTTP_INTERNAL_SERVER_ERROR",
]
