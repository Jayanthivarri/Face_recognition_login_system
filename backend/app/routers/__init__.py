"""
Routers Module

Contains API router definitions for different endpoints.
Each router handles a specific set of related endpoints.

Routers:
    - user: Registration, login, profile, and user list endpoints
"""

from app.routers.user import router as user_router

__all__ = [
    "user_router",
]
