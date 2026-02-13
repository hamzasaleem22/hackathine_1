"""
Vercel serverless function entry point for FastAPI.
Imports the main FastAPI app with all routes configured.
"""
# Import the fully configured app from main.py
from api.main import app

# Vercel will use this app instance
# All routes, middleware, and configuration are in api/main.py
