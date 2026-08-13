"""
Database Session Management Module

This module handles database session creation and management.
Uses dependency injection to provide sessions to FastAPI endpoints.

Features:
    - SessionLocal factory for creating new sessions
    - Automatic session cleanup using dependency injection
    - Proper connection lifecycle management

Usage:
    from app.database.session import get_db
    
    async def my_endpoint(db: Session = Depends(get_db)):
        # Use db session
        user = db.query(User).first()
"""

from sqlalchemy.orm import sessionmaker, Session
from app.database.config import engine
from typing import Generator

# Create a factory for creating new database sessions
SessionLocal = sessionmaker(
    autocommit=False,      # Don't auto-commit changes
    autoflush=False,       # Don't auto-flush changes
    bind=engine            # Bind to the engine
)

async def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection function for database sessions.
    
    This function is used as a dependency in FastAPI endpoints
    to automatically provide and cleanup database sessions.
    
    Usage in endpoint:
        @router.get("/items")
        async def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    
    Yields:
        Session: A database session for the request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

__all__ = ["SessionLocal", "get_db"]
