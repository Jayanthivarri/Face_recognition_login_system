"""
FastAPI Application Initialization Module

This is the main entry point for the FastAPI application.
Configures the application with all necessary middleware, exception handlers,
and route registrations.

Features:
    - CORS configuration for frontend communication
    - Exception handlers for custom exceptions
    - Database initialization
    - Route registration
    - Startup/shutdown event handlers

Usage:
    Run with: uvicorn app.main:app --reload
    Or use: python run.py
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Callable
import logging

from app.utils.exceptions import AppException
from app.utils.constants import (
    APP_NAME,
    APP_VERSION,
    CORS_ORIGINS,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_METHODS,
    CORS_ALLOW_HEADERS,
    DEBUG
)
from app.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# Startup and Shutdown Events
# ============================================================================

async def on_startup():
    """
    Application startup event handler.
    
    Called when the application starts up.
    Initializes the database and other resources.
    """
    logger.info(f"🚀 Starting {APP_NAME} v{APP_VERSION}")
    
    try:
        # Initialize database (create tables)
        init_db()
        logger.info("✓ Database initialized successfully")
    except Exception as e:
        logger.error(f"✗ Failed to initialize database: {str(e)}")
        raise

async def on_shutdown():
    """
    Application shutdown event handler.
    
    Called when the application shuts down.
    Performs cleanup operations.
    """
    logger.info("🛑 Shutting down application")
    # Add any cleanup operations here
    logger.info("✓ Shutdown complete")

# ============================================================================
# Lifespan Context Manager
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup and shutdown.
    
    This is the recommended way in FastAPI 0.93+ to handle startup and shutdown.
    """
    # Startup
    await on_startup()
    yield
    # Shutdown
    await on_shutdown()

# ============================================================================
# FastAPI Application Creation
# ============================================================================

app = FastAPI(
    title=APP_NAME,
    description="A modern passwordless facial authentication system",
    version=APP_VERSION,
    docs_url="/api/docs",           # Swagger UI
    redoc_url="/api/redoc",         # ReDoc
    openapi_url="/api/openapi.json", # OpenAPI schema
    lifespan=lifespan
)

# ============================================================================
# CORS Middleware
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

logger.info(f"✓ CORS configured for origins: {CORS_ORIGINS}")

# ============================================================================
# Exception Handlers
# ============================================================================

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """
    Exception handler for custom AppException and its subclasses.
    
    Returns a consistent error response format for all application exceptions.
    """
    logger.warning(f"AppException: {exc.error_code} - {exc.message}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "error_code": exc.error_code,
            "details": exc.details,
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Generic exception handler for unhandled exceptions.
    
    Logs the full error details and returns a generic error response
    to prevent information leakage in production.
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    # In debug mode, return detailed error
    if DEBUG:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": str(exc),
                "error_code": "INTERNAL_ERROR",
                "details": {
                    "error_type": type(exc).__name__,
                    "debug": True
                }
            }
        )
    
    # In production, return generic error
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "An unexpected error occurred",
            "error_code": "INTERNAL_ERROR",
            "details": {}
        }
    )

# ============================================================================
# Health Check Endpoint
# ============================================================================

@app.get(
    "/api/health",
    tags=["Health"],
    summary="Health Check",
    description="Check if the API is running and healthy",
    response_description="API health status"
)
async def health_check():
    """
    Health check endpoint.
    
    Returns basic API status information.
    Useful for monitoring and load balancers.
    
    Returns:
        dict: Health status with API name and version
    """
    return {
        "status": "healthy",
        "app": APP_NAME,
        "version": APP_VERSION
    }

# ============================================================================
# Root Endpoint
# ============================================================================

@app.get(
    "/",
    tags=["Root"],
    summary="API Information",
    description="Get basic API information"
)
async def root():
    """
    Root endpoint providing API information.
    
    Returns:
        dict: API name, version, and documentation URLs
    """
    return {
        "message": f"Welcome to {APP_NAME}",
        "version": APP_VERSION,
        "docs_url": "/api/docs",
        "redoc_url": "/api/redoc",
        "openapi_url": "/api/openapi.json"
    }

# ============================================================================
# Router Registration
# ============================================================================

from app.routers import user_router

# Include user router for registration, login, and profile endpoints
app.include_router(user_router)

logger.info(f"✓ {APP_NAME} v{APP_VERSION} FastAPI application created successfully")

# ============================================================================
# Debug Information
# ============================================================================

if DEBUG:
    logger.info("🔍 Debug mode is ENABLED")
    logger.info("📍 API Documentation: http://localhost:8000/api/docs")
    logger.info("📍 ReDoc: http://localhost:8000/api/redoc")
else:
    logger.info("✓ Production mode is ACTIVE")

__all__ = ["app"]
