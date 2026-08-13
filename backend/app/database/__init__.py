"""
Database Module

Provides database configuration, session management, and models initialization.

Exports:
    - engine: SQLAlchemy engine
    - SessionLocal: Session factory
    - get_db: Dependency injection function for sessions
    - Base: Declarative base for ORM models
    - init_db: Function to initialize database tables
"""

from app.database.config import engine, DATABASE_URL
from app.database.session import SessionLocal, get_db
from app.database.base import Base

def init_db():
    """
    Initialize database by creating all tables.
    
    This function should be called once during application startup.
    It creates all tables defined in the ORM models that inherit from Base.
    
    Usage:
        from app.database import init_db
        init_db()
    """
    # Import all models to register them with Base
    from app.models import user  # noqa: F401
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")

__all__ = [
    "engine",
    "SessionLocal",
    "get_db",
    "Base",
    "init_db",
    "DATABASE_URL"
]
