"""
Helper Functions Module

Provides utility functions for common operations throughout the application.

Functions:
    - format_error_response: Format error responses consistently
    - format_success_response: Format success responses consistently
    - get_paginated_query: Helper for pagination
"""

from typing import Dict, Any, Optional, List, TypeVar, Generic
from datetime import datetime

T = TypeVar('T')

def format_error_response(
    message: str,
    error_code: str = "UNKNOWN_ERROR",
    details: Optional[Dict[str, Any]] = None,
    status_code: int = 500
) -> Dict[str, Any]:
    """
    Format error response consistently.
    
    Args:
        message: Error message
        error_code: Error code for client handling
        details: Additional details
        status_code: HTTP status code
    
    Returns:
        dict: Formatted error response
    """
    return {
        "success": False,
        "message": message,
        "error_code": error_code,
        "details": details or {},
        "timestamp": datetime.utcnow().isoformat()
    }


def format_success_response(
    message: str = "Operation successful",
    data: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Format success response consistently.
    
    Args:
        message: Success message
        data: Response data
    
    Returns:
        dict: Formatted success response
    """
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }


class PaginatedResponse(Generic[T]):
    """
    Generic paginated response wrapper.
    
    Attributes:
        items: List of items in this page
        total: Total number of items
        page: Current page number
        page_size: Items per page
        total_pages: Total number of pages
    """
    
    def __init__(
        self,
        items: List[T],
        total: int,
        page: int,
        page_size: int
    ):
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size
        self.total_pages = (total + page_size - 1) // page_size
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON response."""
        return {
            "items": self.items,
            "pagination": {
                "total": self.total,
                "page": self.page,
                "page_size": self.page_size,
                "total_pages": self.total_pages
            }
        }


def get_pagination_params(
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    default_limit: int = 50,
    max_limit: int = 100
) -> tuple[int, int]:
    """
    Get validated pagination parameters.
    
    Args:
        skip: Number of items to skip
        limit: Number of items to return
        default_limit: Default limit if not provided
        max_limit: Maximum allowed limit
    
    Returns:
        tuple: (skip, limit) validated values
    """
    skip = skip or 0
    limit = limit or default_limit
    
    # Ensure skip is non-negative
    skip = max(0, skip)
    
    # Ensure limit is within bounds
    limit = max(1, min(limit, max_limit))
    
    return skip, limit


__all__ = [
    "format_error_response",
    "format_success_response",
    "PaginatedResponse",
    "get_pagination_params"
]
