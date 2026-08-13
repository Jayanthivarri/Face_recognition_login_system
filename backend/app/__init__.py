"""
Face Recognition Login System - FastAPI Application Package

A production-grade passwordless authentication system using facial recognition.

This package contains:
- Database models and schemas
- API routers and endpoints
- Business logic services
- Utility functions and validators

Main entry point: app.main:app
"""

from app.main import app

__version__ = "1.0.0"
__author__ = "Face Recognition System"

__all__ = ["app"]
