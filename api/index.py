"""
Vercel Serverless Function Entry Point for Resume Analyzer Flask App
"""
import sys
from pathlib import Path

# Add backend directory to Python path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

# Import the Flask app
from app import app

# Export for Vercel
# Vercel will call this as a WSGI app
