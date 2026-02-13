"""
Vercel serverless function entry point for FastAPI.
Imports the main FastAPI app with all routes configured.
"""
import sys
import os

# Add the parent directory to Python path for proper imports on Vercel
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the fully configured app from main.py
from api.main import app

# Vercel will use this app instance
# All routes, middleware, and configuration are in api/main.py
