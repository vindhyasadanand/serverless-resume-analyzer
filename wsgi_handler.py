"""
WSGI Handler for AWS Lambda
Wraps Flask app for Lambda execution
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import app

def handler(event, context):
    """Lambda handler"""
    import serverless_wsgi
    return serverless_wsgi.handle_request(app, event, context)

