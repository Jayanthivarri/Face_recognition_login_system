"""
Application Entry Point

Run the FastAPI application using Uvicorn.

Usage:
    python run.py

The script reads configuration from environment variables:
    - API_HOST: Server host (default: 0.0.0.0)
    - API_PORT: Server port (default: 8000)
    - DEBUG: Enable debug mode (default: False)

Example:
    DEBUG=True python run.py
    DEBUG=False python run.py
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.utils.constants import API_HOST, API_PORT, DEBUG, APP_NAME

def main():
    """
    Start the FastAPI application.
    
    Uses Uvicorn as the ASGI server.
    """
    print(f"\n{'='*70}")
    print(f"  🚀 Starting {APP_NAME}")
    print(f"{'='*70}\n")
    
    print(f"📍 Server: http://{API_HOST}:{API_PORT}")
    print(f"📍 API Docs: http://localhost:{API_PORT}/api/docs")
    print(f"📍 ReDoc: http://localhost:{API_PORT}/api/redoc")
    print(f"🔍 Debug Mode: {'ON' if DEBUG else 'OFF'}\n")
    
    try:
        uvicorn.run(
            "app.main:app",
            host=API_HOST,
            port=API_PORT,
            reload=DEBUG,  # Auto-reload in debug mode
            log_level="info" if not DEBUG else "debug",
            access_log=True,
            use_colors=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Failed to start server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
